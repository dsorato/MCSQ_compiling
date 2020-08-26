import re
from ess_special_answer_categories import * 
from essmodules import * 

"""
Retrieves the country/language and study metadata based on the input filename,
or survey_item_ID prefix.
The filenames respect a nomenclature rule, as follows:
SSS_RRR_YYYY_CC_LLL
S = study name 
R = round or wave
Y = study year
C = Country (ISO code with two digits, except for SOURCE)
L = Language

Args:
	param1 filename (string): name of the input file.

Returns: 
	country/language (string) and study metadata (string).
"""
def get_country_language_and_study_info(filename):
	if 'txt' in filename:
		filename_without_extension = re.sub('\.txt', '', filename)
		filename_split = filename_without_extension.split('_')
	else:
		filename_split = filename.split('_')

	study = filename_split[0]+'_'+filename_split[1]+'_'+filename_split[2]
	country_language = filename_split[3]+'_'+filename_split[4]

	return study, country_language

"""
Transforms study metadata present in the input file to the standard
used in the MCSQ format.

Args:
	param1 study (string): study metadata extracted from input file (Study column).

Returns:
	Standardized study parameter (string).
"""
def standardize_study_metadata(study):
	dict_year_round = {'ESS Round 1':'ESS_R01_2002', 'ESS Round 2':'ESS_R02_2004',
	'ESS Round 3':'ESS_R03_2006', 'ESS Round 4':'ESS_R04_2008', 'ESS Round 5':'ESS_R05_2010', 
	'ESS Round 6':'ESS_R06_2012', 'ESS Round 7':'ESS_R07_2014', 'ESS Round 8':'ESS_R08_2016',
	'ESS Round 9':'ESS_R09_2018'}

	for k,v in list(dict_year_round.items()):
		if study == k:
			return v


"""
Standardizes the item name metadata of supplementary modules G, H and I

Args:
	param1 item_name: item_name metadata, extracted from input file.

Returns:
	Standardized item_name, when applicable.
"""
def standardize_supplementary_item_name(item_name):
	if 'GF' in item_name:
		return item_name.replace('GF', 'G')
	elif 'IF' in item_name:
		return item_name.replace('IF', 'I')
	elif 'HF' in item_name:
		return item_name.replace('HF', 'H')
	elif 'GS' in item_name:
		return item_name.replace('GS', 'G')
	elif 'IS' in item_name:
		return item_name.replace('IS', 'I')
	elif 'HS' in item_name:
		return item_name.replace('HS', 'I')
	else:
		return item_name


"""
Matches the item_name against the dictionary stored in the ESSModulesRRR objects.
Rotating/supplementary modules are defined by round because they may change from
round to round.
Args:
	param1 essmodules (Python object): ESSModulesRRR object, instantiated according to the round.
	param2 item_name (string): name of survey item, retrieved in previous steps.

Returns: 
	matching value for item name (string).
"""
def retrieve_supplementary_module(essmodules,item_name):
	for k,v in list(essmodules.modules.items()):
		if re.compile(k).match(item_name):
			return v

"""
Retrieves the module of the survey_item, based on information from the ESSModulesRRR objects.
This information comes from the source questionnaires.

Args:
	param1 item_name (string): name of survey item, retrieved in previous steps.
	param2 study (string): study metadata, embedded in the file name.

Returns: 
	module of survey_item (string).
"""
def retrieve_item_module(item_name, study):
	if re.compile(r'A').match(item_name):
		return 'A - Media; social trust'
	elif re.compile(r'B').match(item_name):
		return 'B - Politics, including: political interest, efficacy, trust, electoral and other forms of participation, party allegiance, socio-political evaluations/orientations, multi-level governance'
	elif re.compile(r'C').match(item_name):
		return 'C - Subjective well-being and social exclusion; religion; perceived discrimination; national and ethnic identity'
	elif re.compile(r'F').match(item_name):
		return 'F - Socio-demographic profile, including: Household composition, sex, age, type of area, Education & occupation details of respondent, partner, parents, union membership, household income, marital status'
	else:
		if 'R01' in study:
			essmodules = ESSSModulesR01()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

		elif 'R02' in study:
			essmodules = ESSSModulesR02()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

		elif 'R03' in study:
			essmodules = ESSSModulesR03()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

		elif 'R04' in study:
			essmodules = ESSSModulesR04()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

		elif 'R05' in study:
			essmodules = ESSSModulesR05()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

		elif 'R06' in study:
			essmodules = ESSSModulesR06()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

"""
Cleans Request, Introduction and Instruction text segments by removing
undesired characters and standartizing some character representations.
A string input is expected, if the input is not a string instance, 
the method returns '', so the entry is ignored in the data extraction loop.

Args:
	param1 text (string expected): text to be cleaned.

Returns: 
	cleaned text (string).
"""
def clean_text(text):
	if isinstance(text, str):
		text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)
		text = re.sub('å','å', text)
		text = re.sub('ö','ö', text)
		text = re.sub('ä','ä', text)
		text = re.sub('Ä','ä', text)
		text = re.sub('ü','ü', text)
		text = re.sub('–', '-', text)
		text = re.sub('’',"'", text)
		text = re.sub("…", "...", text)
		text = re.sub(" :", ":", text)
		text = re.sub("’", "'", text)
		text = re.sub("[.]{4,}", "", text)
		text = re.sub("[_]{2,}", "", text)
		text = re.sub('>', "",text)
		text = re.sub('<', "",text)
		text = re.sub('Q[0-9]*\.', "",text)
		text = re.sub('\[', "",text)
		text = re.sub('\]', "",text)
		text = re.sub('^[A-Z]\.\s', "",text)
		text = re.sub('S\.R\.', "SR",text)
		text = re.sub('S\.R', "SR",text)
		text = re.sub('SR\.', "SR",text)
		text = re.sub('s\.r', "SR",text)
		text = re.sub('s\.r\.', "SR",text)
		text = re.sub('S\.r', "SR",text)
		text = text.replace('\n',' ')
		text = text.rstrip()
	else:
		text = ''

	return text

"""
Switches abbreviations of the word interviewer for the full form.

Args:
	param1 text (string): sentence being analyzed.
	param2 country_language (string): country_language metadata embedded in file name.

Returns: 
	text (string) without abbreviations for the word interviewer, when applicable.
"""
def expand_interviewer_abbreviations(text, country_language):
	if 'CZE' in country_language:
		text = text.replace('Taz.', 'Tazatel')
	elif '_ES' in country_language or 'POR' in country_language:
		text = text.replace('Ent.', "Entrevistador")
	elif 'ENG_' in country_language:
		text = text.replace('Int.', "Interviewer")
	elif 'FRE_' in country_language:
		text = text.replace('Enq.', "Enquêteur")
	elif 'GER_' in country_language:
		text = text.replace('Befr.', "Befrager")
	elif 'NOR' in country_language:
		text = text.replace('Int.', "Intervjuer")

	return text

"""
Instantiates the SpecialAnswerCategories object that stores both the text
and category values of the special answers (don't know, refusal, not applicable 
and write down) in accordance to the country_language metadata parameter.

Args:
	param1 country_language (string): country_language metadata parameter, embedded in file name.

Returns: 
	instance of SpecialAnswerCategories object (Python object), in accordance to the country_language.
"""
def instantiate_special_answer_category_object(country_language):
	if 'CAT' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesCAT()
	elif 'CZE' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesCZE()
	elif 'ENG_' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesENG()
	elif 'FRE_' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesFRE()
	elif 'GER_' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesGER()
	elif 'NOR' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesNOR()
	elif 'POR' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesPOR()
	elif 'SPA' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesSPA()
	elif 'RUS' in country_language:
		if '_EE' in country_language:
			ess_special_answer_categories = SpecialAnswerCategoriesRUS_EE()
		elif '_IL' in country_language:
			ess_special_answer_categories = SpecialAnswerCategoriesRUS_IL()
		elif '_LV' in country_language:
			ess_special_answer_categories = SpecialAnswerCategoriesRUS_LV()
		elif '_LT' in country_language:
			ess_special_answer_categories = SpecialAnswerCategoriesRUS_LT()
		else:
			ess_special_answer_categories = SpecialAnswerCategoriesRUS_RU_UA()

	return ess_special_answer_categories

"""
Verifies if a given answer segment is one of the special answer categories,
by testing the answer text against the attributes of SpecialAnswerCategories object.
This method serves the purpose of standartizing the special answer category values.

Args:
	param1 text (string): answer segment currently being analyzed.
	param2 answer_value (string): answer category value, defined in clean_answer() method.
	param3 ess_special_answer_categories (Python object): instance of SpecialAnswerCategories object, 
	in accordance to the country_language.

Returns: 
	answer text (string) and its category value (string). When the answer is a special answer category, 
	the text and category values are the ones stored in the SpecialAnswerCategories object.
"""
def check_if_answer_is_special_category(text, answer_value, ess_special_answer_categories):
	if text.lower() == ess_special_answer_categories.dont_know[0].lower():
		return ess_special_answer_categories.dont_know[0], ess_special_answer_categories.dont_know[1]
	elif text.lower() == ess_special_answer_categories.refuse[0].lower():
		return ess_special_answer_categories.refuse[0], ess_special_answer_categories.refuse[1]
	elif text.lower() == ess_special_answer_categories.dontapply[0].lower():
		return ess_special_answer_categories.dontapply[0], ess_special_answer_categories.dontapply[1]
	elif text.lower() == ess_special_answer_categories.write_down[0].lower():
		return ess_special_answer_categories.write_down[0], ess_special_answer_categories.write_down[1]

	return text, answer_value

"""
Cleans the answer segment, by standartizing the text (when it is a special answer category),
and attributing an category value to it. 

Args:
	param1 text (string): answer segment currently being analyzed.
	param2 ess_special_answer_categories (Python object): instance of SpecialAnswerCategories object, 
	in accordance to the country_language.

Returns: 
	answer text (string) and its category value (string). When the answer is a special answer category, 
	the text and category values are the ones stored in the SpecialAnswerCategories object.
"""
def clean_answer(text, ess_special_answer_categories):
	answer_value = None
	if isinstance(text, str) == False:
		return None, None

	text = text.replace('(No ho sap)','No ho sap')
	text = text.replace("(Don't know)","Don't know")

	if re.compile(r'^00\s\w+').match(text):
		text = text.split('00', 1)
		answer_text = text[1].rstrip()
		answer_value = '0'
	elif re.compile(r'^10\s\w+').match(text):
		text = text.split('10', 1)
		answer_text = text[1].rstrip()
		answer_value = '10'
	elif re.compile(r'^0\s\w+').match(text):
		text = text.split('0', 1)
		answer_text = text[1].rstrip()
		answer_value = '0'
	elif re.compile(r'^88\s\w+').match(text):
		text = text.split('88', 1)
		answer_text = text[1].rstrip()
		answer_value = '888'
	elif re.compile(r'^77\s\w+').match(text):
		text = text.split('77', 1)
		answer_text = text[1].rstrip()
		answer_value = '777'
	elif re.compile(r'^99\s\w+').match(text):
		text = text.split('99', 1)
		answer_text = text[1].rstrip()
		answer_value = '999'
	elif re.compile(r'^J\s.+').match(text):
		text = text.split('J', 1)
		answer_text = text[1].rstrip()
		answer_value = 'J'
	elif re.compile(r'^R\s.+').match(text):
		text = text.split('R', 1)
		answer_text = text[1].rstrip()
		answer_value = 'R'
	elif re.compile(r'^C\s.+').match(text):
		text = text.split('C', 1)
		answer_text = text[1].rstrip()
		answer_value = 'C'
	elif re.compile(r'^M\s.+').match(text):
		text = text.split('M', 1)
		answer_text = text[1].rstrip()
		answer_value = 'M'
	elif re.compile(r'^F\s.+').match(text):
		text = text.split('F', 1)
		answer_text = text[1].rstrip()
		answer_value = 'F'
	elif re.compile(r'^S\s.+').match(text):
		text = text.split('S', 1)
		answer_text = text[1].rstrip()
		answer_value = 'S'
	elif re.compile(r'^K\s.+').match(text):
		text = text.split('K', 1)
		answer_text = text[1].rstrip()
		answer_value = 'K'
	elif re.compile(r'^P\s.+').match(text):
		text = text.split('P', 1)
		answer_text = text[1].rstrip()
		answer_value = 'P'
	elif re.compile(r'^D\s.+').match(text):
		text = text.split('D', 1)
		answer_text = text[1].rstrip()
		answer_value = 'D'
	elif re.compile(r'^H\s.+').match(text):
		text = text.split('H', 1)
		answer_text = text[1].rstrip()
		answer_value = 'H'
	elif re.compile(r'^U\s.+').match(text):
		text = text.split('U', 1)
		answer_text = text[1].rstrip()
		answer_value = 'U'
	elif re.compile(r'^N\s.+').match(text):
		text = text.split('N', 1)
		answer_text = text[1].rstrip()
		answer_value = 'N'
	else:
		answer_text = text.strip()
		answer_value = None

	answer_text = answer_text.strip()
	answer_text, answer_value = check_if_answer_is_special_category(answer_text, answer_value, ess_special_answer_categories)

	return answer_text, answer_value


"""
Calls the appropriate instruction recognition method, according to the language.
Args:
	param1 sentence (string): sentence being analyzed in outer loop of data extraction.
	param2 country_language (string): country_language metadata, embedded in file name.

Returns: 
	bypass the return of instruction_recognition methods (boolean).
"""
def check_if_segment_is_instruction(sentence, country_language):
	if '_ES' in country_language:
		return instruction_recognition_catalan_spanish(sentence,country_language) 
	if 'POR' in country_language:
		return instruction_recognition_portuguese(sentence,country_language)


"""
Recognizes an instruction segment for texts written in Portuguese,
based on regex named groups patterns.

Args:
	param1 text (string): text (in Portuguese) currently being analyzed.
	param2 country_language (string): country_language metadata embedded in file name.

Returns: 
	True if the segment is an instruction or False if it is not.
"""
def instruction_recognition_portuguese(text,country_language):
	regex= r"^(?P<continue>)seguir con la\s(?P<card>)tarjeta"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<show>)(mostrar|manter)\s(?P<gain>)(novamente)?\s?(?P<card>)cartão"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<use>)(utilize|mostrar|use)\s(?P<this>)(este|este mesmo)?\s?(?P<card>)cartão\s(?P<again>)(novamente)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<continue>)continue\s(?P<show>)(mostrando|utilizando)\s(?P<this>)(este|este mesmo)?\s?(?P<card>)cartão"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
		
	regex= r"^(?P<suggest>)sugerir\s(?P<categories>)categorias\s(?P<de>)de\s(?P<answer>)resposta"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
		
	regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<choose>)escolha\s(?P<youranswer>)respostas\s(?P<fromthis>)deste\s(?P<card>)cartão"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<note>)(nota)?\s?(?P<for>)(para)?\s?(?P<interviewer>)entrevistador\s(?P<code>)codifica(r)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<choose>)escolha\s(?P<option>)a afirmação\s(?P<closer>)que mais se aproxima da\s(?P<youropinion>)sua opinião"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)ler\s(?P<one>)uma\s(?P<organization>)organização\s(?P<ateachtime>)de cada vez"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)ler\s(?P<slowly>)(pausadamente)?\s(?P<outloud>)(em voz alta)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)codificar\s(?P<only>)(só)?\s?(?P<one>)uma\s(?P<answer>)resposta"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<describe>)descrever\s(?P<details>)detalhadamente"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)perguntar a\s(?P<all>)todos"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<insist>)insistir"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	return False

"""
Recognizes an instruction segment for texts written either in Spanish or Catalan,
based on regex named groups patterns.

Args:
	param1 text (string): text (in Spanish or Catalan) currently being analyzed.
	param2 country_language (string): country_language metadata embedded in file name.

Returns: 
	True if the segment is an instruction or False if it is not.
"""
def instruction_recognition_catalan_spanish(text,country_language):
	regex= r"^(?P<programador>)programador"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)entrevistador"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	if 'CAT' in country_language:
		regex= r"^(?P<continue>)(continuï)?\s?(?P<show>)mostr(ar|eu|ant)\s(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<use>)(Utilitzi)?\s?(?P<this>)aquesta\s(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<use>)(utilitzi la|segueixi utilitzant|continuï utilitzant)\s(?P<this>)(aquesta)?\s?(?P<same>)(mateixa)?\s?(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<use>)utilitzi\s(?P<this>)aquesta\s(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True
		
		regex= r"^(?P<suggest>)suggerir\s(?P<categories>)categories\s(?P<de>)de\s(?P<answer>)resposta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(\,)?\s?(?P<choose>)encercli\s(?P<one>)una\s(?P<option>)opció"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<choose>)encercli\s(?P<option>)l'opció\s(?P<closer>)més propera"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<choose>)triï\s(?P<youranswer>)seva resposta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<read>)llegi(r|u)\s(?P<out>)(alta)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<read>)llegi(r|u)\s(?P<each>)cada\s(?P<utterance>)afirmació"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<readorcode>)(llegir|codificar)\s(?P<each>)cada\s(?P<organization>)organització"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<note>)nota\s(?P<for>)per\s(?P<interviewer>)entrevistador\s(?P<code>)codificar"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<markorcode>)(marqueu|codificar)\s(?P<all>)tot(s|es)\s(?P<that>)que\s(?P<apply>)(corresponguin|calgui)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<note>)anoteu\s(?P<with>)amb\s(?P<all>)tots\s(?P<details>)detalls"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<ask>)(preguntar)?\s?a\s(?P<all>)tothom"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<insist>)insistiu"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

	elif 'SPA' in country_language:
		regex= r"^(?P<continue>)seguir con la\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<show>)mostrar\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<continueusing>)(siga utilizando|siga usando|use otra vez|use)\s(?P<same>)(la misma)?\s?\s(?P<this>)(esta)?\s?(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<use>)(utilice|use)\s(?P<this>)(esta)?\s?(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True


		regex= r"^(?P<suggest>)sugerir\s(?P<categories>)categorías\s(?P<de>)de\s(?P<answer>)respuesta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True
		
		regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<choose>)(escoja|elija)\s(?P<youranswer>)su respuesta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<mark>)marque\s(?P<one>)una\s(?P<option>)casilla"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<note>)nota\s(?P<for>)per\s(?P<interviewer>)el entrevistador\s(?P<code>)codificar"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True


		regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<mark>)marque\s(?P<option>)la casilla\s(?P<closer>)que mejor represente\s(?P<youropinion>)su opinión"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<readorcode>)(leer|codificar)\s(?P<each>)cada\s(?P<organization>)organización"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<read>)leer\s(?P<out>)(alto)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<read>)leer\s(?P<eachone>)una a una\s(?P<and>)(y)?\s?(?P<note>)anotar"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<ask>)(preguntar)?\s?a\s(?P<all>)todos"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<insist>)insistir"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

	return False

		