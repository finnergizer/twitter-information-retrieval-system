#CSI4107 Assignment 1

_Shaughn Finnerty (6300433), Neil Warnock (Student 6446269)_
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

The Preprocessor class will parse the corpus into a associative array (i.e. Python dictionary) in which the keys are the document ids and the values map to a list of tokens of the message that have been filtered of stopwords, stemmed, and processed in other ways (i.e. URL removal).

In addition, the Preprocessor can create a "corpus counter" which takes the list for every document in the parsed corpus and replaces it with a frequency associative array with words as keys and their frequency in the document as the values. This additional processing useful for the for quick access to the frequency of a term in a document, which is required extensively during the tf-idf weight calculations in the indexing that follows.

We were careful to maintain the encoding of the characters as best as possible during processing. We ensured that any unknown characters were replaced with a standard unicode character. This allowed for tokenization and further processing/stemming to occur to any characters in unicode. While this allowed characters more than just those in standard ASCII, it also increased the amount of tokens created to over 60000. This would only have a notable effect on index creation time, but would allow for foreign words to be used as searchable tokens (i.e. if any future queries involved foreign languages).

This class also provides a method *create_tokens* which generates a unique set of tokens to be used as keys in the index creation that follows. 


###utils.py
utils.py provides helper functions that are used throughout the application, in preprocessing, index creation, and query processing. It was a design decision to place these functions in a seperate file to promote their reuse and consistency in the application. 

For example, we use the `process_txt` method when prepocessing the messages, and apply the same method to queries in `process_query` so that stop words are removed and stem words are used when applying the query. 

In addition, we include the functions used to compute tf-idf index values. The function `find_max_frequency` is used when computing the normalized term frequency for a document or query term and requires a frequency index **(hence why there are two indexes created)**. The function `compute_term_frequency` is used in combination with `find_max_frequency` method to compute term frequencies which are eventually used in `compute_tf_idf_weight` to compute the tf-idf inverted index which is used for the cosine similarity calculations during retrieval and ranking.


###indexing.py
The Indexer class creates the frequency index as well as the actual tf-idf-index used when computing cosine similarity measures for retrieval and ranking. The frequency index is required to compute the term frequencies during the index creation and also during **query processing**.

The frequency index is stored as an associative array (i.e. Dictionary) in which the keys are the token words and the values are associative arrays with keys being document ids and values being the associated **frequency** of the specific token in that document. It is important to keep this index as queries must use it to find the relative term frequency value when computing its vector representation for cosine similarity calculations.

The tf-idf is also stored as an associative array (i.e. Dictionary) in which the keys are the token words and the values are an associative arrays with keys being document ids and values being the **tf-idf computed weight**.

They are saved as txt files in JSON format for easy retrieval so that the program does not have to spend time recreating the index with every run of the program, and they can simply be loaded into memory via JSON loading functions with every consecutive run.

###query.py
The Query class is used to retrieve a limited set of documents (i.e. documents containing at least one word from the query), and then rank and return these documents using cosine similarity measures. 

The class will create a query vector represented as a list of tf-idf weights and create matching document vectors from those retrieved from the limited set. If a document does not contain a word to match one of the query words, it is given a tf-idf-weight of 0. Both the query vector and document vectors will be representative of the respective word based on their index (i.e. first element in both vectors will contain the weight for the first term, etc.).

Using python linear algebra methods, the cosine similarity measure is calculated using the tf-idf-weights and their score is returned in an associative array with keys id and score. These scores are returned as a list and then sorted in descending order on the values represented by the score key.

###system.py
System is the main execution class of the Information Retrieval system. In here we initiate the system specifying the location of the twitter messages, the location of the frequency-index (either to be saved or loaded from), and the location of the tf-idf-index (again, either where it should be saved or loaded from).

When running the `test_system` method, we input the query information (**Note: we have added a root element surrounding the queries so that it would be valid XML, and thus allowed for its use with python XML functions in ElementTree**),  and specify the location to save the results. This system will run `Query.execute_query` on every query in the XML file and output the results to the specified location in the appropriate format for its use with the trec-eval script.

##Running the System
First, ensure you  have installed the NLTK dependencies and downloaded the NLTK data as follows in the Dependencies section.

From the command line, go to twitter_irs directory and run:
	python system.py

If you would like to re-run the creation of the indexes, in system.py change the following lines:

	system = System("data/trec-microblog11.txt", "index/frequency-index.txt", "index/tf-idf-index.txt", False)
	system.test_system("myRun", "data/topics_MB1-50.xml", "data/results.txt")

to:

	system = System("data/trec-microblog11.txt", "index/frequency-index-new.txt", "index/tf-idf-index-new.txt", True)
	system.test_system("myRun", "data/topics_MB1-50.xml", "data/results-new.txt")

The last boolean parameter in the system constructors specifies whether or not the system will load existing indexes or create new indexes (**Note: creating the indexes can take as long as 1 hour**).

###Evaluating the system

Place the results.txt file ine the same directory as the trec_eval script and run the following code ensuring the qrels file is existing there as well:

	./trec_eval Trec_microblog11-qrels.txt results.txt

**Our most recent results file exists at twitter_irs/data/results.txt**

##Notable Algorithms, Data Structures, and Optimizations
While there are tools available for Python Information Retrieval Systems such as Whoosh, we felt it would be a better experience to implement the indexing features from scratch using the methods and algorithms learned during class. In addition, given the nature of the data (Twitter messages), we felt that having more direct control of the index creation would allow more flexibility to handle some of the issues that arise in Twitter data (i.e. mispelled words, URLs, hashtags etc.)

During the preprocessing steps, we implemented a text processor to stem, remove stopwords, shorten contractions, and filter messages as we seemed fit. Creating this global text processor allowd for the method to be used on both messages and queries (to maintain a consistency, for example, in stemmed words matching). Within this processor, we were able to add modifications such as URL removers so that URLs would not be parsed strangely as tokens. We added the possibility of multiple sentences to this processor by first processing the message under the assumption that multiple sentences did exist. If not, it would continue to tokenize the text using a TreeBankWord tokenizer which uniquely split contractions into their primary form.

When creating token list, we used a Set data structure to ensure uniqueness in the tokens generated. When adding all the tokens from the processed messages to the Set, the characteristics of this data structure allowed for constant time, `O(1)`, checking of membership of the token, and would only add to the Set if the token did not already exist.

In addition, we also used a Set data structure for the stopword check. By placing the stopwords in a set, we were able to check if a word was a stopword in constant time using this key-based data structure.

When creating the indexes, we initially used lists containing associative arrays with ids and frequency or term weights, respectively. However, when searching the index, it was realized that the lists would have be traversed in order to find a matching ID. As an alternative, we decided to use associative arrays as the values for each token in the index. The associative arrays contained document ids as keys, and frequency or term-weights as their values. With this approach, we were able to check the associative array value of the token in constant time (by checking if there existed a key-value pair for the document id), instead of iterating through the list of associative arrays as before. We felt that this would increase performance of the retrieval/ranking process.

One late optimization that we performed pertained to the initial index creation. Instead of iterating over the tokens and searching through all documents for each token, we decided to search through the documents, and place the words in the document at their respective token. This process was significantly faster, `O(n)`, where n is the amount of tokens in the entire index. You can see this implementation in `create_frequency_index_optimized`. Conversely, the original algorithm ran in `O(m*n)` where m is the amount of tokens and n is the amount of words in the corpus since it had to traverse the corpus for every token that was generated (hence, taking 30-60 minutes). Interstingly enough, this resulted in slightly different evaluation results (See Results section), with a slightly lower MAP, a **higher** P@5 and a slightly lower P@10.

If you would like to see this optimized algorithm for index creation, please switch the comments in the following portion of system.py

            # Uncomment and run with create_index set to True if you would like to see the results using the
            # different, but faster optimized algorithm for indexing
            # self.frequency_index = self.indexer.create_frequency_index_optimized()
            self.frequency_index = self.indexer.create_frequency_index()

We decided to use the original, lengthier index creation because although it took significantly longer to create, it could be saved and produced better results for MAP and P@10.

For stemming, we used a Snowball based stemming algorithm which is often seen as an improvement over Porter algorithms due to its stricter restrictions and more aggressive stemming rules. After comparing stemming results from Porter, we felt it was best to use this Snowball based stemmer for our data.

The system that we developed ended up with **64166 unique tokens** from **45899 twitter messages**. It is our hope to extend this by reducing the amount of tokens by handling foreign characters more gracefully.

##Results
When running trec-eval, we received the following results for our system using our original algorithm for index creation:

| measure       | query | value  |
|---------------|-------|--------|
| num_q         | all   | 49     |
| num_ret       | all   | 41497  |
| num_rel       | all   | 2640   |
| num_rel_ret   | all   | 2237   |
| map           | all   | 0.2796 |
| gm_ap         | all   | 0.2162 |
| R-prec        | all   | 0.2979 |
| bpref         | all   | 0.3037 |
| recip_rank    | all   | 0.5863 |
| ircl_prn.0.00 | all   | 0.6894 |
| ircl_prn.0.10 | all   | 0.4862 |
| ircl_prn.0.20 | all   | 0.4480 |
| ircl_prn.0.30 | all   | 0.3990 |
| ircl_prn.0.40 | all   | 0.3759 |
| ircl_prn.0.50 | all   | 0.3187 |
| ircl_prn.0.60 | all   | 0.2392 |
| ircl_prn.0.70 | all   | 0.2046 |
| ircl_prn.0.80 | all   | 0.1571 |
| ircl_prn.0.90 | all   | 0.0914 |
| ircl_prn.1.00 | all   | 0.0261 |
| P5            | all   | 0.3796 |
| P10           | all   | 0.3347 |
| P15           | all   | 0.3279 |
| P20           | all   | 0.3102 |
| P30           | all   | 0.2871 |
| P100          | all   | 0.2049 |
| P200          | all   | 0.1418 |
| P500          | all   | 0.0799 |
| P1000         | all   | 0.0457 |

With a MAP of 0.2796, P@5 of 0.3796, and P@10 of 0.3347, we were pleased with the results of our information retrieval system (compared to 0.1785, 0.2667, and 0.3000 in the sample test from TREC). Through removing URLs and handling contracted words, we were able to cut down some of the tokens, but still noticed misspelled tokens. Had time permitted, we would have implemented a spell checking algorithm that would process the text and look for words that may have been mispelled or concatenated (i.e. in hashtags) and could be corrected to accurately match their respective token in the inverted index. Nonetheless, our system provided solid evaluation measures with the optimizations and tweaks made thus far. However, there is definitely room to grow and improve the text processing to provide even more accurate results after close examination of tokens.

As a side note, after running trec-eval with the index created from the faster indexing algorithm, we noted the slightest differences:

| measure       | query | value  |
|---------------|-------|--------|
| num_q         | all   | 49     |
| num_ret       | all   | 41497  |
| num_rel       | all   | 2640   |
| num_rel_ret   | all   | 2154   |
| map           | all   | 0.2768 |
| gm_ap         | all   | 0.2090 |
| R-prec        | all   | 0.2951 |
| bpref         | all   | 0.3099 |
| recip_rank    | all   | 0.5776 |
| ircl_prn.0.00 | all   | 0.6816 |
| ircl_prn.0.10 | all   | 0.5111 |
| ircl_prn.0.20 | all   | 0.4440 |
| ircl_prn.0.30 | all   | 0.3946 |
| ircl_prn.0.40 | all   | 0.3695 |
| ircl_prn.0.50 | all   | 0.3109 |
| ircl_prn.0.60 | all   | 0.2330 |
| ircl_prn.0.70 | all   | 0.1916 |
| ircl_prn.0.80 | all   | 0.1504 |
| ircl_prn.0.90 | all   | 0.0903 |
| ircl_prn.1.00 | all   | 0.0264 |
| P5            | all   | 0.3918 |
| P10           | all   | 0.3306 |
| P15           | all   | 0.3306 |
| P20           | all   | 0.3143 |
| P30           | all   | 0.2884 |
| P100          | all   | 0.2041 |
| P200          | all   | 0.1440 |
| P500          | all   | 0.0765 |
| P1000         | all   | 0.0440 |

###Interesting Issues
An interesting observations was noted when computing cosine similarity values between a query and documents with only one word (**e.g. Query 6: "NSA"**), due to the fact that only 1D vectors are used, every single matching document is given the same score of 1.0. Even if the term weight is heigher in one document, due to the 1 dimensional nature of the vector, the measure always results in 1.0. To compensate, it was proposed that a different similarity measure be used for 1 dimensional vectors that would additionally divide the measure by the maximum term frequency of that term in any document in the corpus.

###100 Example Tokens
Below is a list of sample tokens created from preprocessing. These were used as keys in the inverted index. Note that these tokens have been stemmed and filtered, with stopwords removed.

| Token            |
|------------------|
| mikayla          |
| uuuugh           |
| chicken          |
| kristaken        |
| dandruff         |
| automaat         |
| asterix          |
| birdi            |
| jfdulac          |
| seguimo          |
| lighter-than-air |
| suef             |
| earbud           |
| workin           |
| sagittarius      |
| toschack         |
| 1.38099          |
| dope             |
| toledo           |
| extreme-valu     |
| watercolor       |
| indopottermag    |
| theprogrambtr    |
| kebanyakan       |
| ghetto           |
| embriagu         |
| chemtrail        |
| win98            |
| ebm              |
| 039              |
| paulson          |
| gbbg             |
| radioshack       |
| saltillo         |
| abcenviron       |
| pre-speech       |
| yippi            |
| ebz              |
| closer           |
| entranc          |
| convers          |
| rikohn           |
| closet           |
| ieee             |
| opt-out          |
| mexicano         |
| superb           |
| xray             |
| genius           |
| ashleigh         |
| theta            |
| volturi_badass   |
| cola             |
| weluvsweet       |
| supers           |
| finallt          |
| nicole___x       |
| entic            |
| luisteren        |
| entir            |
| zour             |
| huth             |
| spoil            |
| gooooooooooo     |
| homebrew         |
| freezer          |
| anticat          |
| tiaayu01         |
| teaganthedog     |
| englot           |
| sagaward         |
| llegada          |
| conservationist  |
| egyptair         |
| tormenta         |
| juger            |
| multip           |
| blessed_amigo    |
| 3d-capabl        |
| bbm              |
| lawenforc        |
| sciencemag.org   |
| jugara           |
| heenim           |
| 43-babi          |
| bbc              |
| bbb              |
| bba              |
| morningsex       |
| bours            |
| j.henriqu        |
| 30k-60k-90k      |
| half-hour        |
| bbs              |
| picturesofthen   |
| slopstyl         |
| artisan          |
| treasur          |
| verizon          |
| everglad         |

###Sample Query Results
For Query 1, querying with the words "BBC World Service staff cuts", we returned the following messages:

1. BBC World Service to cut [...] a quarter of its staff - after losing millions in funding from the Foreign Office. http://bbc.in/hyGSHi
2. BBC World Service outlines cuts to staff http://bbc.in/f8hYAT
3. BBC News - BBC World Service cuts to be outlined to staff http://www.bbc.co.uk/news/entertainment-arts-12283356
4. A statement on the BBC World Service, ahead of staff briefings/ further details on Weds http://bbc.in/dFfXIW #bbcworldservice #bbccuts
5. Quarter of BBC world service staff to go, uk foreign office grant reduction of 17.5%.
6. RT @davelength: Anyway, while Twitter goes wild about Andy Gray, a quarter of the BBC World Service staff gets laid off and nobody notices.
7. BBC online cuts shows `contempt` for hard working staff says NUJ (The Drum) http://muk.fm/11zu #medianews
8. BBC World Service confirms cuts: TV News: Broadcaster to lose Macedonian, Albanian and Serbian programming -- Th... http://bit.ly/eusLgP
9. BBC World Service forecast to lose 30m listeners as cuts announced http://gu.com/p/2mkqh/tf
10. News Radio listeners? Save the BBC world service from savage cuts. http://bit.ly/eoGJeS


For Query 25, querying with the words "TSA airport screening", we returned the following messages:

1. TSA Shuts Down Private Airport Screen Program is headline now on www.fedsmith.com.
2. TSA Shuts Door on Private Airport Screening Program ��� Patriot Update http://patriotupdate.com/2451/tsa-shuts-door-on-private-airport-screening-program?sms_ss=twitter&at_xt=4d45868911137f91,0����� via @AddThis
3. TSA shuts door on private airport screening program. Utter BS! - http://bit.ly/fx6Dgw #cnn
4. TF - Travel RT @Bitter_American TSA shuts door on private airport screening program - http://bit.ly/fx6Dgw #cnn:... http://bit.ly/eADg2G
5. TSA shuts door on private airport screening program (CNN) http://feedzil.la/gD1tt6
6. TSA halts private screening program http://bit.ly/hUzJ3t
7. Atl Business Chronicle: TSA to test new screening at Hartsfield-Jackson http://brkg.at/hR3W3y
8. Obama makes fun of his own TSA screening procedures. Someone is off message! #sotu
9. Really looking forward to my TSA screening; haven`t gotten laid in a couple of weeks.
10. TSA to Test New Screening at Hartsfield-Jackson: The TSA in coming days at Hartsfield-Jackson Atlanta Internatio... http://bit.ly/e8NW0S

##Division of Work
1. Preprocessing - Shaughn
2. Indexing - Neil & Shaughn
3. Retrieval & Ranking - Shaughn
4. Results - Shaughn
5. Evaluation - Shaughn & Neil
