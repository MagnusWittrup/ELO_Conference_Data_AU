import json
import os
import nltk
from os import listdir
from os.path import isfile, join
import re
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt


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
        file_path + ".png",
        bbox_inches="tight",
        pad_inches=1,
        transparent=False,
        facecolor="w",
    )
    plt.close(fig)


def parseNLTKMethodsOnString(string):
    word_tokens = nltk.word_tokenize(string)
    word_tokens = [w for w in word_tokens if w.isalpha()]
    word_tokens = [w for w in word_tokens if w.lower() not in stopwords]

    fd = nltk.FreqDist(word_tokens)
    fd_most_common = fd.most_common()

    bigram = nltk.collocations.BigramCollocationFinder.from_words(word_tokens)
    bigram_most_common = bigram.ngram_fd.most_common()

    trigram = nltk.collocations.TrigramCollocationFinder.from_words(word_tokens)
    trigram_most_common = trigram.ngram_fd.most_common()

    quadgram = nltk.collocations.QuadgramCollocationFinder.from_words(word_tokens)
    quadgram_most_common = quadgram.ngram_fd.most_common()

    return {
        "fd": fd,
        "fd_most_common": fd_most_common,
        "bigram": bigram,
        "bigram_most_common": bigram_most_common,
        "trigram": trigram,
        "trigram_most_common": trigram_most_common,
        "quadgram": quadgram,
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


dirname = os.path.dirname(__file__)
dirname_split = dirname.split("\\")
dirname_cleaned = "/".join(dirname_split[: len(dirname_split) - 1])
dirname_input = dirname_cleaned + "/output"


only_files = [f for f in listdir(dirname_input) if isfile(join(dirname_input, f))]


trigger_words = ["platform", "google", "facebook", "right", "data"]
all_files_full_words_cleaned = ""

# Create target Directory if don't exist
if not os.path.exists(dirname_cleaned + "/concordance/"):
    os.mkdir(dirname_cleaned + "/concordance/")

stopwords = nltk.corpus.stopwords.words("english")

file_range = len(only_files)
file_index = 1
for file_name in only_files:
    print("File nr.: " + str(file_index) + " of " + str(file_range))
    print(dirname_input + "/" + file_name)
    with open(dirname_input + "/" + file_name) as f:
        data = json.load(f)

        full_text = full_text_from_json(data)
        sentence_tokens = nltk.sent_tokenize(full_text)

        used_sentence_indeces = []

        all_sent_dict = {}

        trigger_word_range = len(trigger_word)
        trigger_word_index = 1
        for trigger_word in trigger_words:
            # print("\t- Triggerword nr.: " + str(trigger_word_index) + "of " + str(trigger_word_range))

            sentence_index = 0
            trigger_word_sent_dict = {}
            for sentence in sentence_tokens:
                # print("\t\t- Sentence nr.: " + str(sentence_index + 1) + "of " + str(len(sentence_tokens)))

                if trigger_word in sentence:
                    trigger_word_sent_dict[sentence_index] = {}

                    sentence_slice = sentence_tokens[sentence_index - 3 : sentence_index + 3]

                    trigger_word_sent_dict[sentence_index]["before"] = sentence_slice[:2]
                    # for before_sentence in sentence_slice[:2]:
                    #   trigger_word_sent_dict[sentence_index]["before_sentiment"] = before_sentiment

                    trigger_word_sent_dict[sentence_index]["containing"] = sentence_slice[3]

                    trigger_word_sent_dict[sentence_index]["after"] = sentence_slice[4:]

                    sentence_sentiment = parseSentimentFromString(sentence, trigger_word_sent_dict[sentence_index])

                    title = (
                        re.sub(r"\.\w[^\. | $]*\S*", "", file_name) + " - " + trigger_word + " - " + str(sentence_index)
                    )

                    sentiment_file_path = (
                        dirname_cleaned
                        + "/sentiment/"
                        + re.sub(r"\.\w[^\. | $]*\S*", "", file_name)
                        + "/"
                        + trigger_word
                        + "/"
                        + str(sentence_index)
                    )

                    if not os.path.exists(dirname_cleaned + "/sentiment/"):
                        os.mkdir(dirname_cleaned + "/sentiment/")

                    if not os.path.exists(
                        dirname_cleaned + "/sentiment/" + re.sub(r"\.\w[^\. | $]*\S*", "", file_name) + "/"
                    ):
                        os.mkdir(dirname_cleaned + "/sentiment/" + re.sub(r"\.\w[^\. | $]*\S*", "", file_name) + "/")

                    if not os.path.exists(
                        dirname_cleaned
                        + "/sentiment/"
                        + re.sub(r"\.\w[^\. | $]*\S*", "", file_name)
                        + "/"
                        + trigger_word
                        + "/"
                    ):
                        os.mkdir(
                            dirname_cleaned
                            + "/sentiment/"
                            + re.sub(r"\.\w[^\. | $]*\S*", "", file_name)
                            + "/"
                            + trigger_word
                            + "/"
                        )
                    trigger_word_sent_dict[sentence_index]["sentiment_file_path"] = sentiment_file_path

                    saveFig(
                        sentence_sentiment,
                        sentiment_file_path,
                        title,
                    )

                if not sentence_index in used_sentence_indeces:
                    all_files_full_words_cleaned += " " + sentence
                    used_sentence_indeces.append(sentence_index)
                sentence_index = sentence_index + 1

            all_sent_dict[trigger_word] = trigger_word_sent_dict
            trigger_word_index += 1

        file_to_write_to = dirname_cleaned + "/concordance/" + re.sub(r"\.\w[^\. | $]*\S*", "", file_name)

        with open(file_to_write_to + "_concordance.json", "w") as f:
            f.write(json.dumps(all_sent_dict))
    file_index += 1
all_nltk_methods = parseNLTKMethodsOnString(all_files_full_words_cleaned)
all_sentiment = parseSentimentFromString(all_files_full_words_cleaned)


# fig_all = plt.figure(figsize=(12, 6))

# sentimentScatterPlot(all_sentiment, fig_all)
# sentimentPiePlot(all_sentiment, fig_all)

# fig_all.savefig("test_.png")
# plt.close(fig_all)


def saveFig(sentiment_dictionary):
    fig = plt.figure(figsize=(12, 6))

    sentimentScatterPlot(sentiment_dictionary, fig)
    sentimentPiePlot(sentiment_dictionary, fig)

    fig.savefig(
        "test_xd.png",
        bbox_inches="tight",
        pad_inches=1,
        transparent=False,
        facecolor="w",
    )
    plt.close(fig)


saveFig(all_sentiment)
