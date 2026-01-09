def cleanup(*objects):
    """
    Explicit memory cleanup (symbolic).
    """
    for obj in objects:
        del obj
