import pandas as pd
import numpy as np
import sys
import os
from populate_tables import *
from retrieve_from_tables import *




def main():
	responseids = retrieve_responseids('ENG')
	df_responses =  pd.DataFrame(columns=['responseid', 'text']) 

	for responseid in responseids:
		r = get_response_from_id(responseid)
		for text in r:
			data = {'responseid': responseid, 'text': text}
			df_responses = df_responses.append(data, ignore_index=True)
	
	df_responses.to_csv('test_eng.csv', encoding='utf-8', index=False)




if __name__ == "__main__":
	main()