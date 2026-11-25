"""Check a thesis JSON file against the Agent 3 contract: `python -m thesis path/to/thesis.json`.

Prints one line per problem and exits 1 when there is any, 0 when the file meets the contract.
Only the checks that need no database run here (see contract.py).
"""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from pathlib import Path

from thesis.contract import validate_thesis


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("usage: python -m thesis path/to/thesis.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"cannot read {args[0]}: {exc}", file=sys.stderr)
        return 2
    issues = validate_thesis(data)
    for issue in issues:
        print(issue)
    print(f"{len(issues)} problem(s)" if issues else "ok: meets the contract")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
