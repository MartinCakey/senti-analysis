import mysql.connector
import gspread
from oauth2client.service_account import ServiceAccountCredentials

    
# Connect to MySQL database
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", 
    database="stud_feedback"
)


# Connect to Google Sheets
scope = ["https://spreadsheets.google.com/StudentEducationFeedback", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("sentiment-student-feedback-c40ac0f0d4de.json", scope)
gs = gspread.authorize(credentials)
spreadsheet = gs.open("https://docs.google.com/spreadsheets/d/1P12vQjZgNYlFMg3R_wtePTpE4Sv1j65EQyatvCCyRa8/edit?usp=sharing")
worksheet = spreadsheet.get_worksheet(0)

# Fetch new responses and insert into MySQL
responses = worksheet.get_all_records()
for response in responses:
    cursor = mysql_conn.cursor()
    cursor.execute("INSERT INTO gsfeedback (teaching, coursecontent, examination, labwork, library_facilities, extracurricular, other)",
                   (response["teaching"], 
                    response["coursecontent"], 
                    response["examination"], 
                    response["labwork"], 
                    response["library_facilities"],
                    response["extracurricular"],
                    response["other"] ))
    mysql_conn.commit()

# Close connections
cursor.close()
mysql_conn.close()