# read all txt files in folder
# create div with id of keynote file name
#   create div with id of trigger word
#       create div with id of sentence index
#           create div with class before
#               concatanate all strings in before
#           create div with class containing
#               insert the string
#           create div with class after
#               concatanate all strings in after


def build_html(tag, data, attributes):
    attribute_string = ""
    for attr in attributes:
        attribute_string += " " + attr[0] + '="' + attr[1] + '" '

    html_parts = {
        # < + div + " " + class + =" + test + " id=" + test + ">
        "open": "<" + tag + " " + attribute_string + ">",
        "data": data,
        "close": "</" + tag + ">",
    }

    html_parts["full"] = html_parts["open"] + html_parts["data"] + html_parts["close"]

    return html_parts


def build_sentence_html(build_html, file_name, trigger_word, sentece_index, data, order):
    return build_html(
        "p",
        data.replace(trigger_word, '<span class="trigger-word-highlight">' + trigger_word + "</span>"),
        [
            ["class", "sentence " + order],
            [
                "id",
                clean_file_name + "-" + trigger_word + "-" + str(sentece_index) + "-" + order,
            ],
        ],
    )


def build_html_card(card_title, card_content, card_attributes, card_id):
    attribute_string = ' id="' + card_id + '" '
    for attr in card_attributes:
        attribute_string += " " + attr[0] + '="' + attr[1] + '" '

    return (
        '<div class="card" '
        + attribute_string
        + " >"
        + '<header class="card-header">'
        + '<p class="card-header-title">'
        + card_title
        + "</p>"
        + '<button class="card-header-icon" aria-label="more options"><span class="icon"><i class="fas fa-angle-down" aria-hidden="true"></i></span></button></header><div class="card-content"><div class="content">'
        + card_content
        + "</div></div></div>"
    )


import json
import re
import os
from os import listdir
from os.path import isfile, join

dirname = os.path.dirname(__file__)
dirname_split = dirname.split("\\")
dirname_cleaned = "/".join(dirname_split[: len(dirname_split) - 1])
dirname_input = dirname_cleaned + "/concordance"


only_files = [f for f in listdir(dirname_input) if isfile(join(dirname_input, f))]

all_files_string_builder = ""
trigger_words = []

for file_name in only_files:
    print(dirname_input + "/" + file_name)

    if ".txt" in file_name:
        continue
    with open(dirname_input + "/" + file_name) as f:
        data = json.load(f)
    clean_file_name = re.sub(r"\.\w[^\. | $]*\S*", "", file_name)

    trigger_word_string_builder = ""
    for trigger_word in data:
        if len(data[trigger_word]) < 1:
            continue
        if trigger_word not in trigger_words:
            trigger_words.append(trigger_word)

        sentece_index_string_builder = ""

        for sentece_index in data[trigger_word]:
            before_string = " ".join(data[trigger_word][sentece_index]["before"])
            containing_string = data[trigger_word][sentece_index]["containing"]
            after_string = " ".join(data[trigger_word][sentece_index]["after"])

            before_span = build_sentence_html(
                build_html,
                file_name,
                trigger_word,
                sentece_index,
                before_string,
                "before",
            )

            containing_span = build_sentence_html(
                build_html,
                file_name,
                trigger_word,
                sentece_index,
                containing_string,
                "containing",
            )

            after_span = build_sentence_html(
                build_html,
                file_name,
                trigger_word,
                sentece_index,
                after_string,
                "after",
            )

            sentece_index_div = build_html(
                "div",
                before_span["full"] + " " + containing_span["full"] + after_span["full"],
                [
                    ["data-sentence-index", str(sentece_index)],
                    ["data-trigger-word", trigger_word],
                    [
                        "data-file-name",
                        clean_file_name,
                    ],
                    [
                        "id",
                        clean_file_name + "-" + trigger_word + "-" + str(sentece_index),
                    ],
                    ["class", "sentence-full"],
                ],
            )

            sentece_index_string_builder += sentece_index_div["full"] + '<div class="hori-line"></div>'

        trigger_word_card = build_html_card(
            card_attributes=[
                [
                    "data-trigger-word",
                    trigger_word,
                ],
                [
                    "data-file-name",
                    clean_file_name,
                ],
            ],
            card_id=clean_file_name + "-" + trigger_word,
            card_content=sentece_index_string_builder,
            card_title="<b>Trigger Word: </b> " + trigger_word,
        )

        trigger_word_div = build_html(
            "div",
            sentece_index_string_builder,
            [
                ["data-trigger-word", trigger_word],
                ["data-file-name", clean_file_name],
                ["id", clean_file_name + "-" + trigger_word],
                ["class", ""],
            ],
        )

        # trigger_word_string_builder += trigger_word_div["full"]
        trigger_word_string_builder += trigger_word_card

    file_card = build_html_card(
        card_attributes=[
            ["data-file-name", clean_file_name],
        ],
        card_id=clean_file_name,
        card_content=trigger_word_string_builder,
        card_title="<b>File: </b>  " + clean_file_name,
    )

    all_files_div = build_html(
        "div",
        trigger_word_div["full"],
        [
            [
                "data-file-name",
                clean_file_name,
            ],
            [
                "id",
                clean_file_name,
            ],
            ["class", ""],
        ],
    )

    all_files_string_builder += file_card
    # all_files_string_builder += all_files_div["full"]

trigger_word_content = ""
for trigger_word in trigger_words:
    trigger_word_content += (
        '<div class="dropdown-item"'
        + '"><label class="trigger-word-checkbox checkbox" data-trigger-word-toggle="'
        + trigger_word
        + '">'
        + trigger_word
        + '<input type="checkbox" checked></label></div>'
    )

trigger_word_dropdown = (
    """
<div id="trigger-words-dropdown" class="dropdown ">
  <div class="dropdown-trigger">
    <button class="button" aria-haspopup="true" aria-controls="dropdown-menu">
      <span>Filter trigger words</span>
      <span class="icon is-small">
        <i class="fas fa-angle-right" aria-hidden="true"></i>
      </span>
    </button>
  </div>
  <div class="dropdown-menu" id="trigger-words-dropdown-menu" role="menu">
    <div class="dropdown-content">
    """
    + trigger_word_content
    + """
    </div>
  </div>
"""
)

final_html = (
    """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ELO DATA CONCORDANCE</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" integrity="sha512-1ycn6IcaQQ40/MKBW2W4Rhis/DbILU74C1vSrLJxCq57o941Ym01SwNsOMqvEBFlcgUa6xLiPY/NS5R+E6ztJQ==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="styles.css">
    <script src="app.js"></script>
</head>
<body>

<section class="section is-primary" id="header-section">
<div class="container box">
"""
    + trigger_word_dropdown
    + """
</div>
<div id="header-text" class="tag is-info is-large is-light">ELO Conference | Data Analysis </div>
</section>
<section class="section" id="concordance-section">
<div class="container box">
"""
    + all_files_string_builder
    + """
</div>
</section>
</body>
</html>"""
)

with open(dirname_cleaned + "/visualization/index.html", "w") as f:
    f.write(final_html)


#         create div with id of trigger word
#       create div with id of sentence index
#           create div with class before
#               concatanate all strings in before
#           create div with class containing
#               insert the string
#           create div with class after
#               concatanate all strings in after

# build html string
# all in before concat with containing
