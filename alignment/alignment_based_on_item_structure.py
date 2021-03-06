import pandas as pd
import nltk
import sys
import os
import re
import string
from alignment_utils import *
from countryspecificrequest import *
from string import punctuation
from word2word import Word2word
from nltk.corpus import stopwords

def find_best_match(list_source, list_target, item_type):
	"""
	Finds the best match for source and target segments (same item_type) based on the lenght of the segments.

	Args:
		param1 list_source (list): list of source segments (contains segments of same item_name and item_type)
		param2 list_target (list): list of target segments (contains segments of same item_name and item_type)
		param3 item_type (string): the item type of the segments. Can be introduction, instruction or request.

	Returns:
		alignment (list). Alignment pair represented by the index of target and source segments being aligned 
		(index 0 = target,index 1 = source), selected with lenght of the segments strategy.
	"""
	dict_source = dict()
	dict_target = dict()
	alignment_candidates = dict()

	showc = identify_showc_segment(list_source, list_target, item_type)
	if showc != 'No showc segment identified':
		return showc


	for i, item in enumerate(list_source):
		text = preprocessing_alignment_candidates(item[-1])
		dict_source[i] = text
		

	for i, item in enumerate(list_target):
		text = preprocessing_alignment_candidates(item[-1])
		dict_target[i] = text
		


	for target_k, target_v in list(dict_target.items()):
		for source_k, source_v in list(dict_source.items()):
			if 'ENG' in target_language_country:
				if abs(len(target_v)-len(source_v)) in alignment_candidates.keys():
					alignment_candidates[abs(len(target_v)-len(source_v))+0.1] = target_k, source_k 
				else:
					alignment_candidates[abs(len(target_v)-len(source_v))] = target_k, source_k 
			else:
				# print(target_v, source_v)
				# print(abs(len(target_v)-len(source_v)) - 0.05*use_bilingual_dict(source_v, target_v))
				
				if abs(len(target_v)-len(source_v)) - 0.05*use_bilingual_dict(source_v, target_v) in alignment_candidates.keys():
					alignment_candidates[abs(len(target_v)-len(source_v)) - 0.05*use_bilingual_dict(source_v, target_v)+0.1] = target_k, source_k 
				else:
					alignment_candidates[abs(len(target_v)-len(source_v)) - 0.05*use_bilingual_dict(source_v, target_v)] = target_k, source_k 
	

	best_candidate = min(alignment_candidates)

	return alignment_candidates[best_candidate]

def preprocessing_alignment_candidates(text):
	"""
	Preprocesses the text segment by tokenizing it, removing punctuation.
	Args:
		param1 text (string): the text segment to be preprocessed.
	Returns:
		The preprocessed tokens (a list of strings). 
	"""
	text =  re.sub(r"[^\w\s]+",'',text.lower()) 

	tokens = text.split(' ')
	preprocessed_tokens = []

	for token in tokens:
		if token != '':
			preprocessed_tokens.append(token)


	return preprocessed_tokens

def identify_showc_segment(list_source, list_target, item_type):
	"""
	Searches in list_source, list_target if there are intructions that seem to be show card segments that should be aligned together.
	This method was implemented as an additional strategy to align correctly instruction segments.

	Args:
		param1 list_source (list): list of source segments (contains segments of same item_name and item_type)
		param2 list_target (list): list of target segments (contains segments of same item_name and item_type)
		param3 item_type (string): item_type metadata being analyzed. In this method we want to consider only instruction segments.

	Returns:
		str indicating if instructions that follow the show card segments were found.
	"""
	target_regex =  r"(?P<card>)(card|showcard|tarjeta|targeta|kartu|karta|karty|kort|kortet|carte|liste|kort|kortet|carte|karte|Bildblatt|cartão|lista|КАРТОЧКУ|КАРТОЧКА|KAРTOЧКА|карточкой|карточке|карточки|карте|карты)\s(?P<numberorletter>)(\d+|\w+|\w+\d+|\d+\w+)"  
	source_regex =  r"(?P<card>)(card|showcard)\s(?P<numberorletter>)(\d+|\w+|\w+\d+|\d+\w+)"  
	if item_type == 'INSTRUCTION':

		source_candidates = []
		target_candidates = []

		for item in list_source:
			if re.search(source_regex, item[-1], re.IGNORECASE):
				source_candidates.append(item)

		for item in list_target:
			if re.search(target_regex, item[-1], re.IGNORECASE):
				target_candidates.append(item)

		if source_candidates and target_candidates:
			best_candidate = 999
			for source in source_candidates:
				for target in target_candidates:
					source_text = preprocessing_alignment_candidates(source[-1])
					target_text = preprocessing_alignment_candidates(target[-1])

					if abs(len(target_text)-len(source_text)) < best_candidate:
						best_candidate = abs(len(target_text)-len(source_text))
						chosen_source = source
						chosen_target = target

			return list_target.index(chosen_target), list_source.index(chosen_source)
		else:
			return 'No showc segment identified'

	else:
		return 'No showc segment identified'





def use_bilingual_dict(source_text, target_text):
	count = 0
	
	if source_text != '' and target_text != '':
		for word in source_text:
			if word.isdigit() == False and word not in st:
				try:
					a = mcsq_bi(word)
					for item in a:
						if item in target_text:
							count+=1
					
				except KeyError:
					pass 
					

	return count




def get_original_index(list_source, list_target, source_segment_index, target_segment_index, aux_source, aux_target):
	"""
	Gets the original index of aligned segments, as the auxiliary lists are being modified and the indexes
	does not correspond to the original ones.

	Args:
		param1 list_source (list): list of source segments (contains segments of same item_name and item_type).
		param2 list_target (list): list of target segments (contains segments of same item_name and item_type).
		param3 source_segment_index (int): source segment aligned in aux_source list.
		param4 target_segment_index (int): target segment aligned in aux_target list.
		param5 aux_source (list): auxiliary list of source segments being modified in outer loop (contains segments of same item_name and item_type).
		param6 aux_target (list): auxiliary list of target segments being modified in outer loop (contains segments of same item_name and item_type).

	Returns:
		original_index_target (int), original_index_source (int). Original indexes (in list_source, list_target) of source/target segments aligned.
	"""
	target_segment_text = aux_target[target_segment_index]
	original_index_target = list_target.index(target_segment_text)

	source_segment_text = aux_source[source_segment_index]
	original_index_source = list_source.index(source_segment_text)

	return original_index_target, original_index_source



def only_one_segment_in_source_align(alignment, source_segment, target_segment, list_target, aux_target, df):
	"""
	Fills the dataframe with remaining target segments that do not have source correspondencies.
	This method is called when the dataframe contains one source segment to two or more target segments.
	The alignment pair is defined in the find_best_match() method and the remaining target segments
	are included in this method, respecting the structure order.

	Args:
		param1 alignment (list): Alignment pair represented by the index of target and source segments being aligned 
		(index 0 = target,index 1 = source), selected with lenght of the segments strategy.
		param2 source_segment (list): source segment that has a match according to find_best_match().
		param3 target_segment (list): target segment that has a match according to find_best_match().
		param4 list_target (list): list of target segments (contains segments of same item_name and item_type)
		param5 aux_target (list): list of source segments, excluding the target_segment (contains segments of same item_name and item_type)
		param6 df (pandas dataframe): dataframe to store the questionnaire alignment

	Returns:
		df (pandas dataframe) with newly aligned survey item segments.
	"""

	"""
	If the index of the target list that was first aligned is 0 (the first one), then other elements in the list go after this
	"""
	if alignment[0] == 0:
		data = {'source_survey_itemID':source_segment[0], 'target_survey_itemID': target_segment[0], 
		'Study': target_segment[1], 'module': target_segment[2], 'item_type': target_segment[3], 
		'item_name':target_segment[4], 'item_value': None, 'source_text': source_segment[6], 'target_text': target_segment[6],
		'source_ner_tagged_text': source_segment[7],'target_ner_tagged_text': target_segment[7],
		'source_pos_tagged_text': source_segment[8], 'target_pos_tagged_text': target_segment[8]}
		df = df.append(data, ignore_index=True)

		for i, item in enumerate(aux_target):
			data = {'source_survey_itemID': None, 'target_survey_itemID': item[0] , 'Study': item[1], 
			'module': item[2], 'item_type': item[3], 'item_name':item[4], 'item_value': None, 
			'source_text': None, 'target_text':  item[6],
			'source_ner_tagged_text': None,'target_ner_tagged_text': item[7],
			'source_pos_tagged_text': None, 'target_pos_tagged_text': item[8]}
			df = df.append(data, ignore_index=True)

	#If the index of the target list that was first aligned is the last segment on the list then it goes after all other segments.
	elif alignment[0] == len(list_target)-1:
		for i, item in enumerate(aux_target):
			data = {'source_survey_itemID': None, 'target_survey_itemID': item[0] , 'Study': item[1], 
			'module': item[2], 'item_type': item[3], 'item_name':item[4], 'item_value': None, 
			'source_text': None, 'target_text':  item[6],
			'source_ner_tagged_text': None,'target_ner_tagged_text': item[7],
			'source_pos_tagged_text': None, 'target_pos_tagged_text': item[8]}
			df = df.append(data, ignore_index=True)

		data = {'source_survey_itemID': source_segment[0], 'target_survey_itemID': target_segment[0], 
		'Study': target_segment[1], 'module': target_segment[2], 'item_type': target_segment[3], 
		'item_name':target_segment[4], 'item_value': None, 'source_text': source_segment[6], 'target_text': target_segment[6],
		'source_ner_tagged_text': source_segment[7],'target_ner_tagged_text': target_segment[7],
		'source_pos_tagged_text': source_segment[8], 'target_pos_tagged_text': target_segment[8]}
		df = df.append(data, ignore_index=True)
	# If the index of the target list that was first aligned is neither the first nor the last segment, we have to find its place using the index.
	else:
		for i, item in enumerate(list_target):
			if i != alignment[0]:
				data = {'source_survey_itemID': None, 'target_survey_itemID': item[0] , 'Study': item[1], 
				'module': item[2], 'item_type': item[3], 'item_name':item[4], 'item_value': None, 
				'source_text': None, 'target_text':  item[6],
				'source_ner_tagged_text': None,'target_ner_tagged_text': item[7],
				'source_pos_tagged_text': None, 'target_pos_tagged_text': item[8]}
				df = df.append(data, ignore_index=True)
			elif i == alignment[0]:
				data = {'source_survey_itemID': source_segment[0], 'target_survey_itemID': target_segment[0], 
				'Study': target_segment[1], 'module': target_segment[2], 'item_type': target_segment[3], 
				'item_name':target_segment[4], 'item_value': None, 'source_text': source_segment[6], 'target_text': target_segment[6],
				'source_ner_tagged_text': source_segment[7],'target_ner_tagged_text': target_segment[7],
				'source_pos_tagged_text': source_segment[8], 'target_pos_tagged_text': target_segment[8]}
				df = df.append(data, ignore_index=True)

	return df


def only_one_segment_in_target_align(alignment, source_segment, target_segment, list_source, aux_source, df):
	"""
	Fills the dataframe with remaining source segments that do not have target correspondencies.
	This method is called when the dataframe contains one target segment to two or more source segments.
	The alignment pair is defined in the find_best_match() method and the remaining source segments
	are included in this method, respecting the structure order.

	Args:
		param1 alignment (list): Alignment pair represented by the index of target and source segments being aligned 
		(index 0 = target,index 1 = source), selected with lenght of the segments strategy.
		param2 source_segment (list): source segment that has a match according to find_best_match().
		param3 target_segment (list): target segment that has a match according to find_best_match().
		param4 list_source (list): list of source segments (contains segments of same item_name and item_type)
		param5 aux_source (list): list of source segments, excluding the source_segment (contains segments of same item_name and item_type)
		param6 df (pandas dataframe): dataframe to store the questionnaire alignment

	Returns:
		df (pandas dataframe) with newly aligned survey item segments.
	"""
	"""
	If the index of the source list that was first aligned is 0 (the first one), then other elements in the list go after this
	"""
	if alignment[1] == 0:
		data = {'source_survey_itemID':source_segment[0], 'target_survey_itemID': target_segment[0], 
		'Study': target_segment[1], 'module': target_segment[2], 'item_type': target_segment[3], 
		'item_name':target_segment[4], 'item_value': None, 'source_text': source_segment[6], 'target_text': target_segment[6],
		'source_ner_tagged_text': source_segment[7],'target_ner_tagged_text': target_segment[7],
		'source_pos_tagged_text': source_segment[8], 'target_pos_tagged_text': target_segment[8]}
		df = df.append(data, ignore_index=True)

		for i, item in enumerate(aux_source):
			data = {'source_survey_itemID': item[0], 'target_survey_itemID':  None, 'Study': item[1], 
			'module': item[2], 'item_type': item[3], 'item_name':item[4], 'item_value': None, 
			'source_text': item[6], 'target_text': None, 
			'source_ner_tagged_text': item[7],'target_ner_tagged_text': None,
			'source_pos_tagged_text': item[8], 'target_pos_tagged_text':None}
			df = df.append(data, ignore_index=True)

	#If the index of the source list that was first aligned is the last segment on the list then it goes after all other segments.
	elif alignment[1] == len(list_source)-1:
		for i, item in enumerate(aux_source):
			data = {'source_survey_itemID': item[0], 'target_survey_itemID':  None, 'Study': item[1], 
			'module': item[2], 'item_type': item[3], 'item_name':item[4], 'item_value': None, 
			'source_text': item[6], 'target_text': None, 
			'source_ner_tagged_text': item[7],'target_ner_tagged_text': None,
			'source_pos_tagged_text': item[8], 'target_pos_tagged_text':None}
			df = df.append(data, ignore_index=True)

		data = {'source_survey_itemID': source_segment[0], 'target_survey_itemID': target_segment[0], 
		'Study': target_segment[1], 'module': target_segment[2], 'item_type': target_segment[3], 
		'item_name':target_segment[4], 'item_value': None,'source_text': source_segment[6], 'target_text': target_segment[6],
		'source_ner_tagged_text': source_segment[7],'target_ner_tagged_text': target_segment[7],
		'source_pos_tagged_text': source_segment[8], 'target_pos_tagged_text': target_segment[8]}
		df = df.append(data, ignore_index=True)
	# If the index of the source list that was first aligned is neither the first nor the last segment, we have to find its place using the index.
	else:
		for i, item in enumerate(list_source):
			if i != alignment[1]:
				data = {'source_survey_itemID': item[0], 'target_survey_itemID': None , 'Study': item[1], 
				'module': item[2], 'item_type': item[3], 'item_name':item[4], 'item_value': None, 
				'source_text': item[6], 'target_text': None, 
				'source_ner_tagged_text': item[7],'target_ner_tagged_text': None,
				'source_pos_tagged_text': item[8], 'target_pos_tagged_text':None}
				df = df.append(data, ignore_index=True)
			elif i == alignment[1]:
				data = {'source_survey_itemID': source_segment[0], 'target_survey_itemID': target_segment[0], 
				'Study': target_segment[1], 'module': target_segment[2], 'item_type': target_segment[3], 
				'item_name':target_segment[4], 'item_value': None, 'source_text': source_segment[6], 'target_text': target_segment[6],
				'source_ner_tagged_text': source_segment[7],'target_ner_tagged_text': target_segment[7],
				'source_pos_tagged_text': source_segment[8], 'target_pos_tagged_text': target_segment[8]}
				df = df.append(data, ignore_index=True)

	return df


def treat_a_single_pairless_target(list_source, list_target, sorted_aligments, target_segments_without_pair, df):
	"""
	Align source and target segments, in case where there is only one target segment without a pair.

	Args:
		param1 list_source (list): list of source segments (contains segments of same item_name and item_type)
		param2 list_target (list): list of target segments (contains segments of same item_name and item_type)
		param3 sorted_aligments (list): sorted list segments aligned via best match strategy.
		param4 target_segments_without_pair (int): index of pairless target segment
		param5 df (pandas dataframe): dataframe to store the questionnaire alignment

	Returns:
		df (pandas dataframe) with newly aligned survey item segments.
	"""
	if target_segments_without_pair == 0:
		data = {'source_survey_itemID': None, 'target_survey_itemID': list_target[target_segments_without_pair][0], 
		'Study': list_target[target_segments_without_pair][1], 'module': list_target[target_segments_without_pair][2], 
		'item_type': list_target[target_segments_without_pair][3], 'item_name':list_target[target_segments_without_pair][4], 
		'item_value': None, 'source_text': None,'target_text': list_target[target_segments_without_pair][6],
		'source_ner_tagged_text': None, 'target_ner_tagged_text': list_target[target_segments_without_pair][7], 
		'source_pos_tagged_text': None, 'target_pos_tagged_text': list_target[target_segments_without_pair][8]}
		df = df.append(data, ignore_index=True)

		for alignment in sorted_aligments:
			source_index = alignment[1]
			target_index = alignment[0]
			data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
			'Study': list_target[target_index][1], 'module': list_target[target_index][2], 
			'item_type': list_target[target_index][3], 'item_name':list_target[target_index][4], 
			'item_value': None, 'source_text': list_source[source_index][6],'target_text': list_target[target_index][6],
			'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
			'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
			df = df.append(data, ignore_index=True)

	elif target_segments_without_pair == len(list_target)-1:
		for alignment in sorted_aligments:
			source_index = alignment[1]
			target_index = alignment[0]
			data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
			'Study': list_target[target_index][1], 'module': list_target[target_index][2], 
			'item_type': list_target[target_index][3], 'item_name':list_target[target_index][4], 
			'item_value': None, 'source_text': list_source[source_index][6],'target_text': list_target[target_index][6],
			'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
			'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
			df = df.append(data, ignore_index=True)
		data = {'source_survey_itemID': None, 'target_survey_itemID': list_target[target_segments_without_pair][0], 
		'Study': list_target[target_segments_without_pair][1], 'module': list_target[target_segments_without_pair][2], 
		'item_type': list_target[target_segments_without_pair][3], 'item_name':list_target[target_segments_without_pair][4], 
		'item_value': None, 'source_text': None, 'target_text': list_target[target_segments_without_pair][6],
		'source_ner_tagged_text': None, 'target_ner_tagged_text': list_target[target_segments_without_pair][7], 
		'source_pos_tagged_text': None, 'target_pos_tagged_text': list_target[target_segments_without_pair][8]}
		df = df.append(data, ignore_index=True)


	else:

		for alignment in sorted_aligments:
			source_index = alignment[1]
			target_index = alignment[0]

			if target_segments_without_pair == target_index-1: 
				data = {'source_survey_itemID': None, 'target_survey_itemID': list_target[target_segments_without_pair][0], 
				'Study': list_target[target_segments_without_pair][1], 'module': list_target[target_segments_without_pair][2], 
				'item_type': list_target[target_segments_without_pair][3], 'item_name':list_target[target_segments_without_pair][4], 
				'item_value': None, 'source_text': None,'target_text': list_target[target_segments_without_pair][6],
				'source_ner_tagged_text': None, 'target_ner_tagged_text': list_target[target_segments_without_pair][7], 
				'source_pos_tagged_text': None, 'target_pos_tagged_text': list_target[target_segments_without_pair][8]}
				df = df.append(data, ignore_index=True)

				data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
				'Study': list_target[target_index][1], 'module': list_target[target_index][2], 
				'item_type': list_target[target_index][3], 'item_name':list_target[target_index][4], 
				'item_value': None, 'source_text': list_source[source_index][6],'target_text': list_target[target_index][6],
				'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
				'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
				df = df.append(data, ignore_index=True)

			else:
				data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
				'Study': list_target[target_index][1], 'module': list_target[target_index][2], 
				'item_type': list_target[target_index][3], 'item_name':list_target[target_index][4], 
				'item_value': None, 'source_text': list_source[source_index][6],'target_text': list_target[target_index][6],
				'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
				'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
				df = df.append(data, ignore_index=True)

	return df



def treat_a_single_pairless_source(list_source, list_target, sorted_aligments, source_segments_without_pair, df):
	"""
	Align source and target segments, in case where there is only one source segment without a pair.

	Args:
		param1 list_source (list): list of source segments (contains segments of same item_name and item_type)
		param2 list_target (list): list of target segments (contains segments of same item_name and item_type)
		param3 sorted_aligments (list): sorted list segments aligned via best match strategy.
		param4 source_segments_without_pair (int): index of pairless souce segment
		param5 df (pandas dataframe): dataframe to store the questionnaire alignment

	Returns:
		df (pandas dataframe) with newly aligned survey item segments.
	"""
	if source_segments_without_pair == 0:
		data = {'source_survey_itemID': list_source[source_segments_without_pair][0], 'target_survey_itemID': None, 
		'Study': list_source[source_segments_without_pair][1], 'module': list_source[source_segments_without_pair][2], 
		'item_type': list_source[source_segments_without_pair][3], 'item_name':list_source[source_segments_without_pair][4], 
		'item_value': None, 'source_text': list_source[source_segments_without_pair][6],'target_text': None, 
		'source_ner_tagged_text': list_source[source_segments_without_pair][7],'target_ner_tagged_text': None,
		'source_pos_tagged_text': list_source[source_segments_without_pair][8], 'target_pos_tagged_text':None}
		df = df.append(data, ignore_index=True)

		for alignment in sorted_aligments:
			source_index = alignment[0]
			target_index = alignment[1]
			data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
			'Study': list_source[source_index][1], 'module': list_source[source_index][2], 
			'item_type': list_source[source_index][3], 'item_name':list_source[source_index][4], 
			'item_value': None, 'source_text': list_source[source_index][6],'target_text': list_target[target_index][6],
			'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
			'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
			df = df.append(data, ignore_index=True)

	elif source_segments_without_pair == len(list_source)-1:
		for alignment in sorted_aligments:
			source_index = alignment[0]
			target_index = alignment[1]
			data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
			'Study': list_source[source_index][1], 'module': list_source[source_index][2], 
			'item_type': list_source[source_index][3], 'item_name':list_source[source_index][4], 
			'item_value': None, 'source_text': list_source[source_index][6],'target_text': list_target[target_index][6],
			'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
			'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
			df = df.append(data, ignore_index=True)

		data = {'source_survey_itemID': list_source[source_segments_without_pair][0], 'target_survey_itemID': None, 
		'Study': list_source[source_segments_without_pair][1], 'module': list_source[source_segments_without_pair][2], 
		'item_type': list_source[source_segments_without_pair][3], 'item_name':list_source[source_segments_without_pair][4], 
		'item_value': None, 'source_text': list_source[source_segments_without_pair][6],'target_text': None, 
		'source_ner_tagged_text': list_source[source_segments_without_pair][7],'target_ner_tagged_text': None,
		'source_pos_tagged_text': list_source[source_segments_without_pair][8], 'target_pos_tagged_text':None}
		df = df.append(data, ignore_index=True)


	else:
		for alignment in sorted_aligments:
			source_index = alignment[0]
			target_index = alignment[1]

			if source_segments_without_pair == source_index-1:
				data = {'source_survey_itemID': list_source[source_segments_without_pair][0], 'target_survey_itemID': None, 
				'Study': list_source[source_segments_without_pair][1], 'module': list_source[source_segments_without_pair][2], 
				'item_type': list_source[source_segments_without_pair][3], 'item_name':list_source[source_segments_without_pair][4], 
				'item_value': None, 'source_text': list_source[source_segments_without_pair][6],'target_text': None, 
				'source_ner_tagged_text': list_source[source_segments_without_pair][7],'target_ner_tagged_text': None,
				'source_pos_tagged_text': list_source[source_segments_without_pair][8], 'target_pos_tagged_text':None}
				df = df.append(data, ignore_index=True)

				data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
				'Study': list_source[source_index][1], 'module': list_source[source_index][2], 
				'item_type': list_source[source_index][3], 'item_name':list_source[source_index][4], 
				'item_value': None, 'source_text': list_source[source_index][6],'target_text': list_target[target_index][6],
				'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
				'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
				df = df.append(data, ignore_index=True)


			else:
				data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
				'Study': list_source[source_index][1], 'module': list_source[source_index][2], 
				'item_type': list_source[source_index][3], 'item_name':list_source[source_index][4], 
				'item_value': None, 'source_text': list_source[source_index][6],'target_text': list_target[target_index][6],
				'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
				'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
				df = df.append(data, ignore_index=True)
				

	return df


def treat_multiple_pairless_source_segments(list_source, list_target, sorted_aligments, source_segments_without_pair, df):
	"""
	Align source and target segments, in case where there are multiple source segments without a pair.

	Args:
		param1 list_source (list): list of source segments (contains segments of same item_name and item_type)
		param2 list_target (list): list of target segments (contains segments of same item_name and item_type)
		param3 sorted_aligments (list): sorted list segments aligned via best match strategy.
		param4 source_segments_without_pair (list): indexes of pairless souce segments
		param5 df (pandas dataframe): dataframe to store the questionnaire alignment

	Returns:
		df (pandas dataframe) with newly aligned survey item segments.
	"""
	if sorted(source_segments_without_pair) == list(range(min(source_segments_without_pair), max(source_segments_without_pair)+1)):
		if source_segments_without_pair[0] > sorted_aligments[0][-1]:
			for alignment in sorted_aligments:
				source_index = alignment[0]
				target_index = alignment[1]

				data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
				'Study': list_source[source_index][1], 'module': list_source[source_index][2], 
				'item_type': list_source[source_index][3], 'item_name':list_source[source_index][4], 
				'item_value': None, 'source_text': list_source[source_index][6],'target_text': list_target[target_index][6],
				'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
				'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
				df = df.append(data, ignore_index=True)

			for pairless in source_segments_without_pair:
				data = {'source_survey_itemID': list_source[pairless][0], 'target_survey_itemID': None, 
				'Study': list_source[pairless][1], 'module': list_source[pairless][2], 
				'item_type': list_source[pairless][3], 'item_name':list_source[pairless][4], 
				'item_value': None, 'source_text': list_source[pairless][6],'target_text': None, 
				'source_ner_tagged_text': list_source[pairless][7],'target_ner_tagged_text': None,
				'source_pos_tagged_text': list_source[pairless][8], 'target_pos_tagged_text':None}
				df = df.append(data, ignore_index=True)

		elif source_segments_without_pair[0] < sorted_aligments[0][0]:
			for pairless in source_segments_without_pair:
				data = {'source_survey_itemID': list_source[pairless][0], 'target_survey_itemID': None, 
				'Study': list_source[pairless][1], 'module': list_source[pairless][2], 
				'item_type': list_source[pairless][3], 'item_name':list_source[pairless][4], 
				'item_value': None, 'source_text': list_source[pairless][6], 'target_text': None, 
				'source_ner_tagged_text': list_source[pairless][7],'target_ner_tagged_text': None,
				'source_pos_tagged_text': list_source[pairless][8], 'target_pos_tagged_text':None}
				df = df.append(data, ignore_index=True)

			for alignment in sorted_aligments:
				source_index = alignment[0]
				target_index = alignment[1]

				data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
				'Study': list_source[source_index][1], 'module': list_source[source_index][2], 
				'item_type': list_source[source_index][3], 'item_name':list_source[source_index][4], 
				'item_value': None, 'source_text': list_source[source_index][6],'target_text': list_target[target_index][6],
				'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
				'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
				df = df.append(data, ignore_index=True)

	else:
		for alignment in sorted_aligments:
			source_index = alignment[0]
			target_index = alignment[1]
			
			for pairless in source_segments_without_pair:
				if pairless < source_index:
					data = {'source_survey_itemID': list_source[pairless][0], 'target_survey_itemID': None, 
					'Study': list_source[pairless][1], 'module': list_source[pairless][2], 
					'item_type': list_source[pairless][3], 'item_name':list_source[pairless][4], 
					'item_value': None, 'source_text': list_source[pairless][6], 'target_text': None, 
					'source_ner_tagged_text': list_source[pairless][7],'target_ner_tagged_text': None,
					'source_pos_tagged_text': list_source[pairless][8], 'target_pos_tagged_text':None}
					df = df.append(data, ignore_index=True)

					source_segments_without_pair.remove(pairless)

			data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
			'Study': list_source[source_index][1], 'module': list_source[source_index][2], 
			'item_type': list_source[source_index][3], 'item_name':list_source[source_index][4], 
			'item_value': None, 'source_text': list_source[source_index][6],'target_text': list_target[target_index][6],
			'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
			'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
			df = df.append(data, ignore_index=True)

		if source_segments_without_pair:
			index = source_segments_without_pair[0]
			data = {'source_survey_itemID': list_source[index][0], 'target_survey_itemID': None, 
			'Study': list_source[index][1], 'module': list_source[index][2], 
			'item_type': list_source[index][3], 'item_name':list_source[index][4], 
			'item_value': None, 'source_text': list_source[index][6], 'target_text': None, 
			'source_ner_tagged_text': list_source[index][7],'target_ner_tagged_text': None,
			'source_pos_tagged_text': list_source[index][8], 'target_pos_tagged_text':None}
			df = df.append(data, ignore_index=True)

	return df


def treat_multiple_pairless_target_segments(list_source, list_target, sorted_aligments, target_segments_without_pair, df):
	"""
	Align source and target segments, in case where there are multiple target segments without a pair.

	Args:
		param1 list_source (list): list of source segments (contains segments of same item_name and item_type)
		param2 list_target (list): list of target segments (contains segments of same item_name and item_type)
		param3 sorted_aligments (list): sorted list segments aligned via best match strategy.
		param4 target_segments_without_pair (list): indexes of pairless target segments
		param5 df (pandas dataframe): dataframe to store the questionnaire alignment

	Returns:
		df (pandas dataframe) with newly aligned survey item segments.
	"""
	if sorted(target_segments_without_pair) == list(range(min(target_segments_without_pair), max(target_segments_without_pair)+1)):
		if target_segments_without_pair[0] > sorted_aligments[0][-1]:	
			for alignment in sorted_aligments:
				source_index = alignment[1]
				target_index = alignment[0]

				data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
				'Study': list_target[target_index][1], 'module': list_target[target_index][2], 
				'item_type': list_target[target_index][3], 'item_name':list_target[target_index][4], 
				'item_value': None, 'source_text': list_source[source_index][6],'target_text': list_target[target_index][6],
				'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
				'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
				df = df.append(data, ignore_index=True)

			for pairless in target_segments_without_pair:
				data = {'source_survey_itemID': None, 'target_survey_itemID': list_target[pairless][0], 
				'Study': list_target[pairless][1], 'module': list_target[pairless][2], 
				'item_type': list_target[pairless][3], 'item_name':list_target[pairless][4], 
				'item_value': None, 'source_text': None, 'target_text': list_target[pairless][6],
				'source_ner_tagged_text': None, 'target_ner_tagged_text': list_target[pairless][7], 
				'source_pos_tagged_text': None, 'target_pos_tagged_text': list_target[pairless][8]}
				df = df.append(data, ignore_index=True)

		elif target_segments_without_pair[0] < sorted_aligments[0][0]:
			for pairless in target_segments_without_pair:
				data = {'source_survey_itemID': None, 'target_survey_itemID': list_target[pairless][0], 
				'Study': list_target[pairless][1], 'module': list_target[pairless][2], 
				'item_type': list_target[pairless][3], 'item_name':list_target[pairless][4], 
				'item_value': None, 'source_text': None, 'target_text': list_target[pairless][6],
				'source_ner_tagged_text': None, 'target_ner_tagged_text': list_target[pairless][7], 
				'source_pos_tagged_text': None, 'target_pos_tagged_text': list_target[pairless][8]}
				df = df.append(data, ignore_index=True)

			for alignment in sorted_aligments:
				source_index = alignment[1]
				target_index = alignment[0]

				data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
				'Study': list_target[target_index][1], 'module': list_target[target_index][2], 
				'item_type': list_target[target_index][3], 'item_name':list_target[target_index][4], 
				'item_value': None, 'source_text': list_source[source_index][6], 'target_text': list_target[target_index][6],
				'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
				'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
				df = df.append(data, ignore_index=True)

	else:
		for alignment in sorted_aligments:
			source_index = alignment[1]
			target_index = alignment[0]
			
			for pairless in target_segments_without_pair:
				if pairless < target_index:
					data = {'source_survey_itemID': None, 'target_survey_itemID': list_target[pairless][0], 
					'Study': list_target[pairless][1], 'module': list_target[pairless][2], 
					'item_type': list_target[pairless][3], 'item_name':list_target[pairless][4], 
					'item_value': None, 'source_text': None, 'target_text': list_target[pairless][6],
					'source_ner_tagged_text': None, 'target_ner_tagged_text': list_target[pairless][7], 
					'source_pos_tagged_text': None, 'target_pos_tagged_text': list_target[pairless][8]}
					df = df.append(data, ignore_index=True)

					target_segments_without_pair.remove(pairless)

			data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0], 
			'Study': list_target[target_index][1], 'module': list_target[target_index][2], 
			'item_type': list_target[target_index][3], 'item_name':list_target[target_index][4], 
			'item_value': None, 'source_text': list_source[source_index][6], 'target_text': list_target[target_index][6],
			'source_ner_tagged_text': list_source[source_index][7], 'target_ner_tagged_text': list_target[target_index][7], 
			'source_pos_tagged_text': list_source[source_index][8], 'target_pos_tagged_text': list_target[target_index][8]}
			df = df.append(data, ignore_index=True)

		if target_segments_without_pair:
			index = target_segments_without_pair[0]
			data = {'source_survey_itemID': None, 'target_survey_itemID': list_target[index][0], 
			'Study': list_target[index][1], 'module': list_target[index][2], 
			'item_type': list_target[index][3], 'item_name':list_target[index][4], 
			'item_value': None, 'source_text': None, 'target_text': list_target[index][6],
			'source_ner_tagged_text': None, 'target_ner_tagged_text': list_target[index][7], 
			'source_pos_tagged_text': None, 'target_pos_tagged_text': list_target[index][8]}
			df = df.append(data, ignore_index=True)

	return df


def align_more_segments_in_target(list_source, list_target, sorted_aligments, target_segments_without_pair, df):
	"""
	Calls the appropriate method for alignment with more segments in target dataframe, concerning the number
	of pairless segments. 
	This method is called from a broader sets of cases contained in prepare_alignment_with_more_segments_in_source.
	If there is only one pairless target segment, call treat_a_single_pairless_target(),
	otherwise call treat_multiple_pairless_target_segments()

	Args:
		param1 list_source (list): list of source segments (contains segments of same item_name and item_type)
		param2 list_target (list): list of target segments (contains segments of same item_name and item_type)
		param3 sorted_aligments (list): sorted list segments aligned via best match strategy.
		param4 target_segments_without_pair (list): indexes of pairless target segments
		param5 df (pandas dataframe): dataframe to store the questionnaire alignment

	Returns:
		df (pandas dataframe) with newly aligned survey item segments.
	"""
	if len(target_segments_without_pair) == 1:
		df = treat_a_single_pairless_target(list_source, list_target, sorted_aligments, target_segments_without_pair[0], df)
	else:
		df = treat_multiple_pairless_target_segments(list_source, list_target, sorted_aligments, target_segments_without_pair, df)

	return df


def align_more_segments_in_source(list_source, list_target, sorted_aligments, source_segments_without_pair, df):
	"""
	Calls the appropriate method for alignment with more segments in source dataframe, concerning the number
	of pairless segments. 
	This method is called from a broader sets of cases contained in prepare_alignment_with_more_segments_in_source.
	If there is only one pairless source segment, call treat_a_single_pairless_source(),
	otherwise call treat_multiple_pairless_source_segments()

	Args:
		param1 list_source (list): list of source segments (contains segments of same item_name and item_type)
		param2 list_target (list): list of target segments (contains segments of same item_name and item_type)
		param3 sorted_aligments (list): sorted list segments aligned via best match strategy.
		param4 source_segments_without_pair (list): indexes of pairless source segments
		param5 df (pandas dataframe): dataframe to store the questionnaire alignment

	Returns:
		df (pandas dataframe) with newly aligned survey item segments.
	"""
	if len(source_segments_without_pair) == 1:
		df = treat_a_single_pairless_source(list_source, list_target, sorted_aligments, source_segments_without_pair[0], df)
	else:
		df = treat_multiple_pairless_source_segments(list_source, list_target, sorted_aligments, source_segments_without_pair, df)
			
	return df


def prepare_alignment_with_more_segments_in_source(df, list_source, list_target, item_type):
	"""
	Calls the appropriate method for alignment with more segments in source dataframe, concerning the number
	of pairless segments

	Args:
		param1 df (pandas dataframe): dataframe to store the questionnaire alignment
		param2 list_source (list): list of source segments (contains segments of same item_name and item_type)
		param3 list_target (list): list of target segments (contains segments of same item_name and item_type)
		param4 item_type (string): item_type metadata, can be REQUEST, INTRODUCTION or INSTRUCTION

	Returns:
		df (pandas dataframe) with newly aligned survey item segments.
	"""

	"""
	index 0 = target
	index 1 = source
	"""
	first_alignment = find_best_match(list_source, list_target, item_type)
	target_segment_index = first_alignment[0]
	source_segment_index = first_alignment[1]

	aux_source = list_source.copy()
	del aux_source[source_segment_index]

	aux_target = list_target.copy()
	del aux_target[target_segment_index]

	"""
	This is the case where there is only one target segment for two or more source segments
	"""
	if not aux_target:
		df = only_one_segment_in_target_align(first_alignment, list_source[source_segment_index], 
			list_target[target_segment_index], list_source, aux_source, df)
	#If there are still other source segments, call best match method again
	else:
		alignments = [[source_segment_index, target_segment_index]]
		source_segments_paired = [source_segment_index]
		while aux_target:
			alignment = find_best_match(aux_source, aux_target, item_type)
			target_segment_index = alignment[0]
			source_segment_index = alignment[1]

			original_index_target, original_index_source = get_original_index(list_source, list_target, 
				source_segment_index, target_segment_index, aux_source, aux_target)

			alignments.append([original_index_source,original_index_target])

			source_segments_paired.append(original_index_source)

			del aux_source[source_segment_index]
			del aux_target[target_segment_index]

			
		sorted_aligments = sorted(alignments)
		indexes_of_source_segment_index = [index for index, value in enumerate(list_source)]
		source_segments_without_pair = list(set(indexes_of_source_segment_index) - set(source_segments_paired))
		df = align_more_segments_in_source(list_source, list_target, sorted_aligments, source_segments_without_pair, df)

	return df



def prepare_alignment_with_more_segments_in_target(df, list_source, list_target, item_type):
	"""
	Calls the appropriate method for alignment with more segments in target dataframe, concerning the number
	of pairless segments

	Args:
		param1 df (pandas dataframe): dataframe to store the questionnaire alignment
		param2 list_source (list): list of source segments (contains segments of same item_name and item_type)
		param3 list_target (list): list of target segments (contains segments of same item_name and item_type)
		param4 item_type (string): item_type metadata, can be REQUEST, INTRODUCTION or INSTRUCTION

	Returns:
		df (pandas dataframe) with newly aligned survey item segments.
	"""

	"""
	index 0 = target
	index 1 = source
	"""
	first_alignment = find_best_match(list_source, list_target, item_type)
	target_segment_index = first_alignment[0]
	source_segment_index = first_alignment[1]

	aux_source = list_source.copy()
	del aux_source[source_segment_index]

	aux_target = list_target.copy()
	del aux_target[target_segment_index]

	"""
	This is the case where there is only one source segment for two or more target segments
	"""
	if not aux_source:
		df = only_one_segment_in_source_align(first_alignment, list_source[source_segment_index], 
			list_target[target_segment_index], list_target, aux_target, df)
	
	#If there are still other source segments, call best match method again
	else:
		alignments = [[target_segment_index, source_segment_index]]
		target_segments_paired = [target_segment_index]
		while aux_source:
			alignment = find_best_match(aux_source, aux_target, item_type)
			target_segment_index = alignment[0]
			source_segment_index = alignment[1]

			original_index_target, original_index_source = get_original_index(list_source, list_target, 
				source_segment_index, target_segment_index, aux_source, aux_target)

			alignments.append([original_index_target, original_index_source])

			target_segments_paired.append(original_index_target)

			del aux_source[source_segment_index]
			del aux_target[target_segment_index]

			
		sorted_aligments = sorted(alignments)
		indexes_of_target_segment_index = [index for index, value in enumerate(list_target)]
		target_segments_without_pair = list(set(indexes_of_target_segment_index) - set(target_segments_paired))
		df = align_more_segments_in_target(list_source, list_target, sorted_aligments, target_segments_without_pair, df)

	return df 




def b_match(list_target, list_source):
	dict_ratios = dict()
	##
	for target in list_target:
		for source in list_source:
			t = preprocessing_alignment_candidates(target[6])
			s = preprocessing_alignment_candidates(source[6])
			if 'ENG' in target[0]:
				if abs(len(t)-len(s)) in dict_ratios.keys():
					dict_ratios[abs(len(t)-len(s))+0.1] = [target[0],source[0]] 
				else:
					dict_ratios[abs(len(t)-len(s))] = [target[0],source[0]] 
			else:
				print(t, s)
				print(abs(len(t)-len(s))-0.05*use_bilingual_dict(s, t))
				if abs(len(t)-len(s))-0.05*use_bilingual_dict(s, t) in dict_ratios.keys():
					dict_ratios[abs(len(t)-len(s))-0.05*use_bilingual_dict(s, t)+0.1] = [target[0],source[0]] 
				else:
					dict_ratios[abs(len(t)-len(s))-0.05*use_bilingual_dict(s, t)] = [target[0],source[0]] 

	best_candidate = min(dict_ratios)
	print(best_candidate)
	values = dict_ratios[best_candidate]

	for i, item in enumerate(list_source):
		if item[0] == values[1]:
			source_best = list_source[i]
			source_best_index = i
			break

	for i, item in enumerate(list_target):
		if item[0] == values[0]:
			target_best = list_target[i]
			target_best_index = i
			break


	return source_best, source_best_index, target_best, target_best_index

def align_introduction_instruction_request(df, df_source, df_target, item_type):
	"""
	Aligns introduction, instruction and requests segments. Differently from response segments, these other item types can't be
	merged. There are five distinct cases to consider: 1) only source segments (df_target is empty), 2) only target segments (df_source is empty),
	3) df_source has more segments than df_target 4) df_target has more segments than df_source and, 5) df_source and df_target have the 
	same number of segments.

	Args:
		param1 df (pandas dataframe): dataframe to store the questionnaire alignment.
		param2 df_source (pandas dataframe): dataframe containing the data of the source questionnaire (always English).
		param3 df_target (pandas dataframe): dataframe containing the data of the target questionnaire
		param4 item_type (string): metadata that indicates if the dataframes contain introductions, instructions or requests.

	Returns:
		df (pandas dataframe) with newly aligned survey item segments.
	"""
	df_source = df_source[df_source['item_type']==item_type]
	df_target = df_target[df_target['item_type']==item_type]


	if df_source.empty:
		for i,row in df_target.iterrows():
			data = {'source_survey_itemID': None, 'target_survey_itemID': row['survey_item_ID'], 'Study': row['Study'], 
			'module': row['module'], 'item_type': item_type, 'item_name':row['item_name'], 'item_value': None, 
			'source_text': None, 'target_text': row['text'], 'source_ner_tagged_text': None, 
			'target_ner_tagged_text': row['ner_tagged_text'], 'source_pos_tagged_text': None, 'target_pos_tagged_text': row['pos_tagged_text']}
			df = df.append(data, ignore_index=True)
		return df

	if df_target.empty:
		for i,row in df_source.iterrows():
			data = {'source_survey_itemID': row['survey_item_ID'], 'target_survey_itemID': None , 'Study': row['Study'], 
			'module': row['module'], 'item_type': item_type, 'item_name':row['item_name'], 'item_value': None, 
			'source_text': row['text'], 'target_text': None, 'source_ner_tagged_text': row['ner_tagged_text'], 
			'target_ner_tagged_text': None, 'source_pos_tagged_text': row['pos_tagged_text'], 'target_pos_tagged_text':None}
			df = df.append(data, ignore_index=True)
		return df
	else:
		list_target = df_target.values.tolist()
		list_source = df_source.values.tolist()

		if len(list_source) > len(df_target):
			df = prepare_alignment_with_more_segments_in_source(df, list_source, list_target, item_type)
			return df

		elif len(list_target) > len(list_source):
			df = prepare_alignment_with_more_segments_in_target(df, list_source, list_target, item_type)
			return df

		elif len(list_target) == len(list_source):
			showc = identify_showc_segment(list_source, list_target, item_type)
			if item_type == 'INSTRUCTION' and showc != 'No showc segment identified':
				target_index = showc[0]
				source_index = showc[1]

				aux_source = list_source.copy()
				del aux_source[source_index]

				aux_target = list_target.copy()
				del aux_target[target_index]

				data = {'source_survey_itemID': list_source[source_index][0], 'target_survey_itemID': list_target[target_index][0] , 
					'Study': list_source[source_index][1], 'module': list_source[source_index][2], 'item_type': item_type, 
					'item_name':list_source[source_index][4], 'item_value': None, 'source_text': list_source[source_index][6], 
					'target_text':  list_target[target_index][6], 'source_ner_tagged_text': list_source[source_index][7], 
					'target_ner_tagged_text': list_target[target_index][7], 'source_pos_tagged_text': list_source[source_index][8], 
					'target_pos_tagged_text':list_target[target_index][8]}
				df = df.append(data, ignore_index=True)

				del list_source[source_index]
				del list_target[target_index]

			if len(list_source) == 1:
				data = {'source_survey_itemID': list_source[0][0], 'target_survey_itemID': list_target[0][0] , 'Study': list_source[0][1], 
					'module': list_source[0][2], 'item_type': item_type, 'item_name':list_source[0][4], 'item_value': None, 
					'source_text': list_source[0][6], 'target_text':  list_target[0][6], 'source_ner_tagged_text': list_source[0][7], 
					'target_ner_tagged_text': list_target[0][7], 'source_pos_tagged_text': list_source[0][8], 
					'target_pos_tagged_text': list_target[0][8]}
				df = df.append(data, ignore_index=True)

			else:
				while list_source:
					source_best, source_best_index, target_best, target_best_index = b_match(list_target, list_source)
					data = {'source_survey_itemID': source_best[0], 'target_survey_itemID': target_best[0] , 'Study': source_best[1], 
						'module': source_best[2], 'item_type': item_type, 'item_name':source_best[4], 'item_value': None, 
						'source_text': source_best[6], 'target_text':  target_best[6], 'source_ner_tagged_text': source_best[7], 
						'target_ner_tagged_text': target_best[7], 'source_pos_tagged_text': source_best[8], 
						'target_pos_tagged_text': target_best[8]}
					df = df.append(data, ignore_index=True)

					del list_source[source_best_index]
					del list_target[target_best_index]

	return df




def align_responses(df, df_source, df_target):
	"""
	Aligns response segments by merging them on item_value metadata.
	Args:
		param1 df (pandas dataframe): dataframe to store the questionnaire alignment
		param2 df_source (pandas dataframe): dataframe containing the data of the source questionnaire (always English).
		param3 df_target (pandas dataframe): dataframe containing the data of the target questionnaire

	Returns:
		df (pandas dataframe) with newly aligned response segments.
	"""
	df_source = df_source[df_source['item_type']=='RESPONSE']
	df_target = df_target[df_target['item_type']=='RESPONSE']

	df_merge = pd.merge(df_source, df_target, on='item_value')

	for i, row in df_merge.iterrows():
		data = {'source_survey_itemID': row['survey_item_ID_x'], 'target_survey_itemID':  row['survey_item_ID_y'], 'Study': row['Study_x'], 
		'module': row['module_x'], 'item_type': 'RESPONSE', 'item_name':row['item_name_x'], 'item_value': row['item_value'], 
		'source_text': row['text_x'], 'target_text': row['text_y'], 'source_ner_tagged_text': row['ner_tagged_text_x'], 
		'target_ner_tagged_text': row['ner_tagged_text_y'], 'source_pos_tagged_text': row['pos_tagged_text_x'], 'target_pos_tagged_text': row['pos_tagged_text_y']}
		df = df.append(data, ignore_index=True)

	return df


def align_on_metadata(df, df_source, df_target, process_responses):
	"""
	Calls the appropriate method for alignment based on metadata.
	Responses are aligned separately of other item types because answers are merged using the item value.
	
	Args:
		param1 df (pandas dataframe): dataframe to store the questionnaire alignment
		param2 df_source (pandas dataframe): dataframe containing the data of the source questionnaire (always English).
		param3 df_target (pandas dataframe): dataframe containing the data of the target questionnaire
		param4 process_responses (boolean): indicates if the response segments should be processed, country-specific answers are excluded by design. 

	Returns:
		df (pandas dataframe) with newly aligned survey items.
	"""
	df = align_introduction_instruction_request(df, df_source, df_target, 'INTRODUCTION')
	df = align_introduction_instruction_request(df, df_source, df_target, 'INSTRUCTION')
	df = align_introduction_instruction_request(df, df_source, df_target, 'REQUEST')
	if process_responses:
		df = align_responses(df, df_source, df_target)
	

	return df



def filter_by_module(df_source, df_target, module):
	"""
	Filters the source and target dataframes by the module that is being currently analyzed.

	Args:
		param1 df_source (pandas dataframe): dataframe containing the data of the source questionnaire (always English).
		param2 df_target (pandas dataframe): dataframe containing the data of the target questionnaire
		param3 module (string): questionnaire module being currently analyzed in outer loop.

	Returns:
		df_source (pandas dataframe) and param2 df_target (pandas dataframe). Source and target dataframes filtered
		by the module specified by parameter.
	"""
	df_source = df_source[df_source['module']==module]
	df_target = df_target[df_target['module']==module]

	return df_source, df_target
				

def get_study_metadata(filename):
	"""
	Get study metadata embedded in filename. It can be retrieved either from 
	the source or the target file.

	Args:
		param1 filename (string): name of either source or target file.

	Returns:
		study (string). Metadata that identifies the study of the questionnaires that are being aligned.
	"""
	filename = filename.split('_')
	study = filename[0]+'_'+filename[1]+'_'+filename[2]
	
	return study


def get_target_language_country_metadata(filename):
	"""
	Get target language/country metadata embedded in filename, to name the output aligned file.

	Args:
		param1 filename (string): name of target file.

	Returns:
		target_language_country (string). Metadata that identifies the language/country of the target questionnaire being aligned.
	"""
	filename_without_extension = filename.replace('.csv', '')
	filename_without_extension = filename_without_extension.split('_')
	target_language_country = filename_without_extension[3]+'_'+filename_without_extension[4]
	
	return target_language_country




def main(folder_path, filename_source):

	path = os.chdir(folder_path)
	files = os.listdir(path)
	df_source = pd.read_csv(filename_source,  dtype=str, sep='\t')

	for index, filename_target in enumerate(files):
		if filename_target.endswith(".csv"):
			if filename_target != filename_source:
	
				df_target = pd.read_csv(filename_target,  dtype=str, sep='\t')

				df = pd.DataFrame(columns=['source_survey_itemID', 'target_survey_itemID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 
					'source_text', 'target_text', 'source_ner_tagged_text', 'source_pos_tagged_text', 'target_ner_tagged_text', 'target_pos_tagged_text'])


				study = get_study_metadata(filename_source)
				global target_language_country
				target_language_country = get_target_language_country_metadata(filename_target)

				if 'ENG' not in target_language_country:
					global mcsq_bi
					if 'RUS' in target_language_country:
						mcsq_bi = Word2word.load("en", convert_iso_code(target_language_country.split('_')[0]), "/home/danielly/workspace/MCSQ_compiling/resources/bilingual/"+target_language_country.split('_')[0])
					elif target_language_country == 'FRE_LU':
						mcsq_bi = Word2word.load("en", convert_iso_code('FRE'), "/home/danielly/workspace/MCSQ_compiling/resources/bilingual/FRE_CH")
					elif target_language_country == 'GER_LU':
						mcsq_bi = Word2word.load("en", convert_iso_code('GER'), "/home/danielly/workspace/MCSQ_compiling/resources/bilingual/GER_CH")
					elif target_language_country == 'POR_LU':
						mcsq_bi = Word2word.load("en", convert_iso_code('POR'), "/home/danielly/workspace/MCSQ_compiling/resources/bilingual/POR_PT")
					else:
						mcsq_bi = Word2word.load("en", convert_iso_code(target_language_country.split('_')[0]), "/home/danielly/workspace/MCSQ_compiling/resources/bilingual/"+target_language_country)

				global st
				st = stopwords.words('english')

				if 'EVS' in study:
					source_language_country = 'ENG_GB'
				else:
					source_language_country = 'ENG_SOURCE'

				if 'EVS' in study or 'ESS' in study:
					country_specific_requests = instantiate_country_specific_request_object(study)


				"""
				Computes the intersection between the modules of source and target questionnaires.
				We are only interested in aligning modules that are present in both files.
				"""
				intersection_modules = set(df_source.module.unique()).intersection(set(df_target.module.unique()))
				for module in sorted(intersection_modules):
					if 'EVS_R03' in filename_source and 'Socio Demographics' in module:
						"""
						Unfortunately the Socio Demographics section of the EVS wave 3 files have many inconsistencies concerning the item names.
						This module won't be aligned because of the risk of creating many wrongly aligned segments.
						"""
						pass
					else:
						df_source_filtered, df_target_filtered = filter_by_module(df_source, df_target, module)
						
						unique_item_names_source = df_source_filtered.item_name.unique()
						unique_item_names_target = df_target_filtered.item_name.unique()
						
						for unique_item_name in unique_item_names_source:
							process_responses = True
							if 'EVS' in study or 'ESS' in study:
								if unique_item_name.lower() in country_specific_requests.item_names:
									process_responses = False
							"""
							Computes the intersection between the item names of source and target questionnaires.
							We are only interested in aligning questions that are present in both files.
							"""
							df_source_by_item_name = df_source_filtered[df_source_filtered['item_name'].str.lower()==unique_item_name.lower()]
							df_target_by_item_name = df_target_filtered[df_target_filtered['item_name'].str.lower()==unique_item_name.lower()]
							
							if df_target_by_item_name.empty == False and df_source_by_item_name.empty == False:
								df = align_on_metadata(df, df_source_by_item_name, df_target_by_item_name, process_responses)
							
				
				df.to_csv(source_language_country+'_'+target_language_country+'_'+study+'.csv', encoding='utf-8', sep='\t', index=False)
	




if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	filename_source = str(sys.argv[2])
	main(folder_path, filename_source)
