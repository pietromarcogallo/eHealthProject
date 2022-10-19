from scoring import *

if __name__ == '__main__':
    search_term = input("Search PMC Full-Text Archive:\n")
    while True:
        try:
            num_results = int(input("How many articles do you want?\n"))
            break
        # If the user doesn't answer with a number, the message will be repeated until it happens
        except ValueError:
            print('Answer not recognised: please insert an integer number...')
    black_list = generate_black_list() + list(string.punctuation)

    # Using entrez API to gather articles
    papers = find_papers(search_term, str(num_results))

    # Articles are placed in a dataframe
    df = db_creation(papers)

    # Convert the dataframe into a .csv file
    with open('csv_db.txt', 'w', encoding='utf-8') as csv_db:
        df.to_csv(path_or_buf=csv_db, index=False)

    # Creating the reference dictionary with associated weights based of relative frequency
    # of occurrences over the number of abstracts
    occurrences = create_dictionary(papers, black_list)
    f_occurrences = convert_to_float(occurrences)
    ref_dictionary = words_weight_assig(f_occurrences, num_results)
    # Adding the input string as a ref_dict key with value 1
    search_term = search_term.lower()
    input_string = {search_term: 1}
    ref_dictionary.update(input_string)

    # Articles PMID to be classified are inserted in id_list
    id_list = ['33549739', '30195575', '31570648', '33843998', '26585576', '30091808', '29150311',
               '34797010', '25985979', '22013285', '29864032']

    #1Y, 2Y, 3Y, 4Y, 5Nb,
    cpapers = fetch_details(id_list)

    # Creating dictionaries for each article to be classified
    Tdict = create_tdictionary(cpapers, "")  # Title dictionaries
    Kdict = create_kdictionary(cpapers, "")  # Keywords dictionaries
    Adict = create_adictionary(cpapers, black_list)  # Abstract dictionaries

    # Checking common words between the referring dictionary and the other ones
    sk_title = same_keys(ref_dictionary, Tdict, cpapers)
    sk_keywords = same_keys(ref_dictionary, Kdict, cpapers)
    sk_abstract = same_keys(ref_dictionary, Adict, cpapers)

    # Assigning a score to each article
    scoreA = scoring_assignment(ref_dictionary, Adict, sk_abstract)
    scoreK = scoring_assignment(ref_dictionary, Kdict, sk_keywords)
    scoreT = scoring_assignment(ref_dictionary, Tdict, sk_title)
    score = fin_score(scoreT, scoreK, scoreA)
    score = norm(score)

    # Creating a database of the articles to classify with the related score
    cdf = db_creation(cpapers)
    cdf['score'] = score

    # Convert the dataframe into a .csv file
    with open('csv_c.txt', 'w', encoding='utf-8') as csv_c:
        cdf.to_csv(path_or_buf=csv_c, index=False)
    print(ref_dictionary)
