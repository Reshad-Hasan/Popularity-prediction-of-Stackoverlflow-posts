from naive_bayes import naive_bayes
from process_post import feature
from label_features import label_data
import control as co

test_query = {
    'title': 'How to make textbox as not editable in asp.net(c#)',
    'body': "I've creating one ASP web application, in that application one form have to update date value in the textbox field i put calender button near that textbox. it can update the date in that textbox field but its editable . i want update date value through only using calender button , i used read_table-only property but return empty value so not works .",
    'tagCount': '3',
    'reputation': '142',
    'popularity': None
}


def take_input():
    query = {}
    print('** Input title **')
    query['title'] = input()
    print('** Input Body **')
    print('[Paragraphs must be in <p></p> tag', end=' | ')
    print('Codes must be in <code></code> tag]')
    query['body'] = input()
    print('**Input tags** \n [each tag must be separated by comma(,)]')
    s = input()
    tc = s.count(',') + 1
    query['tagCount'] = str(tc) if len(s) else ''  # tagCount empty for zero tags
    print('** Enter reputation on stack-overflow **')
    query['reputation'] = input()
    query['popularity'] = None
    return query


ques = take_input()
obj = feature(ques)  # extracting features
f = obj.get_features()  # returns features dictionary
label = label_data()
f = label.label_post(f)  # labeling features according to data boundaries
print('group values for each attribute')
print(f)
nb = naive_bayes()
nb.read_table()  # reading frequency table essential for naive bayes algorithm
result, probability = nb.get_result(f)
if co.score_group_num != 2:
    result = label.bound['popularity'][result]
else:
    if result:
        result = 'Positive'
    else:
        result = 'Negative'
print('Your score will be :', result)
print('With probability -', probability)
