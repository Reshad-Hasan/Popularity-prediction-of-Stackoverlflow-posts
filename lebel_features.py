import code_optimize as co
import csv
import time
import random


def print_list(l):
    for j in l:
        print(j)
    print()
    print()


class label_data:
    exFeatureList=[]

    def label(self):
        sample_count = len(self.exFeatureList)
        samplePerLabel = sample_count // 5
        print(sample_count)
        print_list(self.exFeatureList)
        for k in reversed(co.feature_keys):
            if k=='popularity':
                pass
            self.exFeatureList = sorted(self.exFeatureList, key=lambda d: d[k])
            label = -1
            for i in range(sample_count):
                if k=='popularity' and co.popularity_numberof_labels==2:
                    self.exFeatureList[i][k]= 0 if self.exFeatureList[i][k]<=0 else 1
                    continue
                if i % samplePerLabel == 0:
                    label += 1
                    # label's value can go up to 5 because we ignored the
                    # decimal part samplePerLabel = sample_count // 5 in here
                    if label>4:
                        label=4
                self.exFeatureList[i][k] = label
        # since we sorted the feture list for every feature we need to shuffle the list
        # for a successful train and test split
        random.shuffle(self.exFeatureList)

    def read(self):
        ex_feature_list = []
        with open(co.processed_data_path, 'r', encoding=co.ENCODING) as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            for row in csv_reader:
                for k in row.keys():
                    row[k] = float(row[k])
                ex_feature_list.append(row)
        self.exFeatureList = ex_feature_list

    def write(self,featureList,fileName):
        with open(fileName, mode='w', encoding=co.ENCODING) as write_file:
            writer = csv.DictWriter(write_file, fieldnames=co.feature_keys)
            writer.writeheader()
            for row in featureList:
                writer.writerow(row)



if __name__ == '__main__':
    start = time.time()
    obj=label_data()
    obj.read()
    # print_list(obj.exFeatureList)
    obj.label()
    test,train=[],[]
    n=len(obj.exFeatureList)
    i=0
    while i< n*0.75:
        train.append(obj.exFeatureList[i])
        i+=1
    while i<n:
        test.append(obj.exFeatureList[i])
        i+=1
    print(len(train))
    obj.write(test,'test.csv')
    obj.write(train,'train.csv')
    end = time.time()
    print(end - start)
