# -*- coding: utf-8 -*-
"""assign_keywords.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16AfmPaJcVYKPEXdHEAJQQ2q1_sxvwhpQ
"""

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os
import nltk
from gensim import models
from gensim import similarities

from collections import defaultdict
from gensim import corpora

from google.colab import drive
drive.mount('/content/drive', force_remount=True)

!pip3 install PyPDF2

path = '/content/drive/MyDrive/NASA Space Apps Challenge/corpus/'
os.listdir(path)

import PyPDF2

# print(filename)

corpus_folder = '/content/drive/MyDrive/NASA Space Apps Challenge/corpus'

import os, json
import pandas as pd
json_files = [pos_json for pos_json in os.listdir(corpus_folder) if pos_json.endswith('.json')]

file_ids = []
for f in json_files:
    file_id = f.split('.')[0]
    file_ids.append(file_id)

print(file_ids)

from pprint import pprint

with open('/content/drive/MyDrive/NASA Space Apps Challenge/broad_topics.json') as f:
    broad_topics = json.load(f)

pprint(broad_topics)

specific_categories = []
for topic in broad_topics.keys():
    specific_categories.extend(list(broad_topics[topic].keys()))

specific_categories

documents = []
content = ''
for broad_cat in broad_topics:
    print(broad_cat)
    print("---"*10)
    for spec_cat in broad_topics[broad_cat]:
        print(spec_cat)
        documents = broad_topics[broad_cat][spec_cat]
        pprint(documents)
        
        stoplist = set('for a of the and to in'.split())
        texts = [
            [word for word in document.lower().split() if word not in stoplist]
            for document in documents
        ]

        # remove words that appear only once
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        texts = [
            [token for token in text if frequency[token] >= 1]
            for text in texts
        ]

        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        
        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=5)

        for file_id in file_ids:
            # print(file_name)
            with open(os.path.join(corpus_folder, file_id+'.json')) as f:
                json_file = json.load(f)
            
            if json_file['subjectCategory'] == spec_cat:
                file_name = os.path.join(corpus_folder, file_id+'.pdf')
                # print(file_name)
                print('\n')
                with open( file_name,'rb') as f:
                    f = PyPDF2.PdfFileReader(f)
                    doc = ''
                    for page in f.pages:
                        doc = doc + ' ' + page.extractText()
                
                vec_bow = dictionary.doc2bow(doc.lower().split())
                vec_lsi = lsi[vec_bow]  # convert the query to LSI space

                index = similarities.MatrixSimilarity(lsi[corpus])

                sims = index[vec_lsi]  # perform a similarity query against the corpus
                # print(list(enumerate(sims)))  # print (document_number, document_similarity) 2-tuples
                sims = sorted(enumerate(sims), key=lambda item: -item[1])
                keywords = []
                for doc_position, doc_score in sims[:5]:
                    print("{} : {}".format(documents[doc_position], round(float(doc_score), 4)))
                    keywords.append(documents[doc_position])
                    # print(documents[doc_position][:100], f": ({round(doc_score, 4)})")

                json_file['keywords'] = keywords

                with open(os.path.join(corpus_folder, file_id+'.json'), 'w') as f:
                    json.dump(json_file, f)
                

        # break
    print("\n")
    # break