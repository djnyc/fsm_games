import pytest
import main as m


@pytest.fixture
def my_initial():
    return m.State('S0')


@pytest.fixture
def my_states(my_initial):
    return my_initial, m.State('S1')


@pytest.fixture
def my_symbols():
    return m.Symbol('A0'), m.Symbol('A1')


@pytest.fixture
def my_transitions(my_states, my_symbols):
    s0, s1 = my_states
    a0, a1 = my_symbols

    return {
        a0: {s0: s0, s1: s1},
        a1: {s0: s1, s1: s0}
        }


@pytest.fixture
def my_fsm(my_states, my_symbols, my_transitions, my_initial):

    test_fsm: m.FiniteStateMachine = m.FiniteStateMachine()

    test_fsm.add_state(my_states)
    test_fsm.add_symbol(my_symbols)
    test_fsm.add_transitions(my_transitions)
    test_fsm.set_initial_state(my_initial)

    return test_fsm


def test_my_fsm(my_symbols, my_states, my_fsm):
    a0, a1 = my_symbols
    s0, s1 = my_states

    test_sequence = [a0, a1, a0, a1, a0]

    test_cursor = m.FiniteStateMachineCursor(my_fsm, test_sequence)

    moving = True

    while moving:
        moving = test_cursor.tick()

    assert test_cursor.trace == [s0, s0, s1, s1, s0, s0]
