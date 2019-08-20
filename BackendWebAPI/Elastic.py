import json
from elasticsearch import Elasticsearch
from ESearch import abstractRuns
from ESearch import clinicalRuns
import time


class Elastic:
    def __init__(self,abQuery=9,tQuery=7):
       self.es = Elasticsearch(timeout=90)
       self.q = abstractRuns.GenerateAbstractQuery() 
       self.t = clinicalRuns.Trials()
       self.arg = abQuery
       self.arg2 = tQuery
    def get(self,index,  id):
        return self.es.get(index=index,  id=id, _source=True)
    def insert(self,type, obj,ndx,id):
        res = self.es.index(index=ndx, doc_type=type, id=id, body=obj)
    def exists(self, ndx, id, type):
        return self.es.exists(index=ndx,id=id,doc_type=type)
    def search(self,ndx,obj,size):
        res = self.es.search(index=ndx, body = obj,size = size, filter_path=['hits.hits'])
        return res
    def trialsSearch(self,disease, gene, dem,other,size=1000):
        dem = dem.split(" ")
        age = int(dem[0].split("-")[0])
        gender = dem[1] 
        genes = gene.split(",")
        obj = self.t.query(self.arg2,disease, genes, age, gender)
        return self.search("trials",obj,size)['hits']['hits']
    def abstractSearch(self,disease, gene, dem, other,size=1000):
        dem = dem.split(" ")
        age = int(dem[0].split("-")[0])
        gender = dem[1] 
        genes = gene.split(",")
        obj = self.q.query(self.arg,disease, genes, age, gender)
        return self.search("abstracts",obj,size)['hits']['hits']
    def abAlt(self,disease, gene, dem, other):
       
        return {}




