import mysql.connector
import credentials as cred
import numpy as np


def get_data(dbname, tblname):
    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()
    cursor.execute("USE " + dbname)
    cursor.execute("SELECT * FROM " + tblname)
    results = cursor.fetchall()

    data_array = np.array([])

    for x in range(len(results)):
        row = results[x]

        if x == 0:
            data_array = np.array(row)
        else:
            rownp = np.array(row)
            data_array = np.vstack([data_array, rownp])

    cursor.close()
    connection.close()

    return data_array


def save_data(dbname, tblname, ndarray):
    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()

    command = "INSERT INTO test_table VALUES ("
    for x in range(ndarray.shape[1]):
        if x == 0:
            command += "%s"
        else:
            command += ", %s"
    command += ")"



    data = (4, "AABBCC", 3.14)

# Insert new row
cursor.execute(add_one, data_one)

row_no = cursor.lastrowid

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()


