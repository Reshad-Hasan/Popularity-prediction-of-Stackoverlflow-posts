import control as co
import csv
import random


# for testing
def print_list(l):
    for j in l:
        print(j)
    print()
    print()


class label_data:
    # for holding processed features
    exFeatureList = []
    # storing group boundary value per group
    # boundaries are store as array for each feature
    bound = {}

    def label_data_set(self):
        # all data is divided in 5 groups more or less can be used
        # using mode groups may improve accuracy
        sample_count = len(self.exFeatureList)
        sample_per_label = sample_count // 5
        print(sample_count)
        print_list(self.exFeatureList)
        for k in co.feature_keys:
            self.bound[k] = []
            self.exFeatureList = sorted(self.exFeatureList, key=lambda d: d[k])
            label = -1
            # group id starts from 0 to co.data_group_num
            for i in range(sample_count):
                if k == 'popularity' and co.score_group_num == 2:
                    self.exFeatureList[i][k] = 0 if self.exFeatureList[i][k] <= 0 else 1
                    continue
                if i % sample_per_label == 0:
                    self.bound[k].append(self.exFeatureList[i][k])
                    label += 1
                    # label_data_set's value can go up to 5 because we ignored the
                    # decimal part sample_per_label = sample_count // 5 in here
                    if label == co.data_group_num:
                        label = co.data_group_num - 1
                self.exFeatureList[i][k] = label
        # since we sorted the feature list for every feature we need to shuffle the list
        # for a successful train and test split
        random.shuffle(self.exFeatureList)

    # reads processed data from file and stores them as list
    def read_data(self):
        ex_feature_list = []
        with open(co.processed_data_path, 'r', encoding=co.ENCODING) as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            for row in csv_reader:
                for k in row.keys():
                    row[k] = float(row[k])
                ex_feature_list.append(row)
        self.exFeatureList = ex_feature_list

    # for writing the labeled data to csv file
    def write_data(self, feature_list, file_name):
        with open(file_name, mode='w', encoding=co.ENCODING) as write_file:
            writer = csv.DictWriter(write_file, fieldnames=co.feature_keys)
            writer.writeheader()
            for row in feature_list:
                writer.writerow(row)

    def print_bound(self):
        for k in self.bound.keys():
            print(k, self.bound[k])

    def write_bound(self):
        with open('data boundary', mode='w', encoding=co.ENCODING) as write_file:
            for k in co.feature_keys:
                if k == 'popularity' and co.score_group_num == 2:
                    continue
                for x in self.bound[k]:
                    write_file.write(str(x) + ' ')
                write_file.write('\n')

    def read_bound(self):
        with open('data boundary', mode='r', encoding=co.ENCODING) as read_file:
            # reading data as 2d list
            data = list(read_file.read().split('\n'))
            i = 0
            for k in co.feature_keys:
                if k == 'popularity' and co.score_group_num == 2:
                    continue
                self.bound[k] = list(float(x) for x in data[i].split())
                i += 1

    def label_post(self, post):
        self.read_bound()
        for k in co.feature_keys:
            if k == 'popularity':
                continue
            for i in range(1, len(self.bound[k])):
                if float(post[k]) < self.bound[k][i]:
                    post[k] = i - 1 if i < co.data_group_num else co.data_group_num - 1
                    break
        return post


if __name__ == '__main__':
    obj = label_data()
    obj.read_data()  # reading processed data
    # print_list(obj.exFeatureList)
    obj.label_data_set()  # labeling processed data
    test, train = [], []
    n = len(obj.exFeatureList)
    i = 0
    # splitting data-set to train and test file
    # 75% in training set, 25% in testing set
    while i < n * 0.75:
        train.append(obj.exFeatureList[i])
        i += 1
    while i < n:
        test.append(obj.exFeatureList[i])
        i += 1
    print('sample count in train file - ', len(train))
    print('sample count in test file - ', len(test))
    obj.write_data(test, 'test.csv')
    obj.write_data(train, 'train.csv')
    obj.write_bound()
    obj.print_bound()
