# Author: Sam Shenoi
# Description: This file interacts with the elastic search client in order to retrieve information
# Modification Log
#   - 4/16/2021  - updated documentation and comments for clarity


######################### Imports ###########################
import json

# This program uses the elasticsearch pip package in order to connect to Elastic Search
from elasticsearch import Elasticsearch

# Look into the ESearch folder for these files. They contain the queries used
#  to query the ES
from ESearch import abstractRuns
from ESearch import clinicalRuns


import time

######################### Class Declarations #################
class Elastic:

    # __init__
    # This function inits the Elastic class
    #
    # preconditions
    #   - abQuery - the abstracts query to use. Multiple query types were tested.
    #         This argument defaults to 9 since the 9th query was found to have
    #         the best results. All queries can be see in the
    #         ESearch/abstractRuns.py file.
    #   - tQuery - the clinical trials query number to be used.
    #         Multiple query types were tested.
    #         This argument defaults to 7 since the 7th query was found to have
    #         the best results. All queries can be see in the
    #         ESearch/clinicalRuns.py file.
    # postconditions - the Elastic object is created
    # return - none
    def __init__(self,abQuery=9,tQuery=7):
       # Init the elastic search connection
       self.es = Elasticsearch(timeout=90)
       
       # Create the abstract query generator
       self.q = abstractRuns.GenerateAbstractQuery()
       
       # Create the clinical trials query generator
       self.t = clinicalRuns.Trials()
       
       # Set the arg (which run to use) for this class
       self.arg = abQuery
       self.arg2 = tQuery
       
    # get
    # this function gets a document from es
    #
    # preconditions
    #   - index - the ES index to use
    #   - id - the id of the document to find
    # postconditions - the requested document is found
    # return - the requested document
    def get(self,index,  id):
        return self.es.get(index=index,  id=id, _source=True)
        
    # insert
    # this function inserts a document into es
    #
    # preconditions
    #   - type - the type of the document
    #   - id - the id of the document to insert
    #   - ndx - the index to use
    #   - obj - the body of the text
    # postconditions - the document is inserted
    # return - none
    def insert(self,type, obj,ndx,id):
        res = self.es.index(index=ndx, doc_type=type, id=id, body=obj)
    
    # exists
    # checks to see if the document exists
    #
    # preconditions
    #   - type - the type of the document
    #   - id - the id of the document to insert
    #   - ndx - the index to use
    # postconditions - whether or not the document exists is found
    # return - whether or not the document exists is returned
    def exists(self, ndx, id, type):
        return self.es.exists(index=ndx,id=id,doc_type=type)
        
    # search
    # search elasticsearch
    #
    # preconditions
    #   - obj - the query object
    #   - size - the number of hits to return
    #   - ndx - the index to use
    # postconditions - elastic search is searched
    # return - the top size number of documents are returned that match the query
    def search(self,ndx,obj,size):
        res = self.es.search(index=ndx, body = obj,size = size, filter_path=['hits.hits'])
        return res
    
    # trialsSearch
    # search elasticsearch for clinical trials
    #
    # preconditions [refer to "Developing a Search Engine" paper for more info]
    #   - disease - the cancer conditions
    #   - gene - the gene(s) of interest in a comma seperated string
    #   - dem - the demographic information (age, gender)
    #   - other - any other information ( not used in this query)
    #   - size - the number of documents to return
    # postconditions - elastic search is searched for clinical trials
    # return - the top size number of documents are returned that match the query
    def trialsSearch(self,disease, gene, dem,other,size=1000):
        dem = dem.split(" ")
        age = int(dem[0].split("-")[0])
        gender = dem[1] 
        genes = gene.split(",")
        obj = self.t.query(self.arg2,disease, genes, age, gender)
        return self.search("trials",obj,size)['hits']['hits']
    
    # abstractSearch
    # search elasticsearch for abstracts
    #
    # preconditions [refer to "Developing a Search Engine" paper for more info]
    #   - disease - the cancer conditions
    #   - gene - the gene(s) of interest in a comma seperated string
    #   - dem - the demographic information (age, gender)
    #   - other - any other information ( not used in this query)
    #   - size - the number of documents to return
    # postconditions - elastic search is searched for abstracts
    # return - the top size number of documents are returned that match the query
    def abstractSearch(self,disease, gene, dem, other,size=1000):
        dem = dem.split(" ")
        age = int(dem[0].split("-")[0])
        gender = dem[1] 
        genes = gene.split(",")
        obj = self.q.query(self.arg,disease, genes, age, gender)
        return self.search("abstracts",obj,size)['hits']['hits']
    
    # Ignore this function
    def abAlt(self,disease, gene, dem, other):
        return {}




