# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from pymed import PubMed
import pandas as pd
from matching_algorithm import *
from process_pubmed_object import *
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


if __name__ == '__main__':
    search_term = input("Search PMC Full-Text Archive:\n")
    num_results = int(input("How many articles do you want?\n"))
    results = search(search_term, str(num_results))
    id_list = results['IdList']
    papers = fetch_details(id_list)
    emp = []
    pertinence_list = []
    black_list = generate_black_list() + list(string.punctuation)     # To eventually update
    referring_dictionary = create_dictionary(papers, black_list)
    # print(referring_dictionary)
    for i, paper in enumerate(papers['PubmedArticle']):
        # print("{}) {}".format(i+1, paper['MedlineCitation']['Article']['ArticleTitle']))
        article = paper['MedlineCitation']['Article']
        title = str(article['ArticleTitle'])
        emp.append({
            'PMID': paper['MedlineCitation']['PMID'],
            'title': title,
            'keywords': process_keywords(paper),
            'authors': process_authors(article),
            'abstract': process_abstract(article)
        })
    df = pd.DataFrame(emp, columns=['PMID', 'title', 'keywords', 'authors', 'abstract'])
    df.head(num_results)

    # Convert the dataframe into a .csv file
    with open('csv_db.txt', 'w') as csv_db:
        df.to_csv(path_or_buf=csv_db, index=False)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
