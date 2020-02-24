from snapy import MinHash, LSH
import uuid

class DedupSRVC:
    def __init__(self, sources_type = "newsapi"):
        if sources_type == "newsapi":
            self.sources_type = "newsapi"
        else:
            raise NotImplementedError
        self.n_gram = 9
        self.seed = 42
        self.lsh_bands = 50
        self.j_thresh = 0.05
        
    def _prepare_articles(self, articles, field = 'title'):
        _ctnt = [str(a[field]) for a in articles]
        return _ctnt
    
    def identify_dublicates(self, ctnt_to_dedup):
        _ix = [i for i in range(len(ctnt_to_dedup))]
        _mn_hash = MinHash(ctnt_to_dedup, n_gram = self.n_gram, seed=self.seed)
        _lsh = LSH(_mn_hash, _ix, no_of_bands=self.lsh_bands)
        candidates = _lsh.adjacency_list(min_jaccard=self.j_thresh)
        return candidates
    
    def assign_uuid(articles):
        results = []
        for i in enumerate(articles):
            i.update({'dn_id' : str(uuid.uuid4())})
        return results
    
    def assign_duplicates(self, articles):
        articles = self.assign_uuid(articles)
        ctnt = self._prepare_articles(articles)
        dup_idx = self.identify_dublicates(ctnt)
        for ix, i in enumerate(articles):
            dups = dup_idx[ix]
            if dups:
                for j in dups:
                    dup_ids = [articles[j]['dn_id'] for j in dup_idx[ix]]
            else:
                dup_ids = []
            i.update({'dn_duplicate_ids' : dup_ids,})
        return articles, dup_idx
            
    @staticmethod
    def assign_uuid(articles):
        _ = [i.update({'dn_id' : str(uuid.uuid4())}) for i in articles]
        return articles
        