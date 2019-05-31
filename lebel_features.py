import code_optimize as co
import csv
import time


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
        for k in co.feature_keys:
            self.exFeatureList = sorted(self.exFeatureList, key=lambda d: d[k])
            label = -1
            for i in range(sample_count):
                if i % samplePerLabel == 0:
                    label += 1
                self.exFeatureList[i][k] = label

    def read(self):
        ex_feature_list = []
        with open(co.processed_data_path, 'r', encoding=co.ENCODING) as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            for row in csv_reader:
                for k in row.keys():
                    row[k] = float(row[k])
                ex_feature_list.append(row)
        self.exFeatureList = ex_feature_list

    def write(self):
        with open(co.labeled_data_path, mode='w', encoding=co.ENCODING) as write_file:
            writer = csv.DictWriter(write_file, fieldnames=co.feature_keys)
            writer.writeheader()
            for row in self.exFeatureList:
                writer.writerow(row)


if __name__ == '__main__':
    start = time.time()
    obj=label_data()
    obj.read()
    obj.label()
    obj.write()
    end = time.time()
    print(end - start)
