import mysql.connector
import os
import webbrowser


def database_connect_function():
    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(
        host="srv735.hstgr.io",
        user="u152993259_stat02",
        password="1234_@*Ab*@_4321",
        database="u152993259_stat02"
    )

    return connection


# Open file
def open_file(file_object, file_name):
    # Create the "temp" directory if it doesn't exist
    os.makedirs("temp", exist_ok=True)

    # Write file data to a temporary file
    temp_file_path = os.path.join("temp", file_name)
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_object.read())

    # Open the temporary file
    webbrowser.open(temp_file_path)


def check_ability(user_datas, cursor):
    # Get user information based on user_datas
    query = "SELECT * FROM users WHERE mail = %s"
    cursor.execute(query, (user_datas,))
    result = cursor.fetchone()

    return result[5]
