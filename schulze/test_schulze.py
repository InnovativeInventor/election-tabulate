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

def test_basic_5():
    """
    Test case: https://en.wikipedia.org/wiki/Schulze_method#Example
    """
    candidates = ["A", "B", "C", "D", "E"]
    prefs_1 = [{"A": 1, "B": 3, "C": 2, "D": 5, "E": 4}]*5
    prefs_2 = [{"A": 1, "B": 5, "C": 4, "D": 2, "E": 3}]*5
    prefs_3 = [{"A": 4, "B": 1, "C": 5, "D": 3, "E": 2}]*8
    prefs_4 = [{"A": 2, "B": 3, "C": 1, "D": 5, "E": 4}]*3
    prefs_5 = [{"A": 2, "B": 4, "C": 1, "D": 5, "E": 3}]*7
    prefs_6 = [{"A": 3, "B": 2, "C": 1, "D": 4, "E": 5}]*2
    prefs_7 = [{"A": 5, "B": 4, "C": 2, "D": 1, "E": 3}]*7
    prefs_8 = [{"A": 3, "B": 2, "C": 5, "D": 4, "E": 1}]*8

    prefs = prefs_1 + prefs_2 + prefs_3 + prefs_4 + prefs_5 + prefs_6 + prefs_7 + prefs_8

    evaluator = schulze.SchulzeMethod(candidates, prefs)
    evaluator.strongest_paths()
    assert evaluator.evaluate() == "E"
