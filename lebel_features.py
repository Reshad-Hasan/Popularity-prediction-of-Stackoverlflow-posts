import code_optimize as co
import csv
import time


def print_list(l):
    for j in l:
        print(j)
    print()
    print()


if __name__ == '__main__':
    start = time.time()
    exFeatureList = co.readcsv_file(co.processed_data_path)
    sample_count = len(exFeatureList)
    samplePerLabel = sample_count // 5
    print(sample_count)
    for k in co.feature_keys:
        exFeatureList = sorted(exFeatureList, key=lambda d: d[k])
        label = -1
        for i in range(sample_count):
            if i % samplePerLabel == 0:
                label += 1
            exFeatureList[i][k] = label
    with open(co.labeled_data_path, mode='w', encoding=co.ENCODING) as write_file:
        writer = csv.DictWriter(write_file, fieldnames=co.feature_keys)
        writer.writeheader()
        for row in exFeatureList:
            writer.writerow(row)
    end = time.time()
    print(end - start)
