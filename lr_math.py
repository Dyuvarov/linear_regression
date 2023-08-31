# Calculate estimate price by mileage
def estimate_price(t0, t1, km):
    return t0 + t1 * km


# Min-max normalization. Scales data to [0,1] interval
def normalize(data, min_val, max_val):
    normalized = []
    for val in data:
        normalized.append((val - min_val) / (max_val - min_val))
    return normalized


# Revert normalization
def denormalize(normalized, denormalized_min, denormalized_max):
    denormalized = []
    for val in normalized:
        denormalized.append(denormalized_min + val * (denormalized_max - denormalized_min))
    return denormalized
