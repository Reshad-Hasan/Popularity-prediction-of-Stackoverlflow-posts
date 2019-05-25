import code_optimize
import random

l=[]
for i in range(10):
    d=dict((i,random.randint(0,10)) for i in code_optimize.feature_keys)
    l.append(d)
    # print(d)
l=sorted(l,key=lambda i:i['bodyToTitle'])
for i in l:
    print(i)