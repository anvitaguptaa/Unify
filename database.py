import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'HeartBeat'

TABLES = {}
TABLES['music_info'] = (
    "CREATE TABLE `music_info` ("
    " `song_id` int(11) AUTO_INCREMENT,"
    " `song_name` varchar(30),"
    " `energy` decimal(18, 9) ,"
    " `tempo` decimal(18, 9) ,"
    " `danceability` decimal(18, 9) ,"
    " `acousticness` decimal(18, 9) ,"
    " `instrumentalness` decimal(18, 9) ,"
    " `liveness` decimal(18, 9) ,"
    " `loudness` decimal(18, 9) ,"
    " `speechiness` decimal(18, 9) ,"
    " `valence` decimal(18, 9) ,"
    "  PRIMARY KEY (`song_id`)"
    ") ENGINE=InnoDB")

TABLES['user_info'] = (
    "CREATE TABLE `user_info` ("
    " `user_name` char(4) ,"
    " `user_id` varchar(40) ,"
    " `date_accessed` date ,"
    " `avg_energy` decimal(18, 9) ,"
    " `avg_tempo` decimal(18, 9) ,"
    " `avg_danceability` decimal(18, 9) ,"
    " `avg_acousticness` decimal(18, 9) ,"
    " `avg_instrumentalness` decimal(18, 9) ,"
    " `avg_liveness` decimal(18, 9) ,"
    " `avg_loudness` decimal(18, 9) ,"
    " `avg_speechiness` decimal(18, 9) ,"
    " `avg_valence` decimal(18, 9) ,"
    "  PRIMARY KEY (`user_id`), UNIQUE KEY `user_name` (`user_name`)"
    ") ENGINE=InnoDB")

def create_connection():
    cnx = mysql.connector.connect(user='root')
    cursor = cnx.cursor()
    return [cnx, cursor]

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def initialize_db(cursor, cnx):
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()

def main():
    connection = create_connection()
    cnx = connection[0]
    cursor = connection[1]
    initialize_db(cursor, cnx)

if __name__ == "__main__":
    main()