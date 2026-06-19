from common import EPSILON


# STATE COUNTER UNTUK THOMPSON
class ThompsonStateCounter:
    def __init__(self):
        self.count = 0
    def new_state(self):
        s = f"q{self.count}"
        self.count += 1
        return s

# TOKENISASI EKSPRESI REGULER (REGEX)
def tokenize_regex(regex):
    tokens = []
    escaped = False
    for c in regex:
        if escaped:
            tokens.append({'type': 'CHAR', 'val': c})
            escaped = False
        elif c == '\\':
            escaped = True
        elif c == EPSILON:
            tokens.append({'type': 'CHAR', 'val': EPSILON})
        elif c in '()|*+?':
            tokens.append({'type': c, 'val': c})
        else:
            tokens.append({'type': 'CHAR', 'val': c})
    if escaped:
        raise ValueError("Escape character tidak memiliki karakter pasangan")

    out = []
    for j in range(len(tokens)):
        out.append(tokens[j])
        if j + 1 < len(tokens):
            cur = tokens[j]
            nxt = tokens[j + 1]
            after = cur['type'] in ('CHAR', '*', '+', '?', ')')
            before = nxt['type'] in ('CHAR', '(')
            if after and before:
                out.append({'type': 'CONCAT', 'val': '.'})
    return out

# KONVERSI REGEX INFIX KE POSTFIX
def regex_to_postfix(tokens):
    prec = {'|': 1, 'CONCAT': 2}
    out = []
    stack = []
    for t in tokens:
        if t['type'] == 'CHAR':
            out.append(t)
        elif t['type'] in ('*', '+', '?'):
            if not out:
                raise ValueError(f"Operator {t['type']} tidak memiliki operand")
            out.append(t)
        elif t['type'] == '(':
            stack.append(t)
        elif t['type'] == ')':
            while stack and stack[-1]['type'] != '(':
                out.append(stack.pop())
            if not stack:
                raise ValueError("Kurung tutup tidak memiliki pasangan")
            stack.pop()
        else:
            while stack and stack[-1]['type'] != '(' and prec.get(stack[-1]['type'], 0) >= prec.get(t['type'], 0):
                out.append(stack.pop())
            stack.append(t)
    while stack:
        if stack[-1]['type'] == '(':
            raise ValueError("Kurung buka tidak memiliki pasangan")
        out.append(stack.pop())
    return out

# KONSTRUKSI NFA DARI POSTFIX THOMPSON
def build_nfa_from_postfix(postfix):
    counter = ThompsonStateCounter()
    stack = []
    transitions = {}
    alphabet = set()

    def add_t(from_state, sym, to_state):
        key = (from_state, sym)
        if key not in transitions:
            transitions[key] = []
        if to_state not in transitions[key]:
            transitions[key].append(to_state)
        if sym != EPSILON:
            alphabet.add(sym)

    for t in postfix:
        if t['type'] == 'CHAR':
            s = counter.new_state()
            e = counter.new_state()
            val = EPSILON if t['val'] == EPSILON else t['val']
            add_t(s, val, e)
            stack.append({
                'start': s,
                'end': e,
                'layout': {'type': 'char', 'start': s, 'end': e}
            })
        elif t['type'] == 'CONCAT':
            if len(stack) < 2:
                raise ValueError("Regex tidak valid")
            b = stack.pop()
            a = stack.pop()
            add_t(a['end'], EPSILON, b['start'])
            stack.append({
                'start': a['start'],
                'end': b['end'],
                'layout': {'type': 'concat', 'left': a['layout'], 'right': b['layout']}
            })
        elif t['type'] == '|':
            if len(stack) < 2:
                raise ValueError("Regex tidak valid")
            b = stack.pop()
            a = stack.pop()
            s = counter.new_state()
            e = counter.new_state()
            add_t(s, EPSILON, a['start'])
            add_t(s, EPSILON, b['start'])
            add_t(a['end'], EPSILON, e)
            add_t(b['end'], EPSILON, e)
            stack.append({
                'start': s,
                'end': e,
                'layout': {
                    'type': 'union',
                    'top': a['layout'],
                    'bottom': b['layout'],
                    'start': s,
                    'end': e
                }
            })
        elif t['type'] == '*':
            if len(stack) < 1:
                raise ValueError("Regex tidak valid")
            a = stack.pop()
            s = counter.new_state()
            e = counter.new_state()
            add_t(s, EPSILON, a['start'])
            add_t(s, EPSILON, e)
            add_t(a['end'], EPSILON, a['start'])
            add_t(a['end'], EPSILON, e)
            stack.append({
                'start': s,
                'end': e,
                'layout': {'type': 'star', 'child': a['layout'], 'start': s, 'end': e}
            })
        elif t['type'] == '+':
            if len(stack) < 1:
                raise ValueError("Regex tidak valid")
            a = stack.pop()
            s = counter.new_state()
            e = counter.new_state()
            add_t(s, EPSILON, a['start'])
            add_t(a['end'], EPSILON, a['start'])
            add_t(a['end'], EPSILON, e)
            stack.append({
                'start': s,
                'end': e,
                'layout': {'type': 'plus', 'child': a['layout'], 'start': s, 'end': e}
            })
        elif t['type'] == '?':
            if len(stack) < 1:
                raise ValueError("Regex tidak valid")
            a = stack.pop()
            s = counter.new_state()
            e = counter.new_state()
            add_t(s, EPSILON, a['start'])
            add_t(s, EPSILON, e)
            add_t(a['end'], EPSILON, e)
            stack.append({
                'start': s,
                'end': e,
                'layout': {'type': 'optional', 'child': a['layout'], 'start': s, 'end': e}
            })

    if len(stack) != 1:
        raise ValueError("Regex tidak valid")

    result = stack[0]
    state_set = set()
    for (source, _symbol), dests in transitions.items():
        state_set.add(source)
        for d in dests:
            state_set.add(d)
    state_set.add(result['start'])
    state_set.add(result['end'])

    def state_key(s):
        try:
            return int(s.removeprefix("q"))
        except ValueError:
            return 99999

    sorted_states = sorted(list(state_set), key=state_key)

    return {
        'states': sorted_states,
        'alpha': sorted(list(alphabet)),
        'start': result['start'],
        'finals': [result['end']],
        'trans': transitions,
        'layoutTree': result['layout']
    }
