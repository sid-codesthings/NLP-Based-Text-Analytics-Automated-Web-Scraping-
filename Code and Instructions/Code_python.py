import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('punkt')

def load_stopwords(stopword_files):
    stopwords = set()
    for file in stopword_files:
        with open(file, 'r', encoding='latin-1') as f:
            for word in f:
                stopwords.add(word.strip().upper())
    return stopwords

stopword_files = [
    'StopWords_Auditor.txt',
    'StopWords_Currencies.txt',
    'StopWords_DatesandNumbers.txt',
    'StopWords_Generic.txt',
    'StopWords_GenericLong.txt',
    'StopWords_Geographic.txt',
    'StopWords_Names.txt'
]

all_stopwords = load_stopwords(stopword_files)

def load_dictionary(file_path, stopwords):
    words = set()
    with open(file_path, 'r', encoding='latin-1') as f:
        for line in f:
            word = line.strip().upper()
            if word not in stopwords:
                words.add(word)
    return words

positive_words = load_dictionary('positive-words.txt', all_stopwords)
negative_words = load_dictionary('negative-words.txt', all_stopwords)

def extract_article(url):

    try:

        session = requests.Session()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                      "image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

        response = session.get(url, headers=headers, timeout=10)

        print("Status Code:", response.status_code, "| URL:", url)

        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1')
        title_text = title.get_text(strip=True) if title else ""

        article = soup.find('div', class_='td-post-content')
        article_text = article.get_text(separator=' ', strip=True) if article else ""

        return title_text + "\n" + article_text

    except Exception as e:
        print("Error:", url)
        return ""


def count_syllables(word):
    word = word.lower()
    vowels = "aeiou"
    syllable_count = 0

    if len(word) == 0:
        return 0

    if word[0] in vowels:
        syllable_count += 1

    for i in range(1, len(word)):
        if word[i] in vowels and word[i-1] not in vowels:
            syllable_count += 1

    if word.endswith("e"):
        syllable_count -= 1

    return max(1, syllable_count)

def analyze_text(text):

    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    cleaned_words = [w.upper() for w in words if w.isalpha()]
    words_no_stop = [w for w in cleaned_words if w not in all_stopwords]

    word_count = len(words_no_stop)
    sentence_count = len(sentences)

    if word_count == 0:
        return [0]*13

    if sentence_count == 0:
        sentence_count = 1

    # POSITIVE SCORE
    positive_score = sum(1 for w in words_no_stop if w in positive_words)

    # NEGATIVE SCORE (MULTIPLY BY -1)
    negative_score = -sum(1 for w in words_no_stop if w in negative_words)

    # POLARITY SCORE
    polarity_score = (positive_score - negative_score) / ((positive_score + abs(negative_score)) + 0.000001)

    # SUBJECTIVITY SCORE
    subjectivity_score = (positive_score + abs(negative_score)) / (word_count + 0.000001)

    # AVG SENTENCE LENGTH
    avg_sentence_length = word_count / sentence_count

    # COMPLEX WORDS
    complex_words = [w for w in words_no_stop if count_syllables(w) > 2]
    complex_word_count = len(complex_words)

    # % COMPLEX WORDS
    percentage_complex_words = complex_word_count / word_count

    # FOG INDEX
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    # SYLLABLE PER WORD
    syllable_per_word = sum(count_syllables(w) for w in words_no_stop) / word_count

    # PERSONAL PRONOUNS
    pronouns = re.findall(r'\b(I|we|my|ours|us)\b', text, re.I)
    pronouns = [p for p in pronouns if p.lower() != 'us' or p != 'US']
    personal_pronouns = len(pronouns)

    # AVG WORD LENGTH
    avg_word_length = sum(len(w) for w in words_no_stop) / word_count

    return [
        positive_score,
        abs(negative_score),
        polarity_score,
        subjectivity_score,
        avg_sentence_length,
        percentage_complex_words,
        fog_index,
        avg_sentence_length,
        complex_word_count,
        word_count,
        syllable_per_word,
        personal_pronouns,
        avg_word_length
    ]


input_df = pd.read_excel('Input.xlsx')

output_data = []

for index, row in input_df.iterrows():

    url_id = row['URL_ID']
    url = row['URL']

    # Scraping
    article_text = extract_article(url)

    # Debug Checking
    if article_text.strip() == "":
        print(f"⚠️ No content extracted from URL_ID {url_id}")

    # Saving text file
    with open(f"{url_id}.txt", "w", encoding='utf-8') as f:
        f.write(article_text)

    # Analysis
    stats = analyze_text(article_text)

    output_data.append([url_id, url] + stats)

columns = [
    'URL_ID',
    'URL',
    'POSITIVE SCORE',
    'NEGATIVE SCORE',
    'POLARITY SCORE',
    'SUBJECTIVITY SCORE',
    'AVG SENTENCE LENGTH',
    'PERCENTAGE OF COMPLEX WORDS',
    'FOG INDEX',
    'AVG NUMBER OF WORDS PER SENTENCE',
    'COMPLEX WORD COUNT',
    'WORD COUNT',
    'SYLLABLE PER WORD',
    'PERSONAL PRONOUNS',
    'AVG WORD LENGTH'
]

output_df = pd.DataFrame(output_data, columns=columns)


output_df.to_excel('Output_Data_final_analysed.xlsx', index=False)
