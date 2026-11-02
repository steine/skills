#!/usr/bin/env python3
"""Mechanical checks on the plugins in this repo.

Free, deterministic, and fast: the invariants in plugins/*/MAINTAINERS.md that
break silently when an improvement lands. Behavioural regression is the eval
suite's job, not this script's.

Usage: python3 scripts/lint_plugins.py
Exit 0 when every check passes, 1 on any error. Warnings never fail the run.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
DEBT_FILE = ROOT / "scripts" / "lint-debt.json"
TERMS_FILE = ROOT / "scripts" / "forbidden-terms.txt"

errors: list[str] = []
warnings: list[str] = []


def error(where: Path | str, msg: str) -> None:
    errors.append(f"{rel(where)}: {msg}")


def warn(where: Path | str, msg: str) -> None:
    warnings.append(f"{rel(where)}: {msg}")


def rel(p: Path | str) -> str:
    try:
        return str(Path(p).resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def skill_dirs() -> list[Path]:
    return sorted(p.parent for p in ROOT.glob("plugins/*/skills/*/SKILL.md"))


def check_self_containment() -> None:
    """A SKILL.md reference resolves against its own skill dir, and nowhere else."""
    for skill in skill_dirs():
        md = skill / "SKILL.md"
        text = md.read_text()
        for link in re.findall(r"\]\(([^)]+)\)", text):
            target = link.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if "<" in target or ">" in target:
                continue  # a placeholder in an output template, not a link
            if target.startswith("../"):
                error(md, f"cross-directory reference `{target}` (breaks on marketplace install)")
                continue
            if target.startswith("/"):
                error(md, f"absolute reference `{target}` (breaks on marketplace install)")
                continue
            if not (skill / target).exists():
                error(md, f"dangling reference `{target}`")


def check_orphan_references() -> None:
    """Every file under references/ is reachable from the SKILL.md that owns it."""
    for skill in skill_dirs():
        text = (skill / "SKILL.md").read_text()
        linked = {l.split("#", 1)[0].strip() for l in re.findall(r"\]\(([^)]+)\)", text)}
        for ref in sorted(skill.glob("references/**/*.md")):
            target = "./" + str(ref.relative_to(skill))
            if target not in linked and target.lstrip("./") not in linked:
                # a pack may be linked from another reference file rather than the spine
                others = " ".join(
                    f.read_text() for f in skill.glob("references/**/*.md") if f != ref
                )
                if ref.name not in others:
                    warn(ref, "not referenced from SKILL.md or any other reference file")


def check_versions() -> None:
    """plugin.json and the marketplace entry agree on the version."""
    if not MARKETPLACE.exists():
        error(MARKETPLACE, "missing")
        return
    listed = {p["name"]: p for p in json.loads(MARKETPLACE.read_text()).get("plugins", [])}
    for manifest in sorted(ROOT.glob("plugins/*/.claude-plugin/plugin.json")):
        data = json.loads(manifest.read_text())
        name, version = data.get("name"), data.get("version")
        entry = listed.get(name)
        if entry is None:
            error(manifest, f"plugin `{name}` is not listed in the marketplace")
        elif entry.get("version") != version:
            error(
                MARKETPLACE,
                f"`{name}` is {entry.get('version')} here and {version} in plugin.json",
            )


def load_debt() -> set[str]:
    if not DEBT_FILE.exists():
        return set()
    return set(json.loads(DEBT_FILE.read_text()).get("cases_without_assertions", []))


def check_evals() -> None:
    """Ids and names identify a case, and a case says what passing means."""
    debt = load_debt()
    seen_debt: set[str] = set()
    for path in sorted(ROOT.glob("plugins/*/skills/*/evals/**/*.json")):
        try:
            cases = json.loads(path.read_text())["evals"]
        except (json.JSONDecodeError, KeyError) as exc:
            error(path, f"not a readable eval file ({exc})")
            continue
        ids, names = [], []
        for case in cases:
            ids.append(case.get("id"))
            names.append(case.get("name"))
            key = f"{rel(path)}::{case.get('name')}"
            if not case.get("prompt", "").strip():
                error(path, f"case `{case.get('name')}` has an empty prompt")
            if not case.get("assertions"):
                if key in debt:
                    seen_debt.add(key)
                else:
                    error(path, f"case `{case.get('name')}` has no assertions")
        for label, values in (("id", ids), ("name", names)):
            dupes = {v for v in values if values.count(v) > 1}
            for dupe in sorted(str(d) for d in dupes):
                error(path, f"duplicate {label} `{dupe}`")
    for stale in sorted(debt - seen_debt):
        warn(DEBT_FILE, f"`{stale}` now has assertions (or is gone) — drop it from the debt list")


def check_forbidden_terms() -> None:
    """Skills ship to other teams: no org, product or system names."""
    if not TERMS_FILE.exists():
        return
    terms = [
        line.strip()
        for line in TERMS_FILE.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if not terms:
        return
    pattern = re.compile("|".join(re.escape(t) for t in terms), re.IGNORECASE)
    for path in sorted(ROOT.glob("plugins/**/*")):
        if not path.is_file() or path.suffix not in {".md", ".json"}:
            continue
        for n, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            hit = pattern.search(line)
            if hit:
                error(path, f"line {n} names `{hit.group(0)}` — skills stay domain-agnostic")


def check_stub_packs() -> None:
    """A stack stubbed in one skill and filled in another is a half-supported stack."""
    status: dict[str, dict[str, bool]] = {}
    for pack in sorted(ROOT.glob("plugins/*/skills/*/references/stacks/*.md")):
        stub = "Status: stub" in pack.read_text()
        status.setdefault(pack.stem, {})[pack.parent.parent.parent.name] = stub
    for stack, per_skill in sorted(status.items()):
        if len(set(per_skill.values())) > 1:
            filled = [s for s, stub in per_skill.items() if not stub]
            stubbed = [s for s, stub in per_skill.items() if stub]
            warn(
                f"plugins/*/skills/*/references/stacks/{stack}.md",
                f"filled in {', '.join(filled)} but still a stub in {', '.join(stubbed)}",
            )


def main() -> int:
    for check in (
        check_self_containment,
        check_orphan_references,
        check_versions,
        check_evals,
        check_forbidden_terms,
        check_stub_packs,
    ):
        check()
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
