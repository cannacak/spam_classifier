import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
import os

nltk.download('punkt')

ps = PorterStemmer()
word_list_index = {}
word_list_counter = {}
counter = 0

name_counter = 0
save_path = '/home/mustafa/Downloads/AI3/new_spams_training'
spamas_path = sorted(os.listdir('/home/mustafa/Downloads/AI3/Spamas/'))

for filename in spamas_path:

    try:
        input_program = open("/home/mustafa/Downloads/AI3/Spamas/" + filename, "r", encoding='utf8',
                             errors='ignore').read()

        # Replace email address with 'emailaddress'
        input_program = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', ' emailadress ', input_program)

        # Replace urls with 'webaddress'
        input_program = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', ' webadress ', input_program)

        # Replace money symbol with 'money-symbol'
        input_program = re.sub(r'£|\$', 'money-symbol', input_program)

        # Replace 10 digit phone number with 'phone-number'
        input_program = re.sub(".*?(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?", ' phone-number ', input_program)

        # Replace normal number with 'number'
        input_program = re.sub('\d', ' number ', input_program)

        # remove punctuation
        input_program = re.sub(r'[^\w\d\s]', ' ', input_program)

        # remove whitespace between terms with single space
        input_program = re.sub(r'\s+', ' ', input_program)

        # remove leading and trailing whitespace
        input_program = re.sub(r'^\s+|\s*?$', ' ', input_program)

        # change words to lower case
        input_program = input_program.lower()
        words = word_tokenize(input_program)

        if name_counter > len(spamas_path) * 0.8:
            save_path = '/home/mustafa/Downloads/AI3/new_spams_test'
        file_name = str(name_counter) + '_spam.txt'
        name_counter += 1
        complete_name = os.path.join(save_path, file_name)

        with open(complete_name, 'w', encoding='utf-8') as f:
            repeat_check = []
            for w in words:
                lex = ps.stem(w)
                if len(lex) > 1 and len(lex) < 78:
                    if lex not in repeat_check:
                        f.write(lex)
                        f.write(' ')
                    repeat_check.append(lex)
                    if name_counter < len(spamas_path) * 0.8:
                        if lex not in word_list_index.keys():
                            word_list_index[lex] = counter
                            word_list_counter[lex] = 1

                            counter = counter + 1
                        else:
                            word_list_counter[lex] = word_list_counter[lex] + 1
                else:
                    continue

    except UnicodeDecodeError:
        continue
print("done!")

print("COUNTER")
print(word_list_counter)

word_list_index_ham = {}
word_list_counter_ham = {}

name_counter = 0
nespamas_save_path = '/home/mustafa/Downloads/AI3/new_nespamas_training'
nespamas_path = sorted(os.listdir('/home/mustafa/Downloads/AI3/Ne spamas/'))
for filename in nespamas_path:
    try:
        input_program = open("/home/mustafa/Downloads/AI3/Ne spamas/"+filename, "r",encoding='utf8',errors='ignore').read()

        # Replace email address with 'emailaddress'
        input_program = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', ' emailadress ', input_program)

        # Replace urls with 'webaddress'
        input_program = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', ' webadress ', input_program)

        # Replace money symbol with 'money-symbol'
        input_program = re.sub(r'£|\$', 'money-symbol', input_program)

        # Replace 10 digit phone number with 'phone-number'
        input_program = re.sub(".*?(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?", ' phone-number ', input_program)

        # Replace normal number with 'number'
        input_program = re.sub('\d', ' number ', input_program)

        # remove punctuation
        input_program = re.sub(r'[^\w\d\s]', ' ', input_program)

        # remove whitespace between terms with single space
        input_program = re.sub(r'\s+', ' ', input_program)

        # remove leading and trailing whitespace
        input_program = re.sub(r'^\s+|\s*?$', ' ', input_program)

        # change words to lower case
        input_program = input_program.lower()
        words = word_tokenize(input_program)
        if name_counter > len(nespamas_path)*0.8:
            nespamas_save_path = '/home/mustafa/Downloads/AI3/new_nespamas_test'
        file_name = str(name_counter) + '_nespam.txt'
        complete_name = os.path.join(nespamas_save_path,file_name)
        name_counter += 1
        with open(complete_name,'w',encoding='utf-8') as f:
            check_list = []
            for w in words:
                lex = ps.stem(w)
                if len(lex) > 1 and len(lex) < 78:
                    if lex not in check_list:
                        f.write(lex)
                        f.write(' ')
                    check_list.append(lex)
                    if name_counter < len(nespamas_path)*0.8:
                        if lex not in word_list_index_ham.keys():
                            if lex in word_list_index.keys():
                                word_list_index_ham[lex] = word_list_index[lex]
                            else:
                                word_list_index_ham[lex] = counter
                                counter = counter + 1
                            word_list_counter_ham[lex] = 1
                        else:
                            word_list_counter_ham[lex] =  word_list_counter_ham[lex] +  1
        if name_counter > len(spamas_path)*0.8:
            save_path = '/home/mustafa/Downloads/AI3/new_nespamas_test'
    except UnicodeDecodeError:
        continue

print("COUNTER")
print(word_list_counter_ham)

import json
with open("counter_spam.json", "w") as outfile:
    json.dump(word_list_counter, outfile)

with open("counter_ham.json", "w") as outfile:
    json.dump(word_list_counter_ham, outfile)

with open("index_spam.json", "w") as outfile:
    json.dump(word_list_index, outfile)

with open("index_ham.json", "w") as outfile:
    json.dump(word_list_index_ham, outfile)

spamicity = {}
total_word_ham = 0
total_word_spam = 0

for i in word_list_counter_ham.keys():
    total_word_ham = total_word_ham + word_list_counter_ham[i]
print(total_word_ham)
print(len(word_list_counter_ham))

for i in word_list_counter.keys():
    total_word_spam = total_word_spam + word_list_counter[i]
print(total_word_spam)
print(len(word_list_counter))

word_list_counter_all = {**word_list_counter, **word_list_counter_ham}

for i in word_list_counter_all.keys():
    if i in word_list_counter_ham and i not in word_list_counter:
        spamicity[i] = 0.01
    elif i not in word_list_counter_ham and i in word_list_counter:
        spamicity[i] = 0.99

    else:
        spamicity[i] = (word_list_counter[i] / total_word_spam) / (
                    word_list_counter_ham[i] / total_word_ham + word_list_counter[i] / total_word_spam)

with open("spamicity.json", "w") as outfile:
    json.dump(spamicity, outfile)

import heapq
highest_spam = heapq.nlargest(8, spamicity, key=spamicity.get)

average_spamicity = sum(spamicity.values()) / len(spamicity.values())

sorted(spamicity.values(), reverse=True)


value = { k : word_list_index[k] for k in set(word_list_index) - set(word_list_index_ham) }

set1 = set(word_list_index.keys())
set2 = set(word_list_index_ham.keys())

len(set1 ^ set2)


def p_calculator(words, N):
    counter = 0
    spam_mult = 1
    spam_mult_minus1 = 1

    for i in sorted(words.values(), reverse=False):
        if counter == N / 2:
            break
        spam_mult *= i
        spam_mult_minus1 *= (1 - i)
        counter += 1

    for j in sorted(words.values(), reverse=True):
        if counter == N:
            break
        spam_mult *= j
        spam_mult_minus1 *= (1 - j)
        counter += 1

    p = spam_mult / (spam_mult + spam_mult_minus1)
    return p


def spam_analyzer(N, lexeme_value, treshold_value):
    Number_of_SPAM_files_classified_HAM = 0
    Number_of_HAM_files_classified_SPAM = 0
    Number_of_SPAM_files_classified_SPAM = 0
    Number_of_HAM_files_classified_HAM = 0
    p_values = {}
    spamicity_dict = {}
    j = 0
    k = 0
    path_decider = 1
    paths = ['/home/mustafa/Downloads/AI3/new_spams_test/', '/home/mustafa/Downloads/AI3/new_nespamas_test/']
    print(len(paths[0]), len(paths[1]))
    for x in paths:
        the_path = sorted(os.listdir(x))

        for file_name in the_path:

            training_file = open(x + file_name, "r", encoding='utf8', errors='ignore').read()
            k += 1
            words = word_tokenize(training_file)

            for i in words:

                if i in spamicity:
                    spamicity_dict[i] = spamicity[i]
                    p_values[i] = p_calculator(spamicity_dict, N)
                else:
                    spamicity_dict[i] = lexeme_value
                    p_values[i] = p_calculator(spamicity_dict, N)

                if path_decider == 1:
                    if p_values[i] > treshold_value:
                        Number_of_SPAM_files_classified_SPAM += 1
                    else:
                        Number_of_SPAM_files_classified_HAM += 1
                else:

                    if p_values[i] > treshold_value:
                        Number_of_HAM_files_classified_SPAM += 1
                    else:
                        Number_of_HAM_files_classified_HAM += 1
        path_decider -= 1
    accuracy = (Number_of_SPAM_files_classified_SPAM + Number_of_HAM_files_classified_HAM) / (
                Number_of_SPAM_files_classified_SPAM + Number_of_HAM_files_classified_HAM + Number_of_SPAM_files_classified_HAM + Number_of_HAM_files_classified_SPAM) * 100
    print(Number_of_SPAM_files_classified_HAM)
    print(Number_of_SPAM_files_classified_SPAM)
    print(Number_of_HAM_files_classified_HAM)
    print(Number_of_HAM_files_classified_SPAM)

    return accuracy


N_values = [4, 8, 16, 32]
lexeme_values = [0.2, 0.4, 0.6, 0.8]
treshold_values = [0.6, 0.7, 0.8, 0.9]

for i in N_values:
    for j in lexeme_values:
        for k in treshold_values:
            accuracy = spam_analyzer(i, j, k)
            print("N : {}, lexeme value : {}, treshold value : {}, accuracy :{}".format(i, j, k, accuracy))
