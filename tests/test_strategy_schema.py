import pytest
import actions.utils
import actions.strategy


def test_valid_strategy_dict(logger):
    data = {
        "out": [
            {"trigger": "TCP:flags:S", "action": {"action": "drop"}}
        ],
        "in": []
    }
    strat = actions.utils.parse(data, logger)
    assert isinstance(strat, actions.strategy.Strategy)
    assert str(strat).strip() == "[TCP:flags:S]-drop-| \\/"
    assert strat.to_dict() == data


def test_invalid_strategy_missing_trigger(logger):
    bad = {"out": [{"action": {"action": "drop"}}], "in": []}
    with pytest.raises(ValueError):
        actions.utils.parse(bad, logger)


def test_invalid_strategy_unknown_action(logger):
    bad = {"out": [{"trigger": "TCP:flags:S", "action": {"action": "nope"}}], "in": []}
    with pytest.raises(ValueError):
        actions.utils.parse(bad, logger)


def test_invalid_strategy_bad_children(logger):
    bad = {
        "out": [
            {
                "trigger": "TCP:flags:S",
                "action": {"action": "drop", "left": {"action": "drop"}}
            }
        ],
        "in": []
    }
    with pytest.raises(ValueError):
        actions.utils.parse(bad, logger)
