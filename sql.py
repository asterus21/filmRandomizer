import mysql.connector

from data import Films

configuration = {
    'user': 'root',
    'password': '123',
    'host': '127.0.0.1',
    'database': 'films'
}

FILMS = Films()
DATA = FILMS.GET_ONE_FROM_A_LIST_OF_FILMS

def get_data(data: tuple) -> dict:

    '''The function is used to create a dictionary from a tuple to insert into a database.'''

    records = [x for x in range(len(data))]
    movies = dict(zip(records, data))

    return movies

def main():

    movies = get_data(DATA)

    try:
        connection = mysql.connector.connect(**configuration)
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
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Connection closed.")

if __name__ == '__main__':
    main()
