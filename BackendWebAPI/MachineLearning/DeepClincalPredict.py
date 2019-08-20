import pandas as pd
# Keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json
import keras

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
json_file = open('/Users/samshenoi/Documents/CPRIT/CPRIT/MachineLearning/Models/abstract_model_gloveFinal.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("/Users/samshenoi/Documents/CPRIT/CPRIT/MachineLearning/Weights/abstract_model_gloveFinal.h5")

# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#Precompile regex
first = re.compile(r"\[\D\S{6}:\S{5}\]")
second = re.compile(r"\/")
third = re.compile(r"\\n*")
f  = re.compile(r"\'")
five = re.compile(r'\,|\.|\:|\&')
six = re.compile(r'\{|\}|\[|\]')
def load_data(file):
    json_file = open(file, "r", encoding ='latin-1')
    data = json_file.read()
    json_file.close()
    return str(data)
nltk.download('stopwords')
nltk.download('wordnet')
wn = nltk.WordNetLemmatizer()
def clean_text(text):
    ## Remove puncuation
    text = text.translate(string.punctuation)
    
    ## Convert words to lower case and split them
    text = text.lower().split()
    
    ## Remove stop words
    stops = set(stopwords.words("english"))
    text = [w for w in text if not w in stops and len(w) >= 3]
    text = " ".join(text)
    # Clean the text
    text = first.sub("", text)
    text = second.sub("", text)
    text = third.sub("", text)
    text = f.sub("", text)
    text = five.sub("", text)
    text = six.sub("", text)
	
    text = text.split()
    stemmer = SnowballStemmer('english')
    stemmed_words = [stemmer.stem(word) for word in text]
    text = [wn.lemmatize(word) for word in text]
    text = " ".join(stemmed_words)
    text = pd.DataFrame({"Abstracts": [text]})
    return text
vocabulary_size = 20000
def process(df):
    tokenizer = Tokenizer(num_words= vocabulary_size)
    tokenizer.fit_on_texts(df['Abstracts'])
    sequences = tokenizer.texts_to_sequences(df['Abstracts'])
    data = pad_sequences(sequences)
    return np.array(data)
# load json and create model
def load_trained_model():
    json_file = open('/Users/samshenoi/Documents/CPRIT/CPRIT/MachineLearning/Models/clinical_model_masked_lstm.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("/Users/samshenoi/Documents/CPRIT/CPRIT/MachineLearning/Weights/clinical_model_masked_lstm.h5")
    print("Loaded model from disk")
     
    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return loaded_model
def predict(file):
    text = clean_text(file)
    x = process(text)
    x = keras.preprocessing.sequence.pad_sequences(x, maxlen=1007)
    model = loaded_model
    pred = model.predict_classes(x)
    pred_p=model.predict(x)

    prediction = pred[0][0]
    return prediction
