#python3.6 script for dataset cleaning
#Author: Danielly Sorato
#Before running the script, install pandas
import pandas as pd
from itertools import groupby
from db_connection import *
import os
import re	

# def write_survey_metadata(connection):
# 	df = pd.DataFrame({'study': ['ESS'], 'wave': 8, 'year': 2016, 'mode': ['unknown']})
# 	df.to_sql('survey', con=connection, if_exists='append', index=False)

def get_code(a):
	first = a.split('_')[0]
	second = a.split('_')[1]

	return first+'_'+second



def group_by_prefix(translations_list):
	groups = [list(i) for j, i in groupby(translations_list, lambda a: get_code(a))]

	return groups


def remove_html_tags(text):
	text = re.sub("<.*?>", "", text)

	return text


def main():
	#change directory to round 8 folder and read csv
	os.chdir('/home/upf/workspace/ESS/round8')
	data = pd.read_excel('tmt_ess_r8_2016v1.xlsx', sheet_name='Sheet2')
	# print(data.head())

	#delete unwanted elements in dataset
	print('Deleting columns there are at least 90 per cent empty')
	cols_to_delete = data.columns[data.isnull().sum()/len(data) > .90]
	data.drop(cols_to_delete, axis = 1, inplace = True)
	# print('Deleted columns: ', cols_to_delete)

	# print('Deleting unwanted columns')
	data = data.drop(['parent_type', 'parent', 'item_name', 'FR_CH_ID'], axis=1)

	# print('Remaining columns:')
	# for col in data.columns:
	# 	print(col)

	df_metadata = data[['doc_id', 'module', 'item_type']]

	df_text = data.drop(['doc_id', 'module', 'item_type'], axis=1)
	translations = []
	for col in df_text.columns:
		translations.append(col)

	groups = group_by_prefix(translations)

	dfs = dict()

	for item in groups:
		dfName = get_code(item[0])
		dfNew = data[item]
		dfs[dfName] = dfNew

	for k, v in enumerate(dfs.items()):
		print(k,v)
    
    




	# df_test = data['FRE_BE']
	# for item in df_test:
	# 	if not isinstance(item, float):
	# 		clean_text = remove_html_tags(item)
	# 		print(clean_text)

	# db = DBConnection()
	# connection = db.connect()

	# sql_command = "SELECT * FROM {}.{};".format(str("public"), str("Survey"))
	# print (sql_command)
	# write_survey_metadata(connection)
	# data = pd.read_sql(sql_command, connection)
	# print(data)


if __name__ == "__main__":
	print("Executing data cleaning script for ESS")
	main()


