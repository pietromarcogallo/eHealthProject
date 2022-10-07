def pertinence(abstract, keywords):
    return sum(1 for word in keywords if word in abstract)