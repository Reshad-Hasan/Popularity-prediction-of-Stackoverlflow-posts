import csv

# extracted features list
feature_keys = ['titleLen', 'bodyToTitle', 'userRep', 'codeLen', 'codeToBody', 'stopWordCount',
                'nonStopWordCount', 'bodyLen', 'codeBlockCount', 'polarity', 'subjectivity',
                'paraCount', 'tagCount', 'popularity'
                ]

temp = ['titleLen', 'bodyToTitle', 'userRep', 'codeLen', 'codeToBody', 'stopWordCount',
        'nonStopWordCount', 'bodyLen', 'codeBlockCount', 'polarity', 'subjectivity',
        'paraCount', 'tagCount', 'lowToUp', 'popularity'
        ]

score_group_num = 2
data_group_num = 5

# initial data-set columns
post_columns = ['title', 'body', 'tagCount', 'reputation', 'popularity']

processed_data_path = 'C:\\Users\\Reshad Hasan\\Desktop\\processed_data_all.csv'

csv_reading_path = 'C:\\Users\\Reshad Hasan\\Desktop\\data 60 to 100.csv'

ENCODING = 'utf-8'

labeled_data_path = 'C:\\Users\\Reshad Hasan\\Desktop\\labeled_data_50000.csv'

frequency_table_path = 'frequency table'

labeled_data_path_test = 'C:\\Users\\Reshad Hasan\\Desktop\\labeled_data_test.csv'


# for reading csv as list
def readcsv_file(file_path):
    ex_feature_list = []
    with open(file_path, 'r', encoding=ENCODING) as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:
            for k in row.keys():
                row[k] = float(row[k])
            ex_feature_list.append(row)
    return ex_feature_list
