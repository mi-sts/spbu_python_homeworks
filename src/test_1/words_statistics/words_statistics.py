import os
import re
from collections import Counter, OrderedDict


def words_statistics(filename: str) -> str:
    punctuation_symbols = [".", "!", "?"]

    if not os.path.exists(filename):
        return ""

    file = open(filename, "r")
    line = file.readline()
    words = Counter()
    n_sentences = 0

    while line:
        line_elements = re.findall(r"[\w']+|['.!?]", line)  # Divide into punctuation and letter symbols.
        last_is_punctuation = False
        for i in line_elements:
            if i in punctuation_symbols and not last_is_punctuation:
                last_is_punctuation = True
                n_sentences += 1
            else:
                last_is_punctuation = False
                word = i.lower()
                words[word] += 1

        line = file.readline()

    top_words = words.most_common()[:10]
    file.close()

    return f"Top-10 words: {', '.join([f'{i[0]} - {i[1]}' for i in top_words])}. Number of sentences: {n_sentences}"


if __name__ == "__main__":
    print(words_statistics("tomsawyer.txt"))
