import sql_functions as sqlf
import numpy as np

the_data = np.array([45658, 'booo', -1234.56])

#print(sqlf.append_data('dev_test', 'test_table', the_data))

print(sqlf.clear_data('dev_test', 'test_table'))

print(sqlf.get_data('dev_test', 'test_table'))
