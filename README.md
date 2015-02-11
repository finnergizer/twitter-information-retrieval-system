#CSI4107 Assignment 1

_Shaughn Finnerty (6300433), Neil Warnock (Student #)_
___

##Dependencies

Natural Language Toolkit (NLTK) - <a href="http://www.nltk.org/install.html">Installation instructions</a>

Once NLTK is installed, you must run the following to download NLTK data - stopwords and punkt for tokenizing and preprocessing.

	import nltk
	nltk.download()

This code will launch an NLTK downloader window. Click the **All Packages** tab, then look for the identifiers **punkt** (for using the punkt punctuation tokenizer), and **stopwords**. Select both and click download. This will download the data needed by the NLTK functions used to tokenize and preprocess the corpus.

##Functionality
The entire system is located under the *twitter_irs* module. Within this module there are multiple python files separated by the functionality that they provide to the system.

###prepocessor.py
This file provides a class that is used to preprocess a document corpus of Twitter messages in the TREC provided format.

The preprocessor will parse the corpus into a hashmap

###utils.py
utils.py provides helper functions that are used throughout the application, in preprocessing, index creation, and query processing. It was a design decision to place these functions in a seperate file to promote their reuse and consistency in the application. For example, we use the **process_txt** method when prepocessing the messages, and apply the same method to queries so that stop words are removed and stem words are used when applying the query.

In addition, we include the functions used to compute tf-idf index values.

###indexing.py
asdf

###query.py

###system.py

##Running the System

##Results
###100 Example Tokens
###Query Results
