import spacy
from collections import Counter
import editdistance

nlp = spacy.load("en_core_web_sm")

class RelevanceClassifier:
    def __init__(self, sources_type = "newsapi"):
        if sources_type == "newsapi":
            self.sources_type = "newsapi"
        else:
            raise NotImplementedError
        
    def _determine_query_type(self, query:str):
        """
        Simple heuristic of what the query is.
        """
        _q_ents = [(e, e.label_) for e in nlp(query).ents \
                   if e.label_ in ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE']]
        _q_types = [e[1] for e in _q_ents]
        if len(_q_ents) == 1:
            query_type = _q_ents[0][1]
        elif len(_q_ents) >= 2 and 'PERSON' in _q_types:
            query_type = 'PERSON'
        else:
            query_type = 'ORG'
        print(f'Query type for {query} -- {_q_ents} will be treated as {query_type}')
        return query_type
        
    def _prepare_text(self, article:dict)->str:
        if self.sources_type == "newsapi":
            article_text = ' '.join([str(article['title']), 
                                     str(article['description']), 
                                     str(article['content'])])
        else:
            #TODO: other news source providers
            pass
        return article_text
        
    def _determine_relevance_single(self, query:str, query_type:str, article_text:str, thresh = 5):
        doc = nlp(article_text)
        #TODO: implement stemmer
        _qual_ents = [e.lemma_.lower() for e in doc.ents \
                               if e.label_ in ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE']]
        _tot_ents = len(_qual_ents)
        _cand_ents = Counter(_qual_ents).most_common(thresh)
        _mentions = 0
        if query_type == 'PERSON':
            _q = query.lower().split()
        else:
            _q = [query.lower()]
        
        for cand in _cand_ents:
            for i in _q:
                _dist = editdistance.eval(cand[0], i)
                _len = max(len(cand[0]), len(i))
                if _dist/_len <= 0.2:
                    _mentions += cand[1]
        
        #control for short articles
        if len(article_text) < 250 and _mentions >= 1:
            return True
        elif _mentions / _tot_ents >= 0.2:
            return True
        else:
            return False
    
    def determine_relevance_batch(self, query:str, articles:list, query_type = None):
        results = []
        if not query_type:
            query_type = self._determine_query_type(query)
        
        for article in articles:
            article_text = self._prepare_text(article)
            relevance = self._determine_relevance_single(query, query_type, article_text)
            article.update({"dn_confidence": '1', "dn_relevance": int(relevance),})
            yield article
            