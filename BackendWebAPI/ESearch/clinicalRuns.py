'''
TRIALS FUNCTIONS
'''
import sys

import requests
import requests_cache
import json
from Meta import *
requests_cache.install_cache('demo_cache')
import re 
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
#UMLS stuff
apikey = "f1554dfe-e80a-403b-a579-4c9909c1de19"
version = "current"

uri = "https://uts-ws.nlm.nih.gov"
content_endpoint = "/rest/search/"+version
##get at ticket granting ticket for the session
AuthClient = Authentication(apikey)
tgt = AuthClient.gettgt()


class Trials:
    def __init__(self):
       self.obj = {}
       self.fields = ["brief_title","brief_summary","mesh_term","keyword","condition","eligibility"]
       self.disease = ""
       self.genes = []
       self.age = ""
       self.gender = ""
       self.headers =  {'Accept': 'application/json'}
    def query(self,arg,disease, genes, age, gender):

        self.disease = disease
        self.genes = genes
        self.age = age
        self.gender = gender
        self.reuse = self.reuseobjs(gender,age)
        switcher = {
            0: self.ct0,  
            1: self.ct1,
            2: self.ct2,
            3: self.ct3,
            4: self.ct4,
            5: self.ct5
        }
       
        
        '''
        3: self.ct3,
        4: self.ct4,
        5: self.ct5,
        6: self.ct6,
        7: self.ct7,
        8: self.ct8,
        9: self.ctHalf
        '''
   

      
   
        obj = switcher.get(int(arg),self.ct0)()
        return obj

    def genMultiMatchObj(self,query,fields,type,boost):
        obj = {
            "multi_match":{
                            "query":query,
                            "fields":fields,
                            "tie_breaker":.4,
                            "type":type,
                            "boost":boost
            }
        }
        return obj
    def pullGeneData(self, u):
        return requests.get(url = u, headers=self.headers).json()["response"]["docs"]

    def genBoolQuery(self, must, should, mn = []):
        obj = {
            "bool":{
                "must":must,
                "should":should,
                "must_not":mn
            }
        }
        return obj
    def reuseobjs(self,gender,age):
        return [{"range":
                 {"minimum_age":{"lte": age,"boost":2 }}},
                 {"range":{"maximum_age":{"gte":  age,"boost":2 }}},
                 {"bool":{"should":[{"match":{"gender":gender}},{"match":{ "gender":"ALL"}}]}}]
    
    #P_5  all 0.4207 , P_10 all 0.3655 ,P_15 all 0.3126
    def ct0(self):
        gList = []
        for g in self.genes: 
            gList.append(self.genMultiMatchObj(g,self.fields,"cross_fields",1))
  
        obj = {
            "query":{
                "bool":{
                    "must":[
                        self.genMultiMatchObj(self.disease,self.fields,"best_fields",1.5), {
                        "bool":{
                            "should":gList
                        }
                    }, {"match_all":{"boost":.001}}
                        
                    ] + self.reuse
                }
            }
        }
        f = open("TRIALSJSON.json","w")
        f.write(json.dumps(obj,indent=4))
        f.close()
        return obj
    #P_5 all 0.4414, P_10  all	0.4103, P_15 all 0.3609
    def ct1(self):
        genes = self.genes
        uri = 'http://rest.genenames.org/search/'
        uri2 = 'http://rest.genenames.org/fetch/symbol/'
        geneList = []
        geneList2 =[]

        #Loop through genes and expand them
        for g in genes: 
            #Pull Gene symbol information 
            u = uri + g
            docs = self.pullGeneData(u)
            #Pull Alias and stuff
            u = uri2 + docs[0]["symbol"]
            docs2 = self.pullGeneData(u)
            for d2 in docs2:
                geneList.append(self.genMultiMatchObj(d2["name"],self.fields,"phrase",.2))
                try:
                    docs3 = d2["alias_symbol"]
                    for d3 in docs3:
                        geneList2.append(self.genMultiMatchObj(d3,self.fields,"cross_fields",.2))
                        geneList2.append(self.genMultiMatchObj(d3,self.fields,"phrase_prefix",.02))
                except:
                    eprint("Error here...")
            #Create a query for each gene
            o2= self.genMultiMatchObj(g,self.fields,"cross_fields",1)
            o3= self.genMultiMatchObj(re.findall("[A-Z]+", docs[0]["symbol"])[0],self.fields,"phrase_prefix",.2)
        
            geneList.append(o2)  
            geneList.append(o3) 
  
        obj = {
            "query":{
                "bool":{
                    "must":[
                        self.genMultiMatchObj(self.disease,self.fields,"best_fields",1.5), {
                        "bool":{
                            "should":geneList + geneList2
                        }
                    }
                        
                    ]+ self.reuse,
                     "should": self.meshSearch()
                }
            }
        }
        return obj
    
    #P_5 all	0.4552, P_10 all 0.3828, P_15 all 0.3448
    def ct2(self):
        di = self.expandDisease()
        p = []
        for d in di:
            if "carcinoma" in d.lower() or "neoplasm" in d.lower() or "cancer" in d.lower() :
                p.append(self.genMultiMatchObj(d,self.fields,"cross_fields",.5))
        gList = []
        for g in self.genes: 
            gList.append(self.genMultiMatchObj(g,self.fields,"cross_fields",1))
  
        obj = {
            "query":{
                "bool":{
                    "must":[
                       {
                           "bool":{
                               "should":[ self.genMultiMatchObj(self.disease,self.fields,"best_fields",1.5),self.genMultiMatchObj(self.disease,self.fields,"phrase",.3), {"match_all":{"boost":.001}}]+ p
                           }
                       },
                       {
                        "bool":{
                            "should":gList
                       }
                    },
                        
                    ]  + self.reuse,
                     "should": self.meshSearch()
                }
            }
        }
        return obj
        #P_5 all 0.4414, P_10 all	0.3759, P_15 all	0.3287
    def ctDMinusMA(self):
        di = self.expandDisease()
        p = []
        for d in di:
            if "carcinoma" in d.lower() or "neoplasm" in d.lower() or "cancer" in d.lower() :
                p.append(self.genMultiMatchObj(d,self.fields,"cross_fields",.5))
        gList = []
        for g in self.genes: 
            gList.append(self.genMultiMatchObj(g,self.fields,"cross_fields",1))
  
        obj = {
            "query":{
                "bool":{
                    "must":[
                       {
                           "bool":{
                               "should":[ self.genMultiMatchObj(self.disease,self.fields,"best_fields",1.5),self.genMultiMatchObj(self.disease,self.fields,"phrase",.3)]+ p
                           }
                       },
                       {
                        "bool":{
                            "should":gList
                       }
                    },
                        
                    ]  + self.reuse,
                     "should": self.meshSearch()  
                }
            }
        }
        return obj
    #P_5  all 0.4414, P_10 all 0.4034, P_15  all 0.3586
    def ct3(self):
        genes = self.genes
        uri = 'http://rest.genenames.org/search/'
        uri2 = 'http://rest.genenames.org/fetch/symbol/'
        geneList = []
        geneList2 =[]

        #Loop through genes and expand them
        for g in genes: 
            #Pull Gene symbol information 
            u = uri + g
            docs = self.pullGeneData(u)
            #Pull Alias and stuff
            u = uri2 + docs[0]["symbol"]
            docs2 = self.pullGeneData(u)
            for d2 in docs2:
                geneList.append(self.genMultiMatchObj(d2["name"],self.fields,"phrase",.2))
                try:
                    docs3 = d2["alias_symbol"]
                    for d3 in docs3:
                        geneList2.append(self.genMultiMatchObj(d3,self.fields,"cross_fields",.2))
                        geneList2.append(self.genMultiMatchObj(d3,self.fields,"phrase_prefix",.02))
                except:
                    eprint("Error here...")
            #Create a query for each gene
            o2= self.genMultiMatchObj(g,self.fields,"cross_fields",1)
            o3= self.genMultiMatchObj(re.findall("[A-Z]+", docs[0]["symbol"])[0],self.fields,"phrase_prefix",.2)
        
            geneList.append(o2)  
            geneList.append(o3) 
  
        di = self.expandDisease()
        p = []
        for d in di:
            if "carcinoma" in d.lower() or "neoplasm" in d.lower() or "cancer" in d.lower() :
                p.append(self.genMultiMatchObj(d,self.fields,"cross_fields",.5))
       
        obj = {
            "query":{
                "bool":{
                    "must":[
                       {
                           "bool":{
                               "should":[ self.genMultiMatchObj(self.disease,self.fields,"best_fields",1.5),self.genMultiMatchObj(self.disease,self.fields,"phrase",.3), {"match_all":{"boost":.001}}]+ p
                           }
                       },
                       {
                        "bool":{
                            "should":geneList + geneList2
                       }
                    },
                        
                    ]  + self.reuse,
                     "should": self.meshSearch() 
                }
            }
        }
        return obj
    #P_5  all	0.2345, P_10 all	0.2103, P_15  all	0.1816
    #Introduces match all in genes as well 
    def ct4(self):
        genes = self.genes
        uri = 'http://rest.genenames.org/search/'
        uri2 = 'http://rest.genenames.org/fetch/symbol/'
        geneList = []
        geneList2 =[]

        #Loop through genes and expand them
        for g in genes: 
            #Pull Gene symbol information 
            u = uri + g
            docs = self.pullGeneData(u)
            #Pull Alias and stuff
            u = uri2 + docs[0]["symbol"]
            docs2 = self.pullGeneData(u)
            for d2 in docs2:
                geneList.append(self.genMultiMatchObj(d2["name"],self.fields,"phrase",.2))
                try:
                    docs3 = d2["alias_symbol"]
                    for d3 in docs3:
                        geneList2.append(self.genMultiMatchObj(d3,self.fields,"cross_fields",.2))
                        geneList2.append(self.genMultiMatchObj(d3,self.fields,"phrase_prefix",.02))
                except:
                    eprint("Error here...")
            #Create a query for each gene
            o2= self.genMultiMatchObj(g,self.fields,"cross_fields",1)
            o3= self.genMultiMatchObj(re.findall("[A-Z]+", docs[0]["symbol"])[0],self.fields,"phrase_prefix",.2)
        
            geneList.append(o2)  
            geneList.append(o3) 
  
        di = self.expandDisease()
        p = []
        for d in di:
            if "carcinoma" in d.lower() or "neoplasm" in d.lower() or "cancer" in d.lower() :
                p.append(self.genMultiMatchObj(d,self.fields,"cross_fields",.5))
       
        obj = {
            "query":{
                "bool":{
                    "must":[
                       {
                           "bool":{
                               "should":[ self.genMultiMatchObj(self.disease,self.fields,"best_fields",1.5),self.genMultiMatchObj(self.disease,self.fields,"phrase",.3), {"match_all":{"boost":.001}}]+ p
                           }
                       },
                       {
                        "bool":{
                            "should":geneList + geneList2 + [{"match_all":{"boost":.001}}]
                       }
                    },
                        
                    ]  + self.reuse,
                     "should": self.meshSearch()
                }
            }
        }
        return obj
    #P_5  all	0.4414,P_10  all	0.4000, P_15 all	0.3494
    def ct5(self):
        genes = self.genes
        uri = 'http://rest.genenames.org/search/'
        uri2 = 'http://rest.genenames.org/fetch/symbol/'
        geneList = []
        geneList2 =[]

        #Loop through genes and expand them
        for g in genes: 
            #Pull Gene symbol information 
            u = uri + g
            docs = self.pullGeneData(u)
            #Pull Alias and stuff
            u = uri2 + docs[0]["symbol"]
            docs2 = self.pullGeneData(u)
            for d2 in docs2:
                geneList.append(self.genMultiMatchObj(d2["name"],self.fields,"phrase",.2))
                try:
                    docs3 = d2["alias_symbol"]
                    for d3 in docs3:
                        geneList2.append(self.genMultiMatchObj(d3,self.fields,"cross_fields",.2))
                        geneList2.append(self.genMultiMatchObj(d3,self.fields,"phrase_prefix",.02))
                except:
                    eprint("Error here...")
            #Create a query for each gene
            o2= self.genMultiMatchObj(g,self.fields,"cross_fields",1)
            o3= self.genMultiMatchObj(re.findall("[A-Z]+", docs[0]["symbol"])[0],self.fields,"phrase_prefix",.2)
        
            geneList.append(o2)  
            geneList.append(o3) 
  
        di = self.expandDisease()
        p = []
        for d in di:
            if "carcinoma" in d.lower() or "neoplasm" in d.lower() or "cancer" in d.lower() :
                p.append(self.genMultiMatchObj(d,self.fields,"cross_fields",.5))
       
        obj = {
            "query":{
                "bool":{
                    "must":[
                       {
                           "bool":{
                               "should":[ self.genMultiMatchObj(self.disease,self.fields,"best_fields",1.5),self.genMultiMatchObj(self.disease,self.fields,"phrase",.3)]+ p
                           }
                       },
                       {
                        "bool":{
                            "should":geneList + geneList2 
                       }
                    },
                        
                    ]  + self.reuse,
                    "should": self.meshSearch()
                }
            }
        }
        return obj
    def expandDisease(self):
        pageNumber=0
        string = self.disease
        ##generate a new service ticket for each page if needed
        ticket = AuthClient.getst(tgt)
        query = {'string':string,'ticket':ticket, 'pageNumber':pageNumber}
        r = requests.get(uri+content_endpoint,params=query).json()
        jsonData = r["result"]["results"]
        new_list = [i["name"] for i in jsonData if len(i["name"].split(" "))<3 and self.disease.lower() not in i["name"].lower()]
        return new_list
    def meshSearch(self):
    
        #Search for age terms first. Using methodology provided in Age Specific Paper 
        ageTerms = []
        '''
        #Child
        if self.age < 19: 
            ageTerms.append(self.genMultiMatchObj("child",self.fields,"best_fields",1))
            ageTerms.append(self.genMultiMatchObj("adolescent",self.fields,"best_fields",1))
            ageTerms.append(self.genMultiMatchObj("infan",self.fields,"best_fields",1))
        #Adult   
        elif self.age < 65:
            #Adult multiple positions
            ageTerms.append({"term":{"mesh_terms":{"value":"middle aged","boost":1}}})
            ageTerms.append({"term":{"mesh_terms":{"value":"adult","boost":1}}})
        #Geriatric
        else:
            #Explode on adult
            ageTerms.append({"term":{"mesh_terms":{"value":"aged","boost":1}}})
            ageTerms.append({"term":{"mesh_terms":{"value":"aged, 80 and over","boost":1}}})
            ageTerms.append({"term":{"mesh_terms":{"value":"adult","boost":1}}})
            ageTerms.append({"term":{"mesh_terms":{"value":"middle aged","boost":1}}})
      
        boolQ = self.genBoolQuery([],ageTerms)

        o = []
        #Analyzing all Mesh-terms shows that Prognosis appears relatively frequently and doesn't overlap with not PM documents, therefore am adding it in 
        o.append({"term":{"mesh_terms":"Prognosis"}})
        #Mutation also appears to do pretty well, so adding that in too 
        o.append({"term":{"mesh_terms":"Mutation [D009154:minor]"}})
        o.append({"term":{"mesh_terms":"Mutation [D009154:major]"}})
        o.append({"term":{"mesh_terms":"Treatment Outcome [D016896:minor]"}})
        o.append(boolQ)
        '''
        if self.age <= 2:
            ageTerms.append(self.genMultiMatchObj("newborn",["mesh_terms"],"best_fields",1))
        elif self.age <=12:
            ageTerms.append(self.genMultiMatchObj("child",["mesh_terms"],"best_fields",1))
        elif self.age <=18:
            ageTerms.append(self.genMultiMatchObj("adolescent",["mesh_terms"],"best_fields",1))
        elif self.age <=44:
            ageTerms.append(self.genMultiMatchObj("adult",["mesh_terms"],"best_fields",1))
        else:
            ageTerms.append(self.genMultiMatchObj("aged",["mesh_terms"],"best_fields",1))
       
       
        
        return ageTerms

           
    def explodeSearch(self):
    
        #Search for age terms first. Using methodology provided in Age Specific Paper 
        ageTerms = []
       
        #Child
        if self.age < 19: 
            ageTerms.append(self.genMultiMatchObj("child",self.fields,"best_fields",1))
            ageTerms.append(self.genMultiMatchObj("adolescent",self.fields,"best_fields",1))
            ageTerms.append(self.genMultiMatchObj("infan",self.fields,"best_fields",1))
        #Adult   
        elif self.age < 65:
            #Adult multiple positions
            ageTerms.append({"term":{"mesh_terms":{"value":"middle aged","boost":1}}})
            ageTerms.append({"term":{"mesh_terms":{"value":"adult","boost":1}}})
        #Geriatric
        else:
            #Explode on adult
            ageTerms.append({"term":{"mesh_terms":{"value":"aged","boost":1}}})
            ageTerms.append({"term":{"mesh_terms":{"value":"aged, 80 and over","boost":1}}})
            ageTerms.append({"term":{"mesh_terms":{"value":"adult","boost":1}}})
            ageTerms.append({"term":{"mesh_terms":{"value":"middle aged","boost":1}}})
        return ageTerms