import sql_functions as sqlf
import numpy as np

the_data = np.array([[45658, 'gehkj ', -1234.56], [34, 'ytb', 46.45]])

#print(sqlf.append_data('dev_test', 'test_table', the_data))

#print(sqlf.clear_data('dev_test', 'test_table'))

print(sqlf.save_data('dev_test', 'test_table', the_data))

print(sqlf.get_data('dev_test', 'test_table'))
