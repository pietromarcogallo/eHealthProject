# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from pymed import PubMed
import pandas as pd
from pertinence import *
import json


def get_data(article, name):
    return getattr(article, name, 'N/A')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Make the query on PubMed
    pubmed = PubMed(tool="PubMedSearcher", email="daspranab239@gmail.com")
    search_term = input("Search PMC Full-Text Archive:\n")
    results = pubmed.query(search_term, max_results=int(input("How many articles do you want?\n")))
    articleList = []
    articleInfo = []

    # Compose the information dictionary to put in the dataframe, given the query
    for article in results:
        pubmedId = article.pubmed_id.partition('\n')[0]
        abstract = article.abstract
        keywords = get_data(article, 'keywords')

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
            u'pertinence': pertinence(abstract, keywords)})

    # Put all information in the dataframe
    df = pd.DataFrame(articleInfo)
    # print(df.iloc[:, 0:2])

    # Convert the dataframe into a .csv file
    with open('csv_db.txt', 'w') as csv_db:
        df.to_csv(path_or_buf=csv_db, index=False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
