from fuzzywuzzy import fuzz


# for name comparison
def levenshteinSimilarity(string1: str, string2: str):
    if string1 == string2:
        return 1

    if not string1 or not string2:
        return 0

    return fuzz.ratio(string1, string2) / 100.0
