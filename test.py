import control as co
import csv
from naive_bayes import naive_bayes

# this is for testing the accuracy of the model
if __name__ == '__main__':
    obj = naive_bayes()
    obj.read_table()
    print('** frequency table **')
    obj.printfre()
    with open('test.csv', 'r', encoding=co.ENCODING) as file:
        reader = csv.DictReader(file, delimiter=',')
        input_of_NB = {}
        right_ans = 0
        total = 0
        for row in reader:
            total += 1
            expected_ans = int(row['popularity'])
            for k in row.keys():
                if k == 'popularity':
                    continue
                input_of_NB[k] = int(row[k])
            ans = obj.get_result(input_of_NB)
            if expected_ans in [ans]:
                right_ans += 1
        print('correct', right_ans)
        print('total', total)
        print('accuracy -', (right_ans / total) * 100)
