# ALGORITMA CEK EKUIVALENSI DUA DFA
import collections
from common import DEAD_STATE, format_word

def check_equivalence(dfa1, dfa2):
    # Cek apakah simbol alphabet kedua mesin sama
    a1 = set(dfa1.alphabet)
    a2 = set(dfa2.alphabet)
    if a1 != a2:
        return False, "Alphabet berbeda"

    alpha = sorted(list(a1))
    discovered = {(dfa1.start_state, dfa2.start_state)}
    queue = collections.deque([(dfa1.start_state, dfa2.start_state)])
    
    # Catat jalur transisi untuk rekonstruksi counterexample jika tidak ekuivalen
    path = {(dfa1.start_state, dfa2.start_state): []}

    while queue:
        s1, s2 = queue.popleft()
        key = (s1, s2)

        f1 = s1 in dfa1.final_states
        f2 = s2 in dfa2.final_states

        if f1 != f2:
            return False, format_word(path[key])

        for a in alpha:
            n1 = dfa1.transitions.get((s1, a), DEAD_STATE)
            n2 = dfa2.transitions.get((s2, a), DEAD_STATE)
            
            nk = (n1, n2)
            if nk not in discovered:
                discovered.add(nk)
                queue.append((n1, n2))
                path[nk] = path[key] + [a]

    return True, None
