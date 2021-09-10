import requests
from bs4 import BeautifulSoup
import sys


def main():
    languages = ['Arabic','English','French','Spanish','Portuguese','German','Japanese','Dutch','Polish','Romanian','Russian','Turkish']
    args = sys.argv

    if len(args) == 1:
        args = input().split()
        if args[0] == 'exit':
            exit()
        word_lang = args[0].capitalize()
        translate_to = args[1].capitalize()
        word = args[2]
    else:
        word_lang = args[1].capitalize()
        translate_to = args[2].capitalize()
        word = args[3]

    if word_lang not in languages:
        print(f"Sorry, the program doesn't support {word_lang}")
        exit()

    if translate_to not in languages:
        if translate_to == 'All':
            for language in languages:
                if language != word_lang:
                    url_text = word_lang.lower() + '-' + language.lower()
                    content = connect(url_text, word)
                    beautiful_soup(content, language, word, 4)
                    name_file.write('___________________________________________________________________________')


        else:
            print(f"Sorry, the program doesn't support {translate_to}")
            exit()
    else:
        url_text = word_lang.lower() + '-' + translate_to.lower()
        content = connect(url_text, word)
        beautiful_soup(content, translate_to, word, 5)
        name_file.write('___________________________________________________________________________')


def connect(url_text, word):
    headers = {'User-Agent': 'Mozilla/5.0'}
    s = requests.Session()
    try:
        page = s.get(f'https://context.reverso.net/translation/{url_text}/{word}', headers=headers)
        if page:  # 200
            return page.content
        else:  # 404
            print(f'Sorry, unable to find {word}')
            exit()
    except requests.exceptions.ConnectionError:   
        print('Something wrong with your internet connection')
        exit()
    

def beautiful_soup(content, translate_to, word, num):
    global name_file, file
    soup = BeautifulSoup(content, 'html.parser')
    file = f'{word}.txt'
    name_file = open(file, 'a', encoding='utf-8')

    translations = soup.find_all('a', {"class": 'translation'}) # no idea how
    sentences_src, sentences_target = soup.find_all('div', {"class": "src ltr"}), \
                                      soup.find_all('div', {"class": ["trg ltr", "trg rtl arabic", "trg rtl"]}) # no idea how

    def print_translations(num):
        num2 = num
        description = '\n' + translate_to + ' Translations:'
        name_file.write(description + '\n')
        for trans in translations:
            if num2 > num >= 0:
                word = trans.text.strip()
                name_file.write(word + '\n')
            num -= 1

    def print_examples(num):
        description = '\n' + translate_to + ' Example:'
        name_file.write(description + '\n')
        for pair1, pair2 in zip(sentences_src, sentences_target):
            if num > 0:
                example = pair1.text.strip()
                example_trans = pair2.text.strip()
                name_file.write(example + '\n')
                name_file.write(example_trans + '\n\n')
                num -= 1

    print_translations(num)
    print_examples(num)

main()
name_file.close()
with open(file, 'r', encoding='utf-8') as fp:
    print(fp.read())
name_file.close()