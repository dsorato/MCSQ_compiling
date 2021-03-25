import os
import sys
import pandas as pd
import string
import nltk
from nltk.tokenize import WhitespaceTokenizer 


all_tokenized_sentences = []
all_intro = []
all_instruction = []
all_request = []
all_response = []
all_tokens = []
all_unique_tokens = []

def remove_punctuation(text):
	text = text.translate(str.maketrans(' ', ' ', string.punctuation))

	text = text.rstrip()
	text = text.lstrip()

	return text

def get_language_iso_code_from_filename(filename):
	return filename.split('.csv')[0]


def get_average_sentence_length(tokens_in_sentences):
	sum_of_lengths = 0
	for sentence in tokens_in_sentences:
		sum_of_lengths = sum_of_lengths + len(sentence)

	return sum_of_lengths/len(tokens_in_sentences)

def get_number_of_sentences_and_length_by_item_type(sentences_per_item_type):
	n_introduction = len(sentences_per_item_type['INTRODUCTION'])
	avg_introduction = get_average_sentence_length(sentences_per_item_type['INTRODUCTION'])

	n_instruction = len(sentences_per_item_type['INSTRUCTION'])
	avg_instruction = get_average_sentence_length(sentences_per_item_type['INSTRUCTION'])

	n_request = len(sentences_per_item_type['REQUEST'])
	avg_request = get_average_sentence_length(sentences_per_item_type['REQUEST'])

	n_response = len(sentences_per_item_type['RESPONSE'])
	avg_response = get_average_sentence_length(sentences_per_item_type['RESPONSE'])

	return_dict = {'intro': [n_introduction, avg_introduction], 'instruction': [n_instruction, avg_instruction], 
	'request': [n_request, avg_request], 'response': [n_response, avg_response]}


	return return_dict

def build_sentences_per_item_type_dictionary(tokens_in_intro, tokens_in_instruction, tokens_in_request, tokens_in_response):
	sentences_per_item_type = dict()

	sentences_per_item_type['INTRODUCTION'] = tokens_in_intro
	sentences_per_item_type['INSTRUCTION'] = tokens_in_instruction
	sentences_per_item_type['REQUEST'] = tokens_in_request
	sentences_per_item_type['RESPONSE'] = tokens_in_response

	return sentences_per_item_type

def summary_statistics_per_language(filename, df, df_statistics_per_language, tokenizer, language_variety):
	unique_tokens = []
	n_tokens = []
	n_sentences = []
	tokenized_sentences = []
	tokens_in_intro = []
	tokens_in_instruction = []
	tokens_in_request = []
	tokens_in_response = []
	
	"""
	the language ISO code is embedded in the filename
	"""
	language_iso_code = get_language_iso_code_from_filename(filename)	

	for i, row in df.iterrows():
		if isinstance(row['text'], str):
			"""
			Removes punctiation from text segment, if it is a string
			"""
			sentence = remove_punctuation(row['text'])
			item_type = row['item_type']
			if isinstance(sentence, str):
				n_sentences.append([sentence])
				tokens = tokenizer.tokenize(sentence)
				tokens_in_sentence = []
				for token in tokens:
					if isinstance(token, str):
						token = token.lower()
						n_tokens.append(token)
						all_tokens.append(token)
						tokens_in_sentence.append(token)
						if token not in unique_tokens:
							unique_tokens.append(token)
						if token not in all_unique_tokens:
							all_unique_tokens.append(token)


				tokenized_sentences.append(tokens_in_sentence)
				all_tokenized_sentences.append(tokens_in_sentence)
				if item_type == 'INTRODUCTION':
					all_intro.append(tokens_in_sentence)
					tokens_in_intro.append(tokens_in_sentence)
				elif item_type == 'INSTRUCTION':
					all_instruction.append(tokens_in_sentence)
					tokens_in_instruction.append(tokens_in_sentence)
				elif item_type == 'REQUEST':
					all_request.append(tokens_in_sentence)
					tokens_in_request.append(tokens_in_sentence)
				else:
					all_response.append(tokens_in_sentence)
					tokens_in_response.append(tokens_in_sentence)

	sentences_per_item_type = build_sentences_per_item_type_dictionary(tokens_in_intro, tokens_in_instruction, tokens_in_request, tokens_in_response)
	stats_by_item_type = get_number_of_sentences_and_length_by_item_type(sentences_per_item_type)

	if language_variety is not None:
		l =  language_variety
	else:
		l = language_iso_code

	avg_sentence_length = get_average_sentence_length(tokenized_sentences)
	data = {'language_iso_code': l, 'number_of_sentences': len(n_sentences), 'average_sentence_length': avg_sentence_length,
	'number_of_introduction_segments': stats_by_item_type['intro'][0], 'average_introduction_segment_length':stats_by_item_type['intro'][1],
	'number_of_instruction_segments': stats_by_item_type['instruction'][0], 'average_instruction_segment_length': stats_by_item_type['instruction'][1],
	'number_of_request_segments': stats_by_item_type['request'][0],  'average_request_segment_length': stats_by_item_type['request'][1],
	'number_of_response_segments':  stats_by_item_type['response'][0], 'average_response_segment_length':  stats_by_item_type['response'][1], 
	'number_of_tokens': len(n_tokens),'number_of_unique_tokens': len(unique_tokens)}
	df_statistics_per_language = df_statistics_per_language.append(data, ignore_index = True)	

	return all_tokenized_sentences, all_intro, all_instruction, all_request, all_response, all_tokens, all_unique_tokens, df_statistics_per_language
	
		   
def summary_statistics(all_tokenized_sentences, all_intro, all_instruction, all_request, all_response, all_tokens, all_unique_tokens, df_statistics_per_language):
	df_statistics = pd.DataFrame(columns=['number_of_sentences', 'average_sentence_length',
		'number_of_introduction_segments','average_introduction_segment_length', 
		'number_of_instruction_segments', 'average_instruction_segment_length',
		'number_of_request_segments', 'average_request_segment_length',
		'number_of_response_segments', 'average_response_segment_length', 
	 	'number_of_tokens','number_of_unique_tokens'])

	n_sentences = df_statistics_per_language['number_of_sentences'].sum()
	avg_sent = get_average_sentence_length(all_tokenized_sentences)

	n_intro = df_statistics_per_language['number_of_introduction_segments'].sum()
	avg_intro = get_average_sentence_length(all_intro)

	n_instruction = df_statistics_per_language['number_of_instruction_segments'].sum()
	avg_instruction = get_average_sentence_length(all_instruction)

	n_request = df_statistics_per_language['number_of_request_segments'].sum()
	avg_request = get_average_sentence_length(all_request)

	n_response = df_statistics_per_language['number_of_response_segments'].sum()
	avg_response = get_average_sentence_length(all_request)



	data = {'number_of_sentences': n_sentences, 'average_sentence_length': avg_sent,
		'number_of_introduction_segments': n_intro,'average_introduction_segment_length': avg_intro, 
		'number_of_instruction_segments': n_instruction, 'average_instruction_segment_length':avg_instruction,
		'number_of_request_segments': n_request, 'average_request_segment_length': avg_request,
		'number_of_response_segments': n_response, 'average_response_segment_length':avg_response, 
	 	'number_of_tokens': len(all_tokens),'number_of_unique_tokens': len(all_unique_tokens)}
	df_statistics = df_statistics.append(data, ignore_index = True)

	return df_statistics
		

def get_language_varieties_in_file(df):
	language_varieties = []

	filtered = df[df['survey_item_ID'].str.contains("_.*_1")]

	for i, row in filtered.iterrows():
		split = row['survey_item_ID'].split('_')
		language_variety = split[3] + '_' + split[4]
		if language_variety not in language_varieties:
			language_varieties.append(language_variety)


	return language_varieties



			

def main(folder_path, results_by_language_variety):
	path = os.chdir(folder_path)
	files = os.listdir(path)

	tokenizer = WhitespaceTokenizer() 

	df_statistics_per_language = pd.DataFrame(columns=['language_iso_code', 'number_of_sentences', 'average_sentence_length',
	'number_of_introduction_segments', 'average_introduction_segment_length',
	'number_of_instruction_segments', 'average_instruction_segment_length',
	'number_of_request_segments',  'average_request_segment_length',
	'number_of_response_segments', 'average_response_segment_length', 
	'number_of_tokens','number_of_unique_tokens'])

	

	

	for index, file in enumerate(files):
		if file.endswith(".csv"):
			print('Getting statistics from file:', file)
			df = pd.read_csv(file, dtype=str, delimiter='\t')
			language_variety = None
			if results_by_language_variety == 1:
				language_varieties = get_language_varieties_in_file(df)
				for language_variety in language_varieties:
					filtered = df[df['survey_item_ID'].str.contains(language_variety)]
					all_tokenized_sentences, all_intro, all_instruction, all_request, all_response,  all_tokens, all_unique_tokens, df_statistics_per_language = summary_statistics_per_language(file, filtered, df_statistics_per_language, tokenizer, language_variety)
			else:
				all_tokenized_sentences, all_intro, all_instruction, all_request, all_response,  all_tokens, all_unique_tokens, df_statistics_per_language = summary_statistics_per_language(file, df, df_statistics_per_language, tokenizer, language_variety)

	if results_by_language_variety == 1:
		df_statistics_per_language.to_csv('df_statistics_per_language_variety.tsv', encoding='utf-8-sig', sep='\t', index=False) 
	else:
		df_statistics_per_language.to_csv('df_statistics_per_language.tsv', encoding='utf-8-sig', sep='\t', index=False) 

	# df_statistics =  summary_statistics(all_tokenized_sentences, all_intro, all_instruction, all_request, all_response, all_tokens, all_unique_tokens, df_statistics_per_language)

	# df_statistics.to_csv('df_statistics.tsv', encoding='utf-8-sig', sep='\t', index=False) 

if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	results_by_language_variety = int(sys.argv[2])
	main(folder_path, results_by_language_variety)