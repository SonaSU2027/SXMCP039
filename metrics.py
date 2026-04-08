def calculate_improvement(old, new):
    """
    Calculates the percentage reduction in tokens.
    A negative result means the new system is more efficient (uses fewer tokens).
    """
    if old == 0:
        return 0
    
    # Formula: ((New - Old) / Old) * 100
    # Example: ((200 - 1000) / 1000) * 100 = -80%
    improvement_percent = ((new - old) / old) * 100
    
    return abs(round(improvement_percent, 2))

def calculate_density(result):
    # We measure the length of the findings vs the tokens used
    # A higher score means the system is more efficient at conveying info
    text_length = len(str(result.get("progress", "")))
    tokens = result.get("tokens", 1)
    return (text_length / tokens) * 100