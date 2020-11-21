import string
import re
import pickle
import sys
from nltk.tokenize import sent_tokenize, word_tokenize

Picklefile3 = open('pos_idx', 'rb')
dict_pos_idx = pickle.load(Picklefile3)

print("Enter the phrase:")
query = input()
query = query.lower()
query = re.sub(r'\S+@\S+', '', query)
query = re.sub(r'\d+', '', query)
query = query.translate(query.maketrans('', '', string.punctuation))
query_token = word_tokenize(query)

print(f"After pre-processing the query is {query_token}")

def and_op(lst1, lst2):
    temp_result1 = lst1
    temp_out = []
    u, v = 0, 0
    while u < len(temp_result1) and v < len(lst2):
        if temp_result1[u] == lst2[v]:
            temp_out.append(temp_result1[u])
            u += 1
            v += 1
        elif temp_result1[u] < lst2[v]:
            u += 1
        else:
            v += 1
    return temp_out

wrd1 = query_token[0]
temp_res = dict_pos_idx.get(wrd1)
if temp_res is None:
    print("The phrase is not present in any of the documents")
    sys.exit(0)

for i in range(1, len(query_token)):
    docs_lst1 = []
    for k in temp_res:
        docs_lst1.append(k)
    wrd2 = query_token[i]
    dict_term2 = dict_pos_idx.get(wrd2)
    if dict_term2 is None:
        print("The phrase is not present in any of the documents")
        sys.exit(0)
    docs_lst2 = []
    for j in dict_term2:
        docs_lst2.append(j)
    docs_lst1.sort()
    docs_lst2.sort()
    intersect_docs = and_op(docs_lst1, docs_lst2)
    if len(intersect_docs) == 0:
        print("The phrase is not present in any of the documents")
        sys.exit(0)

    list_diff_1 = []
    dict_intersect_cond = {}
    sub_dict_word2 = dict_pos_idx[wrd2]

    for m in intersect_docs:
        list_word1 = temp_res[m]
        list_word2 = sub_dict_word2[m]
        p, q = 0, 0
        list_word1.sort()
        list_word2.sort()

        while p < len(list_word1) and q < len(list_word2):
            if list_word2[q] - list_word1[p] == 1:
                if dict_intersect_cond.get(m) is None:
                    dict_intersect_cond[m] = []
                    dict_intersect_cond[m].append(list_word2[q])
                else:
                    dict_intersect_cond[m].append(list_word2[q])
                p += 1
                q += 1
            elif list_word1[p] < list_word2[q]:
                p += 1
            else:
                q += 1

    check_empty = not dict_intersect_cond
    if check_empty:
        print("The phrase is not present in any of the documents")
        sys.exit(0)
    temp_res = dict_intersect_cond

no_matches = len(temp_res)
print(f"The no. of documents where phrase found is {no_matches}")
print("The list of documents where phrase found is :")
for yy in temp_res:
    print(yy)