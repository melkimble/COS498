'''
    Title: FINAL PROJECT
    Name: Melissa Kimble
    Date: 2018-05-06
    Description: Final Project for COS498 - AI for Art & Design. Developed using scikit-learn Naive Bayes
    Multinomial Classifier and Google's pretrained word2vecl model to predict sentiment and place of Maine
    Standard Aquaculture Leases.

    Copyright (C) <2018>  <Melissa Kimble>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    The following libraries are needed to run this code, I recommend installing miniconda:
    Python 3.6 64-bit
    conda create -n filename python=3
    conda activate filename
    conda install numpy
    conda install scipy
    conda install scikit-learn
    conda install -c conda-forge pdfminer.six
    conda install pandas
    conda install matplotlib
    conda install -c conda-forge proj4
    conda install -c conda-forge basemap=1.0.8.dev0
    conda install -c conda-forge basemap-data-hires
    conda install pillow
    conda install gensim
'''

import extr_pdf
import train2test_naivebayes as nb
import sentiment_word2vec as sw2v
import generate_basemap as gb
import numpy as np
import pandas as pd

testDataFolder="D:/Dropbox/01_School/18SP/COS498/FinalProject/TestingData/"
trainDataFile="D:/Dropbox/01_School/18SP/COS498/FinalProject/TrainingData/train.csv"

'''
Section for generating sentiment words based on the pretrained google news model
https://datawarrior.wordpress.com/2015/10/25/codienerd-2-toying-with-word2vec/
'''

def model2SentWords(modelfile,poswordset,negwordset, **kwargs):
    if kwargs:
        subject = kwargs['subject']
        model2Words_output=sw2v.model2Words(modelfile,poswordset, negwordset, 25,subject)
    else:
        model2Words_output=sw2v.model2Words(modelfile,poswordset, negwordset, 25)

    pos_output=model2Words_output[0]
    neg_output=model2Words_output[1]
    # grab first element in each tuple from pos_output and neg_output
    pos_train = [x[0] for x in pos_output]
    neg_train = [x[0] for x in neg_output]
    return(pos_train,neg_train)

# these words didn't really produce a great result.
#poswordset=['positive','good','productive','beneficial','economically_viable',
#            'bioremediation','sustainable','boom','filter','clean','profitable']
#negwordset=['negative','bad','destructive','noisy','eyesore','pollution','algae_bloom',
#            'foulness','unsustainable']

modelfile='D:/Dropbox/01_School/18SP/COS498/FinalProject/TrainingData/GoogleNews-vectors-negative300.bin'
poswordset=['positive','good']
negwordset=['negative','bad']
# subject is optional, it does not have to be included in the model2Words
#subject=['oysters','bivalves','aquaculture','Maine']
#sent_words=model2SentWords(modelfile,poswordset,negwordset, subject=subject)
sent_words=model2SentWords(modelfile,poswordset,negwordset)
pos_train=sent_words[0]
neg_train=sent_words[1]

print(pos_train)
print(neg_train)
'''
Section for predicting site# with a multinomial naive bayes classifier 
https://www.dataquest.io/blog/naive-bayes-tutorial/
http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
'''
def traintestNB(testDataFolder, iscsv, **kwargs):
    prdct = []
    # array of pdfs converted to text
    pdfs2Array_output = extr_pdf.pdfs2Array(testDataFolder)
    parsed_pdfs = pdfs2Array_output[0]
    fname = pdfs2Array_output[1]
    if (iscsv==True):
        # place from CSV
        trainDataFile=kwargs['trainDataFile']
        train=nb.trainCSV2Train(trainDataFile)
        predicted=nb.train2TestMNB(train, parsed_pdfs)
    else:
        # sentiment from arrays
        pos_train=kwargs['pos_train']
        neg_train=kwargs['neg_train']
        train=sw2v.trainDF2Train(pos_train,neg_train)
        predicted=nb.train2TestMNB(train,parsed_pdfs)

    for doc, category in zip(parsed_pdfs, predicted):
        print('%r => \n %s' % (doc, train.target_names[category]))
        prdct.append(train.target_names[category])

    return(prdct, fname)

prdct_place_output=traintestNB(testDataFolder, iscsv=True, trainDataFile=trainDataFile)
prdct_sent_output=traintestNB(testDataFolder, iscsv=False,pos_train=pos_train,neg_train=neg_train)

# only need to grab fname once, since they're both referencing the same files.
fname=prdct_place_output[1]
prdct_place=prdct_place_output[0]
prdct_sent=prdct_sent_output[0]
'''

Section to setup and merge the results with the training data. Adds latitude and longitude columns 
based on predicted results.
'''
def mergeResults(fname,prdct_place,prdct_sent,trainDataFile):
    # create empty dataframe with columns file and predictedSite
    results = pd.DataFrame(columns=['file', 'predictedSite','predictedSent'])
    # column 'file' in results - add fname list
    results['file'] = fname
    # add predicted site and sentiment to array
    results['predictedSite'] = prdct_place
    results['predictedSent'] = prdct_sent
    #print(prdct_sent)
    # replace fields that = 'TargetNames' with 'NA' because these fields
    # did not have a predicted site/sentiment associated with them.
    results.predictedSite.replace(['TargetNames'], ['NA'], inplace=True)
    results.predictedSent.replace(['TargetNames'], ['NA'], inplace=True)

    # read train file in as a pandas dataframe
    trainDF = pd.read_csv(trainDataFile, encoding='ISO-8859-1', usecols=[0, 3, 4],
                          header=0, index_col=False, names=['predictedSite', 'Lat', 'Lon'])
    # merge the train file with predictions based on the SITE#.
    merged_result = pd.merge(trainDF, results, on='predictedSite', how='inner')
    return(merged_result)

merged_result=mergeResults(fname,prdct_place,prdct_sent,trainDataFile)
#print(merged_result)

'''
Section for generating labeled maps from pdf site predictions
https://stackoverflow.com/questions/35716830/basemap-with-python-3-5-anaconda-on-windows
http://www.datadependence.com/2016/06/creating-map-visualisations-in-python/
'''
def resultsToMap(merged_result):
    lats = np.asarray(merged_result['Lat'])
    lons = np.asarray(merged_result['Lon'])
    labels = np.asarray(merged_result['predictedSite'])
    cols=np.asarray(merged_result['predictedSent'])
    gb.array2Map(lats,lons,labels,cols)

resultsToMap(merged_result)