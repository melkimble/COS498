'''
Section for generating sentiment words based on the pretrained google news model
https://datawarrior.wordpress.com/2015/10/25/codienerd-2-toying-with-word2vec/
'''
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim.models.keyedvectors as word2vec
import pandas as pd
import sklearn.datasets
import numpy as np

def trainDF2Train(pos_train, neg_train):
    # function takes negative and positive sentiment lists and converts them to a
    # bunch scikit-learn datatype.
    train_sent_pos = pd.DataFrame(columns=['Data', 'TargetName'])
    train_sent_neg = pd.DataFrame(columns=['Data', 'TargetName'])
    train_sent_pos['Data'] = pos_train
    train_sent_pos['TargetName'] = 'Positive'
    train_sent_neg['Data']= neg_train
    train_sent_neg['TargetName'] = 'Negative'

    # append one dataframe onto the other and reset the index to be 0:EndRows
    train_sent = pd.concat([train_sent_pos, train_sent_neg],ignore_index=True)
    #print(train_sent)

    # create 'target' column, this is what is used for training - i.e., if you have 2 categories, you should only have
    # 1 or 2 for each category a row is associated with.
    # 'target_names' is for labeling and reference, not for training.
    # since this dataset has 2 categories (negative/positive), a np.zeros array is created and
    # filled with the category# (target) based on the length of pos and neg lists.
    totlen=len(train_sent.index)
    first_col_len_pos = len(train_sent_pos.index)
    first_col_len_neg = len(train_sent_neg.index)
    pos_sequence = range(0, first_col_len_pos)
    neg_sequence = range(first_col_len_pos, first_col_len_pos+first_col_len_neg)
    target = np.zeros((totlen,), dtype=np.int64)
    for r in pos_sequence:
        target[r] = 1
    for i in neg_sequence:
        target[i] = 2
    train = sklearn.datasets.base.Bunch(data=train_sent['Data'], target=target,
                                        target_names=train_sent['TargetName'])
    #print(train)
    return(train)

def model2Words(modelfile,poswordset, negwordset, numwords, *args):
    # function to generate words based on the pretrained google news 3.5gig model
    print('starting sentiment...')
    ## we want both the negative and positive word sets to be positively correlated to the subject,
    ## so the following lines concatenate the lists. Subject is optional, so if it has not been
    ## passed in as an argument, then it is ignored.
    if args:
        poswordset_subj=poswordset + args[0]
        negwordset_subj=negwordset + args[0]
    else:
        poswordset_subj=poswordset
        negwordset_subj=negwordset
    # produces two lists of words that are positively correlated with negative or positive sentiment.
    model = word2vec.KeyedVectors.load_word2vec_format(modelfile, binary=True)
    poswords=model.most_similar(positive=poswordset_subj, negative=negwordset, topn=numwords)
    negwords=model.most_similar(positive=negwordset_subj, negative=poswordset, topn=numwords)
    return(poswords,negwords)