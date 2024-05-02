import streamlit as st
import pandas as pd
import mysql.connector

# connect to database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "stud_feedback"
}

def fetch_all_data():
    data = {}

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

        # SQL query to select all data from the table
        query = "SELECT * FROM allsentiment"
        data["senti"] = pd.read_sql(query, db_connection)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

    return data

def main():
    st.header("All Feedback")
    data_dict = fetch_all_data()

    categories = ["teaching", "coursecontent", "examination", "labwork", "libraryfacilities", "extracurricular"]

    if data_dict and not data_dict["senti"].empty:
        # Sidebar filter for categories
        selected_categories = st.sidebar.multiselect("Select Categories", categories, default=categories)
        # filter for sentiment
        selected_sentiment = st.radio("Filter Sentiment by:", ["All", "Positive", "Negative", "Neutral"])

        # Initialize an empty DataFrame to store the final result
        result_data = pd.DataFrame()

        # Apply filters for each selected category
        for selected_category in selected_categories:
            # Apply category filter
            category_data = data_dict["senti"][[selected_category, f'{selected_category}_score', f'{selected_category}_sentiment']]

            # Apply sentiment filter
            if selected_sentiment != "All":
                category_data = category_data[category_data[f'{selected_category}_sentiment'] == selected_sentiment]

            # Append the filtered data to the result DataFrame
            result_data = pd.concat([result_data, category_data])

            # Display filtered data for each category
            st.subheader(f'{selected_category.capitalize()} Analysis ({selected_sentiment} Sentiment)')
            st.dataframe(category_data)
    else:
        st.warning("No data found.")

if __name__ == "__main__":
    main()