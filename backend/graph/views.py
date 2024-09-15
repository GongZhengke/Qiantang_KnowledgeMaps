import json

from django.shortcuts import render
from py2neo import Graph
from django.http import HttpResponse, JsonResponse

# Create your views here.
class AnswerSearcher:
    def __init__(self):
        self.g = Graph('http://localhost:7474/', auth=("neo4j", "pwd"))
        self.num_limit = 20

    def getRelationByName(self, name):
        res = self.g.run("MATCH(n1 {name:\"" + str(name) + "\"})- [rel] - (n2) RETURN n1,rel,n2").data()
        return res

def search(request):
    if request.method == 'POST':
        a1 = str(request.POST['a1'])
        # ans是关系数据库查询
        # ans = []
        # ansname = []
        # if a1 != '':
        #     data = BasicData.objects.all()
        #     for i in data:
        #         if a1 in i.name and not i.name in ansname:
        #             ansname += [i.name]
        #             ans += [i]
    
        # neoans是图数据库查询
        res = AnswerSearcher()
        neoans = res.getRelationByName(a1)
    
        return JsonResponse(neoans, safe=False)
    else:

        neoans = {
            'errcode':403
        }
    
        return JsonResponse(neoans, safe=False)