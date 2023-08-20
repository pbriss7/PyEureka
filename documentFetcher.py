import requests
import json
import pandas as pd
import getpass
import time
import os

# Load configuration from config.json
with open("config.json", "r") as file:
    config = json.load(file)

BASE_URL = config["BASE_URL"]
ENDPOINTS = config["API_ENDPOINTS"]

def authenticate():
    """Fonction qui permet d'acquérir un token. L'utilisateur doit fournir son identifiant Cision et son mot de passe.

    Returns:
        str: token
    """
    base_url = "https://api.cedrom-sni.com/api/auth/login"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Get the username and password from the user
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password (input will be hidden): ")

    data = {
        "grant_type": "password",
        "username": username,
        "password": password
    }

    response = requests.post(base_url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]
    
def simple_search(token, query, days, max_count):
    """Fonction pour lancer une requête simple.

    Args:
        token (str): token obtenu avec la fonction authentificate()
        query (str): mots-clés
        days (int): The number of days, starting from the current date, to include in the search. Use 0 to search only for the documents that came out today.
        max_count (int): nbre maximal de notices retournées

    Returns : Exemple:
        json: "documentId": "news·20230810·LAA·fe18d5b08a53380bba2133259720102e",
        "publicationName": "La Presse+",
        "byLine": "Philippe Teisceira-Lessard",
        "title": "CDPQ Infra reporte son échéance à 2027",
        "publicationDate": "2023-08-10T00:00:00",
        "availableDate": "0001-01-01T00:00:00",
        "publicationTime": "",
        "publicationCode": "LAA",
        "inContext": "... La future station du Réseau express métropolitain (REM) <mark> Griffintown</mark>–Bernard-Landry sera construite d’ici 2027, a indiqué mercredi CDPQ Infra, qui évoquait jusqu’à maintenant une échéance en 2024.   ...",
        "language": "fr",
        "wordCount": 775,
        "externalLinks": {
            "document": "https://nouveau.eureka.cc/WebPages/Document/WsDocViewer.aspx?wsdoc=%c2%b1P33F39mGG0oTaFU4CJzrSrvKIHclbxjSVsw%c2%b1i56CRCiXQf8UHnBnhE5mBgsYVhGRitUWraPkCo3uxZv4cXv%2fkbL8zOC%2fLYZTdjfhyObVnzBZXuAnb2zrnwLkTj5RWo9"
        },
        "apiLinks": {
            "document": "/api/v2/Documents/news·20230810·LAA·fe18d5b08a53380bba2133259720102e"
        },
        "attachmentInfos": []
    """
    url = BASE_URL + ENDPOINTS["SEARCH_SIMPLE"]
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    params = {
        "searchText": query,
        "numberOfDays": days,
        "maxCount": max_count
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def advanced_search(token, query, startDate, endDate, maxCount, document_type, docUrl):
    """_summary_

    Args:
        token (str): token obtenu avec la fonction authentificate()
        query (str): The query used to search in our system. See section \"SEARCH QUERY DOCUMENTATION\" for documentation.
        document_type (str): The document base which determines which type of documents will be returned. The available document bases are News, Companies and Biographies. If not specified, News will be used."
        date_range (str): Date range at which search is restricted. Possible values are: TODAY, SINCE_YESTERDAY, DAYS_3, DAYS_7, DAYS_30, MONTHS_3, MONTHS_6, YEARS_1, YEARS_2, ALL. If dateRange, startDate and endDate are not specified, \"Date Range\" value of search preference from Eureka web site is used.
        includes (str): An array containing criterion and/or publication ids restricting what must be included in the search. If this parameter and <b>excludes</b> are not specified, all the user sources will be used. See \"<b>/Criteria</b>\" and \"<b>/Publications</b>\" to get a list of possible values.
        excludes (str): An array containing criterion and/or publication ids restricting what must be excluded from the search. If this parameter and <b>includes</b> are not specified, all the user sources will be used. See \"<b>/Criteria</b>\" and \"<b>/Publications</b>\" to get a list of possible values.
        docUrl: Indicates that you want an external link to the document with the http(s) protocol you want
        startDate: The date from which the search much start. Only used if <b>dateRange</b> is not specified. "default": "2023-02-26T00:00:00-05:00"
        endDate: The date at which the search much end. Only used if <b>dateRange</b> is not specified. "default": "2023-02-27T00:00:00-05:00"
        sort: (Optional) Indicates the order in which the documents should be sorted. Possible values are: <b>relevance</b>, <b>date</b>

    Returns:
        json: résultat de la requête
    """
    url = BASE_URL + ENDPOINTS["SEARCH_ADVANCED"]
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    params = {
        "query": query,
        "documentBase": document_type,
        # "dateRange": date_range,
        # "includes": includes,
        # "excludes": excludes,
        "docUrl": docUrl,
        "startDate": startDate,
        "endDate": endDate,
        "maxCount": maxCount,
        # "sort": sort
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def get_document(token, document_id):
    """Fonction de requête d'un document

    Args:
        token (str): token obtenu par la fonction authenticate
        document_id (str): identifiant unique

    Returns:
        dictionnaire: dictionnaire de dictionnaires
    """
    url = BASE_URL + ENDPOINTS["DOCUMENT"] + document_id
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None



def extract_metadata(search_results):
    """Fonction d'extraction des métadonnées de la requête de recherche avancée

    Args:
        search_results (list): liste de dictionnaires

    Returns:
        list: métadonnées principales 
    """
    metadata_list = []

    for document in search_results['result']:
        metadata = {
            "Document ID": document['documentId'],
            "Title": document['title'],
            "Publication Name": document['publicationName'],
            "Publication Date": document['publicationDate'],
            "Language": document['language'],
            "Word Count": document['wordCount'],
            "External Link": document['externalLinks']['document'],
            "API Link": document['apiLinks']['document'],
            "In Context": document['inContext']
        }
        metadata_list.append(metadata)

    return metadata_list

def fetch_full_documents(token, metadata_list):
    """Cette fonction prend en entrée le token et la liste des métadonnées comprenant, notamment, les Identifiants qui serviront à obtenir les textes complets.

    Args:
        token (str): token issu de la fonction authenticate()
        metadata_list (list): liste des métadonnées issues de l'exécution de la fonction extract_metadata() 

    Returns:
        list: liste comprenant, pour chaque document, les métadonnées d'un document et son texte complet
    """
    for doc_metadata in metadata_list:
        # Obtention d'un document
        document_id = doc_metadata["Document ID"]
        full_document_data = get_document(token, document_id)

        # Extraction de nouvelles métadonnées
        doc_content = full_document_data['documentContent']
        doc_author = doc_content.get('author', "")
        doc_section = doc_content.get('section', "")
        doc_kicker = doc_content.get('kicker', "")
        doc_coverage = doc_content.get('coverage', "")
        doc_subjects = doc_content.get('subjects', "")
        doc_persons = doc_content.get('persons', "")
        doc_organizations = doc_content.get('organizations', "")
        doc_locations = doc_content.get('locations', "")
        doc_lead = doc_content.get('lead', "")

        # Extraction du texte d'un document
        doc_text = doc_content.get('text', "")
        
        # Ajout du texte et des nouvelles métadonnées dans la liste existante
        doc_metadata["auteur"] = doc_author
        doc_metadata["section"] = doc_section
        doc_metadata["texte_complet"] = doc_text
        doc_metadata["kicker"] = doc_kicker
        doc_metadata["couverture"] = doc_coverage
        doc_metadata["sujets"] = doc_subjects
        doc_metadata["personnes"] = doc_persons
        doc_metadata["organisations"] = doc_organizations
        doc_metadata["lieux"] = doc_locations
        doc_metadata["lead"] = doc_lead

    return metadata_list


def save_to_csv(data_list, filename="document.csv"):
    # Convert the list to a DataFrame
    df = pd.DataFrame(data_list)
    
    # Check if file exists
    if os.path.exists(filename):
        # Append without writing the header
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        # Save new DataFrame to .csv
        df.to_csv(filename, index=False)


def master_search_to_csv():
    """Fonction maîtresse. L'utilisateur doit fournir son ID + mot de passe, puis il est guidé dans l'interrogation de la bdd.
    """
    token = authenticate()
    
    # Informations requises pour la requête (les paramètres peuvent être modifiés au besoin)
    search_query = input("Enter your search query: ")
    document_type = "News"
    docUrl = "https"
    startDate = input("Date de départ de la requête (YYYY-MM-DD)")
    endDate = input("Date finale de la requête (YYYY-MM-DD)")
    maxCount = input("Combien de document au maximum?")
    search_results = advanced_search(token, search_query, document_type=document_type,docUrl=docUrl,startDate=startDate,endDate=endDate,maxCount=maxCount)
    
    # Extraction des métadonnées issues de la requête
    start_time = time.time()
    metadata_list = extract_metadata(search_results)
    
    # Itération sur les identifiants de la liste pour obtenir les textes et de nouvelles métadonnées
    full_data_list = fetch_full_documents(token, metadata_list)
    
    # Transformation de la liste en DataFrame, puis sauvegarde en .csv
    save_to_csv(full_data_list)

    end_time = time.time()  # End time after loading
    
    duration = end_time - start_time

    print(f"Data saved to {startDate}_{endDate}.csv")
    print(f"L'opération a pris {duration:.2f} secondes.")

master_search_to_csv()