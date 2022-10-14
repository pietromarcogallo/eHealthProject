# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from pymed import PubMed
import pandas as pd
from matching_algorithm import *
from Bio import Entrez
import json


def get_data(article, name):
    return getattr(article, name, 'N/A')


def generate_black_list():
    black_list_from_excel = pd.read_excel(
        'venv/List_of_common_words_to_use_as_black_list_for_dictionary_development.xlsx')
    black_list_data = pd.DataFrame(black_list_from_excel, columns=['WORD'])
    return [''.join(map(str, str(word))) for word in black_list_data['WORD'].to_list()]


def search(query, num_results):
    Entrez.email = 'lbalentovic8@gmail.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax=num_results,
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'lbalentovic8@gmail.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


'''
if __name__ == '__main__':

    # Make the query on PubMed
    pubmed = PubMed(tool="PubMedSearcher", email="daspranab239@gmail.com")
    search_term = input("Search PMC Full-Text Archive:\n")
    num_results = int(input("How many articles do you want?\n"))
    results = pubmed.query(search_term, max_results=num_results)
    black_list = generate_black_list()
    print(black_list)
    articleList = []
    articleInfo = []
    print(results)
    print('Found articles: ')
    i = 0

    # Compose the information dictionary to put in the dataframe, given the query
    for article in list(results):
        assert results.__class_getitem__(i) in list(results)
        pubmedId = article.pubmed_id.partition('\n')[0]
        abstract = article.abstract
        keywords = get_data(article, 'keywords')
        pertinence_score = pertinence(search_term, results.__class_getitem__(i), results, num_results, black_list)

        articleInfo.append({
            u'pubmed_id': pubmedId,
            u'title': article.title,
            u'keywords': keywords,
            u'journal': get_data(article, 'journal'),
            u'abstract': abstract,
            u'conclusions': get_data(article, 'conclusions'),
            u'methods': get_data(article, 'methods'),
            u'results': get_data(article, 'results'),
            u'copyrights': article.copyrights,
            u'doi': article.doi,
            u'publication_date': article.publication_date,
            u'authors': article.authors,
            u'pertinence': pertinence_score})
        i = i + 1

    # Put all information in the dataframe
    df = pd.DataFrame(articleInfo)
    #print(df.iloc[:, :])

    # Convert the dataframe into a .csv file
    with open('csv_db.txt', 'w') as csv_db:
        df.to_csv(path_or_buf=csv_db, index=False)
    '''

if __name__ == '__main__':
    search_term = input("Search PMC Full-Text Archive:\n")
    num_results = int(input("How many articles do you want?\n"))
    results = search(search_term, str(num_results))
    id_list = results['IdList']
    papers = fetch_details(id_list)
    emp = []
    pertinence_list = []
    black_list = generate_black_list() + ['<', '>']
    referring_dictionary = create_dictionary(papers, black_list)
    print(referring_dictionary)
    for i, paper in enumerate(papers['PubmedArticle']):
        # print("{}) {}".format(i+1, paper['MedlineCitation']['Article']['ArticleTitle']))
        article = paper['MedlineCitation']['Article']
        title = str(article['ArticleTitle'])
        if 'AbstractText' in article.keys():
            abstract = str(paper['MedlineCitation']['Article']['Abstract']['AbstractText'])
        else:
            abstract = ""
        emp.append((paper['MedlineCitation']['PMID'],
                    title,
                    paper['MedlineCitation']['KeywordList'],
                    paper['MedlineCitation']['Article']['AuthorList'],
                    abstract))
    df = pd.DataFrame(emp)
    #print(df)

    # Convert the dataframe into a .csv file
    with open('csv_db.txt', 'w') as csv_db:
        df.to_csv(path_or_buf=csv_db, index=False)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
