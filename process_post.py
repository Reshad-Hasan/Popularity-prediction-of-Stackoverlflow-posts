from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import control as co


class title:
    titleLen: int = 0

    def set_title(self, data):
        count = 0
        for i in data:
            if i == ' ':
                continue
            count += 1
        self.titleLen = count

    def get_title_len(self):
        return self.titleLen


class body:
    # attributes of body
    codeLen, upCase, lowCase, codeBlock, para, bodyLen = 0, 0, 0, 0, 0, 0
    stopWordCount, nonStopWordCount = 0, 0
    polarity = 0
    subjectivity = 0
    data = ''

    # set input data as class attribute and calls process_body()
    def set_body(self, data):
        self.data = data
        self.word_tokens = word_tokenize(data)
        self.process_body()

    # process the body to extract features
    def process_body(self):
        cb = False
        # <p> in paragraph token
        # <code> in code token
        # </code> end of code segment
        # using this token para_count,code_block_count is calculated
        for i in range(len(self.data)):
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
            if i >= len(self.data):
                break
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

    # right_ans stop words and non stop words using nltk package
    def count_stop_non_stop_word(self):
        stop_words = set(stopwords.words('english'))
        for w in self.word_tokens:
            if w in stop_words:
                self.stopWordCount += 1
            else:
                self.nonStopWordCount += 1

    def get_code_len(self):
        return self.codeLen

    def get_up_count(self):
        return self.upCase

    def get_low_count(self):
        return self.lowCase

    def get_code_block_count(self):
        return self.codeBlock

    def get_para_count(self):
        return self.para

    def get_body_len(self):
        return self.bodyLen

    def get_stop_word_count(self):
        return self.stopWordCount

    def get_nonstop_word_count(self):
        return self.nonStopWordCount

    def get_polarity(self):
        return self.polarity

    def get_subjectivity(self):
        return self.subjectivity

    # calculates polarity and subjectivity of the body
    def cal_pol_sub(self):
        txt = TextBlob(self.data)
        self.polarity, self.subjectivity = txt.sentiment


# feature class is inherited from title and body class
class feature(title, body):
    # features are stored in dictionary which make it easier to use in naive bayes
    featureDict = dict((i, 0.0) for i in co.feature_keys)

    def __init__(self, input_post):
        self.post = input_post
        self.set_body(input_post['body'])
        self.set_title(input_post['title'])

    # returns number of tags which is explicit in data
    def get_tag_count(self):
        if self.post['tagCount'] in '':
            return 0
        return self.post['tagCount']

    def extract_features(self):
        self.featureDict['titleLen'] = self.get_title_len()
        self.featureDict['bodyToTitle'] = self.get_body_len() // \
                                          (self.get_title_len() if self.get_title_len() > 0 else 1)
        self.featureDict['userRep'] = self.post['reputation']
        self.featureDict['codeLen'] = self.get_code_len()
        self.featureDict['codeToBody'] = (self.get_code_len() if self.get_code_len() > 0 else 1) // \
                                         (self.get_body_len() if self.get_body_len() > 0 else 1)
        self.featureDict['stopWordCount'] = self.get_stop_word_count()
        self.featureDict['nonStopWordCount'] = self.get_nonstop_word_count()
        self.featureDict['bodyLen'] = self.get_body_len()
        self.featureDict['codeBlockCount'] = self.get_code_block_count()
        self.featureDict['polarity'] = self.get_polarity()
        self.featureDict['subjectivity'] = self.get_subjectivity()
        self.featureDict['paraCount'] = self.get_para_count()
        self.featureDict['tagCount'] = self.get_tag_count()
        self.featureDict['lowToUp'] = self.get_low_count() // self.get_up_count() if self.get_up_count() > 0 else 1
        self.featureDict['popularity'] = self.post['popularity']

    # feature class extracts all features but all may not be needed for better accuracy
    # needed_features dictionary is used for experimentation with different combination
    # of features for finding better accuracy
    def get_features(self):
        self.extract_features()
        needed_features = {}
        for k in co.feature_keys:
            needed_features[k] = self.featureDict[k]
        return needed_features


# following part is for testing this file
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
            "I do understand that I can just write_data an Erlang module and call it " +
            "from Elixir, but that's not quite what I'm looking for.</p>'",
    'tagCount': 2,
    'reputation': 4,
    'popularity': 10
}

if __name__ == '__main__':
    obj = feature(post)
    print(obj.get_features())
