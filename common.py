EPSILON = "E"
DEAD_STATE = "__DEAD_STATE__"


def clean_items(items):
    return [str(item).strip() for item in items if str(item).strip()]


def parse_input_symbols(input_str):
    """Use whitespace-separated symbols when present, otherwise one character per symbol."""
    raw = str(input_str).strip()
    if not raw:
        return []
    if any(char.isspace() for char in raw):
        return raw.split()
    return list(raw)


def normalize_transitions(transitions, nondeterministic=False):
    """
    Normalize either a Python tuple-key mapping or JSON transition records.

    JSON records use {"state": ..., "symbol": ..., "target": ...}; tuple keys
    remain the only mapping representation inside the automata domain.
    """
    normalized = {}

    if isinstance(transitions, dict):
        entries = [
            (key[0], key[1], value)
            for key, value in transitions.items()
            if isinstance(key, tuple) and len(key) == 2
        ]
        if len(entries) != len(transitions):
            raise ValueError("Transition mapping harus memakai key tuple (state, symbol)")
    elif isinstance(transitions, list):
        entries = []
        for record in transitions:
            if not isinstance(record, dict):
                raise ValueError("Setiap transisi harus berupa object")
            entries.append((
                record.get("state", ""),
                record.get("symbol", ""),
                record.get("target", [] if nondeterministic else ""),
            ))
    else:
        raise ValueError("Format transisi tidak valid")

    for state, symbol, target in entries:
        state = str(state).strip()
        symbol = str(symbol).strip()
        if not state or not symbol:
            continue
        key = (state, symbol)

        if nondeterministic:
            raw_targets = target if isinstance(target, list) else [target]
            targets = clean_items(raw_targets)
            if targets:
                normalized[key] = list(dict.fromkeys(targets))
        else:
            target = str(target).strip()
            if target:
                normalized[key] = target

    return normalized


def transitions_to_records(transitions):
    return [
        {"state": state, "symbol": symbol, "target": target}
        for (state, symbol), target in transitions.items()
    ]


def format_word(symbols):
    if not symbols:
        return EPSILON
    if any(len(symbol) != 1 for symbol in symbols):
        return " ".join(symbols)
    return "".join(symbols)
