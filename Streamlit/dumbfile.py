df['cleaned_teaching'] = [spell_check(preprocess_text(text)) for text in df['teaching']]
            df['teaching_score'] = df['cleaned_teaching'].apply(analyze_vader)
            df['teaching_sentiment'] = df['teaching_score'].apply(analyze)

            df['cleaned_coursecontent'] = [spell_check(preprocess_text(text)) for text in df['coursecontent']]
            df['course_score'] = df['cleaned_coursecontent'].apply(analyze_vader)
            df['course_sentiment'] = df['course_score'].apply(analyze)

            df['cleaned_examination'] = [spell_check(preprocess_text(text)) for text in df['examination']]
            df['exam_score'] = df['cleaned_examination'].apply(analyze_vader)
            df['exam_sentiment'] = df['exam_score'].apply(analyze)

            df['cleaned_labwork'] = [spell_check(preprocess_text(text)) for text in df['labwork']]
            df['labwork_score'] = df['cleaned_labwork'].apply(analyze_vader)
            df['labwork_sentiment'] = df['labwork_score'].apply(analyze)

            df['cleaned_library'] = [spell_check(preprocess_text(text)) for text in df['libraryfacilities']]
            df['library_score'] = df['cleaned_library'].apply(analyze_vader)
            df['library_sentiment'] = df['library_score'].apply(analyze)

            df['cleaned_extracurricular'] = [spell_check(preprocess_text(text)) for text in df['extracurricular']]
            df['curricular_score'] = df['cleaned_extracurricular'].apply(analyze_vader)
            df['curricular_sentiment'] = df['curricular_score'].apply(analyze)



def save_data_to_database(df, table_name, connection):
    try:
        cursor = connection.cursor()

        # Create the table if it doesn't exist
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            teaching TEXT,
            teaching_score FLOAT,
            teaching_sentiment VARCHAR(255),
            coursecontent TEXT,
            course_score FLOAT,
            course_sentiment VARCHAR(255),
            examination TEXT,
            exam_score FLOAT,
            exam_sentiment VARCHAR(255),
            labwork TEXT,
            labwork_score FLOAT,
            labwork_sentiment VARCHAR(255),
            libraryfacilities TEXT,
            library_score FLOAT,
            library_sentiment VARCHAR(255),
            extracurricular TEXT,
            curricular_score FLOAT,
            curricular_sentiment VARCHAR(255)                        
        )
        """

        cursor.execute(create_table_query)

        # Prepare the data for insertion
        data_to_save = df[['teaching', 'teaching_score', 'teaching_sentiment', 
                           'coursecontent', 'course_score', 'course_sentiment', 
                           'examination', 'exam_score', 'exam_sentiment', 
                           'labwork', 'labwork_score', 'labwork_sentiment', 
                           'libraryfacilities', 'library_score', 'library_sentiment', 
                           'extracurricular', 'curricular_score', 'curricular_sentiment']].values.tolist()

        # Insert data into the table
        insert_query = f"""
        INSERT INTO {table_name} (teaching, teaching_score, teaching_sentiment, 
                           coursecontent, course_score, course_sentiment, 
                           examination, exam_score, exam_sentiment, 
                           labwork, labwork_score, labwork_sentiment, 
                           libraryfacilities, library_score, library_sentiment, 
                           extracurricular, curricular_score, curricular_sentiment)
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




with col2:
                # Show Positive Comment
                for sentiment_key, sentiment_df in teaching_data.items():
                    # Show Positive Comment
                    if sentiment_key == "teaching_sentiment" and "Positive" in sentiment_df["teaching_sentiment"].values:
                        # Get rows with Positive sentiment
                        positive_rows = sentiment_df[sentiment_df["teaching_sentiment"] == "Positive"]["teaching"].reset_index(drop=True)
                        
                        num_positive_rows = len(positive_rows)
                        
                        if num_positive_rows > 0:
                            st.write(f'<div class="custom-font" style="padding-top: 380px;">Number of Positive sentiment:</div>', unsafe_allow_html=True)
                            st.write(f'Number of rows with Positive sentiment: {num_positive_rows}')
                            st.write(positive_rows)
                        else:
                            st.write("-")
            
            with col3:
                # Show Neutral Comment
                for sentiment_key, sentiment_df in teaching_data.items():
                    # Show Neutral Comment
                    if sentiment_key == "teaching_sentiment" and "Neutral" in sentiment_df["teaching_sentiment"].values:
                        # Get rows with Neutral sentiment
                        neutral_rows = sentiment_df[sentiment_df["teaching_sentiment"] == "Neutral"]["teaching"].reset_index(drop=True)
                        
                        num_neutral_rows = len(neutral_rows)
                        
                        if num_neutral_rows > 0:
                            st.write(f'<div class="custom-font" style="padding-top: 380px;">Number of Neutral sentiment:</div>', unsafe_allow_html=True)
                            st.write(f'Number of rows with Neutral sentiment: {num_neutral_rows}')
                            st.write(neutral_rows)
                        else:
                            st.write("-")





For Donut chart:
# Create a donut chart with the number in the center
                fig = px.pie(
                    values=[num_negative, len(teaching_data["teaching"]) - num_negative],
                    names=["Negative", "Positive"],
                    hole=0.6,  # Set hole to create a donut
                    title=f"Teaching Sentiments ({num_negative} Negative)",
                    color_discrete_sequence=["green", "lightgreen"],  # Set colors
                )

                # Customize the layout
                fig.update_layout(
                    annotations=[dict(text=str(num_negative), showarrow=False, font_size=20)],
                    showlegend=False,  # Hide legend
                )

                # Display the donut chart
                st.plotly_chart(fig, use_container_width=True)



    