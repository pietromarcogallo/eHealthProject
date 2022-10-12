def count_occurrences(occurrence, text, black_list):
    words = text.split()
    for word in words:
        # Put all words in lower case, because so do they appear in the black list in the .xlsx file
        word = word.lower()
        if word not in black_list:
            if word in occurrence:
                occurrence[word] = occurrence[word] + 1
            else:
                occurrence[word] = 1
    return occurrence


def keep_main_words(occurrence, threshold):
    for word in occurrence.copy():
        if occurrence[word] < threshold:
            del occurrence[word]
    return occurrence


def create_dictionary(articles, black_list):
    occurrence = dict()
    for i, a in enumerate(articles['PubmedArticle']):
        for sentence in a['MedlineCitation']['Article']['Abstract']['AbstractText']:
            occurrence = count_occurrences(occurrence, sentence, black_list)
    threshold = 5
    occurrence = keep_main_words(occurrence, threshold)
    return list(occurrence.keys())


# "Occurrence" will be the dictionary of referring words, which appear the most often
'''
def pertinence(input_word, article, articles, num_articles, black_list):
    assert (article in articles)
    pertinence_dict = dict()
    occurrence = dict()
    for a in articles:
        if not a.title.__contains__(input_word) \
                or input_word not in a.keywords:
            return 0
        occurrence = count_occurrences(occurrence, a.abstract, black_list)
        occurrence = count_occurrences(occurrence, a.conclusions, black_list)
    threshold = 10
    occurrence = keep_main_words(occurrence, threshold)
    relative_frequency = dict()
    for word in occurrence:
        relative_frequency[word] = occurrence[word] / num_articles
    for a in articles:
        pertinence_dict[a] = relative_frequency[input_word]
    return pertinence_dict[article]


def pertinence(paper, num_papers, occurrence):
    return occurrence[paper] / num_papers
'''

