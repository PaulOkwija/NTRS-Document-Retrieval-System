import os
import nltk
import PyPDF2
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize

def get_analytics(filename, keywords):
	with open(filename,'rb') as f:
	    f = PyPDF2.PdfFileReader(f)
	    text = ''
	    for page in f.pages:
	        text = text + ' ' + page.extractText()
	
	word_count = {}
	for word in keywords:
		print("\n")
		print(word)
		print('\n')
		count = text.count(word)
		word_count[word] = count
	
	return word_count