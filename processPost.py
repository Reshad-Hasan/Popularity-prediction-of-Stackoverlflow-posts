from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

class title:
    titleLen = 0

    def setTitle(self, data):
        self.titleLen = len(data)

    def getTitleLen(self):
        return self.titleLen


class body:
    codeLen, upCase, lowCase, codeBlock, para, bodyLen = 0, 0, 0, 0, 0, 0
    stopWordCount, nonStopWordCount = 0, 0
    polarity = 0
    subjectivity = 0
    data=''
    def setBody(self, data):
        self.data = data
        self.wordTokens = word_tokenize(data)
        self.processBody()

    def processBody(self):
        cb = False
        for i in range(0, len(self.data)):
            if self.data[i] == '<':
                if self.data[i:3] == '<p>':
                    self.para += 1
                elif self.data[i:3] == '<co':
                    self.codeBlock += 1
                    cb = True
                elif self.data[i:3] == '</c':
                    cb = False
                while self.data[i]!='>':
                    i+=1
                    if cb:
                        self.codeLen+=1
            if cb:
                self.codeLen += 1
            else:
                self.bodyLen += 1
                if self.data[i].islower():
                    self.lowCase+=1
                elif self.data[i].isupper():
                    self.upCase+=1
        self.countStopNonStopWord()
        self.calPolaritySubjectivity()

    def countStopNonStopWord(self):
        stopWords = set(stopwords.words('english'))
        for w in self.wordTokens:
            if w in stopWords:
                self.stopWordCount += 1
            else:
                self.nonStopWordCount += 1

    def getCodeLen(self):
        return self.codeLen

    def getUpCase(self):
        return self.upCase

    def getLowCase(self):
        return self.lowCase

    def getCodeBlockCount(self):
        return self.codeBlock

    def getParaCount(self):
        return self.para

    def getBodyLen(self):
        return self.bodyLen

    def getStopWordCount(self):
        return self.stopWordCount

    def getNonStopWordCount(self):
        return self.nonStopWordCount

    def getPolarty(self):
        return self.polarity

    def getSubjectividy(self):
        return self.subjectivity

    def calPolaritySubjectivity(self):
        text=TextBlob(self.data)

        self.polarity, self.subjectivity = text.sentiment
        a,b=self.polarity,self.subjectivity
        a, b = text.sentiment
        c=10


class feature(title, body):
    featureDict = {
        'titleLen': 0,
        'bodyToTitle': 0,
        'userRep': 0,
        'codeLen': 0,
        'codeToBody': 0,
        'stopWordCount': 0,
        'nonStopWordCount': 0,
        'bodyLen': 0,
        'codBlockCount': 0,
        'polarity': 0,
        'subjectivity': 0,
        'paraCount': 0,
        'tagCount': 0,
        'lowToUp': 0,
        'popularity': 0
    }

    def __init__(self, post):
        self.post = post
        self.setBody(post['body'])
        self.setTitle(post['title'])

    def extractFeatures(self):
        self.featureDict['titleLen'] = self.getTitleLen()
        self.featureDict['bodyToTitle'] = self.getBodyLen() // self.getTitleLen()
        self.featureDict['userRep'] = self.post['reputation']
        self.featureDict['codeLen'] = self.getCodeLen()
        self.featureDict['codeToBody'] = self.getCodeLen() if self.getCodeLen()>0 else 1 // self.getBodyLen() if self.getBodyLen()>0  else 1
        self.featureDict['stopWordCount'] = self.getStopWordCount()
        self.featureDict['nonStopWordCount'] = self.getNonStopWordCount()
        self.featureDict['bodyLen'] = self.getBodyLen()
        self.featureDict['codeBlockCount'] = self.getCodeBlockCount()
        self.featureDict['polarity'] = self.getPolarty()
        self.featureDict['subjectivity'] = self.getSubjectividy()
        self.featureDict['paraCount'] = self.getParaCount()
        self.featureDict['tagCount'] = self.post['tagCount']
        self.featureDict['lowToUp'] = self.getLowCase() // self.getUpCase() if self.getUpCase()>0 else 1
        self.featureDict['popularity'] = self.post['popularity']

    def getFeatures(self):
        self.extractFeatures()
        return self.featureDict


post = {
    'title': '12345',
    'body': "<p>There are some Erlang constructs I would want to use inside Elixir code. One is Erlang list comprehensions.</p><p>My general question is whether there is some way to 'drop down' to writing Erlang code while coding in Elixir (sort of the way you see people embed C in Ruby or TCL or whatever).  My specific question (related to the general) is whether it is possible for me to somehow get Erlang-style list comprehensions while coding in Elixir.</p><p>If this isn't possible with plain Elixir, perhaps it can be done through a macro (possibly difficult?)?  I do understand that I can just write an Erlang module and call it from Elixir, but that's not quite what I'm looking for.</p>'",
    'tagCount': 2,
    'reputation': 4,
    'popularity': 10
}

if __name__=='__main__':
    obj = feature(post)
    print(obj.getFeatures())

    text=TextBlob("<p>There are some Erlang constructs I would want to use inside Elixir code. One is Erlang list comprehensions.</p><p>My general question is whether there is some way to 'drop down' to writing Erlang code while coding in Elixir (sort of the way you see people embed C in Ruby or TCL or whatever).  My specific question (related to the general) is whether it is possible for me to somehow get Erlang-style list comprehensions while coding in Elixir.</p><p>If this isn't possible with plain Elixir, perhaps it can be done through a macro (possibly difficult?)?  I do understand that I can just write an Erlang module and call it from Elixir, but that's not quite what I'm looking for.</p>'")
    print(text.sentiment)
    a,b=text.sentiment
    print(a,b)