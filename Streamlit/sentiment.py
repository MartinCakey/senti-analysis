from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import pandas as pd
import streamlit as st
from spellchecker import SpellChecker

import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Function to handle contractions
def handle_contractions(text):
    contractions = {
        "n't": " not",
        "'s": " is",
        "'re": " are",
        "'ve": " have",
        "'d": " would",
        "'ll": " will",
        "'m": " am"
    }

    words = text.split()
    for i in range(len(words)):
        if words[i] in contractions:
            words[i] = contractions[words[i]]
    return ' '.join(words)

# Function to preprocess text data
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove URLs, hashtags, mentions, and special characters
    text = re.sub(r"http\S+|www\S+|@\w+|#\w+", "", text)
    text = re.sub(r"[^\w\s]", "", text)

    # Remove numbers/digits
    text = re.sub(r'\b[0-9]+\b\s*', '', text)
    #text = re.sub(r'\d+', '', text)

    # Remove punctuation
    text = ''.join([char for char in text if char not in string.punctuation])
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    stop_words.discard("not")
    stop_words.discard("no")
    stop_words.add("us")
    tokens = [token for token in tokens if token not in stop_words]
    
    # Convert to lowercase
    tokens = [token.lower() for token in tokens]
    # Handle contractions
    text = handle_contractions(' '.join(tokens))
    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in word_tokenize(text)]
    # Join tokens back into a single string
    processed_text = ' '.join(tokens)

    return processed_text

# Function to perform spell checking
def spell_check(text):
    spell = SpellChecker()
    words = word_tokenize(text)

    # Find misspelled words
    misspelled = spell.unknown(words)

    # Correct misspelled words
    corrected_text = [spell.correction(word) if word in misspelled else word for word in words]

    # Check for NoneType values and filter them out
    corrected_text = [word for word in corrected_text if word is not None]

    # Join the corrected words back into a sentence
    corrected_text = ' '.join(corrected_text)

    return corrected_text

# Function to analyze sentiment using Vader
def analyze_vader(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    
    return compound_score

def main():
    st.header('Sentiment Analyzer')

    # Check if the polarity score is above the threshold
    def analyze(compound_score):
        threshold = 0.15  # Adjust this threshold as needed
        return 'Positive' if compound_score >= threshold else ('Negative' if compound_score <= -threshold else 'Neutral')

    st.write('<div class="custom-font">Analyze Text: </div>', unsafe_allow_html=True)
    text = st.text_input('Text here:                     *current threshhold value 0.15')
     # Sentimental Analyzer
    if text:
        preprocessed_text = preprocess_text(text)
        compound_score = analyze_vader(preprocessed_text)
        blob = TextBlob(preprocessed_text)
        subjectivity = round(blob.sentiment.subjectivity, 2)
        sentiment = analyze(compound_score)  # Calculate sentiment label
        aspect_words = blob.noun_phrases

        st.write('Compound Score: ', compound_score)
        st.write('Subjectivity: ', subjectivity)
        st.write('Sentiment: ', sentiment)
        st.write('Aspect: ', aspect_words)

    # Clean text input
    pre = st.text_input('Clean Text: ')
    if pre:
        preprocessed_text = preprocess_text(pre)
        st.write(preprocessed_text)
        

if __name__ == "__main__":
    main()   