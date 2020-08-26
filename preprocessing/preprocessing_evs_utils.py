import re
import utils as ut

"""
Standartizes a response category value, if it is a special response category.

Args:
	param1 filename (string): name of the input file.
	param2 catValu (string): response category value, extracted from input file.
	param3 text (string): text of response category, to test against special response category patterns.

Returns: 
	standardized response category value (string). 
"""
def standardize_special_response_category_value(filename, catValu, text):
	"""
	Standard:
	Refusal=777
	Don't know=888
	Does not apply=999
	"""
	if ut.recognize_standard_response_scales(filename, text)=='refusal':
		catValu = '777'
	elif ut.recognize_standard_response_scales(filename, text)=='dk':
		catValu = '888'
	elif ut.recognize_standard_response_scales(filename, text)=='dontapply':
		catValu = '999'

	return catValu

"""
Retrieves the country/language and study metadata based on the input filename.
Args:
	param filename (string): name of the input file.

Returns: 
	country/language (string) and study (string) metadata.
"""
def get_country_language_and_study_info(filename):
	filename_without_extension = re.sub('\.xml', '', filename)
	filename_split = filename_without_extension.split('_')

	study = filename_split[0]+'_'+filename_split[1]+'_'+filename_split[2]
	country_language = filename_split[3]+'_'+filename_split[4]

	return study, country_language

"""
Standartizes a given item_name, if it is not in the standard
Args:
	param1 item_name (string): item name extracted from the input file.

Returns: 
	standardized item_name (string). 
"""
def standardize_item_name(item_name):
	item_name = item_name.lower()
	item_name = re.sub("^q", "Q", item_name)
	item_name = re.sub("^f", "Q", item_name)

	if '.'  in item_name:
		item_name = item_name.split('.')
		item_name = item_name[0]+item_name[1].lower()

	if '_' in item_name and re.findall(r"^Q", item_name):
		item_name = item_name.split('_')
		item_name = item_name[0]+item_name[1].lower()

	if item_name[0].isdigit() or len(item_name)==1:
		item_name = 'Q'+item_name

	print(item_name)

	return item_name


"""
Removes undesired characters from instruction text. 
Args:
	param1 text (string): instruction text extracted from the input file.

Returns: 
	clean instruction text (string) or '' when text is not an instance of a string. 
"""
def clean_instruction(text):
	if isinstance(text, str):
		text = re.sub("…", "...", text)
		text = re.sub("’", "'", text)
		text = re.sub(";", ",", text)
		text = re.sub("[.]{4,}", "", text)
		text = re.sub('>', "",text)
		text = re.sub('<', "",text)
		text = re.sub('Q[0-9]*\.', "",text)
		text = re.sub('\[', "",text)
		text = re.sub('\]', "",text)
		text = text.replace('\n',' ')
		text = text.rstrip()
		text = text.lstrip()
	else:
		text = ''


	return text


"""
Removes undesired characters from request/response text. 
Args:
	param text (string): request/response text extracted from the input file.
	param filename (string): name of the input file.
Returns: 
	clean request/response text (string). 
"""
def clean_text(text, filename):
	if isinstance(text, str):
		text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)
		text = re.sub("…", "...", text)
		text = re.sub(" :", ":", text)
		text = re.sub(";", ",", text)
		text = re.sub("’", "'", text)
		text = re.sub("[.]{4,}", "", text)
		text = re.sub("[_]{2,}", "", text)
		text = re.sub('>', "",text)
		text = re.sub('<', "",text)
		text = re.sub('Q[0-9]*\.', "",text)
		text = re.sub('\[', "",text)
		text = re.sub('\]', "",text)
		text = re.sub('e\.g\.', "e.g.,",text)
		text = text.replace('\n',' ')
		text = text.rstrip()
		text = standardize_special_response_category(filename, text)
	else:
		text = ''



	return text


"""
Standartizes text of special response categories (don't know, no answer, not applicable),
according to the language (informed in the the filename).

Args:
	param1 filename (string): name of the input file.
	param2 text (string): response text.

Returns: 
	standardized response category text (string).
"""
def standardize_special_response_category(filename, text):
	if 'CZE' in filename:
		text = text.replace(' Nehodí se', "NEHODÍ SE")
		text = text.replace('Nehodí se', "NEHODÍ SE")
		text = text.replace('nehodí se', "NEHODÍ SE")
		text = text.replace(' Neví', "NEVÍ")
		text = text.replace(' Bez odpovìdi', "BEZ ODPOVĚDI")
		text = text.replace('Bez odpovìdi', "BEZ ODPOVĚDI")

	#Currently DUT files are not included in MCSQ
	if 'DUT' in filename:
		text = re.sub('^nap', "niet van toepassing",text, flags=re.IGNORECASE)

	if 'ENG' in filename:
		text = re.sub('^NAP$', "Not applicable",text)
		text = re.sub('^DK$', "Don't know",text)
		text = re.sub('^dk$', "Don't know",text)
		text = re.sub('^na$', "No answer",text)
		text = re.sub('^NA$', "No answer",text)
		text = re.sub('^nap$', "Not applicable",text)
		text = re.sub('^N/A$', "Not applicable",text)

	#Currently FIN files are not included in MCSQ
	if 'FIN' in filename:
		text = re.sub('^EOS', "Ei osaa sanoa",text, flags=re.IGNORECASE)
	
	if 'FRE' in filename:
		text = re.sub('^NSP', "Ne sait pas",text, flags=re.IGNORECASE)
		text = re.sub('^S\.R\.', "Pas de réponse",text)
		text = re.sub('^S\.R', "Pas de réponse",text)
		text = re.sub('^SR\.', "Pas de réponse",text)
		text = re.sub('^s\.r', "Pas de réponse",text)
		text = re.sub('^s\.r\.', "Pas de réponse",text)
		text = re.sub('^S\.r', "Pas de réponse",text)
		text = re.sub('^SR', "Pas de réponse",text)
		text = re.sub('^NAP', "Non applicable",text)
		text = text.replace('77777 - Non applicable', 'Non applicable')
	
	if 'GER' in filename:
		text = re.sub('^TNZ', "Trifft nicht zu",text)
		text = re.sub('^WN', "weiß nicht",text)
		text = re.sub('^KA', "keine antwort",text)
		text = re.sub('^k\.\sA\.', "keine antwort",text)
		text = re.sub('^NZT', "nicht zutreffend",text)

	if 'ITA' in filename:
		text = re.sub('^NS', "Non so",text)
		text = re.sub('^NR', "Non risponde",text)
		text = re.sub('^NP', "Non pertinente",text)

	#Currently LTZ files are not included in MCSQ
	if 'LTZ' in filename:
		text = re.sub('^NSP', "Ne sait pas",text)
		text = re.sub('^SR', "Pas de réponse",text)
		text = re.sub('^S\.R\.', "Pas de réponse",text)

	if 'POR' in filename:
		text = re.sub('^Na\b', "Não se aplica",text, flags=re.IGNORECASE)
		text = re.sub('^NAP', "Não se aplica",text)
		text = re.sub('^Ns', "Não sabe",text, flags=re.IGNORECASE)
		text = re.sub('^NS', "Não sabe",text, flags=re.IGNORECASE)
		text = re.sub('^Nr', "Não responde",text, flags=re.IGNORECASE)
		text = re.sub('^NR', "Não responde",text, flags=re.IGNORECASE)
		text = text.replace('Não se aplica (não se aplica)', "Não se aplica")
		text = text.replace('Não sabe (não sabe)', "Não sabe")
		text = text.replace('Não responde (não responde)', "Não responde")

	if 'RUS_EE' in filename or 'RUS_AZ' in filename or 'RUS_GE' in filename or 'RUS_MD' in filename or 'RUS_LV' in filename:
		text = re.sub('^Н.О.', "Нет ответа",text)
		text = re.sub('^З.О.', "Затрудняюсь ответить",text)
		text = re.sub('^ЗO', "Затрудняюсь ответить",text)
		text = re.sub('^Н.П.', "Не подходит",text)
		text = re.sub('^Н.О', "Нет ответа",text)
		text = re.sub('^З.О', "Затрудняюсь ответить",text)
		text = re.sub('^Н.П', "Не подходит",text)
		text = re.sub('^ЗО', "Затрудняюсь ответить",text)
		text = text.replace('Н о', "Нет ответа")

	if 'RUS_BY' in filename:
		text = re.sub('^НО', "Нет ответа",text)
		text = re.sub('^НЗ', "НЕ ЗНАЮ",text)

	if 'RUS_UA' in filename or 'RUS_RU' in filename:
		text = re.sub('^ЗО', "затрудняюсь ответить",text)
		text = re.sub('^ООО', "отказ от ответа",text)
		text = re.sub('^НП', "Не применимо",text)

	if 'SPA' in filename:
		text = re.sub('^NS', "No sabe",text)
		text = re.sub('^NC', "No contesta",text)

	#Currently TUR files are not included in MCSQ
	if 'TUR' in filename:
		text = re.sub('^FY', "BİLMİYOR-FİKRİ YOK",text, flags=re.IGNORECASE)
		text = re.sub('^CY', "CEVAP VERMİYOR",text, flags=re.IGNORECASE)
		text = re.sub('^SS', "Soru Sorulmadı",text, flags=re.IGNORECASE)


	return text
