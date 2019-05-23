import csv
import code_optimize

def set_lebel(mx,mn,featureValue):
    lebel=1
    x=(mx-mn)/5
    while mn<featureValue:
        lebel+=1
        mn+=x
    return lebel

