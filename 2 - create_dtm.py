#Create the document-term matrix
#ohamilton79
#01/09/2020

import pandas
import pickle

#Create a document term matrix using CountVectorizer, and exclude common stop words
from sklearn.feature_extraction.text import CountVectorizer

#Unpickle the corpus
df = pickle.load(open("corpus.pkl", "rb"))

#Create DTM
cv = CountVectorizer(stop_words='english', ngram_range=(1, 1))
data_cv = cv.fit_transform(df.tweets)
#Convert to pandas data frame
data_dtm = pandas.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
data_dtm.index = df.index

#Pickle the dtm and CountVectorizer object
data_dtm.to_pickle('dtm.pkl')
pickle.dump(cv, open("cv.pkl", "wb"))

