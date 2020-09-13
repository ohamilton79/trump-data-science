#Create corpus from tweets
#ohamilton79
#31/08/2020
import pickle
import csv
import pandas

def clean_text(text):

    #If the text ends with a link, remove it
    if "http" in text:
        linkStart = text.index("http")
        text = text[0:linkStart]
    #Strip leading / trailing whitespace
    text = text.strip()
    #Convert all text to lowercase
    text = text.lower()

    #Strip new lines
    text = " ".join(text.splitlines())
          
    #Remove nonsensical characters
    badChars = ["&amp;", "!", "?", ".", ",", ":: ", ":", "– ", '"', "“", "”", "£", "$", "%", "(", ")", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    badChars2 = [";", "-", "   ", "  ", "—"]

    for badChar in badChars:
        text = text.replace(badChar, "")

    for badChar in badChars2:
        text = text.replace(badChar, " ")

    #Perform a second round of cleaning
    text = clean_text_2(text)
    return text

#Clean individual words
def clean_text_2(text):

    newText = ""
    #Create an array, where each element is a word
    wordsArray = text.split(' ')
    for word in wordsArray:
        #If the word doesn't begin with a hashtag or @ symbol (twitter account link), it can be kept
        if (len(word) > 0 and word[0] != "#" and word[0] != "@"):
            newText += word.strip() + " "

    #Strip the final collection of words of leading / trailing whitespace
    newText.strip()
    return newText

#Clean a users tweets in a csv file
def clean_tweets(fileName):

    #Stores all the tweets collected together
    tweets = ""

    with open(fileName) as csvFile:
        csvReader = csv.reader(csvFile)

        #Counter
        lineCount = 0
        for row in csvReader:
            #Ignore the first row
            if lineCount == 0:
                lineCount += 1
                continue

            #If the text begins with 'RT' (retweet) or http (a link), ignore it
            if row[1][0:2] != "RT" and row[1][0:4] != "http":

                #Clean tweet
                cleanedTweet = clean_text(row[1])
                #Append to tweets variable
                tweets += cleanedTweet

            #Increment the counter
            lineCount += 1

    return tweets


#Clean the tweets of trump and biden
trumpTweets = clean_tweets('donald_tweets.csv')
bidenTweets = clean_tweets('biden_tweets.csv')

#Create a dictionary
tweetsDict = {"Trump": [trumpTweets], "Biden": [bidenTweets]}

#Create a corpus from this dictionary
pandas.set_option('max_columns', 500)
pandas.set_option('max_colwidth', 500)
df = pandas.DataFrame.from_dict(tweetsDict).transpose()
df.columns = ["tweets"]
df = df.sort_index()

#Pickle the corpus for later use
df.to_pickle('corpus.pkl')
