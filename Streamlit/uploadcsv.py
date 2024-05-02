from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import pandas as pd
import streamlit as st
from spellchecker import SpellChecker

import plotly.express as px
import plotly.graph_objects as go

import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import mysql.connector

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

# Define a function to save data to the database
def save_data_to_database(df, table_name, connection):
    try:
        cursor = connection.cursor()

        # Create the table if it doesn't exist
        #create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY,"
        #for column in df.columns:
        #    create_table_query += f"{column} TEXT, {column}_score FLOAT, {column}_sentiment VARCHAR(255),"
        #create_table_query = create_table_query[:-1] + ")"  # Remove the last comma and add closing parenthesis
        #cursor.execute(create_table_query)

        # Prepare the data for insertion
        data_to_save = df[['teaching', 'teaching_score', 'teaching_sentiment', 
                           'coursecontent', 'coursecontent_score', 'coursecontent_sentiment', 
                           'examination', 'examination_score', 'examination_sentiment', 
                           'labwork', 'labwork_score', 'labwork_sentiment', 
                           'libraryfacilities', 'libraryfacilities_score', 'libraryfacilities_sentiment', 
                           'extracurricular', 'extracurricular_score', 'extracurricular_sentiment']].values.tolist()

        # Insert data into the table
        insert_query = f"""
        INSERT INTO {table_name} (teaching, teaching_score, teaching_sentiment, 
                           coursecontent, coursecontent_score, coursecontent_sentiment, 
                           examination, examination_score, examination_sentiment, 
                           labwork, labwork_score, labwork_sentiment, 
                           libraryfacilities, libraryfacilities_score, libraryfacilities_sentiment, 
                           extracurricular, extracurricular_score, extracurricular_sentiment)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, data_to_save)

        # Commit the changes
        connection.commit()
        st.success("Data has been saved to the database.")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()

# Function to analyze sentiment using Vader
def analyze_vader(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    
    return compound_score


def main():
    st.header('Sentiment Analyzer')

    # Check if the polarity score threshold
    def analyze(compound_score):
        threshold = 0.15  # threshold/boundaries
        return 'Positive' if compound_score >= threshold else ('Negative' if compound_score <= -threshold else 'Neutral')
        
    st.write('<div class="custom-font">Analyze csv: </div>', unsafe_allow_html=True)
    upl = st.file_uploader('Upload file')

    def analyze_aspect(df, column_name):
        df[f'cleaned_{column_name}'] = [spell_check(preprocess_text(text)) for text in df[column_name]]
        df[f'{column_name}_score'] = df[f'cleaned_{column_name}'].apply(analyze_vader)
        df[f'{column_name}_sentiment'] = df[f'{column_name}_score'].apply(analyze)

    # Upload csv
    if upl:
        # Check if the file is a CSV
        progress_bar = st.progress(0)  # Initialize progress bar

        # Read the file in chunks to update the progress bar
        df_chunks = pd.read_csv(upl, encoding='latin-1', chunksize=1000)
        df = pd.concat([chunk for chunk in df_chunks])

        progress_bar.progress(10)
        # Display total number of rows
        st.write(f"Total Number of Rows: {len(df)}")

        progress_bar.progress(25)
        aspects = ["teaching", "coursecontent", "examination", "labwork", "libraryfacilities", "extracurricular"]

        # Initialize counts for each sentiment
        sentiment_counts = {"Positive": [], "Negative": [], "Neutral": []}

        for aspect in aspects:
            analyze_aspect(df, aspect)
            # Count sentiments for the current aspect
            sentiment_distribution = df[f'{aspect}_sentiment'].value_counts()
            # Update the counts
            sentiment_counts["Positive"].append(sentiment_distribution.get("Positive", 0))
            sentiment_counts["Negative"].append(sentiment_distribution.get("Negative", 0))
            sentiment_counts["Neutral"].append(sentiment_distribution.get("Neutral", 0))

        # Create a clustered column bar chart
        fig = go.Figure()

        for sentiment, counts in sentiment_counts.items():
            fig.add_trace(go.Bar(
                x=aspects,
                y=counts,
                name=sentiment,
            ))
        fig.update_layout(
            barmode='group',
            title='Sentiment Distribution for Each Aspect',
            xaxis=dict(title='Aspects'),
            yaxis=dict(title='Count'),
        )
        st.plotly_chart(fig, use_container_width=True)


        progress_bar.progress(65)

        for aspect in aspects:
            st.subheader(f'{aspect.capitalize()} Analysis')
            st.write(df[[f'{aspect}', f'{aspect}_score', f'{aspect}_sentiment']].head(10))

        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)

        progress_bar.progress(80)

        # Save to Database
        table_name = "allsentiment"
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", 
            database="stud_feedback"
        )
        save_data_to_database(df, table_name, db_connection)
        db_connection.close()

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='sentiment.csv',
            mime='text/csv',
        )

        # Update progress bar to 100% after file upload is complete
        progress_bar.progress(100)
        
if __name__ == "__main__":
    main()
