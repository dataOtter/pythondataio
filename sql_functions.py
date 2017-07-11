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


def append_row(dbname, tblname, ndarray_input):
    # Append data from the given ndarray in the specified table and database. Return true if some rows were appended.
    if len(ndarray_input.shape) != 1:
        raise Exception("This function only takes a single row as input.")

    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()

    cmd = "SELECT COUNT(*) FROM " + tblname
    cursor.execute(cmd)
    count1 = cursor.fetchall()

    command = "INSERT INTO " + tblname + " VALUES ("
    for x in range(ndarray_input.shape[0]):
        if x == 0:
            command += "%s"
        else:
            command += ", %s"
    command += ")"

    data = ndarray_input.tolist()

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

    cmmnd = "SHOW TABLES"
    cursor.execute(cmmnd)
    tables = cursor.fetchall()

    found = False
    for x in range(len(tables)):
        if tblname in tables[x]:
            found = True
    if not found:
        raise Exception("This table does not exist anyway!")

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


'''def create_table(dbname, tblname, columns, column_types):
    # create a table in the specified database with the given column names and types.
    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()

    command = "CREATE TABLE " + tblname + " ("
     # add columns and their type'''


def save_data(dbname, tblname, ndarray_input):
    # save data in the specified table. Delete previous data from table or create table if it does not exist.
    if len(ndarray_input.shape) < 2:
        raise Exception("This function requires multiple rows as input. Try append_row.")

    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()

    cmmnd = "SHOW TABLES"
    cursor.execute(cmmnd)
    tables = cursor.fetchall()

    # get columns and their types - from ndarray_input[0]

    for x in range(len(tables)):
        if tblname in tables[x]:
            clear_data(dbname, tblname)
        #else:
            #create_table(dbname, tblname, columns, column_types)

    num_of_s = ndarray_input.shape[1]
    num_of_rows = ndarray_input.shape[0]

    command = "INSERT INTO " + tblname + " VALUES ("
    for x in range(num_of_s):
        if x == 0:
            command += "%s"
        else:
            command += ", %s"
    command += ")"

    for x in range(num_of_rows):
        row = ndarray_input[x]
        data = row.tolist()
        cursor.execute(command, data)

    cmd = "SELECT COUNT(*) FROM " + tblname
    cursor.execute(cmd)
    count = cursor.fetchall()

    if count[0][0] > 0:
        success = True
    else:
        success = False

    connection.commit()
    cursor.close()
    connection.close()

    return success