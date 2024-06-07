import re

def abreviation(nom):
    mots = split_string(nom)
    abrev = ""
    for mot in mots:
        if len(mot) > 0:
            abrev += mot[0]

    return abrev.lower()

def split_string(s):
    return re.split(' |-|_|\.|,', s)

def match(word1, word2):
    score = 0.0
    word1dict = {
        "abreviation": abreviation(word1),
        "mots_cles": split_string(word1)
    }
    word2dict = {
        "abreviation": abreviation(word2),
        "mots_cles": split_string(word2)
    }
    # on crée deux dict pour les mots clés et les abréviations des mots, une abréviation à un poids plus important qu'un mot clé, cependat les mots clés sont plus ou moin lourds celon leurs longueurs
    dict1= {}
    for abrev in word1dict["abreviation"]:
        dict1[abrev] = len(abrev)*2
    for mot in word1dict["mots_cles"]:
        dict1[mot] = len(mot)
    dict2= {}
    for abrev in word2dict["abreviation"]:
        dict2[abrev] = len(abrev)*2
    for mot in word2dict["mots_cles"]:
        dict2[mot] = len(mot)

    # on compare
    for key in dict1:
        if key in dict2:
            score += dict1[key] + dict2[key]
    return score

def find_best_match(word, word_list):
    best_score = 0.0
    best_match = None
    for word2 in word_list:
        score = match(word, word2)
        #print(score, word2)
        if score > best_score:
            best_score = score
            best_match = word2
    return [best_match, best_score]

def findairports(depart,arrive, aeroportsdisponames):
    depart = find_best_match(depart, aeroportsdisponames)
    arrive = find_best_match(arrive, aeroportsdisponames)
    return [depart, arrive]

def findavionsmodels(avion, avionsdisponames):
    return find_best_match(avion, avionsdisponames)

