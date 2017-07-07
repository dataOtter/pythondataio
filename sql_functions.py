import mysql.connector
import credentials as cred
import numpy as np


def get_data(dbname, tblname):
    # Get the data from the specified table and database, and put it into an ndarray
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


def append_data(dbname, tblname, ndarray):
    # Save the data from the given ndarray into the specified table and database.
    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()


    print(ndarray.shape)

    command = "INSERT INTO test_table (column1, column2, column3) VALUES ("
    for x in range(ndarray.shape[0]):
        if x == 0:
            command += "%s"
        else:
            command += ", %s"
    command += ")"

    print(command)

    mylist = np.ndarray.tolist(ndarray)

    print(mylist)

    data = mylist

    cursor.execute(command, data)

    connection.commit()
    cursor.close()
    connection.close()


