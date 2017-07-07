import mysql.connector
import credentials as cred
import numpy as np


def get_data(dbname, tblname):
    # Get the data from the specified table and database, and return it as an ndarray
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
    # Save the data from the given ndarray in the specified table and database. Return true if some rows were appended.
    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()

    cmd = "SELECT COUNT(*) FROM " + tblname
    cursor.execute(cmd)
    count1 = cursor.fetchall()

    command = "INSERT INTO " + tblname + " (column1, column2, column3) VALUES ("
    for x in range(ndarray.shape[0]):
        if x == 0:
            command += "%s"
        else:
            command += ", %s"
    command += ")"

    data = np.ndarray.tolist(ndarray)

    cursor.execute(command, data)
    cursor.execute(cmd)
    count2 = cursor.fetchall()

    if count1 < count2:
        success = True
    else:
        success = False

    connection.commit()
    cursor.close()
    connection.close()

    return success


def clear_data(dbname, tblname):
    # Deletes ALL the data/rows in the specified table.
    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()

    command = "DELETE FROM " + tblname

    cursor.execute(command)

    cmd = "SELECT COUNT(*) FROM " + tblname
    cursor.execute(cmd)
    success = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    if success[0][0] == 0:
        return True
    else:
        return False


