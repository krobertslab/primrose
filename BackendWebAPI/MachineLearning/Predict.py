#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import pandas as pd
# Keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Input, Dense, Flatten, LSTM, Conv1D, MaxPooling1D, Dropout, Activation, Masking, Bidirectional
from keras.layers.embeddings import Embedding
from keras.models import model_from_json

# NLTK
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Other
import re
import string
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
import sys


# In[39]:


import csv 
import requests 
import xml.etree.ElementTree as ET 
import pandas as pd
def parsegene(xmlfile): 
    # create element tree object 
    tree = ET.parse(xmlfile) 
    # get root element 
    root = tree.getroot()
    # create empty list for news items 
    geneitems = [] 
    # iterate news items 
    for item in root.findall('./topic/gene'): 
        gene = item.text
        # append news dictionary to news items list 
        geneitems.append(gene)  
    # return news items list 
    for i in range(19,21):
        geneitems.remove(geneitems[i])
    genes = str(geneitems)
    genes = re.sub("[a-x]|\[|\]|\'|\,|\(|\)|\W\d+\W|[y].","", genes).split(" ")
    geneslist = []                
    for i in genes:
        if i != "":
            geneslist.append(i)
    pattern = "|".join(geneslist)
    return pattern


nltk.download('stopwords')
nltk.download('wordnet')
wn = nltk.WordNetLemmatizer()
def clean_text(text):
    genes = parsegene("/Users/samshenoi/Documents/CPRIT/CPRIT/MachineLearning/Topics/topics2018.xml")#"C:/Users/vly2/Documents/CPRIT/MachineLearning/Topics/topics2018.xml")
    ## Remove puncuation
    text = str(text)
    text = text.translate(string.punctuation)
    
    ## Convert words to lower case and split them
    text = text.lower().split()
    
    ## Remove stop words
    stops = set(stopwords.words("english"))
    text = [w for w in text if not w in stops and len(w) >= 3]
    text = " ".join(text)
    # Clean the text
    text = re.sub(r"\[\D\S{6}:\S{5}\]", "", text)
    text = re.sub(r"\/", "", text)
    text = re.sub(r"\\n*", "", text)
    text = re.sub(r"\'", "", text)
    text = re.sub(r'\,|\.|\:|\&', "", text)
    text = re.sub(r'\{|\}|\[|\]|\(|\)', "", text)
    text = re.sub(genes, "gene", text)
    text = text.split()
    stemmer = SnowballStemmer('english')
    stemmed_words = [stemmer.stem(word) for word in text]
    text = [wn.lemmatize(word) for word in text]
    text = " ".join(stemmed_words)
    return text


vocabulary_size = 20000
def process(df):
    tokenizer = Tokenizer(num_words= vocabulary_size)
    tokenizer.fit_on_texts(df['Abstracts'])
    sequences = tokenizer.texts_to_sequences(df['Abstracts'])
    data = pad_sequences(sequences, maxlen=500)
    df_save = pd.DataFrame(data)
    return df_save


# In[40]:


# In[42]:

import sys
import sklearn
x_train, y_train = sklearn.datasets.load_svmlight_file("/Users/samshenoi/Documents/CPRIT/CPRIT/MachineLearning/data/train.txt")#"C:/Users/vly2/Documents/CPRIT/MachineLearning/data/train.txt")
x_valid, y_valid = sklearn.datasets.load_svmlight_file("/Users/samshenoi/Documents/CPRIT/CPRIT/MachineLearning/data/val.txt")#"C:/Users/vly2/Documents/CPRIT/MachineLearning/data/val.txt")
q_train = np.loadtxt("/Users/samshenoi/Documents/CPRIT/CPRIT/MachineLearning/data/train.group")#'C:/Users/vly2/Documents/CPRIT/MachineLearning/data/train.group')
q_valid = np.loadtxt("/Users/samshenoi/Documents/CPRIT/CPRIT/MachineLearning/data/val.group")#C:/Users/vly2/Documents/CPRIT/MachineLearning/data/val.group')
import lightgbm as lgb
gbm = lgb.LGBMRanker()
sys.stdout = open("trash", "w")
bst = gbm.fit(x_train, y_train, group=q_train, eval_set=[(x_valid, y_valid)],
eval_group=[q_valid], eval_at=[1, 3], early_stopping_rounds=20, verbose=True,
callbacks=[lgb.reset_parameter(learning_rate=lambda x: 0.95 ** x * 0.1)])
sys.stdout.close()

# In[43]:


def predict(data):
    data = pd.read_json(path_or_buf = data).iloc[:,3:4].rename(columns={"_source":"Abstracts"})
    df = data.dropna()
    df['Abstracts'] = df['Abstracts'].map(lambda x: clean_text(x))
    test_x = process(df)
    preds = gbm.predict(test_x)
    return preds


# In[44]:
