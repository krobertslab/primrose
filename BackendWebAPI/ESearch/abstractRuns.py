'''
ABSTRACTS FUNCTIONS
Description: This file contains all of the abstract query trials along with their infNDCG score
Observations: 
   - Phrase based matching is not effective in retaining information; having this clause lowers rankings
   - Phrase-prefix based matching is slightly effective in pulling information; having this clause increases rankings by ~.1
'''
import sys
import requests
import requests_cache
import json
import re
from Meta import *


requests_cache.install_cache('demo_cache')
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
#UMLS stuff
apikey = "API KEY FOR THE UMLS"
version = "current"

uri = "https://uts-ws.nlm.nih.gov"
content_endpoint = "/rest/search/"+version
##get at ticket granting ticket for the session
AuthClient = Authentication(apikey)
tgt = AuthClient.gettgt()


class GenerateAbstractQuery:
    def __init__(self):
       self.obj = {}
       self.fields = ["mesh_terms", "text"]
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
        self.reuse = self.reuseobjs(gender)
        switcher = {
            -1: self.abYNeg1,
            0: self.abY0,
            1: self.abY1,
            2: self.abY2,
            3: self.abY3,
            4: self.abY4,
            5: self.abY5,
            6: self.abY6,
            7: self.abYHalf
        }
        
        obj = switcher.get(int(arg), {})()

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
    def reuseobjs(self,gender):

        obj = [ self.genMultiMatchObj(self.gender,["mesh_terms"],"best_fields",1),{"term":{"mesh_terms":{"value":"Humans","boost":1}}},{"term":{"mesh_terms":{"value":"Animals","boost":1}}}] #+ self.explodeSearch()
        return obj
    
    #Minus the expanded mesh terms for age
    def abYNeg1(self):
        gList = []
        for g in self.genes: 
            gList.append(self.genMultiMatchObj(g,["text","mesh_terms"],"cross_fields",1))
        ageT = []
  
        obj = {
            "query":{
                "bool":{
                    "must":[
                        self.genMultiMatchObj(self.disease,["text","mesh_terms"],"best_fields",1.5),
                        
                    {
                        "bool":{
                            "should":gList
                        }
                    }],
                    "should":[
                        self.genMultiMatchObj(self.gender,["mesh_terms"],"best_fields",1)
                
                    ] 
                }
            }
        }
        return obj
    #infNDCG: 0.4130
    #Based off over imimug teams baseline query 
    def abY0(self):
        gList = []
        for g in self.genes: 
            gList.append(self.genMultiMatchObj(g,["text","mesh_terms"],"cross_fields",1))
        ageT = []
  
        obj = {
            "query":{
                "bool":{
                    "must":[
                        self.genMultiMatchObj(self.disease,["text","mesh_terms"],"best_fields",1.5),
                        
                    {
                        "bool":{
                            "should":gList
                        }
                    }],
                    "should":[
                        self.genMultiMatchObj(self.gender,["mesh_terms"],"best_fields",1)
                
                    ] #+ self.explodeSearch()
                }
            }
        }

        return obj
    def abYHalf(self):
        gList = []
        for g in self.genes: 
            gList.append(self.genMultiMatchObj(g,["text","mesh_terms"],"cross_fields",1))
        ageT = []
  
        obj = {
            "query":{
                "bool":{
                    "must":[
                        self.genMultiMatchObj(self.disease,["text","mesh_terms"],"best_fields",1.5),
                        
                    {
                        "bool":{
                            "should":gList
                        }
                    }],
                    "should":[
                        self.genMultiMatchObj(self.gender,["mesh_terms"],"best_fields",1)
                
                    ] #+ self.explodeSearch()
                }
            }
        }
        return obj

    #Gene expanded only
    def abY1(self):
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
                            self.genMultiMatchObj(self.disease,["text","mesh_terms"],"best_fields",1.5),   
                            {
                                "bool":{
                                    "should":geneList +  geneList2
                                }
                            }
                            ],
                            "should":[
                                self.genMultiMatchObj(self.gender,["mesh_terms"],"best_fields",1),
                            ] #+ self.explodeSearch()
                        }
            }
        }
        return obj

    #Gene expanded only
    def abY2(self):
        di = self.expandDisease()
        p = []
        for d in di:
            if "carcinoma" in d.lower() or "neoplasm" in d.lower() or "cancer" in d.lower() :
                p.append(self.genMultiMatchObj(d,self.fields,"cross_fields",.5))
        gList = []
        for g in self.genes: 
            gList.append(self.genMultiMatchObj(g,["text","mesh_terms"],"cross_fields",1))
        ageT = []
  
        obj = {
            "query":{
                "bool":{
                    "must":[
                    {
                        "bool":{
                            "should":[self.genMultiMatchObj(self.disease,["text","mesh_terms"],"best_fields",1.5),self.genMultiMatchObj(self.disease,["text","mesh_terms"],"phrase",.3)] + p
                        }
                    }, 
                        
                    {
                        "bool":{
                            "should":gList
                        }
                    }],
                    "should":[
                        self.genMultiMatchObj(self.gender,["mesh_terms"],"best_fields",1)
                
                    ] #+ self.explodeSearch()
                }
            }
        }
        return obj
     #infNDCG: 0.4555
    def abY3(self):
        di = self.expandDisease()
        p = []
        for d in di:
            if "carcinoma" in d.lower() or "neoplasm" in d.lower() or "cancer" in d.lower() :
                p.append(self.genMultiMatchObj(d,self.fields,"cross_fields",.5))

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
                geneList.append(self.genMultiMatchObj(d2["name"],self.fields,"phrase",.3))
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
                  "should":[
                        {"bool":{
                            "must":[
                            {
                                "bool":{
                                    "should":[self.genMultiMatchObj(self.disease,["text","mesh_terms"],"best_fields",1.5),self.genMultiMatchObj(self.disease,["text","mesh_terms"],"phrase",.3)] + p
                                }
                            },    
                            {
                                "bool":{
                                    "should":geneList +  geneList2
                                }
                            }
                            ],
                            "should":[
                                self.genMultiMatchObj(self.gender,["mesh_terms"],"best_fields",1),
                            ] + self.explodeSearch() 
                        }}
                  ]
              }
               
            }
        }
        f = open("AB1.json","w")
        f.write(json.dumps(obj,indent=4))
        f.close()
        return obj
    #infNDCG: 0.4555
    def abY4(self):
        di = self.expandDisease()
        p = []
        for d in di:
            if "carcinoma" in d.lower() or "neoplasm" in d.lower() or "cancer" in d.lower() :
                p.append(self.genMultiMatchObj(d,self.fields,"cross_fields",.5))

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
                geneList.append(self.genMultiMatchObj(d2["name"],self.fields,"phrase",.3))
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
                  "should":[
                        {"bool":{
                            "must":[
                            {
                                "bool":{
                                    "should":[self.genMultiMatchObj(self.disease,["text","mesh_terms"],"best_fields",1.5),self.genMultiMatchObj(self.disease,["text","mesh_terms"],"phrase",.3)] + p
                                }
                            },    
                            {
                                "bool":{
                                    "should":geneList +  geneList2
                                }
                            }
                            ],
                            "should":[
                                self.genMultiMatchObj(self.gender,["mesh_terms"],"best_fields",1),
                            ] #+ self.explodeSearch() 
                        }},
                        #Catch partial matches and include them
                        { "bool":{
                                    "should":[self.genMultiMatchObj(self.disease,["text","mesh_terms"],"best_fields",1.5),self.genMultiMatchObj(self.disease,["text","mesh_terms"],"phrase",.3)] + p,
                                    "boost":.01
                            }
                        }
                  ]
              }
               
            }
        }
        return obj
    #infNDCG: 0.4555
    def abY5(self):
        di = self.expandDisease()
        p = []
        for d in di:
            if "carcinoma" in d.lower() or "neoplasm" in d.lower() or "cancer" in d.lower() :
                p.append(self.genMultiMatchObj(d,self.fields,"cross_fields",.5))

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
                geneList.append(self.genMultiMatchObj(d2["name"],self.fields,"phrase",.3))
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
                  "should":[
                        {"bool":{
                            "must":[
                            {
                                "bool":{
                                    "should":[self.genMultiMatchObj(self.disease,["text","mesh_terms"],"best_fields",1.5),self.genMultiMatchObj(self.disease,["text","mesh_terms"],"phrase",.3)] + p,
                                }
                            },    
                            {
                                "bool":{
                                    "should":geneList +  geneList2
                                }
                            }
                            ],
                            "should":[
                                self.genMultiMatchObj(self.gender,["mesh_terms"],"best_fields",1),
                            ] #+ self.explodeSearch()
                        }},
                        #Catch partial matches and include them
                        {
                                "bool":{
                                    "should":geneList +  geneList2,
                                    "boost":.01
                                }
                        }
                  ]
              }
               
            }
        }
        return obj
    #infNDCG: 0.4555
    def abY6(self):
        di = self.expandDisease()
        p = []
        for d in di:
            if "carcinoma" in d.lower() or "neoplasm" in d.lower() or "cancer" in d.lower() :
                p.append(self.genMultiMatchObj(d,self.fields,"cross_fields",.5))

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
                geneList.append(self.genMultiMatchObj(d2["name"],self.fields,"phrase",.3))
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
                  "should":[
                        {"bool":{
                            "must":[
                            {
                                "bool":{
                                    "should":[self.genMultiMatchObj(self.disease,["text","mesh_terms"],"best_fields",1.5),self.genMultiMatchObj(self.disease,["text","mesh_terms"],"phrase",.3)] + p
                                }
                            },    
                            {
                                "bool":{
                                    "should":geneList +  geneList2
                                }
                            }
                            ],
                            "should":[
                                self.genMultiMatchObj(self.gender,["mesh_terms"],"best_fields",1),
                            ] ##+ self.explodeSearch()
                        }},
                        #Catch partial matches and include them
                        {
                                "bool":{
                                    "should":geneList +  geneList2,
                                    "boost":.01
                                }
                        },
                         { 
                            "bool":{
                                    "should":[self.genMultiMatchObj(self.disease,["text","mesh_terms"],"best_fields",1.5),self.genMultiMatchObj(self.disease,["text","mesh_terms"],"phrase",.3)] + p,
                                    "boost":.01
                            }
                        }

                  ]
              }
               
            }
        }
        return obj
    def expandDisease(self):
        pageNumber = 0
        string = self.disease
        ##generate a new service ticket for each page if needed
        ticket = AuthClient.getst(tgt)
        fList = []
        while pageNumber < 10:
            try:
                query = {'string':string,'ticket':ticket, 'pageNumber':pageNumber}
                r = requests.get(uri+content_endpoint,params=query).json()
                jsonData = r["result"]["results"]
            except Exception as e:
                pageNumber = 11
                jsonData = []
            #print(jsonData)
            new_list = [i["name"] for i in jsonData if len(i["name"].split(" "))<3 and self.disease.lower() not in i["name"].lower() and "protein" not in i["name"].lower() and "antigen" not in i["name"].lower()and "gene" not in i["name"].lower()]
            fList = fList + new_list
            pageNumber = pageNumber + 1
           
        return fList
    def meshSearch(self):
    
        #Search for age terms first. Using methodology provided in Age Specific Paper 
        ageTerms = []
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

       





