import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'HeartBeat'

# This is a dict of tables, with the key being the name of the table,
# and the value being the actual SQL command to create the table with
# certain information.
TABLES = {}

# music_info is being added to the TABLES which is going to be used for
# recommending system for community based addition of songs.
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

# This adds the user_info to TABLES which is going to be used for
# the recommending system for recommending songs based on the variance that
# we create.
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

# create_connection():
    # returns a list containing both cnx (the connection to the DB)
    # and a cursor (which is used to use the database commands)
    # mysql API documentation is very good if you dont understand parts of this
    # FYI user='root' is for local use purposes as it will work on all machines.
def create_connection():
    cnx = mysql.connector.connect(user='root')
    cursor = cnx.cursor()
    return [cnx, cursor]

# create_database(cursor):  
    # this creates a database with name DB_NAME (variable set above)
    # This takes in the cursor itself which is used to execute the commands.
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

# initialize_db(cursor, cnx):
    # this is the main chunk of what is really important, and it uses both the above functions within it.
    # this function takes in a cursor and cnx, and uses them to create the database itself, by using functions listed above.
    # this returns the cursor and cnx yet again as a list so that we can use them in any way to populate the database through our other files.
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

    return [cursor, cnx]

def main():
    connection = create_connection()
    cnx = connection[0]
    cursor = connection[1]
    return initialize_db(cursor, cnx)

if __name__ == "__main__":
    main()