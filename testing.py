import sql_functions as sqlf
import numpy as np

the_data = np.array([777, 'frobby', -1234.56])

sqlf.append_data('dev_test', 'test_table', the_data)

print(sqlf.get_data('dev_test', 'test_table'))
