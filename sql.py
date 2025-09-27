import mysql.connector
import sqlite3
import subprocess


def get_data_from_tuple(films: tuple) -> dict:

    '''The function is used to create a dictionary from a tuple to insert into a database.'''

    records = [x for x in range(len(films))]
    movies = dict(zip(records, films))

    return movies


def insert_data_into_database(data: dict, database_configuration: dict) -> None:

    '''The function accepts a dictionary and inserts its values into a database.'''

    movies = get_data_from_tuple(data)

    try:
        connection = mysql.connector.connect(**database_configuration)
        print("Successfully connected to the database!")
        cursor = connection.cursor(buffered=True)
        
        query = "INSERT INTO films.films (ID, FILM) VALUES (%s, %s)"
        
        for id, film in movies.items():
            try:
                cursor.execute(query, (id, film))
                print(f"Inserted: ID={id}, Film='{film}'")
            except mysql.connector.Error as err:
                print(f"Error inserting ID {id}: {err}")
        
        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: invalid credentials")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Error: database does not exist")
        else:
            print(err)
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Connection closed.")


def export_database(password: str):

    return subprocess.run(['mysqldump', '-u', 'root', f'-p{password}', 'films'], 
                         stdout=open('films.sql', 'w')).returncode


def convert_database(database_configuration: dict):
    # probably not correct
    converter = sqlite3(
        mysql_host=database_configuration['host'],
        mysql_user=database_configuration['user'],
        mysql_database=database_configuration['database'],
        mysql_password=database_configuration['password'],
        sqlite_file="films.db"
        )
    
    return converter.transfer()
