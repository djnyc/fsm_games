class State:
    """
    Defining a state.
    May as well store whether it is allowable here.
    """

    def __init__(self, name=None, is_allowable=False):
        self.name = name
        self.is_allowable = is_allowable

    def __repr__(self):
        return self.name


class Symbol:
    """
    A letter in the input alphabet.
    """

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return self.name


class FiniteStateMachine:
    """
    Describing the elements of a Finite State Machine
    We need the following:
        States (at least one)
        An alphabet
        State-Transitions (implemented as a dictionary of dictionaries?)
        An initial state
        A parser
    """

    def __init__(self,
                 states: list[State] = [],
                 alphabet: list[Symbol] = [],
                 transitions: dict[Symbol: dict[State: State]] = {},
                 initial_state: State = None
                 ):
        """
        Need to get the hang of this docstring malarky
        :param states:
        :param alphabet:
        :param transitions:
        :param initial_state:
        """
        self.states = []

        if states:
            self.add_state(states)

        self.alphabet = []

        if alphabet:
            self.add_symbol(alphabet)

        self.transitions = {}

        if transitions:
            self.add_transitions(transitions)

        self.initial_state = initial_state

    def __consistent(self):
        if not self.states:
            return False
        elif not self.initial_state:
            return False
        elif self.initial_state not in self.states:
            return False

    def add_state(self, args):
        self.states += args

    def add_symbol(self, args):
        self.alphabet += args

    def add_transitions(self, transitions: dict[Symbol: dict[State: State]]):
        for symbol, actions in transitions.items():
            self.transitions |= {symbol: actions}

    def set_initial_state(self, initial_state: State):
        if initial_state not in self.states:
            raise Exception(f'{initial_state} not in {self.states}')
        else:
            self.initial_state = initial_state


class FiniteStateMachineCursor:
    def __init__(self, machine: FiniteStateMachine, actions: list[Symbol]):
        self.machine = machine
        self.actions = actions
        self.state = machine.initial_state
        self.iterator = iter(self.actions)
        self.trace = [self.state]

    def tick(self):
        next_action = next(self.iterator, None)

        if next_action:

            if next_action in self.machine.transitions:

                transition = self.machine.transitions[next_action]

                if self.state in transition:

                    self.state = transition[self.state]
                    self.trace.append(self.state)

                    return True

                else:
                    raise Exception(f'No transition in {transition} for for {self.state}.')
            else:
                raise Exception(f'No transitions in {self.machine.transitions} for action {next_action}. Trace so far is {self.trace}')
        else:
            return False

    def run_to_finish(self):
        running = True

        while running:
            running = self.tick()