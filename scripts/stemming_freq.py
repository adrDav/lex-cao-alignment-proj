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
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer

def cal_freq():
    #suffix_list = ['ion','sion','er','ment','ant','ent','age','al','ence','ance','ery','ry','ship','ity','ness','cy','ive','ous','ful','less','able','ee', 'or','ly']
    nlp = stanza.Pipeline('en')
    chunk_size = 11000
    files = ['../test-sheets/SUBTLEX_USfrequency_above1_c1.csv']
    freq = pd.read_csv(files[0], nrows=chunk_size)
    porter = PorterStemmer()
    lancaster = LancasterStemmer()
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
        curr_word = (lancaster.stem(dicts[0][0]['text'])).lower()
        if curr_word.lower() not in dict_word:
            dict_word[curr_word] = curr_freq
        else: 
            dict_word[curr_word] += curr_freq

    for key in dict_word:
        new_row = []
        new_row.append(key)
        new_row.append(dict_word[key])
        csv_data.append(new_row)
    csv_file = pd.DataFrame(csv_data, columns=['Word', 'FREQcount'])
    csv_file.to_csv('SUBTLEX_USfrequency_above1_result.csv')

def main():
    cal_freq()

if __name__ == "__main__":
    main()