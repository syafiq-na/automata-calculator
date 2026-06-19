from common import DEAD_STATE, clean_items, normalize_transitions, parse_input_symbols


# LOGIKA MESIN DFA
class DFA:
    def __init__(self, states, alphabet, start_state, final_states, transitions):
        self.states = clean_items(states)
        self.alphabet = clean_items(alphabet)
        self.start_state = str(start_state).strip()
        self.final_states = clean_items(final_states)
        self.transitions = normalize_transitions(transitions)

        if DEAD_STATE in self.states:
            raise ValueError(f"Nama state {DEAD_STATE} dicadangkan untuk proses internal")
        if self.start_state not in self.states:
            raise ValueError("Start state harus terdaftar pada states")
        if not set(self.final_states).issubset(self.states):
            raise ValueError("Semua final state harus terdaftar pada states")
        for (state, symbol), target in self.transitions.items():
            if state not in self.states or target not in self.states:
                raise ValueError(f"Transisi ({state}, {symbol}) mengacu ke state yang tidak terdaftar")
            if symbol not in self.alphabet:
                raise ValueError(f"Simbol transisi '{symbol}' tidak ada di alphabet")

    def test_string(self, input_str):
        symbols = parse_input_symbols(input_str)

        current = self.start_state
        trace = []
        ok = True
        trace.append({
            'state': current,
            'info': f"Start: {current}",
            'type': 'info'
        })

        for sym in symbols:
            if sym not in self.alphabet:
                ok = False
                trace.append({
                    'state': None,
                    'info': f"'{sym}' tidak ada di alphabet",
                    'type': 'fail'
                })
                break
            
            next_state = self.transitions.get((current, sym))
            if not next_state:
                ok = False
                trace.append({
                    'state': DEAD_STATE,
                    'info': f"δ({current}, {sym}) = {DEAD_STATE} — tidak ada transisi",
                    'type': 'fail'
                })
                break
            
            trace.append({
                'state': next_state,
                'info': f"δ({current}, {sym}) = {next_state}",
                'type': 'ok'
            })
            current = next_state

        accepted = ok and (current in self.final_states)
        return accepted, trace, current

    def minimize(self):
        # Impor lokal untuk mencegah circular import
        from minimizer import minimize_dfa
        return minimize_dfa(self)
