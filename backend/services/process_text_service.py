#process raw message input received from customer

#!pip install emoji
#!pip install autocorrect
#!pip install spacy
#pip3 install stopwords
#python -m spacy download en_core_web_lg
#python -m nltk download wordnet, punkt, stopwords
#python -m nltk download averaged_perceptron_tagger

#import libraries
import re
import emoji
import nltk
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
import itertools
from autocorrect import Speller

from tkinter.constants import X
#download the stopwords from nltk using
import stopwords
from nltk.corpus import stopwords
import spacy.cli

class raw_text_clean(): 

    def sentence_token(data):
        return sent_tokenize(data)
        
    def replace(data, sent_clean_list):
        """
        replace/remove symbols, irrelevant characters from raw message (emoji, abb, regex patterns,...)

        *param: data - a string; sent_clean_list: an empty list containing cleaned string
        *return: sent_clean_list (list of clean sentences)
        """

        #dictionary consisting of the contraction and the actual value
        Apos_dict={"'s":" is","n't":" not","'m":" am","'ll":" will",
                "'d":" would","'ve":" have","'re":" are"}
        #replace the contractions
        for key,value in Apos_dict.items():
            if key in data:
                data=data.replace(key,value)
        
        #remove emoji
        data = emoji.replace_emoji(data, replace='')
        # Defining regex patterns.
        replace_pattern = {
            "urlPattern"      : r"http\S+ | www\S+.",
            "userPattern"     : '@[^\s]+',
            "alphaPattern"    : "[^a-zA-Z0-9]"
        }
        for pattern in replace_pattern.keys(): #remove irrelevant characters
            data = re.sub(replace_pattern[pattern]," ", data)
        
        #replace location abbreviations (HCM -> Ho Chi Minh, HN = Ha Noi)
        abb_dict = {"hcm":"Ho Chi Minh", "hn":"Hanoi", "ha noi":"Hanoi", "vn":"Viet Nam"}
        for key, value in abb_dict.items():
            if key in data.lower():
                before = data[:data.lower().find(key)]
                after = data[data.lower().find(key)+len(key):]
                data = before+value+after

        #One letter in a word should not be present more than twice in continuation
        data = ''.join(''.join(s)[:2] for _, s in itertools.groupby(data))

        #remove extra whitespaces
        data = re.sub(r"\s\s+", "", data)  # \s matches all white spaces
        if " ".join(data.split()).strip() != "":
            sent_clean_list.append(data.strip()) #save cleaned sentence in a new list, remove sentences without word/content

        return sent_clean_list
    
    def grammar_vocab(data, location_count, date_count):
        """
        - scope of works:
            + identify NER tagger
            + contemporarily replace some common abb of job position/industry, location (not being auto corrected)
            + auto correct mispelled words
            + return org job abb
        - params:
            + data (str): text to be processed
            + count (int): index of replacing location (location1, location2,...)
        - return: a dict containing cleaned sentence + its NER dict
        """
        # NER identifier
        nlp = spacy.load("en_core_web_lg")
        ner = {}
        doc = nlp(data)
        for ent in doc.ents:
            #print(ent.text, ent.start_char, ent.end_char, ent.label_)
            ner[ent.text] = ent.label_
        ner_dict = {}
        location_count, date_count = location_count, date_count
        for key, value in ner.items():
            if value == "GPE":
                data = data.replace(key, f'location{location_count}')
                ner_dict[f'location{location_count}'] = key
                location_count +=1
            elif value == "DATE":
                data = data.replace(key, f'date{date_count}')
                # if list(ner.keys)[list(ner.keys).index(key)-1] == "": print("")
                ner_dict[f'date{date_count}'] = key
                date_count +=1

        #exclude some abb words related to job
        job_position_abb = ['IT', 'HR', 'BPO', 'QC', 'QC']
        no = 1
        abb_job = {}
        for word in data.split():
            if word in job_position_abb:
                data = data.replace(word, f"job{no}")
                abb_job[f'job{no}'] = word
                no += 1

        #auto correct mispelled words
        spell = Speller(lang='en')
        data = spell(data)

        #return abb_job back
        no = 1
        for word in data.split():
            if word == 'job'+ str(no):
                data = data.replace(f'job{no}', abb_job[word])
                no += 1

        return {"data": data, "ner_dict": ner_dict, "location_count":location_count, "date_count":date_count}

    def vocab(sent_clean):
    #remove stop words
        for i in sent_clean:

            #import english stopwords list from nltk
            stop = stopwords.words('english')
            excluded_words = ['each', 'and', "of", 'now']
            stop = [word for word in stop if word not in excluded_words]

            x_tokens = i.split()
            x_list=[]
            #remove stopwords
            for word in x_tokens:
                if word not in stop:
                    x_list.append(word)

            sent_clean[sent_clean.index(i)] = " ".join(s for s in x_list)

    #lemmatize    
        for i in sent_clean:
            wordnet_lemmatizer = WordNetLemmatizer()

            x = [wordnet_lemmatizer.lemmatize(n) for n in i.split()]
            sent_clean[sent_clean.index(i)] = " ".join(s for s in x)

        return sent_clean

    def POStagger(sent_clean):
        """
        - Label each word in each sentence by POS tagger, select only noun/adj words, return a dict with key is filtered sentence, value is tagger dict
        - params: sent_clean (list) - list of sentence
        - return: result (dict) {sent: dict(tagger)}
        """
        result = {}

        for i in sent_clean:

            wordsList = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(wordsList)
            resultDictionary = dict((x, y) for x, y in tagged)
            filteredDictionary = {}
            wordnet_lemmatizer = WordNetLemmatizer()

            for (key, value) in resultDictionary.items():
                if value in ["JJR", "JJS", "JJ", "NN", 'NNP', "NNS",'IN', 'RB']:
                    filteredDictionary[wordnet_lemmatizer.lemmatize(key)]=value
            filtersent = " ".join(s for s in list(filteredDictionary.keys()))

            result[filtersent] = filteredDictionary

        return result   
    
    def rename_key(d, old_key, new_key):
        if old_key in d:
            d[new_key] = d.pop(old_key)

    def clean_data(raw_data): 
        """
        a collection of basic steps to clean data

        *params: raw_data: raw message sent by the user
        *return: a list of cleaned sentence
        """   
        
        cleaned_text = []
        for i in raw_text_clean.sentence_token(raw_data):
            cleaned_text = raw_text_clean.replace(i, cleaned_text)
        ner_dict = {}
        location_count = 1
        date_count = 1

        for i in cleaned_text:
            # print(cleaned_text[cleaned_text.index(i)])
            grammar_vocab_result = raw_text_clean.grammar_vocab(i, location_count, date_count)
            cleaned_text[cleaned_text.index(i)] = grammar_vocab_result['data']
            ner_dict[grammar_vocab_result['data']] = grammar_vocab_result['ner_dict']
            location_count = grammar_vocab_result['location_count']
            date_count = grammar_vocab_result['date_count']            
        
        postag_result = raw_text_clean.POStagger(cleaned_text)
        cleaned_text = list(postag_result.keys())
        #postag_ vari to store postagger dict
        postag_ = list(postag_result.values())

        cleaned_text = raw_text_clean.vocab(cleaned_text)

        old_key_ner = list(ner_dict.keys())

        #replace old words by new words from postagger_
        for i in range (len(old_key_ner)):
            ner_dict[cleaned_text[i]] = ner_dict.pop(old_key_ner[i])
        ner_dict_all = {} #key: clean text  #value: {'ner_dict': ner_dict[clean_text], 'filter_pos_tag': raw_text_clean.POStagger(cleaned_text).value()}
        for key, value in ner_dict.items():
            ner_dict_all.update(value)
        filter_pos_dict = {}
        for i in postag_:
            filter_pos_dict.update(i)        

        data_pos = {"clean_text":" ".join(i for i in cleaned_text), "ner_dict": ner_dict_all, "filtered_dict": filter_pos_dict} 
        
        return data_pos 
    