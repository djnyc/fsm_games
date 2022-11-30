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
    return m.Symbol('0'), m.Symbol('1')


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


@pytest.fixture
def test_sequence(my_symbols):

    a0, a1 = my_symbols

    return [a0, a1, a0, a1, a0]


@pytest.fixture
def test_trace(my_states):

    s0, s1 = my_states

    return [s0, s0, s1, s1, s0, s0]


@pytest.fixture
def one_click_out(my_states):

    s0, s1 = my_states

    return s0


@pytest.fixture
def my_cursor(my_fsm, test_sequence):

    return m.FiniteStateMachineCursor(my_fsm, test_sequence)


def test_one_click(my_cursor, my_initial, one_click_out):

    my_cursor.tick()

    assert my_cursor.trace == [my_initial, one_click_out]


def test_cursor(my_cursor, test_trace):

    my_cursor.run_to_finish()

    assert my_cursor.trace == test_trace
