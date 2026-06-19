# ALGORITMA MINIMISASI DFA
import collections
from common import DEAD_STATE

def minimize_dfa(dfa_instance):
    # 1. Analisis Keterjangkauan State (Reachability)
    reachable = {dfa_instance.start_state}
    queue = collections.deque([dfa_instance.start_state])
    completed_transitions = dict(dfa_instance.transitions)
    dead_needed = False
    while queue:
        curr = queue.popleft()
        for sym in dfa_instance.alphabet:
            nxt = completed_transitions.get((curr, sym))
            if nxt is None:
                nxt = DEAD_STATE
                completed_transitions[(curr, sym)] = nxt
                dead_needed = True
            if nxt not in reachable:
                reachable.add(nxt)
                queue.append(nxt)

    if dead_needed:
        for sym in dfa_instance.alphabet:
            completed_transitions[(DEAD_STATE, sym)] = DEAD_STATE

    r_states = sorted(list(reachable))

    # Fungsi bantu untuk mencari indeks kelompok state
    def get_group_idx(state, partition):
        for i, group in enumerate(partition):
            if state in group:
                return i
        return -1

    # 2. Partisi Awal: Kelompok State Final vs Non-Final
    group_finals = [s for s in r_states if s in dfa_instance.final_states]
    group_nonfinals = [s for s in r_states if s not in dfa_instance.final_states]

    partition = []
    if group_finals:
        partition.append(group_finals)
    if group_nonfinals:
        partition.append(group_nonfinals)

    # 3. Iterasi Penyempurnaan Partisi (Refinement)
    changed = True
    while changed:
        changed = False
        new_partition = []
        for group in partition:
            if len(group) <= 1:
                new_partition.append(group)
                continue

            # Kelompokkan state berdasarkan kemiripan transisi
            subgroups = {}
            for s in group:
                sig = []
                for a in dfa_instance.alphabet:
                    dest = completed_transitions[(s, a)]
                    sig.append(get_group_idx(dest, partition))
                
                sig_tuple = tuple(sig)
                if sig_tuple not in subgroups:
                    subgroups[sig_tuple] = []
                subgroups[sig_tuple].append(s)

            if len(subgroups) > 1:
                changed = True
            
            for sub in subgroups.values():
                new_partition.append(sub)
        partition = new_partition

    # Cari kelompok yang berisi start state
    start_group_idx = -1
    for idx, group in enumerate(partition):
        if dfa_instance.start_state in group:
            start_group_idx = idx
            break

    # Atur posisi agar kelompok start state berada di urutan pertama (M0)
    if start_group_idx > 0:
        partition.insert(0, partition.pop(start_group_idx))

    # 4. Bangun Hasil DFA Minimal
    min_states = [f"M{i}" for i in range(len(partition))]
    min_start = "M0"
    min_finals = []
    min_transitions = {}
    partition_mapping = []
    represented_original_groups = 0

    for i, group in enumerate(partition):
        state_name = f"M{i}"
        if any(state != DEAD_STATE for state in group):
            represented_original_groups += 1
        partition_mapping.append({
            'group': [s for s in group],
            'name': state_name
        })
        
        if any(s in dfa_instance.final_states for s in group):
            min_finals.append(state_name)

        rep = group[0]
        for a in dfa_instance.alphabet:
            dest = completed_transitions[(rep, a)]
            dest_group_idx = get_group_idx(dest, partition)
            if dest_group_idx != -1:
                min_transitions[(state_name, a)] = f"M{dest_group_idx}"

    return {
        'states': min_states,
        'alpha': dfa_instance.alphabet,
        'start': min_start,
        'finals': min_finals,
        'trans': min_transitions,
        'mapping': partition_mapping,
        'reduced_count': len(dfa_instance.states) - represented_original_groups,
        'added_dead_state': dead_needed
    }
