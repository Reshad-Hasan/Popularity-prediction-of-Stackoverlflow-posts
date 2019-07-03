from naive_bayes import  naive_bayes

q={
    'title':'akljfkalsjfaskfjakfj',
    'body' : 'klsjfklasjflkasj',
    'tagCount': '5',
    'reputation': '20',
    'popularity': '100'
}

obj=naive_bayes()
x=obj.get_result(q)
print(obj)
