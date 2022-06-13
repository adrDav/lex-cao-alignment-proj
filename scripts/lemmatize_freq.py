# ----------------------------------------------------
# obtain lemma frequency of the words.
# author: Adrian Avendano.
# e-mail: adavendanon@miners.utep.edu
# ----------------------------------------------------
from tempfile import tempdir
from numpy import append
import pandas as pd
from pkg_resources import to_filename
import stanza

def cal_freq():
    #suffix_list = ['ion','sion','er','ment','ant','ent','age','al','ence','ance','ery','ry','ship','ity','ness','cy','ive','ous','ful','less','able','ee', 'or','ly']
    nlp = stanza.Pipeline('en')
    chunk_size = 11000
    files = ['test.csv','SUBTLEX_USfrequency_above1_c1.csv', 'SUBTLEX_USfrequency_above1_2.csv']
    freq = pd.read_csv(files[1], nrows=chunk_size)
    print(freq)
    lst_freq = freq.values.tolist()

    csv_data = []
    dict_word = {}
    sub_info = [0,0,0]
    output_count = 0

    for row in range(len(lst_freq)):
        if output_count % 100 == 0:
            print(output_count)
        output_count += 1

        # convert all uppercase into lowercase string
        lst_freq[row][0] = lst_freq[row][0].lower()
        # word for current row
        doc = nlp(lst_freq[row][0])
        # frequency for current row
        curr_freq = lst_freq[row][1]

        dicts = doc.to_dict()
        curr_word = dicts[0][0]['lemma']
        keys = list(dict_word.keys())
        
        # to-do: get rid of the entry in keys
        for i in range(len(keys)):
            sub_info = obtain_substring(curr_word.lower(), keys[i].lower())

        if(sub_info[1] == True):
            curr_freq += dict_word[sub_info[2]] 
            # getting rid of entry
            del dict_word[sub_info[2]]
            curr_word = sub_info[0]

        if curr_word.lower() not in dict_word:
            dict_word[curr_word.lower()] = curr_freq
        else: 
            dict_word[curr_word.lower()] += curr_freq
    
    for key in dict_word:
        new_row = []
        new_row.append(key)
        new_row.append(dict_word[key])
        csv_data.append(new_row)
    csv_file = pd.DataFrame(csv_data, columns=['Word', 'FREQcount'])
    csv_file.to_csv('SUBTLEX_USfrequency_above1_result.csv')

# function determines if str1 is a substring of str2
# input: string, string
# output: string
def obtain_substring(str1, str2):
    # storing the original str1 and str2
    og_string = str1
    key = str2

    # determine which string is the longest
    if len(str1) > len(str2):
        temp = str2
        str2 = str1
        str1 = temp
    # if first character does not match return false
    if str1[0] != str2[0]:
        return og_string, False, key
    # if the string is longer than 3 perform the comparison
    if len(str1) > 3:
        for i in range(len(str1)):
            if str1[i] != str2[i]:
                return og_string, False, key
        return str1, True, key
    # else do not perform the comparison
    else:
        return [0,0,0]

def obtain_eng_spelling(str1, str2):
    # storing the original str1 and str2
    og_string = (str1 + '.')[:-1]
    key = (str2 + '.')[:-1]

    # determine which string is the longest
    if len(str1) > len(str2):
        temp = str2
        str2 = str1
        str1 = temp
    # if first character does not match return false
    if str1[0] != str2[0]:
        return og_string, False, key
    # if the string is longer than 3 perform the comparison
    if len(str1) > 3:
        counter = 0
        for i in range(len(str1)):
            if str1[i] != str2[i] and counter > 1:
                return og_string, False, key
            if  str1[i] != str2[i] and len(str1) < len(str2):
                counter += 1
                str2 = str2[:i] + str2[i+1:]
        return og_string, True, key
    # else do not perform the comparison
    else:
        return [0,0,0]
        

def main():
    cal_freq()

if __name__ == "__main__":
    main()