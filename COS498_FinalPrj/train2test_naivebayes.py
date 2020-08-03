'''
Section for predicting site# with a multinomial naive bayes classifier
https://www.dataquest.io/blog/naive-bayes-tutorial/
http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
'''

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import sklearn.datasets
import csv
import numpy as np

def trainCSV2Train(trainDataFile):
    # function to setup the trainCSV as a scikit-learn bunch datatype
    # Read in the training data.
    with open(trainDataFile, 'r') as file:
        trainCSV = list(csv.reader(file))

    # create 'target' column, this is what is used for training - i.e., if you have more than 2 categories,
    # then you should have a number <1 for each category a row is associated with.
    # 'target_names' is for labeling and reference, not for training.
    first_col_len=len([r[0] for r in trainCSV])
    sequence = range(1, first_col_len)
    target = np.zeros((first_col_len,), dtype=np.int64)
    for r in sequence:
        target[r] = r
    # convert trainCSV to a scikit-learn bunch datatype. The r[0] column has SITE#, r[2] has the words for prediction,
    # and target was created based on the number of rows in trainCSV.
    train = sklearn.datasets.base.Bunch(data=[r[2] for r in trainCSV], target=target,
                                        target_names=[r[0] for r in trainCSV])
    # close train csv file
    file.close()
    return(train)

def train2TestMNB(train, parsed_pdfs):
    # Generate counts from text using a vectorizer. There are other vectorizers available, and lots of options you can set.
    # This performs our step of computing word counts. Text preprocessing, tokenizing and filtering of stopwords are
    # included in a high level component that is able to build a dictionary of features and transform documents to feature
    # vectors
    count_vect = CountVectorizer(stop_words='english')
    X_train_counts = count_vect.fit_transform(train.data)

    # CountVectorizer supports counts of N-grams of words or consecutive characters. Once fitted,
    # the vectorizer has built a dictionary of feature indices. The index value of a word in the vocabulary is linked to
    # its frequency in the whole training corpus.
    count_vect.vocabulary_.get(u'algorithm')

    # Occurrence count is a good start but there is an issue - longer documents will have higher average count values than
    # shorter documents, even though they might talk about the same topics.
    # To avoid these potential discrepancies it suffices to divide the number of occurrences of each word in a document
    # by the total number of words in the document - these new features are called 'tf' for Term Frequencies.
    # Another refinement on top of tf is to downscale weights for words that occur in many documents in the corpus and are
    # therefore less informative than those that occur only in a smaller portion of the corpus.
    # this downscaling is called tf-idf for "Term Frequency times Inverse Document Frequency".
    #  i.e., removing bias from the size of documents, which is essentially reducing frequencies to 1. Same as
    # f(x)/x raw transform from MaxEnt.
    tfidf_transformer = TfidfTransformer()
    # fit() method to fit the estimator to the data, transform() method to transform the count-matrix to a tf-idf
    # (Term Frequency times Inverse Document Frequency) representation. They are combined in fit_transform.
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    X_train_tfidf.shape

    # training a classifier to try to predict each site category. MultinomialNB is a naive Bayes classifier, which is
    # most suitable for word counts.
    clf = MultinomialNB().fit(X_train_tfidf, train.target)

    # Predict the outcome for each parsed pdf by extracting the features from the pdfs based on the same process
    # used to parse the training file. Calling transform rather than fit_transform because fit_transform was used to
    # fit the training set and is unnecessary for the test dataset.
    X_new_counts = count_vect.transform(parsed_pdfs)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    # predict site based on combination of words for each site
    predicted = clf.predict(X_new_tfidf)
    return(predicted)
