def sint(s, d=0):
    """Parses s into an integer. Returns d if the parsing fails."""
    try:
        return int(s.strip())
    except ValueError:
        return d