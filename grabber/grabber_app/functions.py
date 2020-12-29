def chunks(lister, size):
    return list(lister[i:i + size] for i in range(0, len(lister), size))
