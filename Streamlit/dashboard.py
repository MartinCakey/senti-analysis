import streamlit as st
import pandas as pd # read csv, df manipulation
import plotly.express as px # interactive charts
import plotly.graph_objects as go # interactive graph
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt # Horizontal bar chart
from textblob import TextBlob
import re
from collections import Counter
import mysql.connector

# connect to database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "stud_feedback"
}

def fetch_aspect():
    try:
        # Establish a database connection
        db_connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )

        aspectdata = {}

        # Create a cursor object to execute SQL queries
        cursor = db_connection.cursor()

        # SQL query to select all data from the table
        query = f"SELECT * FROM aspect_word WHERE aspect IS NOT NULL AND aspect != ''"
        aspectdata['aspect'] = pd.read_sql(query, db_connection)

        db_connection.close()

        return aspectdata

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

# Function to display bar chart for aspect word frequencies
def display_aspect_word_chart(aspect_df, aspect_column):
    fig = px.bar(aspect_df, x=aspect_column, title=f"Aspect Word Frequencies for {aspect_column}")
    st.plotly_chart(fig, use_container_width=True)

# Function to display bar chart for top N words
def display_top_n_words_chart(sentiment_df, n, sentiment_type):
    comments = " ".join(sentiment_df[sentiment_df["analysis"] == sentiment_type]["cleaned_text"])
    words = pd.Series(comments.split())
    top_words = words.value_counts().head(n)

    fig = px.bar(top_words, x=top_words.index, y=top_words.values, title=f"Top {n} Words for {sentiment_type} Sentiment")
    st.plotly_chart(fig, use_container_width=True)

def fetch_all_data():
    try:
        # Establish a database connection
        db_connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        data = {}
        # Create a cursor object to execute SQL queries
        cursor = db_connection.cursor()

        # SQL query to select all data from the table
        query = "SELECT * FROM allsentiment"
        data["senti"] = pd.read_sql(query, db_connection)

        db_connection.close()

        return data

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

    try:
        # Establish a database connection
        db_connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        data = {}
        # Create a cursor object to execute SQL queries
        cursor = db_connection.cursor()

        db_connection.close()

        return data

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

# main features of dashboard
def display_top_sentences(categories):
    try:
        # Establish a database connection
        db_connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        # Create a cursor object to execute SQL queries
        cursor = db_connection.cursor()

        # Initialize lists to store the top and least sentences
        top_sentences_data = []
        least_sentences_data = []

        for category in categories:
            # SQL query to select the top positive sentence for each category based on the score
            top_query = f"""
                SELECT {category}, {category}_score
                FROM allsentiment
                ORDER BY {category}_score DESC
                LIMIT 1
            """
            # SQL query to select the top negative sentence for each category based on the score
            least_query = f"""
                SELECT {category}, {category}_score
                FROM allsentiment
                ORDER BY {category}_score
                LIMIT 1
            """
            # Execute the queries
            cursor.execute(top_query)
            top_sentence_data = cursor.fetchone()
            top_sentences_data.append(top_sentence_data)

            cursor.execute(least_query)
            least_sentence_data = cursor.fetchone()
            least_sentences_data.append(least_sentence_data)

        db_connection.close()

        # Create a list of column names
        columns = ["Sentence", "Score"]

        # Create a list of data rows for top sentences
        top_rows = [columns] + [list(row) for row in top_sentences_data]

        # Create a list of data rows for least sentences
        least_rows = [columns] + [list(row) for row in least_sentences_data]

        # Display top 10
        st.header("Top Positive Sentences based on Overall Score")
        st.table(top_rows)
        st.header("Top Negative Sentences based on Overall Score")
        st.table(least_rows)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

def display_ten_sentences(categories):
    try:
        # Establish a database connection
        db_connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )

        # Create a cursor object to execute SQL queries
        cursor = db_connection.cursor()

        # Initialize lists to store the top and least sentences
        top_ten_sentences_data = []
        least_ten_sentences_data = []

        for category in categories:
            # SQL query to select the top positive sentence for each category based on the score
            top_query = f"""
                SELECT {category}, {category}_score
                FROM allsentiment
                ORDER BY {category}_score DESC
                LIMIT 10
            """
            # SQL query to select the top negative sentence for each category based on the score
            least_query = f"""
                SELECT {category}, {category}_score
                FROM allsentiment
                ORDER BY {category}_score
                LIMIT 10
            """

            # Execute the queries
            cursor.execute(top_query)
            top_ten_sentences_data += cursor.fetchall()

            cursor.execute(least_query)
            least_ten_sentences_data += cursor.fetchall()

        db_connection.close()

        # Create a list of column names
        columns = ["Sentence", "Score"]

        # Create a list of data rows for top sentences
        top_rows = [columns] + [list(row) for row in top_ten_sentences_data]

        # Create a list of data rows for least sentences
        least_rows = [columns] + [list(row) for row in least_ten_sentences_data]

        # Display top 10
        st.header("Top 10 Positive Sentences")
        st.table(top_rows)
        st.header("Top 10 Negative Sentences")
        st.table(least_rows)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

def display_horizontal_chart(aspects):
    # Count the frequency of each aspect
        aspect_counts = Counter(aspects)

        # Display the top N aspects in an interactive chart
        top_n = 10
        top_aspects = aspect_counts.most_common(top_n)
        top_aspects_df = pd.DataFrame(top_aspects, columns=['Aspect', 'Frequency'])

        
        # Display the bar chart
        st.title("Frequent Aspect")
         # Create an Altair chart
        chart = alt.Chart(top_aspects_df).mark_bar().encode(
            x='Frequency:Q',
            y=alt.Y('Aspect:N', sort='-x'),
            color='Aspect:N',
            tooltip=['Aspect:N', 'Frequency:Q']
        ).properties(
            width=600,
            height=400
        )

        # Display the Altair chart using Streamlit
        st.altair_chart(chart, use_container_width=True)

def display_semi_circle(avgs):
    average_score = avgs
    # Create a semi-circle donut chart
    fig = go.Figure(go.Pie(
        values=[average_score, 100 - average_score],
        hole=0.6,
        labels=["Average Score", ""],
        marker=dict(colors=["#00cc00", "white"]),  # Green color for the average score
    ))

    # Customize the layout
    fig.update_layout(
        title=dict(text="Average Sentiment Score", font=dict(size=24)),
        showlegend=False,  # Disable legend
    )

    # Display the semi-circle donut chart
    st.plotly_chart(fig, use_container_width=True)

def display_histogram(score):
    # Create a histogram using Plotly Express
    fig = px.histogram(x=score, nbins=20, labels={'x': 'Sentiment Score', 'y': 'Frequency'},
                       title='Sentiment Score Distribution', color_discrete_sequence=['#00cc00'])

    # Customize the layout
    fig.update_layout(
        bargap=0.05,  # Gap between bars
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
    )

    # Display the histogram
    st.plotly_chart(fig, use_container_width=True)

def display_comparison(score,aspects):
    data = fetch_all_data()
    # Create a DataFrame for comparison
    comparison_data = pd.DataFrame({
        "Teaching": score,
        **{aspect: data["senti"][f"{aspect}_score"] for aspect in aspects}
    })

    # Plot box plot for comparison
    box_plot = alt.Chart(comparison_data.melt(id_vars=['Teaching']),
                        title=" ").mark_boxplot().encode(
        x='variable:N',
        y='value:Q',
        color=alt.Color('variable:N', legend=None),
        tooltip=['variable', 'value']
    ).properties(width=600, height=400)

    st.altair_chart(box_plot, use_container_width=True)  

def preprocess_text(text):
    # Preprocess the text (you can customize this based on your needs)
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    return text

def extract_aspects(text):
    # Use TextBlob to perform sentiment analysis and extract aspects
    blob = TextBlob(text)
    aspects = [str(chunk) for sentence in blob.sentences for chunk in sentence.noun_phrases]

    return aspects

def main():

    st.header("Sentimental Analysis Dashboard")

    # Define a green container style
    green_container_style = 'background-color: #00cc00; padding: 10px; margin: 10px; border-radius: 10px;'
    red_container_style = 'background-color: #FF2A2A; padding: 10px; margin: 10px; border-radius: 10px;'
    grey_container_style = 'background-color: #A2A2A2; padding: 10px; margin: 10px; border-radius: 10px;'
    black_container_style = 'background-color: black; padding: 10px; margin: 10px; border-radius: 10px;'

    # Overall result
    def display_overall():

         # Fetch all rows from the result set
        data_dict = fetch_all_data()
        aspect_dict = fetch_aspect()

        col1, col2 = st.columns(2)

        if data_dict and "senti" in data_dict:
            # Calculate sentiment counts based on the database data
            sentiment_columns = ["teaching_sentiment", "coursecontent_sentiment", "examination_sentiment",
                                "labwork_sentiment", "libraryfacilities_sentiment", "extracurricular_sentiment"]

            sentiment_counts = pd.concat([data_dict["senti"][column].value_counts() for column in sentiment_columns])

            # number of rows in data (to count feedback)
            num_rows = len(data_dict["senti"])
            with col1:
                st.write('<div class="custom-font" style="padding-bottom: 100px;">Numbers of Feedbacks: </div>', unsafe_allow_html=True)
                st.write(f'<div class="custom-font">{num_rows}</div>', unsafe_allow_html=True)

            with col2:
                # Create a pie chart based on the calculated sentiment counts
                data = {
                    "Sentiment": sentiment_counts.index,
                    "Count": sentiment_counts.values
                }

                df = pd.DataFrame(data)

                # Calculate percentages
                total_count = df["Count"].sum()
                df["Percentage"] = (df["Count"] / total_count) * 100

                # Create a pie chart using Plotly Express
                fig = px.pie(df, values="Count", names="Sentiment", labels={"Count": "Sentiment Count"}, title="Overall Sentiment")

                # Customize the layout
                fig.update_layout(
                    font=dict(family="Arial, sans-serif", size=18),
                    title=dict(text="Overall Sentiment", font=dict(size=24)),
                    showlegend=True,  # legend
                )

                # Display the pie chart
                st.plotly_chart(fig, use_container_width=True)

            # Initialize counts for each sentiment
            sentiment_counts = {"Positive": [], "Negative": [], "Neutral": []}

            # Define aspects
            aspects = ["teaching", "coursecontent", "examination", "labwork", "libraryfacilities", "extracurricular"]

            # sentiment_distribution
            for aspect in aspects:
                # Count sentiments for the current aspect
                sentiment_distribution = data_dict["senti"][f'{aspect}_sentiment'].value_counts()

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
                title=dict(text="Sentiment Distribution for Each Category", font=dict(size=24)),
                xaxis=dict(title='Category'),
                yaxis=dict(title='Count'),
            )

            # Display the chart
            st.plotly_chart(fig, use_container_width=True)

        if aspect_dict and "sentiment" in data_dict:
            with col1:
                # Show Negative Comment
                for sentiment_key, sentiment_df in data_dict.items():
                    # Show Negative Comment
                    if sentiment_key == "sentiment" and "Negative" in sentiment_df["analysis"].values:
                        # Get rows with Negative sentiment
                        negative_rows = sentiment_df[sentiment_df["analysis"] == "Negative"]["cleaned_text"].reset_index(drop=True)
                    
                        if not negative_rows.empty:
                            st.write(f'<div class="custom-font" style="padding-top: 380px;">Data for {sentiment_key} with Negative sentiment:</div>', unsafe_allow_html=True)
                            st.write(negative_rows)
                        else:
                            st.write("No rows with Negative sentiment found.")
                    
                    
            with col2:
                # Show Positive Comment
                for sentiment_key, sentiment_df in data_dict.items():
                    if sentiment_key == "sentiment" and "Positive" in sentiment_df["analysis"].values:
                        # Get rows with Positive sentiment
                        positive_rows = sentiment_df[sentiment_df["analysis"] == "Positive"]["cleaned_text"].reset_index(drop=True)
                        
                        # Filter rows with more than one word
                        positive_rows = positive_rows[positive_rows.apply(lambda x: len(x.split()) > 1)]
                        
                        if not positive_rows.empty:
                            st.write(f'<div class="custom-font" style="padding-top: 100px;">Data for {sentiment_key} with Positive sentiment:</div>', unsafe_allow_html=True)
                            st.write(positive_rows)
                        else:
                            st.write("No or only one row with Positive sentiment found.")

        if aspect_dict:
            display_aspect_word_chart(aspect_dict["aspect"], "aspect")    
        
        # Define the categories
        categories = ["teaching", "coursecontent", "examination", "labwork", "libraryfacilities", "extracurricular"]
        display_top_sentences(categories)

    # teaching
    def display_teaching():
        st.write('<div class="custom-font">Sentiment Category: Teaching </div>', unsafe_allow_html=True)
        # Fetch teaching data
        teaching_data = fetch_all_data()
        # set columns
        col1, col2, col3 = st.columns(3)
        with col1:
            # Display the number of Positive sentiments in the "teaching_sentiment" column
            if "senti" in teaching_data and "teaching_sentiment" in teaching_data["senti"]:
                num_positive = (teaching_data["senti"]["teaching_sentiment"] == "Positive").sum()
                st.markdown(
                    f'<div style="{green_container_style}"><div class="custom-font">Numbers of Positive: </div>'
                    f'<div class="custom-font">{num_positive}</div></div>',
                    unsafe_allow_html=True
                )
        with col2:
            # Display the number of negative sentiments in the "teaching_sentiment" column
            if "senti" in teaching_data and "teaching_sentiment" in teaching_data["senti"]:
                num_negative = (teaching_data["senti"]["teaching_sentiment"] == "Negative").sum()
                st.markdown(
                    f'<div style="{red_container_style}"><div class="custom-font">Numbers of Negative: </div>'
                    f'<div class="custom-font">{num_negative}</div></div>',
                    unsafe_allow_html=True
                )
        with col3:
            # Display the number of Neutral sentiments in the "teaching_sentiment" column
            if "senti" in teaching_data and "teaching_sentiment" in teaching_data["senti"]:
                num_neutral = (teaching_data["senti"]["teaching_sentiment"] == "Neutral").sum()
                st.markdown(
                    f'<div style="{grey_container_style}"><div class="custom-font">Numbers of Neutral: </div>'
                    f'<div class="custom-font">{num_neutral}</div></div>',
                    unsafe_allow_html=True
                )

        if "senti" in teaching_data and "teaching_score" in teaching_data["senti"]:
            teaching_score = teaching_data["senti"]["teaching_score"]
            average_score = teaching_score.mean()
            max_score = teaching_score.max()
            min_score = teaching_score.min()

        with col1:
            # Calculate the average sentiment score
            st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Average Score: </div>'
                    f'<div class="custom-font">{average_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )
        with col2:
            # Calculate max scores
            st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Maximum Score: </div>'
                    f'<div class="custom-font">{max_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )
        with col3:
            # Calculate min scores
            st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Minimum Score: </div>'
                    f'<div class="custom-font">{min_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )

        # Extract aspects from sentences
        all_aspects = []
        for sentence in teaching_data["senti"]["teaching"]:
            preprocessed_sentence = preprocess_text(sentence)
            aspects = extract_aspects(preprocessed_sentence)
            all_aspects.extend(aspects)

        # Display the aspect frequency
        display_horizontal_chart(all_aspects)
       
        # Distribution of Sentiment Scores
        st.subheader("Distribution of Sentiment Scores")
        display_histogram(teaching_score)

        # Comparison with Other Aspects
        st.subheader("Comparison with Other Aspects")
        # Select aspects to compare
        aspects_to_compare = ["coursecontent", "examination", "labwork", "libraryfacilities", "extracurricular"]
        display_comparison(teaching_score, aspects_to_compare)

        # Define the categories
        categories = ["teaching"]
        display_ten_sentences(categories)

    # course content                
    def display_course():
        st.write('<div class="custom-font">Sentiment Category: Course content </div>', unsafe_allow_html=True)

        # Fetch teaching data
        course_data = fetch_all_data()

        col1, col2, col3 = st.columns(3)

        with col1:
            # Display the number of Positive sentiments in the "coursecontent_sentiment" column
            if "senti" in course_data and "coursecontent_sentiment" in course_data["senti"]:
                num_positive = (course_data["senti"]["coursecontent_sentiment"] == "Positive").sum()
                st.markdown(
                    f'<div style="{green_container_style}"><div class="custom-font">Numbers of Positive: </div>'
                    f'<div class="custom-font">{num_positive}</div></div>',
                    unsafe_allow_html=True
                )
            
        with col2:
            # Display the number of negative sentiments in the "coursecontent_sentiment" column
            if "senti" in course_data and "coursecontent_sentiment" in course_data["senti"]:
                num_negative = (course_data["senti"]["coursecontent_sentiment"] == "Negative").sum()
                st.markdown(
                    f'<div style="{red_container_style}"><div class="custom-font">Numbers of Negative: </div>'
                    f'<div class="custom-font">{num_negative}</div></div>',
                    unsafe_allow_html=True
                )
                
        with col3:
            # Display the number of Neutral sentiments in the "coursecontent_sentiment" column
            if "senti" in course_data and "coursecontent_sentiment" in course_data["senti"]:
                num_neutral = (course_data["senti"]["coursecontent_sentiment"] == "Neutral").sum()
                st.markdown(
                    f'<div style="{grey_container_style}"><div class="custom-font">Numbers of Neutral: </div>'
                    f'<div class="custom-font">{num_neutral}</div></div>',
                    unsafe_allow_html=True
                )

        if "senti" in course_data and "coursecontent_score" in course_data["senti"]:
            coursecontent_score = course_data["senti"]["coursecontent_score"]
            average_score = coursecontent_score.mean()
            max_score = coursecontent_score.max()
            min_score = coursecontent_score.min()

        with col1:
            # Calculate the average sentiment score
                st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Average Score: </div>'
                    f'<div class="custom-font">{average_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )
        with col2:
            # Calculate max scores
            st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Maximum Score: </div>'
                    f'<div class="custom-font">{max_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )
        with col3:
            # Calculate min scores
            st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Minimum Score: </div>'
                    f'<div class="custom-font">{min_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )    

        # Extract aspects from sentences
        all_aspects = []
        for sentence in course_data["senti"]["coursecontent"]:
            preprocessed_sentence = preprocess_text(sentence)
            aspects = extract_aspects(preprocessed_sentence)
            all_aspects.extend(aspects)

        # Display the aspect frequency
        display_horizontal_chart(all_aspects)

        # Distribution of Sentiment Scores
        st.subheader("Distribution of Sentiment Scores")
        display_histogram(coursecontent_score)

        # Comparison with Other Aspects
        st.subheader("Comparison with Other Aspects")
        # Select aspects to compare
        aspects_to_compare = ["teaching", "examination", "labwork", "libraryfacilities", "extracurricular"]
        display_comparison(coursecontent_score, aspects_to_compare)

        # Define the categories
        categories = ["coursecontent"]
        display_ten_sentences(categories)

    # examination
    def display_examination():
        st.write('<div class="custom-font">Sentiment Category: Examination </div>', unsafe_allow_html=True)

        # Fetch examination data
        examination_data = fetch_all_data()

        col1, col2, col3 = st.columns(3)

        with col1:
            # Display the number of Positive sentiments in the "examination_sentiment" column
            if "senti" in examination_data and "examination_sentiment" in examination_data["senti"]:
                num_positive = (examination_data["senti"]["examination_sentiment"] == "Positive").sum()
                st.markdown(
                    f'<div style="{green_container_style}"><div class="custom-font">Numbers of Positive: </div>'
                    f'<div class="custom-font">{num_positive}</div></div>',
                    unsafe_allow_html=True
                )
            
        with col2:
            # Display the number of negative sentiments in the "examination_sentiment" column
            if "senti" in examination_data and "examination_sentiment" in examination_data["senti"]:
                num_negative = (examination_data["senti"]["examination_sentiment"] == "Negative").sum()
                st.markdown(
                    f'<div style="{red_container_style}"><div class="custom-font">Numbers of Negative: </div>'
                    f'<div class="custom-font">{num_negative}</div></div>',
                    unsafe_allow_html=True
                )
                
        with col3:
            # Display the number of Neutral sentiments in the "examination_sentiment" column
            if "senti" in examination_data and "examination_sentiment" in examination_data["senti"]:
                num_neutral = (examination_data["senti"]["examination_sentiment"] == "Neutral").sum()
                st.markdown(
                    f'<div style="{grey_container_style}"><div class="custom-font">Numbers of Neutral: </div>'
                    f'<div class="custom-font">{num_neutral}</div></div>',
                    unsafe_allow_html=True
                )    

        if "senti" in examination_data and "examination_score" in examination_data["senti"]:
            examination_score = examination_data["senti"]["examination_score"]
            average_score = examination_score.mean()
            max_score = examination_score.max()
            min_score = examination_score.min()

        with col1:
            # Calculate the average sentiment score
                st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Average Score: </div>'
                    f'<div class="custom-font">{average_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )
        with col2:
            # Calculate max scores
            st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Maximum Score: </div>'
                    f'<div class="custom-font">{max_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )
        with col3:
            # Calculate min scores
            st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Minimum Score: </div>'
                    f'<div class="custom-font">{min_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )

        # Extract aspects from sentences
        all_aspects = []
        for sentence in examination_data["senti"]["examination"]:
            preprocessed_sentence = preprocess_text(sentence)
            aspects = extract_aspects(preprocessed_sentence)
            all_aspects.extend(aspects)

        # Display the aspect frequency
        display_horizontal_chart(all_aspects)

        # Distribution of Sentiment Scores
        st.subheader("Distribution of Sentiment Scores")
        display_histogram(examination_score)

        # Comparison with Other Aspects
        st.subheader("Comparison with Other Aspects")
        # Select aspects to compare
        aspects_to_compare = ["teaching", "coursecontent", "labwork", "libraryfacilities", "extracurricular"]
        display_comparison(examination_score, aspects_to_compare)

        # Define the categories
        categories = ["examination"]
        display_ten_sentences(categories)

    # Labwork
    def display_labwork():
        st.write('<div class="custom-font">Sentiment Category: Labwork </div>', unsafe_allow_html=True)

        # Fetch labwork data
        labwork_data = fetch_all_data()

        col1, col2, col3 = st.columns(3)

        with col1:
            # Display the number of Positive sentiments in the "labwork_sentiment" column
            if "senti" in labwork_data and "labwork_sentiment" in labwork_data["senti"]:
                num_positive = (labwork_data["senti"]["labwork_sentiment"] == "Positive").sum()
                st.markdown(
                    f'<div style="{green_container_style}"><div class="custom-font">Numbers of Positive: </div>'
                    f'<div class="custom-font">{num_positive}</div></div>',
                    unsafe_allow_html=True
                )
            
        with col2:
            # Display the number of negative sentiments in the "labwork_sentiment" column
            if "senti" in labwork_data and "labwork_sentiment" in labwork_data["senti"]:
                num_negative = (labwork_data["senti"]["labwork_sentiment"] == "Negative").sum()
                st.markdown(
                    f'<div style="{red_container_style}"><div class="custom-font">Numbers of Negative: </div>'
                    f'<div class="custom-font">{num_negative}</div></div>',
                    unsafe_allow_html=True
                )
                
        with col3:
            # Display the number of Neutral sentiments in the "labwork_sentiment" column
            if "senti" in labwork_data and "labwork_sentiment" in labwork_data["senti"]:
                num_neutral = (labwork_data["senti"]["labwork_sentiment"] == "Neutral").sum()
                st.markdown(
                    f'<div style="{grey_container_style}"><div class="custom-font">Numbers of Neutral: </div>'
                    f'<div class="custom-font">{num_neutral}</div></div>',
                    unsafe_allow_html=True
                )

        if "senti" in labwork_data and "labwork_score" in labwork_data["senti"]:
            labwork_score = labwork_data["senti"]["labwork_score"]
            average_score = labwork_score.mean()
            max_score = labwork_score.max()
            min_score = labwork_score.min()

        with col1:
            # Calculate the average sentiment score
                st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Average Score: </div>'
                    f'<div class="custom-font">{average_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )
        with col2:
            # Calculate max scores
            st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Maximum Score: </div>'
                    f'<div class="custom-font">{max_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )
        with col3:
            # Calculate min scores
            st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Minimum Score: </div>'
                    f'<div class="custom-font">{min_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )

        # Extract aspects from sentences
        all_aspects = []
        for sentence in labwork_data["senti"]["labwork"]:
            preprocessed_sentence = preprocess_text(sentence)
            aspects = extract_aspects(preprocessed_sentence)
            all_aspects.extend(aspects)

        # Display the aspect frequency
        display_horizontal_chart(all_aspects)

        # Distribution of Sentiment Scores
        st.subheader("Distribution of Sentiment Scores")
        display_histogram(labwork_score)

        # Comparison with Other Aspects
        st.subheader("Comparison with Other Aspects")
        # Select aspects to compare
        aspects_to_compare = ["teaching", "examination", "examination", "libraryfacilities", "extracurricular"]
        display_comparison(labwork_score, aspects_to_compare)

        # Define the categories
        categories = ["labwork"]
        display_ten_sentences(categories)

    # Library Facilities
    def display_library():
        st.write('<div class="custom-font">Sentiment Category: Library </div>', unsafe_allow_html=True)

        # Fetch libraryfacilities data
        library_data = fetch_all_data()

        col1, col2, col3 = st.columns(3)

        with col1:
            # Display the number of Positive sentiments in the "libraryfacilities_sentiment" column
            if "senti" in library_data and "libraryfacilities_sentiment" in library_data["senti"]:
                num_positive = (library_data["senti"]["libraryfacilities_sentiment"] == "Positive").sum()
                st.markdown(
                    f'<div style="{green_container_style}"><div class="custom-font">Numbers of Positive: </div>'
                    f'<div class="custom-font">{num_positive}</div></div>',
                    unsafe_allow_html=True
                )
            
        with col2:
            # Display the number of negative sentiments in the "libraryfacilities_sentiment" column
            if "senti" in library_data and "libraryfacilities_sentiment" in library_data["senti"]:
                num_negative = (library_data["senti"]["libraryfacilities_sentiment"] == "Negative").sum()
                st.markdown(
                    f'<div style="{red_container_style}"><div class="custom-font">Numbers of Negative: </div>'
                    f'<div class="custom-font">{num_negative}</div></div>',
                    unsafe_allow_html=True
                )
                
        with col3:
            # Display the number of Neutral sentiments in the "libraryfacilities_sentiment" column
            if "senti" in library_data and "libraryfacilities_sentiment" in library_data["senti"]:
                num_neutral = (library_data["senti"]["libraryfacilities_sentiment"] == "Neutral").sum()
                st.markdown(
                    f'<div style="{grey_container_style}"><div class="custom-font">Numbers of Neutral: </div>'
                    f'<div class="custom-font">{num_neutral}</div></div>',
                    unsafe_allow_html=True
                )  

        if "senti" in library_data and "libraryfacilities_score" in library_data["senti"]:
            libraryfacilities_score = library_data["senti"]["libraryfacilities_score"]
            average_score = libraryfacilities_score.mean()
            max_score = libraryfacilities_score.max()
            min_score = libraryfacilities_score.min()

        with col1:
            # Calculate the average sentiment score
                st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Average Score: </div>'
                    f'<div class="custom-font">{average_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )
        with col2:
            # Calculate max scores
            st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Maximum Score: </div>'
                    f'<div class="custom-font">{max_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )
        with col3:
            # Calculate min scores
            st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Minimum Score: </div>'
                    f'<div class="custom-font">{min_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )

        # Extract aspects from sentences
        all_aspects = []
        for sentence in library_data["senti"]["libraryfacilities"]:
            preprocessed_sentence = preprocess_text(sentence)
            aspects = extract_aspects(preprocessed_sentence)
            all_aspects.extend(aspects)

        # Display the aspect frequency
        display_horizontal_chart(all_aspects)

        # Distribution of Sentiment Scores
        st.subheader("Distribution of Sentiment Scores")
        display_histogram(libraryfacilities_score)

        # Comparison with Other Aspects
        st.subheader("Comparison with Other Aspects")
        # Select aspects to compare
        aspects_to_compare = ["teaching", "examination", "labwork", "labwork", "extracurricular"]
        display_comparison(libraryfacilities_score, aspects_to_compare)

        # Define the categories
        categories = ["libraryfacilities"]
        display_ten_sentences(categories)

    # Extracurricular
    def display_extracurricular():
        st.write('<div class="custom-font">Sentiment Category: Extracurricular </div>', unsafe_allow_html=True)

        # Fetch extracurricular data
        extracurricular_data = fetch_all_data()

        col1, col2, col3 = st.columns(3)

        with col1:
            # Display the number of Positive sentiments in the "extracurricular_sentiment" column
            if "senti" in extracurricular_data and "extracurricular_sentiment" in extracurricular_data["senti"]:
                num_positive = (extracurricular_data["senti"]["extracurricular_sentiment"] == "Positive").sum()
                st.markdown(
                    f'<div style="{green_container_style}"><div class="custom-font">Numbers of Positive: </div>'
                    f'<div class="custom-font">{num_positive}</div></div>',
                    unsafe_allow_html=True
                )
            
        with col2:
            # Display the number of negative sentiments in the "extracurricular_sentiment" column
            if "senti" in extracurricular_data and "extracurricular_sentiment" in extracurricular_data["senti"]:
                num_negative = (extracurricular_data["senti"]["extracurricular_sentiment"] == "Negative").sum()
                st.markdown(
                    f'<div style="{red_container_style}"><div class="custom-font">Numbers of Negative: </div>'
                    f'<div class="custom-font">{num_negative}</div></div>',
                    unsafe_allow_html=True
                )
                
        with col3:
            # Display the number of Neutral sentiments in the "extracurricular_sentiment" column
            if "senti" in extracurricular_data and "extracurricular_sentiment" in extracurricular_data["senti"]:
                num_neutral = (extracurricular_data["senti"]["extracurricular_sentiment"] == "Neutral").sum()
                st.markdown(
                    f'<div style="{grey_container_style}"><div class="custom-font">Numbers of Neutral: </div>'
                    f'<div class="custom-font">{num_neutral}</div></div>',
                    unsafe_allow_html=True
                )  

        if "senti" in extracurricular_data and "extracurricular_score" in extracurricular_data["senti"]:
            extracurricular_score = extracurricular_data["senti"]["extracurricular_score"]
            average_score = extracurricular_score.mean()
            max_score = extracurricular_score.max()
            min_score = extracurricular_score.min()

        with col1:
            # Calculate the average sentiment score
                st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Average Score: </div>'
                    f'<div class="custom-font">{average_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )
        with col2:
            # Calculate max scores
            st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Maximum Score: </div>'
                    f'<div class="custom-font">{max_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )
        with col3:
            # Calculate min scores
            st.markdown(
                    f'<div style="{black_container_style}"><div class="custom-font">Minimum Score: </div>'
                    f'<div class="custom-font">{min_score:.3f}</div></div>',
                    unsafe_allow_html=True
                )

        # Extract aspects from sentences
        all_aspects = []
        for sentence in extracurricular_data["senti"]["extracurricular"]:
            preprocessed_sentence = preprocess_text(sentence)
            aspects = extract_aspects(preprocessed_sentence)
            all_aspects.extend(aspects)

        # Display the aspect frequency
        display_horizontal_chart(all_aspects)

        # Distribution of Sentiment Scores
        st.subheader("Distribution of Sentiment Scores")
        display_histogram(extracurricular_score)

        # Comparison with Other Aspects
        st.subheader("Comparison with Other Aspects")
        # Select aspects to compare
        aspects_to_compare = ["teaching", "examination", "labwork", "libraryfacilities", "libraryfacilities"]
        display_comparison(extracurricular_score, aspects_to_compare)

        # Define the categories
        categories = ["extracurricular"]
        display_ten_sentences(categories)

    # Define Page
    sections = {
        "Overall Sentiment Result": display_overall,
        "Teaching": display_teaching,
        "Course Content": display_course,
        "Examination": display_examination,
        "Labwork": display_labwork,
        "Library Facilities": display_library,
        "Extracurrilular": display_extracurricular,
    }

    # Selectbox for the page selection
    selected_page = st.selectbox("Select a page:", list(sections.keys()))

    # Display the content based on the selected page
    sections[selected_page]()

 
if __name__ == "__main__":
    main()  