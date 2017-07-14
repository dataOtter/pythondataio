import mysql.connector
import credentials as cred
import numpy as np


def get_data(dbname, tblname):
    """Get the data from the specified table and database, and return it as an ndarray"""
    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()
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
    """Append data from the given ndarray in the specified table and database.
    Return true if some rows were appended."""
    if len(ndarray_input.shape) != 1:
        raise Exception("This function only takes a single row as input.")

    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()

    cursor.execute("SELECT count(*) FROM information_schema.columns WHERE table_name = '" + tblname + "'")
    columns = cursor.fetchall()
    if columns[0][0] != len(ndarray_input):
        raise Exception("This row does not have the same number of entries as there are columns!")

    count1 = count_rows(dbname, tblname)
    print(count1)

    command = "INSERT INTO " + tblname + " VALUES ("
    for x in range(ndarray_input.shape[0]):
        if x == 0:
            command += "%s"
        else:
            command += ", %s"
    command += ")"

    data = ndarray_input.tolist()

    cursor.execute(command, data)

    connection.commit()
    cursor.close()
    connection.close()

    count2 = count_rows(dbname, tblname)
    print(count2)

    if count2 == count1+1:
        success = True
    else:
        success = False

    return success


def clear_data(dbname, tblname):
    """Deletes ALL the data/rows in the specified table."""
    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()

    tables = show_tables(dbname)
    found = False

    for x in range(len(tables)):
        if tblname in tables[x]:
            found = True
    if not found:
        raise Exception("This table does not exist anyway!")

    command = "DELETE FROM " + tblname
    cursor.execute(command)

    success = count_rows(dbname, tblname)

    connection.commit()
    cursor.close()
    connection.close()

    if success == 0:
        return True
    else:
        return False


def save_data(dbname, tblname, ndarray_input):
    """Save data in the specified table. Delete previous data from table or create table if it does not exist."""
    if len(ndarray_input.shape) != 2:
        raise Exception("This function requires multiple rows and an nd-array as input. "
                        "Try append_row or check the entries in each row.")

    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()

    tables = show_tables(dbname)

    present = False
    for x in range(len(tables)):
        if tblname in tables[x]:
            present = True
            cleared = clear_data(dbname, tblname)
            if not cleared:
                raise Exception("Data wasn't cleared!")
            break
    if not present:
        raise Exception("Table does not exist!")
        # create_table(dbname, tblname, columns, column_types)

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

    connection.commit()
    cursor.close()
    connection.close()

    count = count_rows(dbname, tblname)

    if count > 0:
        success = True
    else:
        success = False

    return success


def show_tables(dbname):
    """Executes the SQL command to show all tables in the specified database."""
    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()
    cmmnd = "SHOW TABLES"
    cursor.execute(cmmnd)
    tables = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return tables


def count_rows(dbname, tblname):
    """Executes the SQL command to count the number of rows in the specified table."""
    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()
    cmd = "SELECT COUNT(*) FROM " + tblname
    cursor.execute(cmd)
    count = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    return count[0][0]


'''def create_table(dbname, tblname, columns, column_types):
    # create a table in the specified database with the given column names and types.
    connection = mysql.connector.connect(user=cred.get_user_name(), password=cred.get_password(),
                                         host=cred.get_server_address(),
                                         database=dbname)
    cursor = connection.cursor()

    command = "CREATE TABLE " + tblname + " ("
     # add columns and their type'''