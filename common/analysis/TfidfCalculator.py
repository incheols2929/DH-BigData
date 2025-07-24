import warnings

from common.handler.FileHandler import FileHandler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from common.utils import write_log
warnings.filterwarnings(action='ignore')

class TfidfCalculator():  
    def __init__(self):
        self.fh = FileHandler()

    def get_count_vector(self, tokenized_sentence_list):
        # TF Vector
        vect = CountVectorizer(token_pattern=r'\S+')
        bow_vect  = vect.fit_transform(tokenized_sentence_list)
        word_list = vect.get_feature_names_out()
        count_list = bow_vect.toarray().sum(axis=0)
        
        return [vect, bow_vect]

    def get_tfidf_vector(self, vector):
        tfidf_vectorizer = TfidfTransformer()
        tf_idf_vect = tfidf_vectorizer.fit_transform(vector)

        return tf_idf_vect