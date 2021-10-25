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

import json
import re
import os
from os import listdir
from os.path import isfile, join
from os import listdir


def capitalize(string):
    return string[0].upper() + string[1:]


dirname = os.path.dirname(__file__)
dirname_split = dirname.split("/")
dirname_cleaned = "/".join(dirname_split[: len(dirname_split) - 1])
dirname_input = dirname_cleaned + "/concordance"

only_files = [f for f in listdir(dirname_input) if isfile(join(dirname_input, f))]

all_files_string_builder = ""
trigger_words = []

dirname = os.path.dirname(__file__)
dirname_split = dirname.split("\\")
dirname_cleaned = "/".join(dirname_split)
dirname_input = dirname_cleaned + "/bigrams"

bigram_options = ""

only_files = [f for f in listdir(dirname_input) if isfile(join(dirname_input, f))]
for file_name in only_files:
    clean_file_name = (
        file_name.replace(".html", "").replace("bigram", "").replace("_", " ")
    )
    bigram_options += (
        '<option value="./bigrams/'
        + file_name
        + '" >'
        + capitalize(clean_file_name)
        + "</option>"
    )

bigram_div = (
    """
<div id="bigram-container block">
    <div id="bigram-select" class="select block">
        <select>
        <option value="">Choose bigram to show</option>
            """
    + bigram_options
    + """
        </select>
    </div>
    <div id="bigram-button" class="control block">
        <button class="button is-primary">
            Open Chosen Bigram
        </button>
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
    <link rel="stylesheet" href="styles/main.css">
    <script src="app.js"></script>
</head>
<body>

<section class="" id="header-section">
<div class="container box">
"""
    # + trigger_word_dropdown
    + bigram_div
    + """
    <div id="header-text" class="tag is-info is-large is-light">ELO Conference | Data Analysis </div>
</div>

</section>
<div id="modal-overlay">
</div>


</body>
</html>"""
)

with open(dirname_cleaned + "/index.html", "w") as f:
    f.write(final_html)
