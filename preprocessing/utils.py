"""
Python3 script with utility functions for preprocessing
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 
import re
from itertools import groupby
import pandas as pd
import nltk

initial_sufix = 0


def reset_initial_sufix():
	global initial_sufix
	initial_sufix = 0

def update_survey_item_id(prefix):
	global initial_sufix
	initial_sufix = initial_sufix + 1
	survey_item_id = prefix+str(initial_sufix)
	
	return survey_item_id

def get_survey_item_id(prefix):
	global initial_sufix
	survey_item_id = prefix+str(initial_sufix)

	return survey_item_id

def decide_on_survey_item_id(prefix, old_item_name, new_item_name):
	if old_item_name == new_item_name:
		survey_item_id = get_survey_item_id(prefix)
	else:
		survey_item_id = update_survey_item_id(prefix)


	return survey_item_id

def recognize_standard_response_scales(filename, text):
	if 'BUL' in filename:
		dk_pattern = re.compile("(Не зная)", re.IGNORECASE)
		refusal_pattern = re.compile("(Без отговор)", re.IGNORECASE)
		dontapply_pattern = re.compile("(Неприложимо|Не се отнася|до мен Не се отнася за мен)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'CZE' in filename:
		dk_pattern = re.compile("(Neví)", re.IGNORECASE)
		refusal_pattern = re.compile("(Neodpověděl|neodpověděl(a)|BEZ ODPOVĚDI)", re.IGNORECASE)
		dontapply_pattern = re.compile("(Nehodí se)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'DAN' in filename:
		dk_pattern = re.compile("(Ved ikke)", re.IGNORECASE)
		refusal_pattern = re.compile("(Uoplyst)", re.IGNORECASE)
		dontapply_pattern = re.compile("(Irrelevant)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'DUT' in filename:
		dk_pattern = re.compile("(weet niet)", re.IGNORECASE)
		refusal_pattern = re.compile("(geen antwoord)", re.IGNORECASE)
		dontapply_pattern = re.compile("(niet van toepassing)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'ENG' in filename:
		dk_pattern = re.compile("(don't know)", re.IGNORECASE)
		refusal_pattern = re.compile("(refusal|no answer)", re.IGNORECASE)
		dontapply_pattern = re.compile("(not applicable)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None 

	if 'EST' in filename:
		dk_pattern = re.compile("(RÖ)", re.IGNORECASE)
		refusal_pattern = re.compile("(VP)", re.IGNORECASE)
		dontapply_pattern = re.compile("(niet van toepassing)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'FIN' in filename:
		dk_pattern = re.compile("(Ei osaa sanoa)", re.IGNORECASE)
		refusal_pattern = re.compile("(Ei vastausta)", re.IGNORECASE)
		dontapply_pattern = re.compile("(Ei sovellu|Ei sovi vastaajaan)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'FRE' in filename:
		dk_pattern = re.compile("(ne sait pas)", re.IGNORECASE)
		refusal_pattern = re.compile("(pas de réponse|refus|sans réponse|sans reponse)", re.IGNORECASE)
		dontapply_pattern = re.compile("(ne s'applique pas|Non applicable|Pas d'application|Non concerné)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None 

	if 'GER' in filename:
		dk_pattern = re.compile("(weiß nicht|weiss nicht)", re.IGNORECASE)
		refusal_pattern = re.compile("(verweigert|keine Antwort|Keine Antwort)", re.IGNORECASE)
		dontapply_pattern = re.compile("(trifft nicht zu|nicht zutreffend)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None 

	if 'GRE' in filename:
		dk_pattern = re.compile("(Δεν ξέρω)", re.IGNORECASE)
		refusal_pattern = re.compile("(Δεν απαντώ)", re.IGNORECASE)
		dontapply_pattern = re.compile("(Δεν ισχύει)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None 

	if 'HRV' in filename:
		dk_pattern = re.compile("(ne znam)", re.IGNORECASE)
		refusal_pattern = re.compile("(nema odgovora)", re.IGNORECASE)
		dontapply_pattern = re.compile("(pitanje se ne odnosi na ispitanika|ne primjenjuje se)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None 

	if 'HUN' in filename:
		dk_pattern = re.compile("(nem tudom)", re.IGNORECASE)
		refusal_pattern = re.compile("(nincs válasz)", re.IGNORECASE)
		dontapply_pattern = re.compile("(nem kellet feltenni a kérdést|nem kellett feltenni)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None 


	if 'ITA' in filename:
		dk_pattern = re.compile("(Non so|Non sa)", re.IGNORECASE)
		refusal_pattern = re.compile("(non risponde)", re.IGNORECASE)
		dontapply_pattern = re.compile("(non pertinente)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'ICE' in filename:
		dk_pattern = re.compile("(veit ekki)", re.IGNORECASE)
		refusal_pattern = re.compile("(svarar ekki|Neitar að svara)", re.IGNORECASE)
		dontapply_pattern = re.compile("(non pertinente)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'LIT' in filename:
		dk_pattern = re.compile("(netaikoma)", re.IGNORECASE)
		refusal_pattern = re.compile("(neatsakė)", re.IGNORECASE)
		dontapply_pattern = re.compile("(nežinau)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'LAV' in filename:
		dk_pattern = re.compile("(nezin)", re.IGNORECASE)
		refusal_pattern = re.compile("(nav atbildes)", re.IGNORECASE)
		dontapply_pattern = re.compile("(nav atbilstošs)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'LTZ' in filename:
		dk_pattern = re.compile("(Ne sait pas)", re.IGNORECASE)
		refusal_pattern = re.compile("(Keng Äntwert|Pas de réponse|Refus)", re.IGNORECASE)
		dontapply_pattern = re.compile("(nav atbilstošs)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None


	if 'NOR' in filename:
		dk_pattern = re.compile("(Vet ikke)", re.IGNORECASE)
		refusal_pattern = re.compile("(Ikke svar)", re.IGNORECASE)
		dontapply_pattern = re.compile("(NA)")

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None


	if 'POR' in filename:
		dk_pattern = re.compile("(não sabe)", re.IGNORECASE)
		refusal_pattern = re.compile("(não responde)", re.IGNORECASE)
		dontapply_pattern = re.compile("(não se aplica)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'POL' in filename:
		dk_pattern = re.compile("(trudno powiedzieć)", re.IGNORECASE)

		#fake values - no translation for these items in XML
		refusal_pattern = re.compile("(CEVAP VERMİYOR)", re.IGNORECASE)
		dontapply_pattern = re.compile("(Soru Sorulmadı)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'RUS' in filename:
		if 'LV' in filename:
			dk_pattern = re.compile("(Затрудняюсь ответить|Не знает)", re.IGNORECASE)
			refusal_pattern = re.compile("(Отказ от ответа|Нет ответа)", re.IGNORECASE)
			dontapply_pattern = re.compile("(не соответствующий|не применимо)", re.IGNORECASE)

			if dk_pattern.match(text):
				return 'dk'
			elif refusal_pattern.match(text):
				return 'refusal'
			elif dontapply_pattern.match(text):
				return 'dontapply'
			else:
				return None


		else:
			dk_pattern = re.compile("(Затрудняюсь ответить|Не знаю)", re.IGNORECASE)
			refusal_pattern = re.compile("(Отказ от ответа|Нет ответа)", re.IGNORECASE)
			if 'BY' in filename:
				dontapply_pattern = re.compile("(вопрос не применим|не применимо)", re.IGNORECASE)
			else:
				dontapply_pattern = re.compile("(Не подходит|НЕ ПРИМЕНИМО)", re.IGNORECASE)

			if dk_pattern.match(text):
				return 'dk'
			elif refusal_pattern.match(text):
				return 'refusal'
			elif dontapply_pattern.match(text):
				return 'dontapply'
			else:
				return None

	if 'SPA' in filename:
		dk_pattern = re.compile("(No sabe)", re.IGNORECASE)
		refusal_pattern = re.compile("(no contesta)", re.IGNORECASE)
		dontapply_pattern = re.compile("(no aplicable)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'SWE' in filename:
		dk_pattern = re.compile("(Vet ej)", re.IGNORECASE)

		#fake values - no translation for these items in XML
		refusal_pattern = re.compile("(CEVAP VERMİYOR)", re.IGNORECASE)
		dontapply_pattern = re.compile("(Soru Sorulmadı)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'SLO' in filename:
		dk_pattern = re.compile("(nevie)", re.IGNORECASE)
		refusal_pattern = re.compile("(neodpovedal)", re.IGNORECASE)
		dontapply_pattern = re.compile("(nehodí sa)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'SLV' in filename:
		dk_pattern = re.compile("(ne vem)", re.IGNORECASE)
		refusal_pattern = re.compile("(brez odgovora)", re.IGNORECASE)
		dontapply_pattern = re.compile("(se ne nanaša)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'TUR' in filename:
		dk_pattern = re.compile("(BİLMİYOR-FİKRİ YOK)", re.IGNORECASE)
		refusal_pattern = re.compile("(CEVAP VERMİYOR)", re.IGNORECASE)
		dontapply_pattern = re.compile("(Soru Sorulmadı)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None

	if 'UKR' in filename:
		dk_pattern = re.compile("(Важко відповісти)", re.IGNORECASE)
		refusal_pattern = re.compile("(Відмова від відповіді)", re.IGNORECASE)
		dontapply_pattern = re.compile("(Не підходить)", re.IGNORECASE)

		if dk_pattern.match(text):
			return 'dk'
		elif refusal_pattern.match(text):
			return 'refusal'
		elif dontapply_pattern.match(text):
			return 'dontapply'
		else:
			return None



	




def determine_country(filename):
	if '_AT' in filename:
		country = 'Austria'
	if '_AZ' in filename:
		country = 'Azerbaijan'
	if '_BE' in filename:
		country = 'Belgium'
	if '_BY' in filename:
		country = 'Belarus'
	if '_BG' in filename:
		country = 'Bulgaria'
	if '_CH' in filename:
		country = 'Switzerland'
	if '_CY' in filename:
		if 'TUR' in filename:
			country = 'Northern Cyprus'
		else:
			country = 'Cyprus'
	if '_CZ' in filename:
		country = 'Czech Republic'
	if '_DE' in filename:
		country = 'Germany'
	if '_DK' in filename:
		country = 'Denmark'
	if '_EE' in filename:
		country = 'Estonia'
	if '_ES' in filename:
		country = 'Spain'
	if '_FI' in filename:
		country = 'Finland'
	if '_FR' in filename:
		country = 'France'
	if '_GE' in filename:
		country = 'Georgia'
	if '_GB' in filename or 'SOURCE' in filename:
		country = 'Great Britain'
	if '_GR' in filename:
		country = 'Greece'
	if '_HV' in filename:
		country = 'Bosnia and Herzegovina'
	if '_HU' in filename:
		country = 'Hungary'
	if '_IE' in filename:
		country = 'Ireland'
	if '_IT' in filename:
		country = 'Italy'
	if '_IS' in filename:
		country = 'Iceland'		
	if '_NIR' in filename:
		country = 'Northern Ireland'
	if '_LU' in filename:
		country = 'Luxembourg'
	if '_LV' in filename:
		country = 'Latvia'
	if '_LT' in filename:
		country = 'Lithuania'
	if '_MD' in filename:
		country = 'Moldova'
	if '_ME' in filename:
		country = 'Montenegro'
	if '_MK' in filename:
		country = 'Macedonia'
	if '_MT' in filename:
		country = 'Malta'
	if '_NO' in filename:
		country = 'Norway'
	if '_NL' in filename:
		country = 'Neatherlands'
	if '_PT' in filename:
		country = 'Portugal'
	if '_PL' in filename:
		country = 'Poland'
	if '_RU' in filename:
		country = 'Russian Federation'
	if '_SE' in filename:
		country = 'Sweden'
	if '_SI' in filename:
		country = 'Slovenia'
	if '_SK' in filename:
		country = 'Slovakia'
	if '_TR' in filename:
		country = 'Turkey'
	if '_UA' in filename:
		country = 'Ukraine'


	return country

"""
Provide the sentence splitter suffix to instantiate it in accordance 
to the target language (information emebedded on filename).
:param filename: input file name.
:returns: a sentence splitter suffix according to the target language.
"""
def determine_sentence_tokenizer(filename):
	#there is no sentence segmentation for bulgarian in NLTK.. 
	if 'BUL_' in filename:
		sentence_splitter_suffix = 'turkish.pickle'
	if 'CZE_' in filename:
		sentence_splitter_suffix = 'czech.pickle'
	if 'DAN_' in filename:
		sentence_splitter_suffix = 'danish.pickle'
	if 'DUT_' in filename:
		sentence_splitter_suffix = 'dutch.pickle'
	if 'ENG_' in filename:
		sentence_splitter_suffix = 'english.pickle'
	if 'EST_' in filename:
		sentence_splitter_suffix = 'estonian.pickle'
	if 'FRE_' in filename:
		sentence_splitter_suffix = 'french.pickle'
	if 'FIN_' in filename:
		sentence_splitter_suffix = 'finnish.pickle'
	if 'GER_' in filename:
		sentence_splitter_suffix = 'german.pickle'
	if 'GRE_' in filename:
		sentence_splitter_suffix = 'greek.pickle'
	
	
	if 'ITA_' in filename:
		sentence_splitter_suffix = 'italian.pickle'
	
	if 'NOR_' in filename:
		sentence_splitter_suffix = 'norwegian.pickle'
	if 'POL_' in filename:
		sentence_splitter_suffix = 'polish.pickle'
	if 'POR_' in filename:
		sentence_splitter_suffix = 'portuguese.pickle'
	if 'RUS_' in filename:
		sentence_splitter_suffix = 'russian.pickle'

	if 'SPA_' in filename or 'CAT_' in filename:
		sentence_splitter_suffix = 'spanish.pickle'
	
	if 'SLV_' in filename:
		sentence_splitter_suffix = 'slovene.pickle'
	
	if 'SWE_' in filename:
		sentence_splitter_suffix = 'swedish.pickle'
	if 'TUR_' in filename:
		sentence_splitter_suffix = 'turkish.pickle'

	#there is no sentence segmentation for louxemburgish in NLTK.. 
	if 'UKR_' in filename:
		sentence_splitter_suffix = 'russian.pickle'
	#there is no sentence segmentation for louxemburgish in NLTK.. 
	if 'LTZ_' in filename:
		sentence_splitter_suffix = 'german.pickle'
	#there is no sentence segmentation for maltese in NLTK.. 
	if 'MLT_' in filename:
		sentence_splitter_suffix = 'turkish.pickle'
	#there is no sentence segmentation for croatian in NLTK.. 
	if 'HRV_' in filename:
		sentence_splitter_suffix = 'turkish.pickle'
	

	return sentence_splitter_suffix



"""
Decide what sentence splitter should be instantiated, according to 
the information embedded in the filename.
:param filename: input file name.
:returns: a sentence splitter instantiated according to the target language.
"""
def get_sentence_splitter(filename):
	"""
	Instantiate Punkt Sentence Tokenizer from NLTK	
	"""
	sentence_splitter_prefix = 'tokenizers/punkt/'
	sentence_splitter_suffix = determine_sentence_tokenizer(filename)
	sentence_splitter_path = sentence_splitter_prefix+sentence_splitter_suffix
	sentence_splitter = nltk.data.load(sentence_splitter_path)

	return sentence_splitter
