def almost_equal(value, target, delta):
    if value - delta > target: return False
    if value + delta < target: return False
    return True