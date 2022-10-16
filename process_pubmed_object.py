def process_abstract(article):
    return str(article['Abstract']['AbstractText'][0]) if 'Abstract' in article.keys() else ""


def process_keywords(paper):
    keywords = list()
    for keyword in paper['MedlineCitation']['KeywordList']:
        keywords.append(str(keyword[0]))
    return keywords


def process_authors(article):
    if 'AuthorList' not in article.keys():
        return []
    authors = list()
    for author in article['AuthorList']:
        if 'ForeName' in author.keys() and 'LastName' in author.keys():
            authors.append(str(author['ForeName']) + " " + str(author['LastName']))
    return authors