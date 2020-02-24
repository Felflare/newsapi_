FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app
COPY requirements.txt /app/requirements.txt

ENV API_KEY=#<REPLACE WITH YOUR OWN API KEY FROM https://newsapi.org/>

RUN pip install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm