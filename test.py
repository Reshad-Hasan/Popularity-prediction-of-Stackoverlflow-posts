import code_optimize as co
import csv
from frequency_table_create import frequency_table_class as ft


class naive_bayes(ft):
    probality_of_outputs = list(0 for i in range(co.popularity_numberof_labels))
    dataset_length=0

    def init(self):
        for i in range(co.popularity_numberof_labels):
            self.dataset_length += self.fre_table['popularity'][i][i]
        print('training set length -', self.dataset_length)

        for i in range(co.popularity_numberof_labels):
            self.probality_of_outputs[i] = float(self.fre_table['popularity'][i][i] / self.dataset_length)
        print(self.probality_of_outputs)

    def get_result(self,input):
        result=list(1 for i in range(co.popularity_numberof_labels))
        for i in range(co.popularity_numberof_labels):
            for k in co.feature_keys:
                if k=='popularity' or k not in input.keys():
                    continue
                x=self.fre_table[k][input[k]][i]
                if x==0:
                    x=1
                y=self.fre_table['popularity'][i][i]
                result[i]*=x/y
            result[i]*=self.probality_of_outputs[i]
        sum=0
        for i in result:
            sum+=i
        for i in range(co.popularity_numberof_labels):
            result[i]=result[i]/sum
        sum=0
        ans, mx = -1, -1
        for i in range(co.popularity_numberof_labels):
            sum+=result[i]
            if mx<result[i]:
                mx=result[i]
                ans=i
        return ans

obj=naive_bayes()
obj.read()
obj.printfre()
obj.init()
with open('test.csv', 'r', encoding=co.ENCODING) as file:
    reader = csv.DictReader(file, delimiter=',')
    input_of_NB={}
    count=0
    total=0
    for row in reader:
        total+=1
        expected_ans=int(row['popularity'])
        for k in row.keys():
            if k=='popularity':
                continue
            input_of_NB[k]=int(row[k])
        ans=obj.get_result(input_of_NB)
        if expected_ans in [ans-1,ans,ans+1]:
            count+=1
    print(count)
    print(total)
    print('accuracy -',(count/total)*100)
