#Exploratory data analysis
#ohamilton79
#01/09/2020

import pandas
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#Unpickle the DTM and corpus
data_dtm = pickle.load(open("dtm.pkl", "rb"))
df = pickle.load(open("corpus.pkl", "rb"))
    
#Find top 10 words for Trump and for Biden
data_dtm = data_dtm.transpose()
topDict = {}

for c in data_dtm.columns:
    topWords = data_dtm[c].sort_values(ascending=False).head(10)
    topDict[c] = list(zip(topWords.index, topWords.values))

#Configure plot size
plt.figure(figsize=(12, 5))

#Create word clouds using raw corpus
wc = WordCloud(background_color="black", colormap='rainbow', max_font_size=200, max_words=500, collocations=False)

for index, person in enumerate(topDict):
    wc.width = 1000
    wc.height = 1000
    wc.generate(df.transpose()[person].tweets)

    plt.subplot(1, 2, index+1)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(person)

plt.show()

#Plot graphs showing the 10 most common words for Trump and for Biden
for person in topDict.keys():
    #Configure plot size for graphs
    plt.figure(figsize=(15, 5))
    
    wordProperties = {word[0]: word[1] for word in topDict[person]}
    #Ignore 'll', which appears due to removing apostrophes
    if ("ll" in wordProperties):
        wordProperties.pop("ll")

    #Plot most common words as a bar graph for each person
    plt.title(person + "'s 10 most common words")
    plt.xticks(range(len(wordProperties)), wordProperties.keys())
    plt.bar(range(len(wordProperties)), wordProperties.values())
    plt.show()
