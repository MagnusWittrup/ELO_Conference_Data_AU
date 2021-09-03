import nltk
from nltk.corpus import stopwords
import json
import os


dirname = os.path.dirname(__file__)

# Fixme use the dirname to get all the JSON files in a specific folder
with open("C:/Users/Magnu/repos/data-scraping-elo/output/Lai_Tze_Fan.mp4.txt.json") as f:
    print(f)
    data = json.load(f)


# Create one big contiguous string
full_text = ""
for elem in data:
    if elem == "unknown":
        continue
    for string in data[elem]:
        full_text += string + " "
# print(full_text)

# tokenize the big string
from nltk.tokenize import word_tokenize

clean_full_text = nltk.word_tokenize(full_text)


# Stemming
from nltk.stem import SnowballStemmer

# create object of SnowbllStemmer
snstem = SnowballStemmer("english")
stem_full_text = [snstem.stem(token) for token in clean_full_text]

# Lemmatization
from nltk.stem import WordNetLemmatizer

lemma = WordNetLemmatizer()
lemma_full_text = [lemma.lemmatize(token) for token in stem_full_text]

# Stop word removal
from nltk.corpus import stopwords

# config the language name
stoplist = stopwords.words("english")
sans_stop_full_text = [token for token in lemma_full_text if token not in stoplist]

# remove commas and periods
def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]


sans_comma = remove_values_from_list(sans_stop_full_text, ",")
sans_period = remove_values_from_list(sans_comma, ".")
sans_apostrophe_s = remove_values_from_list(sans_period, "'s")
sans_apostrophe_m = remove_values_from_list(sans_apostrophe_s, "'m")
sans_apostrophe_nt = remove_values_from_list(sans_apostrophe_m, "n't")
sans_question_mark = remove_values_from_list(sans_apostrophe_nt, "?")

full_sans_comma = remove_values_from_list(clean_full_text, ",")
full_sans_period = remove_values_from_list(full_sans_comma, ".")
full_sans_apostrophe_s = remove_values_from_list(full_sans_period, "'s")
full_sans_apostrophe_m = remove_values_from_list(full_sans_apostrophe_s, "'m")
full_sans_apostrophe_nt = remove_values_from_list(full_sans_apostrophe_m, "n't")
full_sans_question_mark = remove_values_from_list(full_sans_apostrophe_nt, "?")

from nltk.probability import FreqDist

fdist = FreqDist(sans_question_mark)

import matplotlib.pyplot as plt

fdist.plot(
    30,
    cumulative=False,
)
plt.show()

# nltk_sans_period = nltk.Text(sans_period)
# # nltk_sans_period.concordance("platform")

# nltk_full_text = nltk.Text(full_sans_apostrophe_nt)
# nltk_full_text.concordance("platform")

# sent_nltk_full_text = nltk.Text(sent_clean_full_text)
# sent_nltk_full_text.concordance("platform")

# index = 0
# for sentence in sent_clean_full_text:
#     if "platform" in sentence:
# sentence_before_plus = sent_clean_full_text[index - 2]
# sentence_before = sent_clean_full_text[index - 1]
# sentence_containing = sent_clean_full_text[index]
# sentence_after = sent_clean_full_text[index + 1]
# sentence_after_plus = sent_clean_full_text[index + 2]
# print(sentence_before)
# print(sentence_containing)
# print(sentence_after)
# index = index + 1

from colorama import Fore, Back, Style

trigger_words = ["platform", "google", "facebook", "right", "data"]


all_sent_string = ""
all_sent_dict = {}
for trigger_word in trigger_words:
    index = 0
    trigger_word_sent_string = "\nTRIGGER WORD: " + trigger_word
    trigger_word_sent_dict = {}
    for sentence in sent_clean_full_text:
        if trigger_word in sentence:
            trigger_word_sent_string += "\n\tSENTENCE INDEX " + str(index + 1)
            trigger_word_sent_dict[index] = {}

            sentence_slice = sent_clean_full_text[index - 3 : index + 3]

            trigger_word_sent_string += "\n\tBEFORE: "

            trigger_word_sent_dict[index]["before"] = sentence_slice[:2]
            for before_sent in sentence_slice[:2]:
                trigger_word_sent_string += "\n\t\t" + before_sent + "\n"

            trigger_word_sent_dict[index]["before"] = sentence_slice[4]
            trigger_word_sent_string += "\n\tCONTAINING:\n\t\t" + sentence_slice[3] + "\n"

            trigger_word_sent_string += "\n\tAFTER: "

            trigger_word_sent_dict[index]["after"] = sentence_slice[4:]
            for after_sent in sentence_slice[4:]:
                trigger_word_sent_string += "\n\t\t" + after_sent + "\n"

            trigger_word_sent_string += "\n"

        index = index + 1

    all_sent_string += trigger_word_sent_string + "\n"
    all_sent_dict[trigger_word] = trigger_word_sent_dict
print(all_sent_dict)
with open("test_concordance.json", "w") as f:
    f.write(json.dumps(all_sent_dict))
with open("test_concordance.txt", "w") as f:
    f.write(all_sent_string)
