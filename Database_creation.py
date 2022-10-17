from Bio import Entrez
import pandas as pd


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


def process_abstract(article):
    return str(article['Abstract']['AbstractText'][0]) if 'Abstract' in article.keys() else ""


def process_keywords(paper):
    keywords = list()
    for keyword in paper['MedlineCitation']['KeywordList']:
        keywords.append(str(keyword[0]))
    return keywords


def process_authors(article):
    authors = list()
    for author in article['AuthorList']:
        if 'ForeName' in author.keys() and 'LastName' in author.keys():
            authors.append(author['ForeName'] + " " + author['LastName'])
        else:
            authors.append("")
    return authors

def find_papers(search_term, num_results):
    results = search(search_term, str(num_results))
    id_list = results['IdList']
    papers = fetch_details(id_list)
    return papers

def db_creation(papers):
    emp = []
    pertinence_list = []
    #referring_dictionary = create_dictionary(papers, black_list)
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
    df = pd.DataFrame(emp)
    return df