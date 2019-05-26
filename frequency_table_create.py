import code_optimize as CO
import time
if __name__=='__main__':
    start=time.time()
    freuqency_table=dict((i,[[0]*6 for j in range(6)]) for i in CO.feature_keys)
    labeled_data_list=CO.readcsv_file(CO.labeled_data_path)
    for row in labeled_data_list:
        for k in row.keys():
            # print(k)
            # print(row[k])
            # print(row['popularity'])
            freuqency_table[k][int(row[k])][int(row['popularity'])]+=1
            # print(freuqency_table[k][int(row[k])][int(row['popularity'])])
            # freuqency_table[k][row[k]][row['popularity']]+=1
    for i in freuqency_table.items():
        print(i)
    end=time.time()
    print(end-start)