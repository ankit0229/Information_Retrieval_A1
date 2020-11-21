import string
import re
import os
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter

lemmatizer = WordNetLemmatizer()
files = []
words_list1 = []
directory = r'D:\M.TECH SEM 2\IR\Assignments\A1\20_newsgroups\\'
for entry in os.listdir(directory):
    if os.path.isdir(os.path.join(directory, entry)):
        files.append(entry)

docs = []
directory = r'D:\M.TECH SEM 2\IR\Assignments\A1\20_newsgroups\\'

mstr_dict = {}
mstr_dict_dict = {}
dict_indiv_inv_idx = {}
ctr = 1
all_doc_ids = []

for fol in files:
    temp_dir = os.path.join(directory, fol)
    docs = []
    complete_doc_loc = []
    mstr_dict = {}
    mstr_dict_dict = {}
    for entry in os.listdir(temp_dir):
        if os.path.isfile(os.path.join(temp_dir, entry)):
            docs.append(entry)
            doc_loc = os.path.join(fol, entry)
            complete_doc_loc.append(doc_loc)

    all_doc_ids.extend(complete_doc_loc)
    for doc in docs:
        full_path = os.path.join(temp_dir, doc)
        fp = open(full_path, "r")
        text = fp.read()
        fp.close()
        ll = text.split("\n\n")
        del ll[0]
        text = "\n\n".join(ll)
        text = text.lower()
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'\d+', '', text)
        text = text.translate(text.maketrans('', '', string.punctuation))
        word_tokens = word_tokenize(text)
        stop_words = set(stopwords.words("english"))
        text = [word for word in word_tokens if word not in stop_words]
        lemmas = [lemmatizer.lemmatize(word) for word in text]
        wd_lst_doc = lemmas
        dict_doc = Counter(wd_lst_doc)
        unq_wrds = []
        for k in dict_doc:
            unq_wrds.append(k)
        doc_location = os.path.join(fol, doc)
        mstr_dict[doc_location] = unq_wrds
        mstr_dict_dict[doc_location] = dict_doc

    dict_inv_idx = {}
    for doc_num in mstr_dict_dict:
        for tkn in mstr_dict_dict[doc_num]:
            if dict_inv_idx.get(tkn) is None:
                tmp_lst = []
                tmp_lst.append(doc_num)
                dict_inv_idx[tkn] = tmp_lst
            else:
                dict_inv_idx[tkn].append(doc_num)

    dict_indiv_inv_idx[ctr] = dict_inv_idx
    ctr = ctr + 1

dict_inverted_index = {}
for c in dict_indiv_inv_idx:
    fldr_dict = dict_indiv_inv_idx[c]
    for k in fldr_dict:
        val_list = fldr_dict[k]
        if dict_inverted_index.get(k) is None:
            dict_inverted_index[k] = []
            dict_inverted_index[k].append(val_list)
        else:
            dict_inverted_index[k][0].extend(val_list)

for k in dict_inverted_index:
    dict_inverted_index[k][0].sort()
    len_posting = len(dict_inverted_index[k][0])
    dict_inverted_index[k].append(len_posting)

Picklefile1 = open('inv_idx_file', 'wb')
pickle.dump(dict_inverted_index, Picklefile1)
Picklefile1.close()

Picklefile2 = open('doc_ids', 'wb')
pickle.dump(all_doc_ids, Picklefile2)
Picklefile2.close()

print("Pickle done")