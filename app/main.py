import os

from fastapi import FastAPI
from newsapi import NewsApiClient

from dedup_service import DedupSRVC
from rel_clf import RelevanceClassifier

API_KEY = os.getenv('API_KEY')

app = FastAPI()
dedup_svc = DedupSRVC()
rel_clf = RelevanceClassifier()
newsapi = NewsApiClient(api_key=API_KEY)

@app.get("/")
async def read_root():
    message = f"Hello, this is a demo of NewsAPI with heuristic-based entity relevance classifier and duplication detection based on title.\n Use /articles endpoint"
    return {"message": message}

@app.get("/articles/")
async def process_articles(search_query: str, language: str = "en", API_KEY: int = None):
    #TODO: flesh out swagger defs
    #TODO: sanitize inputs
    #TODO: error handling
    if API_KEY: #start news client with provided API keys
        newsapi_p = NewsApiClient(api_key=API_KEY)
        all_articles = newsapi_p.get_everything(q=search_query,
                                      language=language,
                                      sort_by='relevancy',
                                      page_size=100,
                                      page=1)
    else:
        all_articles = newsapi.get_everything(q=search_query,
                                      language=language,
                                      sort_by='relevancy',
                                      page_size=100,
                                      page=1)
    dup_assnd_arts, _ = dedup_svc.assign_duplicates(all_articles['articles'])
    gen = rel_clf.determine_relevance_batch(search_query, dup_assnd_arts)
    resp_articles = []
    for i in gen:
        resp_articles.append(i)
    resp_len = len(resp_articles)
    
    return {
        "query": search_query,
        "results": resp_len,
        "articles": resp_articles,
    }




if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description='This is a demo of NewsAPI \
        with heuristic-based entity relevance classifier and duplication \
        detection based on title.')
    parser.add_argument("--search_query",
        default=None, type=str,required=True,
        help="The search query to issue against NewsAPI",
    )
    parser.add_argument("--language", type=str, default="en", help="Language of the input.")
    parser.add_argument("--api_key", type=str, default=None, help="APIKEY for the Newsapi service. Get yours at - https://newsapi.org/")
    args = parser.parse_args()
    
    search_query = args.search_query
    language = args.language
    if not args.api_key:
        API_KEY = os.getenv('API_KEY')
    else:
        API_KEY = args.api_key
        
    newsapi = NewsApiClient(api_key=API_KEY)
    print(f"q-{search_query},  l-{language},  apikey-{API_KEY}")
    all_articles = newsapi.get_everything(q=search_query,
                                      language=language,
                                      sort_by='relevancy',
                                      page_size=100,
                                      page=1)
    dup_assnd_arts, _ = dedup_svc.assign_duplicates(all_articles['articles'])
    gen = rel_clf.determine_relevance_batch(search_query, dup_assnd_arts)
    resp_articles = []
    for i in gen:
        resp_articles.append(i)
    resp_len = len(resp_articles)
    payload = {
        "query": search_query,
        "results": resp_len,
        "articles": resp_articles,
    }
    
    print(json.dumps(payload, indent=4))


    