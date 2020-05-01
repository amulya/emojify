from flask import Flask, render_template, request, url_for
import emoji
import nltk
from nltk.corpus import stopwords, brown

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    result = []
    similar_words = []
    if request.method == 'POST':
        user_input = request.form["text"]

        # all original words + symbols - need this to add noisewords at end
        text_list = user_input.split()

        result = text_list.copy()

        # remove punctuation/symbols/etc
        result = remove_symbols(result)

        # remove noise words
        result = remove_noise_words(result)

        # TEST: print all 'similar' words to each word
        text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
        print(text.similar("finger"))
        print('\n\n\n')
        print(text.similar("thumb"))

        result = " ".join(result)

    return render_template('home.html', result=result, similar_words=similar_words)

# scans for and removes noise words from text (using text file of noise words)


def remove_noise_words(text):

    # open noise words file
    f = open('noise-words.txt', 'r')

    # read words into list
    noise_words = f.read().split('\n')

    # close file
    f.close()

    result = []

    for word in text:
        if word.lower() not in noise_words:
            result.append(word)

    return result


def remove_symbols(result):
    for word in result:
        if word != word.strip('0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'):
            result.append(word.strip(
                '0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'))
            result.remove(word)
    return result


if __name__ == '__main__':
    app.run(debug=True)
