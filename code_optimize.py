import csv

feature_keys = ['titleLen', 'bodyToTitle', 'userRep', 'codeLen', 'codeToBody', 'stopWordCount',
                'nonStopWordCount', 'bodyLen', 'codeBlockCount', 'polarity', 'subjectivity',
                'paraCount', 'tagCount', 'lowToUp', 'popularity'
                ]

post_columns = ['title', 'body', 'tagCount', 'reputation', 'popularity']

processed_data_path = 'C:\\Users\\Reshad Hasan\\Desktop\\processed_data-50000.csv'

csv_reading_path = 'C:\\Users\\Reshad Hasan\\Desktop\\data-50000.csv'

ENCODING = 'utf-8'

labeled_data_path = 'C:\\Users\\Reshad Hasan\\Desktop\\labeled_data-50000.csv'

frequency_table_path = 'C:\\Users\\Reshad Hasan\\Desktop\\frequency   -50000.csv'


def readcsv_file(file_path):
    ex_feature_list = []
    with open(file_path, 'r', encoding=ENCODING) as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:
            for k in row.keys():
                row[k] = float(row[k])
            ex_feature_list.append(row)
    return ex_feature_list
