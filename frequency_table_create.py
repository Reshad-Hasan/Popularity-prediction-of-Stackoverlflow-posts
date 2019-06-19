import code_optimize as co


class frequency_table_class:
    fre_table = dict((i, [[0] * 5 for j in range(5)]) for i in co.feature_keys)

    def create(self):
        labeled_data_list = co.readcsv_file('train.csv')
        for row in labeled_data_list:
            for k in row.keys():
                if int(row[k]==5):
                    pass
                self.fre_table[k][int(row[k])][int(row['popularity'])] += 1

    def write(self):
        with open(co.frequency_table_path, mode='w', encoding=co.ENCODING) as write_file:
            for ll in self.fre_table.values():
                for l in ll:
                    for n in l:
                        write_file.write(str(n) + ' ')

    def read(self):
        with open(co.frequency_table_path, mode='r', encoding=co.ENCODING) as read_file:
            nums = list(int(i) for i in read_file.read().split())
            index = 0
            for k in co.feature_keys:
                for i in range(5):
                    for j in range(5):
                        self.fre_table[k][i][j] = nums[index]
                        index += 1

    def printfre(self):
        for k in self.fre_table.keys():
            print(k)
            for row in self.fre_table[k]:
                print(row)


if __name__ == '__main__':
    fretab = frequency_table_class()
    fretab.create()
    fretab.write()
    fretab.read()
    print()
    fretab.printfre()
