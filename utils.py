def normalize_gender(g):
    if not isinstance(g, str):
        g = str(g)
    g = g.strip().lower()
    if g in ['male', 'm']:
        return 'M'
    elif g in ['female', 'f']:
        return 'F'
    elif g in ['prefer not to say', 'none', '']:
        return ''
    else:
        return 'O'
