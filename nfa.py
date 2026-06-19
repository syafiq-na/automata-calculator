from common import DEAD_STATE, EPSILON, clean_items, normalize_transitions, parse_input_symbols


# LOGIKA MESIN NFA
class NFA:
    def __init__(self, states, alphabet, start_state, final_states, transitions):
        self.states = clean_items(states)
        self.alphabet = clean_items(alphabet)
        self.start_state = str(start_state).strip()
        self.final_states = clean_items(final_states)
        self.transitions = normalize_transitions(transitions, nondeterministic=True)

        if DEAD_STATE in self.states:
            raise ValueError(f"Nama state {DEAD_STATE} dicadangkan untuk proses internal")
        if EPSILON in self.alphabet:
            raise ValueError(f"Simbol {EPSILON} dicadangkan untuk epsilon")
        if self.start_state not in self.states:
            raise ValueError("Start state harus terdaftar pada states")
        if not set(self.final_states).issubset(self.states):
            raise ValueError("Semua final state harus terdaftar pada states")
        for (state, symbol), targets in self.transitions.items():
            if state not in self.states or any(target not in self.states for target in targets):
                raise ValueError(f"Transisi ({state}, {symbol}) mengacu ke state yang tidak terdaftar")
            if symbol != EPSILON and symbol not in self.alphabet:
                raise ValueError(f"Simbol transisi '{symbol}' tidak ada di alphabet")

    def epsilon_closure(self, start_states):
        closure = set(start_states)
        stack = list(start_states)
        while stack:
            s = stack.pop()
            eps_targets = self.transitions.get((s, EPSILON))
            if eps_targets:
                for t in eps_targets:
                    if t not in closure:
                        closure.add(t)
                        stack.append(t)
        return closure

    def move(self, states, symbol):
        moved = set()
        for s in states:
            targets = self.transitions.get((s, symbol))
            if targets:
                for t in targets:
                    moved.add(t)
        return moved

    def test_string(self, input_str):
        symbols = parse_input_symbols(input_str)

        current_set = self.epsilon_closure([self.start_state])
        
        for sym in symbols:
            if sym not in self.alphabet:
                return False, []
            moved_set = self.move(current_set, sym)
            current_set = self.epsilon_closure(moved_set)

        accepted = any(s in self.final_states for s in current_set)
        return accepted, sorted(list(current_set))
