import string
import re
import os
import pickle
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter

files = []
words_list1 = []
directory = r'D:\M.TECH SEM 2\IR\Assignments\A1\Assign1_Q2_data\\'
for entry in os.listdir(directory):
    if os.path.isdir(os.path.join(directory, entry)):
        files.append(entry)

docs = []
directory = r'D:\M.TECH SEM 2\IR\Assignments\A1\Assign1_Q2_data\\'

mstr_dict = {}
mstr_dict_dict = {}
dict_indiv_inv_idx = {}
dict_use_pos = {}
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
        wd_lst_doc = word_tokens
        doc_location = os.path.join(fol, doc)
        dict_use_pos[doc_location] = wd_lst_doc
        dict_doc = Counter(wd_lst_doc)
        unq_wrds = []
        for k in dict_doc:
            unq_wrds.append(k)
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

#Start making positional index

dict_pos_idx = {}
for k in dict_inverted_index:
    k_doc_ids = dict_inverted_index[k]
    k_doc_ids = k_doc_ids[0]
    dict_k = {}
    for did in k_doc_ids:
        unq_wrds_did = dict_use_pos[did]
        pos_lst = [m for m, wrd in enumerate(unq_wrds_did) if wrd == k]
        dict_k[did] = pos_lst

    dict_pos_idx[k] = dict_k

Picklefile3 = open('pos_idx', 'wb')
pickle.dump(dict_pos_idx, Picklefile3)
Picklefile3.close()
print("Pickle has been created")