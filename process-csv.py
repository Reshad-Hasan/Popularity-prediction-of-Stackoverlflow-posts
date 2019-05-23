import csv
from processPost import feature
import time
import code_optimize

start = time.time()

inf = 1000000


class post:
    item = dict((i, None) for i in code_optimize.post_columns)

    def __init__(self, item):
        self.item = item
        obj = feature(item)
        self.exFeatures = obj.getFeatures()

    def getFeatures(self):
        return self.exFeatures


def set_lebel(mx, mn, featureValue):
    lebel = 1
    x = (mx - mn) / 5
    mn+=x
    while mn < int(featureValue):
        lebel += 1
        mn += x
    return lebel


if __name__ == '__main__':
    mx = dict((i, -inf) for i in code_optimize.feature_keys)
    mn = dict((i, inf) for i in code_optimize.feature_keys)
    processed_feature_list = []
    with open(code_optimize.processed_data_path, mode='w', encoding=code_optimize.ENCODING) as write_file:
        writer = csv.DictWriter(write_file, fieldnames=code_optimize.feature_keys)
        writer.writeheader()
        line_count = 0
        with open(code_optimize.csv_reading_path, mode='r', encoding=code_optimize.ENCODING) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                postObj = post(row)
                exFeatures = postObj.getFeatures()
                writer.writerow(exFeatures)
                processed_feature_list.append(exFeatures.copy())
                line_count += 1
                print(line_count)
                for k in exFeatures.keys():
                    mn[k] = min(mn[k], int(exFeatures[k]))
                    mx[k] = max(mx[k], int(exFeatures[k]))

    with open(code_optimize.labeled_data_path, mode='w', encoding=code_optimize.ENCODING) as write_file:
        writer = csv.DictWriter(write_file, fieldnames=code_optimize.feature_keys)
        writer.writeheader()
        feature_label = dict()
        for row in processed_feature_list:
            print(row)
            for k in code_optimize.feature_keys:
                feature_label[k] = set_lebel(mx[k], mn[k], row[k])
            writer.writerow(feature_label)

end = time.time()
print(end - start)
