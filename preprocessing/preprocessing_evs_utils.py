import re

"""
Retrieves the country/language and study metadata based on the input filename.
:param filename: name of the input file.
:returns: country/language and study metadata.
"""
def get_country_language_and_study_info(filename):
	filename_without_extension = re.sub('\.xml', '', filename)
	filename_split = filename_without_extension.split('_')

	study = filename_split[0]+'_'+filename_split[1]+'_'+filename_split[2]
	country_language = filename_split[3]+'_'+filename_split[4]

	return study, country_language

"""
Standartizes a given item_name, if it is not in the standard
:param item_name: item name extracted from the input file.
:returns: standartized item_name. 
"""
def standartize_item_name(item_name):
	item_name = re.sub("\.", "", item_name)
	item_name = item_name.lower()
	item_name = re.sub("^q", "Q", item_name)
	item_name = re.sub("^f", "Q", item_name)

	if '_'  in item_name:
		item_name = item_name.split('_')
		item_name = item_name[0]+item_name[1].lower()

	if item_name[0].isdigit() or len(item_name)==1:
		item_name = 'Q'+item_name

	return item_name


"""
Removes undesired characters from instruction text. 
:param text: instruction text extracted from the input file.
:returns: clean instruction text. 
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
:param text: request/response text extracted from the input file.
:param filename: name of the input file.
:returns: clean request/response text. 
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
		text = re.sub('^[A-Z]\.\s', "",text)
		text = re.sub('^[A-Z]\s', "",text)
		text = re.sub('e\.g\.', "e.g.,",text)


		if 'ITA' in filename:
			text = re.sub('^NS', "Non so",text)
			text = re.sub('^NR', "Non risponde",text)
			text = re.sub('^NP', "Non pertinente",text)
		if 'FRE' in filename:
			text = re.sub('^NSP', "Ne sait pas",text, flags=re.IGNORECASE)
			text = re.sub('^S\.R\.', "Pas de réponse",text)
			text = re.sub('^S\.R', "Pas de réponse",text)
			text = re.sub('^SR\.', "Pas de réponse",text)
			text = re.sub('^s\.r', "Pas de réponse",text)
			text = re.sub('^s\.r\.', "Pas de réponse",text)
			text = re.sub('^S\.r', "Pas de réponse",text)
			text = re.sub('^SR', "Pas de réponse",text)
		if 'GER' in filename:
			text = re.sub('^TNZ', "Trifft nicht zu",text)
			text = re.sub('^WN', "weiß nicht",text)
			text = re.sub('^KA', "keine antwort",text)
			text = re.sub('^NZT', "nicht zutreffend",text)

		if 'HRV' in filename:
			text = re.sub('^n\.o\.', "nema odgovora",text)
			text = re.sub('^n\.z\.', "ne znam",text)
			

		if 'ENG' in filename:
			text = re.sub('^NAP', "Not applicable",text)
			text = re.sub('^DK', "Don't know",text)
			text = re.sub('^na', "No answer",text)
			text = re.sub('^NA', "No answer",text)
			text = re.sub('^nap', "Not applicable",text)
			text = re.sub('^dk', "Don't know",text)
			text = re.sub('^N/A', "Not applicable",text)
			
		if 'POR' in filename:
			text = re.sub('^Na\b', "Não se aplica",text, flags=re.IGNORECASE)
			text = re.sub('^NAP', "Não se aplica",text)
			text = re.sub('^Ns', "Não sabe",text, flags=re.IGNORECASE)
			text = re.sub('^NS', "Não sabe",text, flags=re.IGNORECASE)
			text = re.sub('^Nr', "Não responde",text, flags=re.IGNORECASE)
			text = re.sub('^NR', "Não responde",text, flags=re.IGNORECASE)

		if 'SPA' in filename:
			text = re.sub('^NS', "No sabe",text)
			text = re.sub('^NC', "No contesta",text)
		
		if 'DUT' in filename:
			text = re.sub('^nap', "niet van toepassing",text, flags=re.IGNORECASE)

		if 'FIN' in filename:
			text = re.sub('^EOS', "Ei osaa sanoa",text, flags=re.IGNORECASE)

		if 'LTZ' in filename:
			text = re.sub('^NSP', "Ne sait pas",text)
			text = re.sub('^SR', "Pas de réponse",text)
			text = re.sub('^S\.R\.', "Pas de réponse",text)
		if 'TUR' in filename:
			text = re.sub('^FY', "BİLMİYOR-FİKRİ YOK",text, flags=re.IGNORECASE)
			text = re.sub('^CY', "CEVAP VERMİYOR",text, flags=re.IGNORECASE)
			text = re.sub('^SS', "Soru Sorulmadı",text, flags=re.IGNORECASE)

		if 'RUS_EE' in filename or 'RUS_AZ' in filename or 'RUS_GE' in filename or 'RUS_MD' in filename:
			text = re.sub('^Н.О.', "Нет ответа",text)
			text = re.sub('^З.О.', "Затрудняюсь ответить",text)
			text = re.sub('^Н.П.', "Не подходит",text)
			text = re.sub('^Н.О', "Нет ответа",text)
			text = re.sub('^З.О', "Затрудняюсь ответить",text)
			text = re.sub('^Н.П', "Не подходит",text)
			text = re.sub('^ЗО', "Затрудняюсь ответить",text)

		if 'RUS_BY' in filename:
			text = re.sub('^НО', "Нет ответа",text)
			text = re.sub('^НЗ', "НЕ ЗНАЮ",text)

		if 'RUS_UA' in filename:
			text = re.sub('^ЗО', "затрудняюсь ответить",text)
			text = re.sub('^ООО', "отказ от ответа",text)



		text = text.replace('\n',' ')
		text = text.rstrip()
	else:
		text = ''



	return text