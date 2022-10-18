from weight_assignment import *


def create_tdictionary(papers, black_list):
    dicts = []
    for i, a in enumerate(papers['PubmedArticle']):
        occurrence = dict()
        is_keyword = dict()
        paper_keywords = process_keywords(a)
        article = a['MedlineCitation']['Article']
        title_text = article['ArticleTitle']
        title_text = title_text.translate(str.maketrans('', '', string.punctuation))
        occurrence, is_keyword = \
            count_occurrences_and_spot_keywords(occurrence, is_keyword, paper_keywords, title_text, black_list)
        dicts.append(occurrence)
    for i in range(0, len(dicts)):
        dicts[i] = convert_to_float(dicts[i])
    return dicts


def keywords_to_string(paper):
    keywords = ""
    for keyword in paper['MedlineCitation']['KeywordList']:
        for i in range(0, len(keyword)):
            keywords = keywords + str(keyword[i]) + " "
    return keywords


def create_kdictionary(papers, black_list):
    dicts = []
    for i, a in enumerate(papers['PubmedArticle']):
        occurrence = dict()
        is_keyword = dict()
        paper_keywords = keywords_to_string(a)
        paper_keywords = paper_keywords.translate(str.maketrans('', '', string.punctuation))
        occurrence, is_keyword = \
            count_occurrences_and_spot_keywords(occurrence, is_keyword, paper_keywords, paper_keywords, black_list)
        dicts.append(occurrence)
    for i in range(0, len(dicts)):
        dicts[i] = convert_to_float(dicts[i])
    return dicts


def create_adictionary(papers, black_list):
    dicts = []
    for i, a in enumerate(papers['PubmedArticle']):
        occurrence = dict()
        is_keyword = dict()
        paper_keywords = process_keywords(a)
        article = a['MedlineCitation']['Article']
        if 'Abstract' in article.keys():
            abstract_text = article['Abstract']['AbstractText']
            for sentence in abstract_text:
                sentence = sentence.translate(str.maketrans('', '', string.punctuation))
                occurrence, is_keyword = \
                    count_occurrences_and_spot_keywords(occurrence, is_keyword, paper_keywords, sentence, black_list)
        dicts.append(occurrence)
    return dicts


def same_keys(ref_dict, dict_list, papers):
    keys_one = set(ref_dict.keys())
    sk = []
    for i, a in enumerate(papers['PubmedArticle']):
        keys_two = set(dict_list[i].keys())
        same_keys = keys_one.intersection(keys_two)
        # To get a list of the keys:
        result = list(same_keys)
        sk.append(result)
    return sk


def scoring_assignment(ref_dict, d_occ, sk):
    score_list = []
    for c, list_i in enumerate(sk):
        score = 0
        for i in range(0, len(list_i)):
            a = int(i)
            score = score + ref_dict[list_i[a]]*d_occ[c][list_i[a]]
        score_list.append(score)
    return score_list

def fin_score(scoreT, scoreK, scoreA):
    score_list = []
    for i in range(0, len(scoreT)):
        score = scoreA[i] + 5*scoreK[i] + 5*scoreT[i]
        score_list.append(score)
    return score_list

def norm(score_list):
    max_value = max(score_list)
    for i in range(0, len(score_list)):
        score_list[i] = score_list[i] / max_value
    return score_list