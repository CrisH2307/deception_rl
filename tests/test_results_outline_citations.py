"""Every `results/<file>.json:<key path>` citation in the results outline resolves.

The repo's convention is that every number in the paper is script-emitted. The outline
is the map from a claim to the artifact key behind it, so a citation that does not
resolve is the same class of bug as a number typed from a draft: it reads as sourced
and is not. This fails when a key is renamed, an artifact is regenerated without it, or
a citation is mistyped.

It checks resolution, not value. A value check here would duplicate the artifact.
"""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / "docs" / "P2" / "RESULTS_OUTLINE.md"

# `results/T6_gate_record.json:pooled_existence_rate` inside backticks. Key-path
# segments may carry `|` and `/` (cell ids such as `CTRL|F1`, `CTRL/F1`) and `*`
# (every key at that level).
CITATION = re.compile(r"`results/([A-Za-z0-9_]+\.json):([^`\s]+)`")


def _resolve(node, segments, where):
    """Resolve a dotted key path, allowing dots inside a key (e.g. "0.25", "1e-12").

    Tries the longest joinable prefix first, so `divergence_curve_pool.0.25.pooled`
    finds the key "0.25" rather than failing on "0".
    """
    if not segments:
        return
    if not isinstance(node, dict):
        raise AssertionError(f"{where}: '{'.'.join(segments)}' is under a non-object")
    if segments[0] == "*":
        assert node, f"{where}: '*' matched an empty object"
        for key, child in node.items():
            _resolve(child, segments[1:], f"{where} (* = {key})")
        return
    for take in range(len(segments), 0, -1):
        key = ".".join(segments[:take])
        if key in node:
            _resolve(node[key], segments[take:], where)
            return
    raise AssertionError(
        f"{where}: no key matches '{segments[0]}' "
        f"(available: {sorted(node)[:12]}{' ...' if len(node) > 12 else ''})"
    )


def _citations():
    text = OUTLINE.read_text(encoding="utf-8")
    found = CITATION.findall(text)
    assert found, "no citations found; the outline's citation format has drifted"
    return sorted(set(found))


@pytest.mark.parametrize("filename,keypath", _citations())
def test_citation_resolves(filename, keypath):
    path = ROOT / "results" / filename
    assert path.exists(), f"{filename} is cited by the outline and does not exist"
    _resolve(json.loads(path.read_text(encoding="utf-8")), keypath.split("."),
             f"{filename}:{keypath}")


def test_outline_exists_and_cites_every_results_file_it_should():
    """A citation naming an artifact that is not in results/ is a typo, not a finding."""
    cited = {f for f, _ in _citations()}
    present = {p.name for p in (ROOT / "results").glob("*.json")}
    assert cited <= present, f"cited but absent from results/: {sorted(cited - present)}"
