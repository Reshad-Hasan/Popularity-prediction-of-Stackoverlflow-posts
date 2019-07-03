import control as co
from frequency_table_create import frequency_table_class as ft


class naive_bayes(ft):
    probability_of_outputs = list(0 for i in range(co.popularity_numberof_labels))
    dataset_length = 0

    def init(self):
        for i in range(co.popularity_numberof_labels):
            self.dataset_length += self.fre_table['popularity'][i][i]

        # calculate each item's independent probability
        for i in range(co.popularity_numberof_labels):
            self.probability_of_outputs[i] = float(self.fre_table['popularity'][i][i] / self.dataset_length)
        print(self.probability_of_outputs)

    def get_result(self, input):
        result = list(1 for i in range(co.popularity_numberof_labels))
        for i in range(co.popularity_numberof_labels):
            for k in co.feature_keys:
                if k == 'popularity' or k not in input.keys():
                    continue
                x = self.fre_table[k][input[k]][i]
                # if somethings value is zero we can increment all related value
                # and it will not affect the result
                if x == 0:
                    x = 1
                y = self.fre_table['popularity'][i][i]
                result[i] *= x / y
            result[i] *= self.probability_of_outputs[i]
        sum = 0
        for i in result:
            sum += i
        for i in range(co.popularity_numberof_labels):
            result[i] = result[i] / sum
        sum = 0
        ans, mx = -1, -1
        for i in range(co.popularity_numberof_labels):
            sum += result[i]
            if mx < result[i]:
                mx = result[i]
                ans = i
        return ans
