import code_optimize as CO
import csv
import time
from operator import itemgetter

def read_file():
    extractedFeatureList = []
    with open(CO.processed_data_path,'r',encoding=CO.ENCODING) as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:
            for k in row.keys():
                row[k]=float(row[k])
            extractedFeatureList.append(row)
    return extractedFeatureList


def print_list(l):
    for i in l:
        print(i)
    print()
    print()
if __name__=='__main__':
    start=time.time()
    exFeatureList=read_file()
    sample_count=len(exFeatureList)
    samplePerLabel=sample_count//5
    print(sample_count)
    for k in CO.feature_keys:
        exFeatureList=sorted(exFeatureList,key=lambda i:i[k])
        label=0
        for i in range(sample_count):
            if i%samplePerLabel==0:
                label+=1
            exFeatureList[i][k]=label
    with open(CO.labeled_data_path,mode='w',encoding=CO.ENCODING) as write_file:
        writer=csv.DictWriter(write_file,fieldnames=CO.feature_keys)
        writer.writeheader()
        for row in exFeatureList:
            writer.writerow(row)
    end=time.time()
    print(end-start)