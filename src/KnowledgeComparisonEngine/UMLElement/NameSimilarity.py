from Levenshtein import distance as levenshtein_distance


# for name comparison
def calculate_similarity(string1: str, string2: str) -> float:
    # The levenshteinSimilarity is used to compare between two strings
    return levenshtein_distance(string1, string2)
