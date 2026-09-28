import pytest
from deterministic.security import SecurityGuard, SecurityViolation


def test_prompt_size_is_bounded():
    guard = SecurityGuard()
    guard.validate_prompt("ok")
    with pytest.raises(SecurityViolation):
        guard.validate_prompt("x" * (64 * 1024 + 1))


def test_output_size_is_bounded():
    guard = SecurityGuard()
    guard.validate_raw_output('{"ok":true}')
    with pytest.raises(SecurityViolation):
        guard.validate_raw_output("x" * (1024 * 1024 + 1))


def test_disallowed_control_character_stops():
    with pytest.raises(SecurityViolation):
        SecurityGuard().validate_prompt("bad\x00input")


def test_json_parser_fails_closed():
    with pytest.raises(SecurityViolation):
        SecurityGuard.parse_json("not json")


def test_normal_json_is_accepted():
    assert SecurityGuard.parse_json('{"ok": true}') == {"ok": True}
