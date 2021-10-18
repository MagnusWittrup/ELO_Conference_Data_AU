import json
import os
import nltk
from os import listdir
from os.path import isfile, join
import re
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from gensim.parsing.preprocessing import remove_stopwords
from pyvis.network import Network


def sentimentPiePlot(
    sentiment_dict,
    fig,
):

    ax_pie = fig.add_subplot(122)

    xs = [
        "Negative",
        "Neutral",
        "Positive",
    ]
    ys = [
        sentiment_dict["neg"],
        sentiment_dict["neu"],
        sentiment_dict["pos"],
    ]

    colors = [
        "lightcoral",
        "slategray",
        "springgreen",
    ]
    for y, i in zip(ys, range(len(ys))):
        if y == 0.0:
            del ys[i]
            del xs[i]
            del colors[i]

    # explode = (0.05, 0.05, 0.05)

    ax_pie.pie(
        ys,
        colors=colors,
        labels=xs,
        autopct="%1.1f%%",
        pctdistance=0.85,
        # explode=explode,
    )

    centre_circle = plt.Circle((0, 0), 0.60, fc="white")
    fig = plt.gcf()

    fig.gca().add_artist(centre_circle)

    ax_pie.set_title("Sentiment Pie Chart")

    return ax_pie


def sentimentScatterPlot(
    sentiment_dict,
    fig,
):

    xs = [
        "Negative",
        "Neutral",
        "Positive",
        "Compound",
    ]
    ys = [
        sentiment_dict["neg"],
        sentiment_dict["neu"],
        sentiment_dict["pos"],
        sentiment_dict["compound"],
    ]

    colors = [
        "lightcoral",
        "slategray",
        "springgreen",
        "dodgerblue",
    ]

    ax_compound = fig.add_subplot(121)

    ax_compound.set_title("Sentiment Scatter Plot")
    for y, c, x in zip(ys, colors, xs):
        if y < 0:
            y_pct = -y * 100
        else:
            y_pct = y * 100
        ax_compound.scatter(x, y, color="lavender", marker="o", s=y_pct * 10)
        ax_compound.scatter(x, y, color=c, marker="x", s=y_pct * 5)

    ax_compound.set_ylim([-1.0, 1.0])

    return ax_compound


def saveFig(sentiment_dictionary, file_path, title):

    fig = plt.figure(figsize=(12, 6))

    sentimentScatterPlot(sentiment_dictionary, fig)
    sentimentPiePlot(sentiment_dictionary, fig)
    fig.suptitle(title)

    fig.savefig(
        file_path + ".svg",  # ".png",
        bbox_inches="tight",
        pad_inches=1,
        transparent=False,
        facecolor="w",
    )
    plt.close(fig)


def parseNLTKMethodsOnString(string):
    no_stop_words = remove_stopwords(string)
    word_tokens = nltk.word_tokenize(no_stop_words)
    word_tokens = [w for w in word_tokens if w.isalpha()]

    fd = nltk.FreqDist(word_tokens)
    fd_most_common = fd.most_common()

    bigram = nltk.collocations.BigramCollocationFinder.from_words(word_tokens)
    bigram_most_common = bigram.ngram_fd.most_common()

    trigram = nltk.collocations.TrigramCollocationFinder.from_words(word_tokens)
    trigram_most_common = trigram.ngram_fd.most_common()

    quadgram = nltk.collocations.QuadgramCollocationFinder.from_words(word_tokens)
    quadgram_most_common = quadgram.ngram_fd.most_common()

    return {
        # "fd": fd,
        "fd_most_common": fd_most_common,
        # "bigram": bigram,
        "bigram_most_common": bigram_most_common,
        # "trigram": trigram,
        "trigram_most_common": trigram_most_common,
        # "quadgram": quadgram,
        "quadgram_most_common": quadgram_most_common,
        "word_tokens": word_tokens,
    }


def parseSentimentFromString(string, dictionary=None):
    sia = SentimentIntensityAnalyzer()
    sentece_sentiment = sia.polarity_scores(string)
    if dictionary is not None:
        dictionary["sentiment"] = sentece_sentiment
        return dictionary["sentiment"]
    return sentece_sentiment


def full_text_from_json(data):
    full_text = ""
    for elem in data:
        if elem == "unknown":
            continue
        for string in data[elem]:
            full_text += string + " "
    return full_text


def saveSentimentImage(dirname_cleaned, file_name, trigger_word, sentence_index, trigger_word_sent_dict):
    file_name_cleaned = re.sub(r"\.\w[^\. | $]*\S*", "", file_name)
    title = file_name_cleaned + " - " + trigger_word + " - " + str(sentence_index)

    sentiment_file_path = (
        dirname_cleaned
        + "/visualization/sentiment/"
        + file_name_cleaned
        + "/"
        + trigger_word
        + "/"
        + str(sentence_index)
    )

    if not os.path.exists(dirname_cleaned + "/visualization/sentiment/"):
        os.mkdir(dirname_cleaned + "/visualization/sentiment/")

    if not os.path.exists(dirname_cleaned + "/visualization/sentiment/" + file_name_cleaned + "/"):
        os.mkdir(dirname_cleaned + "/visualization/sentiment/" + file_name_cleaned + "/")

    if not os.path.exists(dirname_cleaned + "/visualization/sentiment/" + file_name_cleaned + "/" + trigger_word + "/"):
        os.mkdir(dirname_cleaned + "/visualization/sentiment/" + file_name_cleaned + "/" + trigger_word + "/")
    trigger_word_sent_dict[sentence_index]["sentiment_file_path"] = sentiment_file_path

    saveFig(
        containing_sentiment,
        sentiment_file_path,
        title,
    )


def create_bigram_netork_graph(file_name, word_tokens, folder_name=""):
    fd = nltk.FreqDist(word_tokens)

    bigram = nltk.collocations.BigramCollocationFinder.from_words(word_tokens)

    net = Network(
        height="100%",
        width="100%",
        directed=True,
    )
    net.force_atlas_2based()

    for (source, target), weight in bigram.ngram_fd.most_common(200):
        net.add_node(
            source,
            title='"' + source + '"' + ":" + str(fd.get(source)),
            label=source,
            value=fd.get(source) * 10,
        )
        net.add_node(
            target,
            title='"' + target + '"' + ":" + str(fd.get(target)),
            label=target,
            value=fd.get(target) * 10,
        )
        net.add_edge(
            source,
            target,
            value=weight * 10,
            title=source + " ➡ " + target + ": " + str(weight),
        )

    # net.show_buttons()
    net.save_graph("../visualization/" + folder_name + file_name + "_bigram.html")


###################################################################################################

dirname = os.path.dirname(__file__)
dirname_split = dirname.split("\\")
dirname_cleaned = "/".join(dirname_split[: len(dirname_split) - 1])
dirname_input = dirname_cleaned + "/output"


only_files = [f for f in listdir(dirname_input) if isfile(join(dirname_input, f))]


trigger_words = ["platform", "google", "facebook", "right", "data"]

# Create target Directory if don't exist
if not os.path.exists(dirname_cleaned + "/concordance/"):
    os.mkdir(dirname_cleaned + "/concordance/")

# Create target Directory if don't exist
if not os.path.exists(dirname_cleaned + "/all/"):
    os.mkdir(dirname_cleaned + "/all/")

stopwords = nltk.corpus.stopwords.words("english")

file_range = len(only_files)
file_index = 1

all_files_all_text_string_builder = ""
for file_name in only_files:
    print("File nr.: " + str(file_index) + " of " + str(file_range))
    print(dirname_input + "/" + file_name)
    with open(dirname_input + "/" + file_name) as f:
        data = json.load(f)

        full_text = full_text_from_json(data)
        sentence_tokens = nltk.sent_tokenize(full_text)

        all_files_all_text_string_builder += " " + full_text

        used_sentence_indeces = []

        all_sent_dict = {}
        all_single_file_data_dict = {}

        trigger_word_index = 1

        # initial run through of all sentences
        for trigger_word in trigger_words:

            trigger_word_all_text = ""

            sentence_index = 0
            trigger_word_sent_dict = {}
            for sentence in sentence_tokens:

                if trigger_word in sentence:
                    trigger_word_sent_dict[sentence_index] = {}
                    if len(sentence_tokens) < 5 or sentence_index < 3  :
                        continue

                    sentence_slice = sentence_tokens[sentence_index - 2 : sentence_index + 3]
                    if sentence_index < 20:
                        print(sentence_slice)

                    trigger_word_sent_dict[sentence_index]["before"] = sentence_slice[:2]
                    before_sentiment = []
                    for before_sentence in sentence_slice[:2]:
                        before_sentiment.append(parseSentimentFromString(before_sentence))
                    trigger_word_sent_dict[sentence_index]["before_sentiment"] = before_sentiment

                    trigger_word_sent_dict[sentence_index]["containing"] = sentence_slice[2]
                    containing_sentiment = parseSentimentFromString(sentence, trigger_word_sent_dict[sentence_index])
                    trigger_word_sent_dict[sentence_index]["containing_sentiment"] = containing_sentiment

                    trigger_word_sent_dict[sentence_index]["after"] = sentence_slice[3:]
                    after_sentiment = []
                    for after_sentence in sentence_slice[4:]:
                        after_sentiment.append(parseSentimentFromString(after_sentence))
                    trigger_word_sent_dict[sentence_index]["after_sentiment"] = after_sentiment

                    # FIXME UNCOMMENT TO MAKE GRAPHS
                    # saveSentimentImage(dirname_cleaned, file_name, trigger_word, sentence_index, trigger_word_sent_dict)

                    file_name_cleaned = re.sub(r"\.\w[^\. | $]*\S*", "", file_name)

                    if not os.path.exists(dirname_cleaned + "/visualization/sentiment/"):
                        os.mkdir(dirname_cleaned + "/visualization/sentiment/")

                    if not os.path.exists(dirname_cleaned + "/visualization/sentiment/" + file_name_cleaned + "/"):
                        os.mkdir(dirname_cleaned + "/visualization/sentiment/" + file_name_cleaned + "/")

                    if not os.path.exists(
                        dirname_cleaned + "/visualization/sentiment/" + file_name_cleaned + "/" + trigger_word + "/"
                    ):
                        os.mkdir(
                            dirname_cleaned + "/visualization/sentiment/" + file_name_cleaned + "/" + trigger_word + "/"
                        )

                    trigger_word_all_text += " ".join(sentence_slice)

                sentence_index = sentence_index + 1

            if len(trigger_word_sent_dict) < 1:
                continue
            all_single_file_data_dict[trigger_word] = {
                "individual_sentiment": trigger_word_sent_dict,
                "all_sentiment": parseSentimentFromString(trigger_word_all_text),
                "all_NLTK_methods": parseNLTKMethodsOnString(trigger_word_all_text),
            }

            all_sent_dict[trigger_word] = trigger_word_sent_dict

            trigger_word_index += 1

        # combined trigger word NLTK methods and graphing
        for trigger_word_all_data in all_single_file_data_dict:
            if len(all_single_file_data_dict[trigger_word_all_data]["individual_sentiment"]) < 1:
                continue

            all_trigger_word_title = file_name_cleaned + " - " + trigger_word_all_data

            trigger_word_all_data_sentiment_file_path = (
                dirname_cleaned
                + "/visualization/sentiment/"
                + file_name_cleaned
                + "/"
                + trigger_word_all_data
                + "_all_sentiment"
            )

            all_single_file_data_dict[trigger_word_all_data][
                "sentiment_file_path"
            ] = trigger_word_all_data_sentiment_file_path

            # saveFig(
            #     all_single_file_data_dict[trigger_word_all_data]["all_sentiment"],
            #     trigger_word_all_data_sentiment_file_path,
            #     all_trigger_word_title,
            # )

        all_file_data_sentiment_file_path = (
            dirname_cleaned + "/visualization/sentiment/" + file_name_cleaned + "_all_sentiment"
        )

        all_single_file_data_dict["sentiment_file_path"] = all_file_data_sentiment_file_path

        # saveFig(
        #     parseSentimentFromString(full_text),
        #     all_file_data_sentiment_file_path,
        #     file_name_cleaned + " - Sentiment",
        # )

        ##### WRITE FILES ####
        file_to_write_to_concordance = dirname_cleaned + "/concordance/" + file_name_cleaned
        file_to_write_to_all_data = dirname_cleaned + "/all/" + file_name_cleaned

        with open(file_to_write_to_concordance + "_concordance.json", "w") as f:
            f.write(json.dumps(all_sent_dict))
        with open(file_to_write_to_all_data + "_all_data.json", "w") as f:
            f.write(json.dumps(all_single_file_data_dict))

        word_tokens = nltk.word_tokenize(full_text)
        word_tokens = [w for w in word_tokens if w.isalpha()]
        word_tokens = [w for w in word_tokens if w.lower() not in stopwords]

        if not os.path.exists(dirname_cleaned + "/visualization/bigrams/"):
            os.mkdir(dirname_cleaned + "/visualization/bigrams/")

        create_bigram_netork_graph(file_name_cleaned, word_tokens, folder_name="bigrams/")

    file_index += 1
    print(" - File completed ✔\n")

all_nltk_methods = parseNLTKMethodsOnString(full_text)
all_sentiment = parseSentimentFromString(full_text)

word_tokens_all = nltk.word_tokenize(all_files_all_text_string_builder)
word_tokens_all = [w for w in word_tokens_all if w.isalpha()]
word_tokens_all = [w for w in word_tokens_all if w.lower() not in stopwords]

create_bigram_netork_graph("all_files", word_tokens_all, folder_name="bigrams/")

print("SCRIPT FINISHED SUCCESSFULLY!")
