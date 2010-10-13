import Levenshtein

def match(term1, term2):
    term1 = term1.lower()
    term2 = term2.lower()
    return term2.startswith(term1)
    
def similarity(term1, term2):
    term1 = term1.lower()
    term2 = term2.lower()
    distance = Levenshtein.distance(term1, term2)
    return 1.0 - distance / float(max(1, min(len(term1), len(term2))))
