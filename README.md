# newsapi_

### Intro

This repository provides an overview of pulling news articles from [NewsAPI](https://newsapi.org/).
In addition the code here will do a simple deduplication based on the title and entity relevance determination.

Deduplication is based on Min-hash & LSH
While relevance detemination is based on Spacy and a simple heuristic.

To run the code, clone the repo, then install the requirements
```bash
pip install -r requirements.txt
```

The entry is located at:
```bash
app/main.py
```
The code can be executed via:
```bash
main.py --search_query Bloomberg --language en --api_key <APIKEY HERE>
```
You will need to provision your APIKEYS from [NewsAPI](https://newsapi.org/) yourself.
***
### Docker
Additionally, the repository contains a Dockerfile that can deploy a service
**Make sure to obtain API KEYs from [NewsAPI](https://newsapi.org/) and include it in the Dockerfile on line #6**
> ENV API_KEY=#<REPLACE WITH YOUR OWN API KEY FROM https://newsapi.org/>

Then, to set up the docker simply run the following commands
```bash
#build docker container based on Dockerfile and tag it
docker build -t news_api ./

#run to start container based on image
docker run -d --name newsapi_ctnr -p 8002:80 -v ~/newsapi_sample/:/data news_api
```
Now you can test if the docker is  running by using python -
```python
# in python to test the connection
import requests
params={
    "search_query":"Bloomberg",    
}
resp = requests.get('http://127.0.0.1:8002/articles',params=params)
print(f'{resp.json()}')
```
***

### Sample Results

* The sample payload looks as follows -
```json
{
    "query": "Bloomberg",
    "results": 100,
    "articles": [
        {
            "source": {
                "id": "wired",
                "name": "Wired"
            },
            "author": "Noam Cohen",
            "title": "Michael Bloomberg, Geezer Tech Bro",
            "description": "He may have founded his startup way back in the early 1980s, but he likes to \u201cmove fast and break things\u201d too.",
            "url": "https://www.wired.com/story/michael-bloomberg-geezer-tech-bro/",
            "urlToImage": "https://media.wired.com/photos/5e45e1590334170008035101/191:100/w_1280,c_limit/Ideas-Bloomberg-Tech-1200442377.jpg",
            "publishedAt": "2020-02-14T13:00:00Z",
            "content": "Bloombergs tech startup wasnt typical. It was always based in New York City, for one thing. The time was the early 1980s, and Bloomberg was 39, a general partner at the prominent Wall Street firm Salomon Brothers. He had been a successful trader who was then \u2026 [+3844 chars]",
            "dn_id": "f9aff21e-8a2b-426f-803d-86784fd5e9f2",
            "dn_duplicate_ids": [],
            "dn_confidence": "1",
            "dn_relevance": 1
        },
```
where fields: 
`"dn_id"` - UUID of the article
`"dn_duplicate_ids"` - list of UUID IDs that are duplicates of the article (based on minhash & LSH hash)
`"dn_confidence"` - Entity relevance confidence, this value is always 1 due to use of a heuristic
`"dn_relevance"` - Entity relevance of an article belonging to the query