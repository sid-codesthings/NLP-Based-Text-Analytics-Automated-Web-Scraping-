# Automated Web Scraping & NLP-Based Text Analysis

## Overview

This project implements an **automated data pipeline** that scrapes articles from multiple URLs and performs **Natural Language Processing (NLP) based text analytics** to compute linguistic and readability metrics.

The system extracts article content from web pages, processes the text using NLP techniques, and calculates **13 key sentiment and readability features** which are exported into a structured dataset.

---

## Features

* Automated **web scraping of article content from URLs**
* **HTML parsing and content extraction**
* **Text preprocessing and cleaning**
* **Stopword removal using multiple stopword dictionaries**
* **Dictionary-based sentiment analysis**
* Computation of **13 linguistic and readability metrics**
* Export of results to an **Excel dataset**

---

## Tech Stack

* Python
* pandas
* requests
* BeautifulSoup
* nltk
* regex

---

## Workflow

1. **Input Data**

   * URLs are provided through an Excel file (`Input.xlsx`).

2. **Web Scraping**

   * Each URL is accessed using HTTP requests.
   * HTML content is parsed using BeautifulSoup.
   * Article title and body text are extracted.

3. **Text Preprocessing**

   * Tokenization using NLTK.
   * Stopword filtering using multiple stopword dictionaries.
   * Cleaning of non-alphabetic tokens.

4. **Sentiment Analysis**

   * Uses predefined **positive and negative word dictionaries**.
   * Computes:

     * Positive Score
     * Negative Score
     * Polarity Score
     * Subjectivity Score

5. **Readability & Linguistic Metrics**
   The system calculates the following metrics:

   * Positive Score
   * Negative Score
   * Polarity Score
   * Subjectivity Score
   * Average Sentence Length
   * Percentage of Complex Words
   * Fog Index
   * Average Words per Sentence
   * Complex Word Count
   * Word Count
   * Syllables per Word
   * Personal Pronouns
   * Average Word Length

6. **Output Generation**

   * Extracted article text is saved as `.txt` files.
   * Final analytics results are exported to:

     ```
     Output_Data_submission_final.xlsx
     ```

---

## Project Structure

```
project/
│
├── Input.xlsx
├── Code.py
├── positive-words.txt
├── negative-words.txt
├── StopWords_Auditor.txt
├── StopWords_Currencies.txt
├── StopWords_DatesandNumbers.txt
├── StopWords_Generic.txt
├── StopWords_GenericLong.txt
├── StopWords_Geographic.txt
├── StopWords_Names.txt
│
├── extracted_articles/
│   ├── 1.txt
│   ├── 2.txt
│   └── ...
│
└── Output_Data_final_analysed.xlsx
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/your-username/repository-name.git
cd repository-name
```

Install required dependencies

```bash
pip install pandas requests beautifulsoup4 nltk openpyxl
```

Download required NLTK tokenizer

```python
import nltk
nltk.download('punkt')
```

---

## How to Run

```bash
python Code.py
```

The script will:

1. Read URLs from `Input.xlsx`
2. Scrape article text
3. Perform NLP analysis
4. Save extracted text files
5. Generate the final Excel output

---

## Output Example

The final output file contains sentiment and readability metrics for each article URL.

| URL_ID | POSITIVE SCORE | NEGATIVE SCORE | POLARITY SCORE | FOG INDEX |
| ------ | -------------- | -------------- | -------------- | --------- |
| 1      | 35             | 10             | 0.55           | 12.3      |

---

## Applications

* Content sentiment analysis
* Readability analysis of articles
* Automated content analytics
* NLP research and experimentation
* Data pipelines for text processing

---

## Author

Siddhartha Sen

---
