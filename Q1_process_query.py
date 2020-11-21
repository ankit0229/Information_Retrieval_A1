import string
import re
import pickle
import sys
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

Picklefile1 = open('inv_idx_file', 'rb')
dict_inverted_index = pickle.load(Picklefile1)

Picklefile2 = open('doc_ids', 'rb')
all_doc_ids = pickle.load(Picklefile2)

print("Enter the no. of words to be entered")
query_len = int(input())

query = []
operators = []
for i in range(query_len):
    query.append(input())

#Pre-processing the query
temp_query = []
for q in query:
    q = q.lower()
    q = re.sub(r'\d+', '', q)
    q = q.translate(q.maketrans('', '', string.punctuation))
    temp_query.append(q)
stop_words = set(stopwords.words("english"))
new_temp_query = [word for word in temp_query if word not in stop_words]
lemmas = [lemmatizer.lemmatize(word) for word in new_temp_query]
query = lemmas

print(f"The query tokens after preprocessing are:  {query}")
print("Enter the operators : 1 for AND , 2 for OR, 3 for NOT and 0 end")

a = int(input())

while a != 0:
    operators.append(a)
    a = int(input())

ch_and = 0
for ab in operators:
    if ab == 1:
        ch_and = 1
    else:
        ch_and = 0
        break

ch_or = 0
for ab in operators:
    if ab == 2:
        ch_or = 1
    else:
        ch_or = 0
        break

ch_an_not = 0
if len(operators) % 2 == 1:
    ch_an_not = 0
else:
    for axy in range(0,len(operators)-1,2):
        if operators[axy] == 1 and operators[axy + 1] == 3:
            ch_an_not = 1
        else:
            ch_an_not = 0
            break

ch_or_not = 0
if len(operators) % 2 == 1:
    ch_or_not = 0
else:
    for axy in range(0,len(operators)-1,2):
        if operators[axy] == 2 and operators[axy + 1] == 3:
            ch_or_not = 1
        else:
            ch_or_not = 0
            break

def and_not(lst1, lst2):
    ret_val = []
    n_cmp = 0
    temp_out = []
    u, v = 0, 0
    while u < len(lst1) and v < len(lst2):
        if lst1[u] == lst2[v]:
            u += 1
            v += 1
            n_cmp += 1
        elif lst1[u] < lst2[v]:
            temp_out.append(lst1[u])
            u += 1
            n_cmp += 2
        else:
            v += 1
            n_cmp += 2

    if u != len(lst1):
        for i in range(u, len(lst1)):
            temp_out.append(lst1[i])

    ret_val.append(n_cmp)
    ret_val.append(temp_out)
    return ret_val


def or_op(lst1, lst2):
    ret_val = []
    n_cmp = 0
    temp_result1 = lst1
    temp_out = []
    u, v = 0, 0
    while u < len(temp_result1) and v < len(lst2):
        if temp_result1[u] == lst2[v]:
            temp_out.append(temp_result1[u])
            u += 1
            v += 1
            n_cmp += 1
        elif temp_result1[u] < lst2[v]:
            temp_out.append(temp_result1[u])
            u += 1
            n_cmp += 2
        else:
            temp_out.append(lst2[v])
            v += 1
            n_cmp += 2
    if u == len(temp_result1):
        for i in range(v, len(lst2)):
            temp_out.append(lst2[i])
    elif v == len(lst2):
        for i in range(u, len(temp_result1)):
            temp_out.append(temp_result1[i])
    ret_val.append(n_cmp)
    ret_val.append(temp_out)
    return ret_val


def and_op(lst1, lst2):
    ret_val = []
    n_cmp = 0
    temp_result1 = lst1
    temp_out = []
    u, v = 0, 0
    while u < len(temp_result1) and v < len(lst2):
        if temp_result1[u] == lst2[v]:
            temp_out.append(temp_result1[u])
            u += 1
            v += 1
            n_cmp += 1
        elif temp_result1[u] < lst2[v]:
            u += 1
            n_cmp += 2
        else:
            v += 1
            n_cmp += 2
    ret_val.append(n_cmp)
    ret_val.append(temp_out)
    return ret_val


if ch_and == 1:
    list_query = []
    temp_out = []
    no_cmp = 0
    for q in query:
        temp = []
        temp.append(q)
        a = dict_inverted_index.get(q)
        if a is None:
            print("The no. of docs retrieved is 0 and no. of comparisons is 0")
            sys.exit(0)
        temp.append(a[1])
        list_query.append(temp)
    list_query.sort(key=lambda x: x[1])
    pslt1 = dict_inverted_index.get(list_query[0][0])
    pslt1 = pslt1[0]
    len_list_query = len(list_query)
    for j in range(1, len_list_query):
        pslt2 = dict_inverted_index.get(list_query[j][0])
        pslt2 = pslt2[0]
        temp_out = and_op(pslt1, pslt2)
        no_cmp = no_cmp + temp_out[0]
        pslt1 = temp_out[1]
        if len(temp_out[1]) == 0:
            print(f"The no. of docs retrieved is 0 and no. of comparisons is {no_cmp}")
            sys.exit(0)

    print(f"The no. of comparisons done is {no_cmp}")
    print(f"The no. of docs retrieved is : {len(pslt1)}")
    print("The list of doc ids is:")
    for nn in pslt1:
        print(nn)

elif ch_or == 1:
    pslt1 = dict_inverted_index.get(query[0])
    if pslt1 == None:
        pslt1 = []
    else:
        pslt1 = pslt1[0]
    no_cmp = 0
    temp_out = pslt1

    for i in range(1,len(query)):
        pslt2 = dict_inverted_index.get(query[i])
        if pslt2 == None:
            pslt2 = []
        pslt2 = pslt2[0]
        temp_out = or_op(pslt1, pslt2)
        no_cmp = no_cmp + temp_out[0]
        pslt1 = temp_out[1]

    print(f"The no. of docs retrieved is {len(pslt1)}")
    print(f"The no. of comparisons is {no_cmp}")
    for nn in pslt1:
        print(nn)

elif ch_an_not == 1:
    pslt1 = dict_inverted_index.get(query[0])
    if pslt1 is None:
        print("The no. of docs retrieved is 0 and no. of comparisons is 0")
        sys.exit(0)
    pslt1 = pslt1[0]
    no_cmp = 0
    temp_out = pslt1
    for i in range(1,len(query)):
        pslt2 = dict_inverted_index.get(query[i])
        if pslt2 is None:
            pslt2 = []
        else:
            pslt2 = pslt2[0]
        temp_out = and_not(pslt1, pslt2)
        no_cmp = no_cmp + temp_out[0]
        pslt1 = temp_out[1]

    print(f"The no. of docs retrieved is {len(pslt1)}")
    print(f"The no. of comparisons is {no_cmp}")
    for nn in pslt1:
        print(nn)

elif ch_or_not == 1:
    pslt1 = dict_inverted_index.get(query[0])
    if pslt1 is None:
        pslt1 = []
    else:
        pslt1 = pslt1[0]
    no_cmp = 0
    temp_out = pslt1
    for i in range(1,len(query)):
        temp_l2 = dict_inverted_index.get(query[i])
        if temp_l2 is None:
            temp_l2 = []
        else:
            temp_l2 = temp_l2[0]
        pslt2 = list(set(all_doc_ids) - set(temp_l2))
        temp_out = or_op(pslt1, pslt2)
        no_cmp = no_cmp + temp_out[0]
        pslt1 = temp_out[1]

    print(f"The no. of docs retrieved is {len(pslt1)}")
    print(f"The no. of comparisons is {no_cmp}")
    for nn in pslt1:
        print(nn)

#Handling the case of mixed operators
else:
    no_cmp = 0
    mod_op = []
    #Preparing the modified list of operators
    for i in range(len(operators)):
        if i != len(operators) - 1:
            if operators[i + 1] == 3:
                new_op = (operators[i] * 10) + 3
                mod_op.append(new_op)
                i = i + 1
            elif operators[i] != 3:
                mod_op.append(operators[i])
        elif i == len(operators) - 1:
            if operators[i] != 3:
                mod_op.append(operators[i])
    qry_postings = []
    #Preparing a list which contains doc ids list as well as the operators
    m = 0
    for i in range(len(query)):
        x = dict_inverted_index.get(query[i])
        if x is None:
            x = [[], 0]
        qry_postings.append(x[0])
        if m < len(mod_op):
            qry_postings.append(mod_op[m])
            m += 1

    k = 0
    while k < len(qry_postings):
        if qry_postings[k] == 13:
            temp_list_new = []
            pslt1 = qry_postings[k - 1]
            pslt2 = qry_postings[k + 1]
            temp_out = and_not(pslt1, pslt2)
            no_cmp = no_cmp + temp_out[0]
            for ww in range(k - 1):
                temp_list_new.append(qry_postings[ww])
            temp_list_new.append(temp_out[1])
            for ww in range(k + 2, len(qry_postings)):
                temp_list_new.append(qry_postings[ww])
            qry_postings = temp_list_new
        else:
            k = k + 1

    k = 0
    while k < len(qry_postings):
        if qry_postings[k] == 23:
            temp_list_new = []
            pslt1 = qry_postings[k - 1]
            pslt2 = qry_postings[k + 1]
            t2 = list(set(all_doc_ids) - set(pslt2))
            pslt2 = t2
            temp_out = or_op(pslt1, pslt2)
            no_cmp = no_cmp + temp_out[0]
            for ww in range(k - 1):
                temp_list_new.append(qry_postings[ww])
            temp_list_new.append(temp_out[1])
            for ww in range(k + 2, len(qry_postings)):
                temp_list_new.append(qry_postings[ww])
            qry_postings = temp_list_new
        else:
            k = k + 1

    k = 0
    while k < len(qry_postings):
        if qry_postings[k] == 1:
            temp_list_new = []
            pslt1 = qry_postings[k - 1]
            pslt2 = qry_postings[k + 1]
            temp_out = and_op(pslt1, pslt2)
            no_cmp = no_cmp + temp_out[0]
            for ww in range(k - 1):
                temp_list_new.append(qry_postings[ww])
            temp_list_new.append(temp_out[1])
            for ww in range(k + 2, len(qry_postings)):
                temp_list_new.append(qry_postings[ww])
            qry_postings = temp_list_new
        else:
            k = k + 1

    k = 0
    while k < len(qry_postings):
        if qry_postings[k] == 2:
            temp_list_new = []
            pslt1 = qry_postings[k-1]
            pslt2 = qry_postings[k+1]
            temp_out = or_op(pslt1, pslt2)
            no_cmp = no_cmp + temp_out[0]
            for ww in range(k-1):
                temp_list_new.append(qry_postings[ww])
            temp_list_new.append(temp_out[1])
            for ww in range(k+2, len(qry_postings)):
                temp_list_new.append(qry_postings[ww])
            qry_postings = temp_list_new
        else:
            k = k + 1

    print(f"The no. of comparisons done is {no_cmp}")
    print(f"The no. of docs retrieved is : {len(qry_postings[0])}")
    print("The list of doc ids is:")
    for mm in qry_postings[0]:
        print(mm)