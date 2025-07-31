def normalize_gender(g):
    print(f"Original: {repr(g)}")  # <-- DEBUGGING LINE
    if not isinstance(g, str):
        g = str(g)
    g = g.strip().lower()
    print(f"Normalized: {repr(g)}")  # <-- DEBUGGING LINE

    if g in ['male', 'm']:
        return 'M'
    elif g in ['female', 'f']:
        return 'F'
    elif g in ['prefer not to say', 'none', '']:
        return ''
    else:
        return 'O'
