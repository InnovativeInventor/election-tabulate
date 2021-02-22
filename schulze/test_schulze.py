import schulze
import pytest


def test_basic():
    candidates = ["x", "y", "z"]
    prefs = [{"x": 1, "y": 3, "z": 5}, {"x": 1, "y": 2}]

    evaluator = schulze.SchulzeMethod(candidates, prefs)
    evaluator.strongest_paths()
    assert evaluator.evaluate() == "x"


def test_basic_2():
    candidates = ["x", "y", "z"]
    prefs = [{"x": 8, "y": 9, "z": 10}, {"x": 10, "y": 20}, {"z": 3}]

    evaluator = schulze.SchulzeMethod(candidates, prefs)
    evaluator.strongest_paths()
    assert evaluator.evaluate() == "x"


def test_basic_4():
    candidates = ["x", "y", "z"]
    prefs = [{"x": 1, "y": 2, "z": 3}, {"x": 2, "y": 1}, {"z": 1}]

    with pytest.raises(AssertionError):
        evaluator = schulze.SchulzeMethod(candidates, prefs)
        evaluator.strongest_paths()
        assert evaluator.evaluate() == "x"
