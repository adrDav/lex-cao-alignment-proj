# ----------------------------------------------------
# code implemented to tag words
# author: Adrian Avendano; adavendanon@miners.utep.edu
# ----------------------------------------------------
import glob
from itertools import count
import re
import pandas as pd
import stanza 
#import nltk
import json
#from nltk.corpus import words
#from nltk.tokenize import word_tokenize
#from nltk import *
from stanza.utils.conll import CoNLL
a_c = pd.read_csv('../SUBTLEX/result-sheets/lemmatizing/SUBTLEX_USfrequency_above1_result.csv')
c_g = pd.read_csv('../SUBTLEX/result-sheets/lemmatizing/SUBTLEX_USfrequency_above2_result.csv')
g_m = pd.read_csv('../SUBTLEX/result-sheets/lemmatizing/SUBTLEX_USfrequency_above3_result.csv')
m_r = pd.read_csv('../SUBTLEX/result-sheets/lemmatizing/SUBTLEX_USfrequency_above4_result.csv')
r_t = pd.read_csv('../SUBTLEX/result-sheets/lemmatizing/SUBTLEX_USfrequency_above5_result.csv')
t_z = pd.read_csv('../SUBTLEX/result-sheets/lemmatizing/SUBTLEX_USfrequency_above6_result.csv')

a_c = a_c.set_index(a_c['Word']).agg(list, axis=1).to_dict()
c_g = c_g.set_index(c_g['Word']).agg(list, axis=1).to_dict()
g_m = g_m.set_index(g_m['Word']).agg(list, axis=1).to_dict()
m_r = m_r.set_index(m_r['Word']).agg(list, axis=1).to_dict()
r_t = r_t.set_index(r_t['Word']).agg(list, axis=1).to_dict()
t_z = t_z.set_index(t_z['Word']).agg(list, axis=1).to_dict()

def extract_subtlex(token_word):
    freq_count = -1

    ascii = ord(token_word[0])

    if ascii >= 97 and ascii <= 103:
        if token_word in a_c:
            freq_count = a_c[token_word][2]
        elif token_word in c_g:
            freq_count = c_g[token_word][2]
    elif ascii >= 103 and ascii <= 114:
        if token_word in g_m:
            freq_count = g_m[token_word][2]
        elif token_word in m_r:
            freq_count = m_r[token_word][2]
    elif ascii >= 114 and ascii <= 122:
        if token_word in r_t:
            freq_count = r_t[token_word][2]
        elif token_word in m_r:
            freq_count = t_z[token_word][2]

    return freq_count

def find_speaker(word):
    speaker = ""
    for symb in word[1:]:
        if symb == ':':
            return speaker
        else:
            speaker = speaker + symb
    return speaker

def extract_words():
    #snlp = stanfordnlp.Pipeline()
    #nlp = StanfordCoreNLP('C:\\stanford\stanford-corenlp-4.3.0')
    nlp = stanza.Pipeline('en')
    # list of transcripts to iterate
    transcript_list = glob.glob("../transcripts/*.txt")
    #transcript_list = ['../transcripts/KB0RE00E.txt']
    # participant's turn in conversation.
    turn = 0
    # all the information of the rows will be stored in this variable.
    csv_total = []
    csv_data = []
    # stores the word with its number of repetition.
    dict = {}
    row = []
    context_to_extract = ['@Location:', '@Room Layout:', '@Situation:', '@Date:', '@ID:', '@Participants:']
    context_list = []
    speaker = ""
    dict_last_speaker = {}
    dict_first_speaker = {}
    dict_id = {}
    dict_part = {}
    dict_pos_tagset = {'CC':'CCONJ','CD':'NUMBER',
    'DT':'DET','EX':'ADV','FW':'FW','IN':'IN',
    'JJ':'ADJ','JJR':'ADJ','JJS':'ADJ','LS':'LS',
    'MD':'VERB','NN':'NOUN','NNS':'NOUN','NNP':'NOUN',
    'NNPS':'NOUN','PDT':'DET','POS':'POS','PRP':'PRON',
    'PRP$':'PRON','RB':'ADV','RBR':'ADV','RBS':'ADV',
    'RP':'RP','SYM':'SYM','TO':'TO','UH':'INTJ','VB':'VERB',
    'VBD':'VERB','VBG':'VERB','VBN':'VERB','VBP':'VERB','VBZ':'VERB',
    'WDT':'DET','WP':'PRON','WP$':'PRON','WRB':'ADV','.':'SYM', '-RRB-': 'SYM', ',':'SYM',}
    list_content_POS = ['NOUN', 'VERB', 'ADJ', 'ADV']
    content_word = False
    id_items =[]

    for transcript in transcript_list:
        with open(transcript) as fp:
            for line in fp:
                line = line = line.replace('[', "")
                line = line = line.replace(']', "")
                line = line = line.replace('(', "")
                line = line = line.replace(')', "")
                line = line.replace('.', "")
                line = line.strip()
                # traversing through list of context.
                count = 0
                if count < 6:
                    for i in range(6):
                        if context_to_extract[i] in line:
                            if '@ID:' in context_to_extract[i]:
                                context = line.partition(context_to_extract[i])[2].strip()
                                id_items = context.split('|')
                                dict_id[id_items[2]] = id_items
                                #print(dict_id)
                            elif '@Participants:' in context_to_extract[i]:
                                context = line.partition(context_to_extract[i])[2].strip()
                                part_items = [context.split(',')[0].split(' ')]
                                part_items.append(context.split(',')[1].split(' '))
                                dict_part[part_items[0][0]] = part_items[0][1]
                                dict_part[part_items[1][1]] = part_items[1][2]
                            else:
                                context = line.partition(context_to_extract[i])[2].strip()
                                context_list.append(context)
                                count += 1
                            #print("context", context, "\nid_items", id_items, "\ndict_id", dict_id, "\npart_items", part_items, "\ndict_part", dict_part, "\ncontext_list", context_list)
                # current not important information contains @ or http.
                if '@' not in line and 'http' not in line:
                    words_of_line  = line.split(" ")
                    for word in words_of_line:
                        if '*' in word:
                            turn += 1
                            speaker = find_speaker(word)
                            line = line.replace('*'+speaker+':', "")
                            line = line.strip()
                    line = re.sub(r'[^\w\s]','', line)
                    line = re.sub(r'[0-9]', '', line)
                    line = re.sub(r'[_]', '', line)
                    line = line.strip() 
                    if line:
                        doc = nlp(line)
                        dicts = doc.to_dict()
                        for sentences in dicts:
                            for word in sentences:
                                token_word = word['text']
                                if token_word in dict:
                                    dict[token_word] += 1
                                elif token_word not in dict:
                                    dict[token_word] = 1
                                if token_word not in dict_last_speaker:
                                    dict_last_speaker[token_word] = 'NA'
                                    dict_first_speaker[token_word] = speaker
                                elif token_word in dict_last_speaker:
                                    dict_last_speaker[token_word] = speaker
                                if dict_pos_tagset[word['xpos']] in list_content_POS:
                                    content_word = 'Content'
                                else:
                                    content_word = 'Function'
                                row.append(transcript)
                                row.extend(context_list)
                                row.append(speaker)
                                row.append(dict_part[speaker])
                                row.append(dict_id[speaker][4])
                                if dict_id[speaker][9] == 'SES is UU' or dict_id[speaker][9] == 'SES is AB':
                                    row.append(dict_id[speaker][9])
                                else:
                                    row.append('NA')
                                row.append(dict_id[speaker][5])
                                row.append(turn)
                                row.append(token_word)
                                row.append(dict[token_word])
                                row.append(dict_first_speaker[token_word])
                                row.append(dict_last_speaker[token_word])
                                row.append(dict_pos_tagset[word['xpos']])
                                row.append(content_word)
                                row.append(word['lemma'])
                                row.append(extract_subtlex(token_word))
                                csv_data.append(row)
                                row = []
        print('Finished:', transcript)
        context_list = []       
    csv_file = pd.DataFrame(csv_data, columns=['Transcript','Location', 'Room_Layout', 'Situation','Date', 'Speaker_ID','Speaker_Name','Sex', 'Socio_Economic_Status','Occupation', 'Turn', 'Word', 'Repetitions', 'First_Spoken_By', 'Last_Spoken_By', 'Part_Of_Speech', 'Content vs Function','Lemmatized', 'FREQcount'])
    csv_file.to_csv('sentences-universal-tags.csv')


def main():
    extract_words()

if __name__ == "__main__":
    main()