'''
Name: xmlParser
Description: This file parses the XML topics on the Trec CDS website and then runs them through the serach engine
Author: Sam Shenoi
Acknowledgments: 
  - the code for this xml parser is a modifed copy of: https://github.com/dcsgman/TREC-2017-PM/blob/master/solution_by_elastic/extract_xml.py
'''

from __future__ import print_function
import time

import xml.etree.ElementTree as ET 
import sys
import argparse
import pprint
pp = pprint.PrettyPrinter(indent=4)
from Elastic import Elastic
import csv
import json
import functools

#!/usr/bin python3
# -*- coding: utf-8 -*-
import glob
import collections
import os


#from MachineLearning import Predict
#from MachineLearning import DeepPredict
#from MachineLearning import ClinicalPredict
#from MachineLearning import DeepClinicalPredict

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)



"""
    Extracting the desired data from the input xml files.
    After extracting the desired data from each input xml file, it is stored in an ordered dictionary.
    This dictionary is then passed to the elastic_index function which will index the data in Elasticsearch.
"""
def extract_trial_data_xml(xml_path,es_index='pm_ct', doc_type='xmldata'):
    ElasticClient = Elastic(abQuery=8,tQuery=7)
    # Provide the path to the input xml files
    list_of_files = glob.glob(xml_path )#+'/*/*' + '/*.xml')
    print(list_of_files)

    # Counter variable to count each processed file
    ctr = 0

    # We will print the progress as we process each file
    print('\nProgress extracting the data from the xml files:')

    # This for loop iterates over each input file. Within each try-except block we try to extract the data from one particular xml field.
    # This extracted data is stored in an ordered dictionary with key as the field name and value as the extracted data.
    # Currently the following fields are extracted: nct_id, brief_title, brief_summary, detailed_description, overall_status, condition,
    #                                               eligibility, gender, gender_based, minimum_age, maximum_age, keyword, mesh_term
    # Not all the files contain all the fields we desire, hence the multiple try-except blocks.
    for input_file in list_of_files:
            tree = ET.parse(input_file)
            root = tree.getroot()

            #Create an ordered dictionary and lists to store the keywords and mesh terms
            extracted_data = collections.OrderedDict()
            condition_list = []
            keyword_list = []
            mesh_term_list = []
            id = ''
            #nct_id
            try:
                    nct_id = root.find('id_info').find('nct_id').text
                    id  = nct_id
            except:
                    #ensure that the id is recieved from the filename. Use this field as the id of the document
                    base=os.path.basename(input_file) 
                    id = os.path.splitext(base)[0]
            #brief_title
            try:
                    brief_title = root.find('brief_title').text
                    extracted_data['brief_title'] = brief_title
            except:
                    extracted_data['brief_title'] = None

            #brief_summary
            try:
                    brief_summary = root.find('brief_summary').find('textblock').text
                    extracted_data['brief_summary'] = brief_summary
            except:
                    extracted_data['brief_summary'] = None

            #detailed_description
            try:
                    detailed_description = root.find('detailed_description').find('textblock').text
                    extracted_data['detailed_description'] = detailed_description
            except:
                    extracted_data['detailed_description'] = None

            #overall_status
            try:
                    overall_status = root.find('overall_status').text
                    extracted_data['overall_status'] = overall_status
            except:
                    extracted_data['overall_status'] = None

            #condition
            try:
                    # 031/03106/NCT03106844.xml
                    condition = root.findall('condition')
                    for index, item in enumerate(condition):
                        condition_list.append(item.text)
                    extracted_data['condition'] = condition_list
            except:
                    extracted_data['condition'] = None

            #eligibility
            try:
                    eligibility = root.find('eligibility').find('criteria').find('textblock').text
                    extracted_data['eligibility'] = eligibility
            except:
                    extracted_data['eligibility'] = None

            #gender
            try:
                    gender = root.find('eligibility').find('gender').text
                    extracted_data['gender'] = gender
            except:
                    extracted_data['gender'] = None

            #gender_based
            try:
                    gender_based = root.find('eligibility').find('gender_based').text
                    extracted_data['gender_based'] = gender_based
            except:
                    extracted_data['gender_based'] = None

            #minimum_age
            try:
                    minimum_age = root.find('eligibility').find('minimum_age').text
                    try:
                        extracted_data['minimum_age'] = int(minimum_age.split(' ')[0])
                    except:
                        extracted_data['minimum_age'] = 0
            except:
                    extracted_data['minimum_age'] = None

            #maximum_age
            try:
                    maximum_age = root.find('eligibility').find('maximum_age').text
                    try:
                        extracted_data['maximum_age'] = int(maximum_age.split(' ')[0])
                    except:
                        extracted_data['maximum_age'] = 99
            except:
                    extracted_data['maximum_age'] = None

            #keyword
            try:
                    keyword = root.findall('keyword')
                    for index, item in enumerate(keyword):
                        keyword_list.append(item.text)
                    extracted_data['keyword'] = keyword_list
            except:
                    extracted_data['keyword'] = None

            #mesh_term
            try:
                    mesh_term = root.find('condition_browse').findall('mesh_term')
                    for index, item in enumerate(mesh_term):
                        mesh_term_list.append(item.text)
                    extracted_data['mesh_term'] = mesh_term_list
            except:
                    extracted_data['mesh_term'] = None

            #Pass the counter 'ctr' and the dictionary 'extracted_data' to elastic_index function which indexes it in Elasticsearch.
  
            #ElasticClient.insert("trials", extracted_data,"trials",id)
            print(extracted_data)

            #Increment the counter and print the progress in the following format: current counter value/total number of input files.
            ctr+=1
            print(ctr,'/',len(list_of_files))

    return
'''
  name:          extract_abstract_data_xml
  description:   This function inserts data into the abstract folder 
  precondition:  the path to the folder is passed in
  postcondition: the abstract data is inserted into ElasticSearch
'''
def extract_abstract_data_xml(xml_path,es_index='abstracts', doc_type='xmldata'):
    Elastic(abQuery=8,tQuery=7)
    if doc_type == 'textdata': 
        # Provide the path to the input xml files
        list_of_files = glob.glob(xml_path +'/*/*' + '/*.txt')
    else:
        # Provide the path to the input xml files
        list_of_files = glob.glob(xml_path +'/*/*' + '/*.xml')


    # Counter variable to count each processed file
    ctr = 0

    # We will print the progress as we process each file
    print('\nProgress extracting the data from the xml files:')

    # This for loop iterates over each input file. Within each try-except block we try to extract the data from one particular xml field.
    # This extracted data is stored in an ordered dictionary with key as the field name and value as the extracted data.
    # Currently the following fields are extracted: nct_id, brief_title, brief_summary, detailed_description, overall_status, condition,
    #                                               eligibility, gender, gender_based, minimum_age, maximum_age, keyword, mesh_term
    # Not all the files contain all the fields we desire, hence the multiple try-except blocks.
    for input_file in list_of_files:
        if doc_type =='xmldata':
                tree = ET.parse(input_file)
                root = tree.getroot().findall('Document')
              
                for child in root: 
                        #Create an ordered dictionary and lists to store the keywords and mesh terms
                        extracted_data = collections.OrderedDict()
                        mesh_term_list = []
                        assert(child.tag =='Document')
                        id = child.attrib["id"]
                        #Meta tags
                        try:
                                metaList = child.find('MetaData')
                                metalist = metaList.findall('MetaDatum')
                                for m in metaList:
                                        if "mesh" in m.attrib['key']:
                                          mesh_term_list.append(m.attrib['value'])
                                extracted_data["mesh_terms"] = mesh_term_list
                        except Exception as e:
                                extracted_data["mesh_terms"] = None
                        #Text
                        try:
                                extracted_data["text"] = child.find('Text').text  
                        except:
                                extracted_data['text'] = None
                        ElasticClient.insert("abstracts", extracted_data,"abstracts",id)
                        ctr+=1
                        print(ctr,'/',len(list_of_files))
        else:
                extracted_data = collections.OrderedDict()
                id = input_file.split(".")[0]
                id = id.split("/")
                id = id[len(id) -1]
                extracted_data["mesh_terms"] = None
                extracted_data["text"] = open(input_file).read()
               
                #ElasticClient.insert("abstracts", extracted_data,"abstracts",id)
                ctr+=1
                print(ctr,'/',len(list_of_files))

    return 


"""
    The query topics are provided in an XML file. This function is used to extract query terms from that XML file.
    After extracting the query terms, it is stored in an ordered dictionary.
    This dictionary is then passed to the es_query function which will query Elasticsearch with those terms.
"""
def extract_query_xml(trials,query):
  
    if trials:
        ElasticClient = Elastic(tQuery=query)
    else:
       ElasticClient = Elastic(abQuery=query)
    
    # Provide the path to the query xml file
    query_file = open("topics2017.xml")
    '''
    PM = dict()
    NotPM = dict() 

    #Get the PM stuff so that we only check if its a valid PM mesh tag
    with open('MachineLearning/abstracts.judgments.2017.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
           if row[2] == "Not PM":
                if row[0] in NotPM.keys():
                   NotPM[row[0]].append(row[1]) 
                else:
                   NotPM[row[0]] = [row[1]]
           else:
                if row[0] in PM.keys():
                   PM[row[0]].append(row[1]) 
                else:
                   PM[row[0]] = [row[1]]


    '''
    tree = ET.parse(query_file)
    root = tree.getroot()
    query_file.close()
   
    # Create an ordered dictionary to store the query terms
    extracted_data = collections.OrderedDict()
    writeOut = open("out.txt",'w')
    # There are 30 query topics provided. First we store all the topics and iterate over each of them using a for loop.
    # Each query topic contains multiple fields. In the try-except block we try to extract the terms for each particular query.
    # These extracted terms are stored in an ordered dictionary with key as the field name and value as the extracted terms.
    try:
        topics = root.findall('topic')
       
        for index, item in enumerate(topics):
                eprint(index)
                mesh = dict()
                disease = item.find('disease').text
                gene = item.find('gene').text
                demographic = item.find('demographic').text
                other = item.find('other').text
                x = []
                w = []
                if trials == True:
                        x = hits = ElasticClient.trialsSearch(disease,gene,demographic,other)
                        count = 0
                        fNum = 50
                        #Find the range between the top 50
                        try:
                            r = hits[0]["_score"] - hits[fNum]["_score"]
                        except:
                            fNum = len(hits)-1
                            r = hits[0]["_score"] - hits[len(hits)-1]["_score"]
                        try: 
                                for theP in range(fNum): 
                                        isPM = DeepPredict.predict(str(hits[theP]["_source"]))
                                        hits[theP]["_score"] = hits[theP]["_score"] + (r/2  * isPM)
                                hits.sort(key=lambda y: y["_score"], reverse=True) 
                        except Exception as e: 
                                eprint(e)
                        x  = hits
                       
 
                        '''
                        x = ClinicalPredict.predict(json.dumps(hits))
                        
                        for i in range(0,len(x)):
                           w.append((hits[i],x[i]))

                        w.sort(key=lambda y: y[1], reverse=True)
                        '''
                      
                
                #if "cancer" in disease and trials == False:
                else:
                        x = hits = ElasticClient.abstractSearch(disease,gene,demographic,other)
                        #Deep Learning Code for abstracts
                       
                        count = 0
                        fNum = 50
                        #Find the range between the top 50
                        try:
                            r = hits[0]["_score"] - hits[fNum]["_score"]
                        except:
                            fNum = len(hits)-1
                            r = hits[0]["_score"] - hits[len(hits)-1]["_score"]
                        
                        try: 
                                for theP in range(fNum): 
                                        isPM = DeepPredict.predict(str(hits[theP]["_source"]))
                                        hits[theP]["_score"] = hits[theP]["_score"] + (r/2  * isPM)
                                hits.sort(key=lambda y: y["_score"], reverse=True) 
                        except Exception as e: 
                                eprint(e)
                        x  = hits
                       
 
                        '''
                        #L2R code for abstracts
                       
                        x = Predict.predict(json.dumps(hits))
                       
                        for i in range(0,len(x)):
                           w.append((hits[i],x[i]))

                        w.sort(key=lambda y: y[1], reverse=True)
                        '''
                     

                c = 0 
                found = []
                while c < len(x) and c <1000:
                        #L2R Write
                        #writeOut.write("%s  0  %s  %s  %s  xCGG1 \n" % (item.attrib["number"],str(w[c][0]["_id"]),str(c),str(w[c][0]["_score"])))
                        #Deep Write
                        writeOut.write("%s  0  %s  %s  %s  xCGG1 \n" % (item.attrib["number"],str(x[c]["_id"]),str(c),str(x[c]["_score"])))
                        #Reg Write
                        #writeOut.write("%s  0  %s  %s  %s  xCGG1 \n" % (item.attrib["number"],str(hits[c]["_id"]),str(c),str(hits[c]["_score"]) ))
                        c = c + 1
                
                '''
                        if c < 10:
                                isPM = theBigPM(json.dumps(hits[c]["_source"])) 
                                if isPM < 1: 
                                   eprint(hits[c]["_id"])
                                if hits[c]["_id"] in PM[item.attrib["number"]] :
                                     try:
                                        
                                        found.append(hits[c]["_id"]) 
                                        #PM[item.attrib["number"]].remove(hits[c]["_id"])
                                        f = open("./data/%s/%s-%s.txt"%(item.attrib["number"],str(c).zfill(4),hits[c]["_id"]),"w") 
                                        f.write("PMID: %s" %(hits[c]["_id"]))
                                        f.write(str(hits[c]["_source"]))
                                        f.write("ML Classifier Result: %s"%(isPM))
                                        f.close()
                                     except Exception as e: 
                                         eprint(e)
                                elif hits[c]["_id"] in NotPM[item.attrib["number"]]:
                                      try:
                                        f = open("./data/%s/Top10NotPM/%s-%s.txt"%(item.attrib["number"],str(c).zfill(4),hits[c]["_id"]),"w") 
                                        f.write("PMID: %s" %(hits[c]["_id"]))
                                        f.write(str(hits[c]["_source"]))
                                        f.write("ML Classifier Result: %s"%(isPM))
                                        f.close()
                                      except Exception as e: 
                                        eprint(e)
                                else:
                                      try:
                                        f = open("./data/%s/Top10NotJudged/%s-%s.txt"%(item.attrib["number"],str(c).zfill(4),hits[c]["_id"]),"w") 
                                        f.write("PMID: %s" %(hits[c]["_id"]))
                                        f.write(str(hits[c]["_source"]))
                                        f.write("ML Classifier Result: %s"%(isPM))
                                        f.close()
                                      except Exception as e: 
                                        eprint(e)
                        else:
                                if hits[c]["_id"] in PM[item.attrib["number"]]:
                                     isPM = theBigPM(json.dumps(hits[c]["_source"])) 
                                     if isPM < 1: 
                                         eprint(hits[c]["_id"])
                                    
                                     found.append(hits[c]["_id"]) 

                                     try:
                                        #PM[item.attrib["number"]].remove(hits[c]["_id"])
                                        f = open("./data/%s/OtherPM/%s-%s.txt"%(item.attrib["number"],str(c).zfill(4),hits[c]["_id"]),"w") 
                                        f.write("PMID: %s" %(hits[c]["_id"]))
                                        f.write(str(hits[c]["_source"]))
                                        f.write("ML Classifier Result: %s"%(isPM))
                                        f.close()
                                     except Exception as e: 
                                        eprint("OTHER PM:", e)  
                        #hits[c]["_score"] =  hits[c]["_score"] #+ (10 * theBigPM(json.dumps(hits[c])))
                        c = c + 1
        
                l = PM[item.attrib["number"]]
                l = list(set(l) - set(found))
                
                for i in l:
                        try: 
                                res = ElasticClient.get(index="abstracts",  id=i)
                                f = open("./data/%s/OtherPM/XXXX-%s.txt"%(item.attrib["number"],i),"w") 
                                isPM = theBigPM(json.dumps(res["_source"])) 
                                f.write("PMID: %s" %(i))
                                f.write(str(res["_source"]))
                                f.write("ML Classifier Result: %s"%(isPM))
                                f.close()
                        except Exception as e: 
                                eprint(e)
                #hits.sort(key=lambda y: y["_score"], reverse=True)
                
                #Mesh terms total list
                '''
                '''
                c = 0
                
                #Clear File from previous run
                f = open('TotalMesh/%s/Total.txt'%(item.attrib["number"]),"w")
             
                f.close()
                f = open('TotalMesh/%s/NotPM.txt'%(item.attrib["number"]),"w")
             
                f.close()
                f = open('TotalMesh/%s/PM.txt'%(item.attrib["number"]),"w")
            
                f.close()
                
                while c <len(x) and c < 1000:
                        if not os.path.exists("/Users/samshenoi/Documents/CPRIT/CPRIT/TotalMesh/%s/"%(item.attrib["number"])):
                               os.mkdir("/Users/samshenoi/Documents/CPRIT/CPRIT/TotalMesh/%s/"%(item.attrib["number"]))
                        f = open('TotalMesh/%s/Total.txt'%(item.attrib["number"]),"a")
                        try:
                           f.write(json.dumps(x[c]["_source"]["mesh_terms"]) + "\n")
                        except:
                            eprint("Error: " + x[c]["_id"])
                        f.close()

                        if x[c]["_id"] in PM[item.attrib["number"]]:
                                f = open('TotalMesh/%s/PM.txt'%(item.attrib["number"]),"a")
                                try:
                                        f.write(json.dumps(x[c]["_source"]["mesh_terms"]) + "\n")
                                except:
                                        eprint("Error: " + x[c]["_id"])
                                f.close()
                        if x[c]["_id"] in PM[item.attrib["number"]]:
                                f = open('TotalMesh/%s/NotPM.txt'%(item.attrib["number"]),"a")
                                try:
                                        f.write(json.dumps(x[c]["_source"]["mesh_terms"]) +  "\n")
                                except:
                                        eprint("Error: " + x[c]["_id"])
                                f.close()
                        
                        c = c + 1
                print("DOne")
                '''
        writeOut.close()   
               
                

       
            
    except Exception as e:
        print(e)
        extracted_data['tnum'] = None
        extracted_data['disease'] = None
        extracted_data['gene'] = None
        extracted_data['age'] = None
        extracted_data['sex'] = None
        extracted_data['other'] = None

    return
'''
 Description: This function caches results from the ML
'''

'''
 Description: this function runs the PM classifier over the hits. It's main purpose is to decrease running time
'''
@functools.lru_cache(maxsize=3000)
def theBigPM(hit):

     #isPM = Predict.main(str(json.loads(hit)))
    
     return isPM
'''
 Description: This function converts bool command line arguments to something actually useful. 
 Acknowledgements: 
          - Code from: https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
'''
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

'''
  name: main 
  description: Contains the main function declaration for inserting data into Elastic Search
               Uses command line argument flags to call the correct insert function 
  precondition: 
          - flags have to be set 
                 -f for the folder name 
                 -c to insert into clinical trials 
                 -a to insert into abstracts
  postcondition: 
          - folder containing data is inserted into ElasticSearch
'''
def main():

  parser = argparse.ArgumentParser(description='Interact with search engine')

  parser.add_argument('-f', help='xml file to input', dest='xml_path')
  parser.add_argument('-c', help='insert into clincal trials, requires -f argument to be set as well', dest='trials', type=str2bool, nargs='?', const=True, default=False)
  parser.add_argument('-a', help='insert into abstracts, requires -f argument to be set as well', dest='abstracts', type=str2bool, nargs='?', const=True, default=False)
  parser.add_argument('-t', help='query clinical trials', dest='t', type=str2bool, nargs='?', const=True, default=False)
  parser.add_argument('-b', help='query abstracts', dest='b', type=str2bool, nargs='?', const=True, default=False)
  parser.add_argument('-X', help='Query number (1-8)', dest='QNum',  nargs='?', const=True, default=8)
  args = parser.parse_args()


  if args.trials: 
    extract_trial_data_xml(args.xml_path,es_index='trials', doc_type='xmldata')
  elif args.abstracts:
    extract_abstract_data_xml(args.xml_path,es_index='abstracts', doc_type='xmldata')
  elif args.t:
    extract_query_xml(True,args.QNum)
  elif args.b:
     extract_query_xml(False,args.QNum)
  else:
    print("Unsuccessful. For help run 'python main.py -h'")

 


if __name__=="__main__":
  main()  


    
