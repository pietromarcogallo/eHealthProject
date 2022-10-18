import string
import operator
from Database_creation import *


def count_occurrences_and_spot_keywords(occurrence, is_keyword, keywords, text, black_list):
    words = text.split()
    for word in words:
        # Put all words in lower case, because so do they appear in the black list in the .xlsx file
        word = word.lower()
        if word not in black_list:
            occurrence[word] = occurrence[word] + 1 if word in occurrence else 1
            # The value of each key in is_keyword is a boolean: is the word in question a keyword of the article's?
            is_keyword[word] = word in keywords
    return occurrence, is_keyword


def keep_main_words(occurrence, is_keyword, threshold):
    for word in occurrence.copy():
        if occurrence[word] < threshold and not is_keyword[word]:
            del occurrence[word]
    return occurrence


def create_dictionary(papers, black_list):
    # This dictionary counts the occurrences of each word in the analyzed sentences
    occurrence = dict()
    '''
    This dictionary keeps track of whether a word is included in the list of an article's keywords
    The idea is that keywords in the abstract must be kept regardless of their occurrence due to their higher 
    importance.
    '''
    is_keyword = dict()
    for i, a in enumerate(papers['PubmedArticle']):
        paper_keywords = process_keywords(a)
        article = a['MedlineCitation']['Article']
        if 'Abstract' in article.keys():
            abstract_text = article['Abstract']['AbstractText']
            for sentence in abstract_text:
                sentence = sentence.translate(str.maketrans('', '', string.punctuation))
                occurrence, is_keyword = \
                    count_occurrences_and_spot_keywords(occurrence, is_keyword, paper_keywords, sentence, black_list)
    # This threshold can be changed according to desire.
    threshold = 10
    # Keep only the word with a minimum number of occurrences in the dictionary (so to discard useless words)
    occurrence = keep_main_words(occurrence, is_keyword, threshold)
    # Sort occurrence dictionary by descending order of occurrences
    occurrence = dict(sorted(occurrence.items(), key=operator.itemgetter(1), reverse=True))
    return occurrence


def convert_to_float(occ):
    for key in occ.keys():
        occ[key] = float(occ[key])
    return occ


def words_weight_assig(occurence, num_results):
    occurence.update((x, y / num_results) for x, y in occurence.items())
    max_key = max(occurence, key=occurence.get)
    max_freq = occurence[max_key] / 2
    occurence[max_key] = occurence[max_key] / 2
    occurence.update((x, y / max_freq) for x, y in occurence.items())
    return occurence