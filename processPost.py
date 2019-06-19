from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import code_optimize as CO


class title:
    titleLen: int = 0

    def set_title(self, data):
        self.titleLen = len(data)

    def get_title_len(self):
        return self.titleLen


class body:
    codeLen, upCase, lowCase, codeBlock, para, bodyLen = 0, 0, 0, 0, 0, 0
    stopWordCount, nonStopWordCount = 0, 0
    polarity = 0
    subjectivity = 0
    data = ''

    def set_body(self, data):
        self.data = data
        self.wordTokens = word_tokenize(data)
        self.process_body()

    def process_body(self):
        cb = False
        i = 0
        while i < len(self.data):
            if self.data[i] == '<':
                token = self.data[i] + self.data[i + 1] + self.data[i + 2]
                if token == "<p>":
                    self.para += 1
                elif token == "<co":
                    self.codeBlock += 1
                    cb = True
                elif token == "</c":
                    cb = False
                while self.data[i] != '>':
                    i += 1
                    if cb:
                        self.codeLen += 1
                i += 1
            if cb:
                self.codeLen += 1
            else:
                self.bodyLen += 1
                if self.data[i].islower():
                    self.lowCase += 1
                elif self.data[i].isupper():
                    self.upCase += 1
            i += 1
        self.count_stop_non_stop_word()
        self.cal_pol_sub()

    def count_stop_non_stop_word(self):
        stopWords = set(stopwords.words('english'))
        for w in self.wordTokens:
            if w in stopWords:
                self.stopWordCount += 1
            else:
                self.nonStopWordCount += 1

    def get_code_len(self):
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

    def cal_pol_sub(self):
        text = TextBlob(self.data)

        self.polarity, self.subjectivity = text.sentiment
        a, b = self.polarity, self.subjectivity
        a, b = text.sentiment
        c = 10



class feature(title, body):
    featureDict = dict((i, 0.0) for i in CO.feature_keys)

    def __init__(self, post):
        self.post = post
        self.set_body(post['body'])
        self.set_title(post['title'])
    def getTagCount(self):
        if self.post['tagCount'] in '':
            return 0
        return self.post['tagCount']
    def extract_features(self):
        self.featureDict['titleLen'] = self.get_title_len()
        self.featureDict['bodyToTitle'] = self.getBodyLen() //\
                                          (self.get_title_len() if self.get_title_len() > 0 else 1)
        self.featureDict['userRep'] = self.post['reputation']
        self.featureDict['codeLen'] = self.get_code_len()
        self.featureDict['codeToBody'] = (self.get_code_len() if self.get_code_len() > 0 else 1) // \
                                         (self.getBodyLen() if self.getBodyLen() > 0 else 1)
        self.featureDict['stopWordCount'] = self.getStopWordCount()
        self.featureDict['nonStopWordCount'] = self.getNonStopWordCount()
        self.featureDict['bodyLen'] = self.getBodyLen()
        self.featureDict['codeBlockCount'] = self.getCodeBlockCount()
        self.featureDict['polarity'] = self.getPolarty()
        self.featureDict['subjectivity'] = self.getSubjectividy()
        self.featureDict['paraCount'] = self.getParaCount()
        self.featureDict['tagCount'] = self.getTagCount()
        self.featureDict['lowToUp'] = self.getLowCase() // self.getUpCase() if self.getUpCase() > 0 else 1
        self.featureDict['popularity'] = self.post['popularity']

    def getFeatures(self):
        self.extract_features()
        neededFeatures={}
        for k in CO.feature_keys:
            neededFeatures[k]=self.featureDict[k]
        return neededFeatures


post = {
    'title': '12345',
    'body': "<p>There are some Erlang constructs I would want to u" +
            "se inside Elixir code. One is Erlang list comprehensions." +
            "</p><p>My general question is whether there is some way to " +
            "'drop down' to writing Erlang code while coding in Elixir " +
            "(sort of the way you see people embed C in Ruby or TCL or whatever)." +
            "  My specific question (related to the general) is whether it is " +
            "possible for me to somehow get Erlang-style list comprehensions while" +
            " coding in Elixir.</p><p>If this isn't possible with plain Elixir," +
            " perhaps it can be done through a macro (possibly difficult?)?  " +
            "I do understand that I can just write an Erlang module and call it " +
            "from Elixir, but that's not quite what I'm looking for.</p>'",
    'tagCount': 2,
    'reputation': 4,
    'popularity': 10
}

if __name__ == '__main__':
    obj = feature(post)
    print(obj.getFeatures())

    text = TextBlob("<p>There are some Erlang constructs I would want to u" +
                    "se inside Elixir code. One is Erlang list comprehensions." +
                    "</p><p>My general question is whether there is some way to " +
                    "'drop down' to writing Erlang code while coding in Elixir " +
                    "(sort of the way you see people embed C in Ruby or TCL or whatever)." +
                    "  My specific question (related to the general) is whether it is " +
                    "possible for me to somehow get Erlang-style list comprehensions while" +
                    " coding in Elixir.</p><p>If this isn't possible with plain Elixir," +
                    " perhaps it can be done through a macro (possibly difficult?)?  " +
                    "I do understand that I can just write an Erlang module and call it " +
                    "from Elixir, but that's not quite what I'm looking for.</p>'"
                    )
    print(text.sentiment)
    a, b = text.sentiment
    print(a, b)
