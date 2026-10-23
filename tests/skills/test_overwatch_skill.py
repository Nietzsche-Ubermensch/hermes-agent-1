"""Tests for the overwatch bundled skill.

Validates frontmatter structure, body content, and the audit-framework
sections. No live network, no external dependencies — stdlib + pytest only.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import hermes_yaml as yaml

SKILL_PATH = (
    Path(__file__).resolve().parents[2]
    / "skills"
    / "autonomous-ai-agents"
    / "overwatch"
    / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_content() -> str:
    return SKILL_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def frontmatter(skill_content: str):
    assert skill_content.startswith("---"), "SKILL.md must start with ---"
    m = re.search(r"\n---\s*\n", skill_content[3:])
    assert m, "Unclosed frontmatter"
    fm = yaml.safe_load(skill_content[3 : m.start() + 3])
    assert isinstance(fm, dict), "Frontmatter must be a YAML mapping"
    return fm


def test_skill_file_exists():
    assert SKILL_PATH.is_file(), f"SKILL.md not found at {SKILL_PATH}"


def test_required_fields(frontmatter):
    for field in ("name", "description", "version", "author", "license", "platforms"):
        assert field in frontmatter, f"Missing required field: {field}"


def test_description_under_60_chars(frontmatter):
    desc = frontmatter["description"]
    assert len(desc) <= 60, f"description is {len(desc)} chars, hardline is 60"


def test_description_ends_with_period(frontmatter):
    assert frontmatter["description"].endswith("."), "description must end with a period"


def test_description_has_no_hedging(frontmatter):
    desc = frontmatter["description"].lower()
    hedge_words = ("may help", "could potentially", "might reduce", "i think", "it appears")
    for word in hedge_words:
        assert word not in desc, f"description contains hedge '{word}'"


def test_name_is_valid(frontmatter):
    name = frontmatter["name"]
    assert len(name) <= 64, f"name too long: {name}"
    assert re.match(r"^[a-z][a-z0-9-]*$", name), f"name must be lowercase-hyphenated: {name}"


def test_platforms_present(frontmatter):
    assert "platforms" in frontmatter, "Missing platforms field"
    assert isinstance(frontmatter["platforms"], list), "platforms must be a list"


def test_related_skills_resolve(frontmatter):
    repo = SKILL_PATH.parents[3]
    related = frontmatter.get("metadata", {}).get("hermes", {}).get("related_skills", [])
    for skill_name in related:
        found = False
        for base in ("skills", "optional-skills"):
            for skillemd in (repo / base).rglob("SKILL.md"):
                if skill_name in str(skillemd.parent):
                    found = True
                    break
        assert found, f"related_skill '{skill_name}' not found in-repo"


def test_no_marketing_words(skill_content):
    marketing = re.compile(
        r"\b(powerful|comprehensive|seamless|revolutionary|cutting-edge|state-of-the-art)\b",
        re.IGNORECASE,
    )
    assert not marketing.search(skill_content), "Contains marketing words"


def test_no_machine_local_paths(skill_content):
    machine_local = re.compile(r"/home/(?!runner\b)[a-z0-9_-]+/")
    assert not machine_local.search(skill_content), "Contains machine-local paths"


def test_body_non_empty(skill_content):
    m = re.search(r"\n---\s*\n", skill_content[3:])
    assert m is not None, "Unclosed frontmatter"
    body = skill_content[m.end() :]
    assert len(body.strip()) > 0, "Body is empty"


def test_has_when_to_use(skill_content):
    assert "## When to Use" in skill_content, "Missing When to Use section"


def test_has_prerequisites(skill_content):
    assert "## Prerequisites" in skill_content, "Missing Prerequisites section"


def test_has_how_to_run(skill_content):
    assert "## How to Run" in skill_content, "Missing How to Run section"


def test_has_quick_reference(skill_content):
    assert "## Quick Reference" in skill_content, "Missing Quick Reference section"


def test_has_procedure(skill_content):
    assert "## Procedure" in skill_content, "Missing Procedure section"


def test_has_pitfalls(skill_content):
    assert "## Pitfalls" in skill_content, "Missing Pitfalls section"


def test_has_verification(skill_content):
    assert "## Verification" in skill_content, "Missing Verification section"


def test_has_risk_classification(skill_content):
    assert "SAFE" in skill_content, "Missing SAFE risk level"
    assert "MODERATE" in skill_content, "Missing MODERATE risk level"
    assert "DANGEROUS" in skill_content, "Missing DANGEROUS risk level"
    assert "BLOCKED" in skill_content, "Missing BLOCKED risk level"


def test_has_audit_log(skill_content):
    assert "overwatch.log" in skill_content, "Missing audit log reference"


def test_not_a_sandbox_warning(skill_content):
    assert "not a sandbox" in skill_content.lower(), "Missing sandbox limitation warning"
