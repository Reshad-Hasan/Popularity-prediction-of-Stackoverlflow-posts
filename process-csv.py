import csv
from processPost import feature
import time
import  code_optimize
start=time.time()

inf=1000000
class post:
    item=dict((i,None) for i in code_optimize.post_columns)

    def __init__(self,item):
        self.item=item
        obj=feature(item)
        self.exFeatures=obj.getFeatures()

    def getFeatures(self):
        return self.exFeatures


if __name__=='__main__':
    with open(code_optimize.processed_data_path,mode='w',encoding=code_optimize.ENCODING) as write_file:
        writer=csv.DictWriter(write_file,fieldnames=code_optimize.feature_keys)
        writer.writeheader()
        line_count=0

        mx = dict((i,-inf) for i in code_optimize.feature_keys)
        mn = dict((i, inf) for i in code_optimize.feature_keys)

        with open(code_optimize.csv_reading_path,mode='r',encoding=code_optimize.ENCODING) as csv_file:
            csv_reader=csv.DictReader(csv_file,delimiter=',')
            line_count=0
            for row in csv_reader:
                postObj=post(row)
                exFeatures=postObj.getFeatures()
                writer.writerow(exFeatures)
                line_count+=1
                print(line_count)
                for k in exFeatures.keys():
                    mn[k]=min(mn[k],int(exFeatures[k]))
                    mx[k]=max(mx[k],int(exFeatures[k]))
            with open('C:\\Users\\Reshad Hasan\\Desktop\\min-max.txt','w',encoding=code_optimize.ENCODING) as file:
                file.write('max values\n')
                file.write(str(mx))
                file.write('\nmin values\n')
                file.write(str(mn))
            print(mx)
            print(mn)

end=time.time()
print(end-start)