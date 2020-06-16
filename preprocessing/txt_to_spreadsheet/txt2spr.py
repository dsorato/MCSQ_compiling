import pandas as pd
import csv
import re
import nltk.data
import sys
sys.path.insert(0, 'utils')
import utils as ut
import string


initial_sufix = 0

#The '{INTRO}' tag refers to the introductory text that comes before the first question of a module.
#In the ESS text files, the '{INTRO}' tag comes always after the answer of the last question of the previous module,
#and before the first question of the new module.
def find_intro_in_answer(answer):
	size = len(answer)
	idx_list = [idx for idx, val in enumerate(answer) if val == '{INTRO}']
	res = [answer[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[-1] != size else []))]
	answer = res[0]
	intro = res[1]

	
	return answer, intro

#Deprecated. Keeping this method here just in case something changes in the future.
def find_intro_in_question(question):
	size = len(question)
	idx_list = [idx for idx, val in enumerate(question) if val == '{INTRO}']
	res = [question[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[-1] != size else []))]

	intro_and_text_question = res[-1]
	size_intro_and_text_question = len(intro_and_text_question)
	idx_list = [idx for idx, val in enumerate(intro_and_text_question) if val == '{QUESTION}']
	res2 = [intro_and_text_question[i: j] for i, j in zip([0] + idx_list, idx_list + ([size_intro_and_text_question] 
		if idx_list[-1] != size_intro_and_text_question else []))]

	question_id = res[0][0]
	question = res2[1]
	question.insert(0, question_id)
	
	return question, res2[0]
	
#Split a question into question and answer segments to treat them accordingly.
def split_list(a_question, item_name_question_pattern):
	size = len(a_question)
	idx_list = [idx for idx, val in enumerate(a_question) if val == '{ANSWERS}']
	question_and_answer = [a_question[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[-1] != size else []))] 
	question = question_and_answer[0]
	answer = question_and_answer[1]

	return question, answer


def remove_trailing(clean):
	without_trailing = []
	for item in clean:
		item = item.rstrip()
		without_trailing.append(item)

	return without_trailing


def get_begin_end_question(index_questions, lines, last_line):
	all_questions = []
	group = []
	for i, index in enumerate(index_questions):
		aux = []
		if index != index_questions[-1]:
			aux.append(index_questions[i])
			aux.append(index_questions[i+1])
			
		else:
			aux.append(index_questions[i])
			aux.append(last_line)
		group.append(aux)

	for item in group:
		begin =item[0]
		end = item[1]
		dirty = lines[begin:end]
		clean = list(filter(lambda a: a != '\n', dirty))
		all_questions.append(remove_trailing(clean))
	
	return all_questions

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

def assign_survey_item_id_to_supplementary(prefix):
	return update_survey_item_id(prefix)

def decide_on_survey_item_id(prefix, old_item_name, new_item_name):
	if old_item_name == new_item_name:
		survey_item_id = get_survey_item_id(prefix)
	else:
		survey_item_id = update_survey_item_id(prefix)


	return survey_item_id

def check_if_module_is_supplementary(value, supplementary_modules_in_txt):
	match = re.match(r"([A-Z]+)([0-9]+)", value, re.I)
	match_groups = match.groups()
	module = match_groups[0]
	
	if module in supplementary_modules_in_txt:
		module = 'SUPP_'+module
	else:
		module =  module

	return module

def define_language_country_param(language_country, filename):
	if 'CAT' in language_country:
		dk = '(No ho sap)'
		refusal =  '(No contesta)'
		dontapply =  "(No s'aplica)"
		showc = 'MOSTRAR TARGETA'
		showc_lower = showc.lower()
		abbreviation_interviewer = 'Ent.'
		full_form_interviewer = 'Entrevistador'
		value_range_pattern = re.compile('(\d+ a \d+)')

		if 'R01' in filename:
			write_down = "(Escriure'ls)"
			supplementary_modules_in_txt = ['I']
		if 'R02' in filename:
			supplementary_modules_in_txt = ['I']
			write_down = "(ANOTAR'L)"
		if 'R03' in filename:
			supplementary_modules_in_txt = ['']
			refusal =  '(Refusa)'
		if 'R04' in filename:
			supplementary_modules_in_txt = ['']
			write_down = "(Escriure)"
		if 'R05' in filename:
			supplementary_modules_in_txt = ['IF']
			write_down = "(Anoteu-lo)"
		if 'R06' in filename:
			supplementary_modules_in_txt = ['']
			write_down = "(Anoteu-lo)"

	if 'CZE'  in language_country:
		dk = "(Neví)"
		refusal =  '(Odmítl)'
		dontapply =  '(Gjelder ikke)'
		write_down = "(Vypište)"
		if 'R02' in filename:
			showc = 'KARTA'
		else:
			showc = 'KARTU'

		abbreviation_interviewer = 'Taz.'
		full_form_interviewer = 'Tazatel'
		value_range_pattern = re.compile('(\d+ až \d+)')

		if 'R01' in filename:
			supplementary_modules_in_txt = ['H']
		if 'R02' in filename:
			supplementary_modules_in_txt = ['G', 'H', 'I', 'J']
		#CZE didnt participate in ESS R03
		if 'R04' in filename:
			dontapply = '(Bez odpovědi)'
			supplementary_modules_in_txt = ['']
		if 'R05' in filename:
			dontapply = '(Bez odpovědi)'
			supplementary_modules_in_txt = ['IF']
		if 'R06' in filename:
			dk = "(Nevím)"
			refusal =  '(Odmítl(a))'
			write_down = "(Vypište)"
			supplementary_modules_in_txt = ['']

	if 'ENG' in language_country:
		dk = "(Don't know)"
		refusal =  '(Refusal)'
		dontapply =  "(Not applicable)"
		write_down = "(Write in)"
		showc = 'Show Card'
		showc_lower = showc.lower()
		abbreviation_interviewer = 'Int.'
		full_form_interviewer = 'Interviewer'
		value_range_pattern = re.compile('(\d+ to \d+)')

		if '_GB' in language_country:
			if 'R01' in filename:
				supplementary_modules_in_txt = ['I', 'K']
			if 'R02' in filename:
				supplementary_modules_in_txt = ['IS', 'G', 'H']
			if 'R03' in filename:
				supplementary_modules_in_txt = ['']
			if 'R04' in filename:
				supplementary_modules_in_txt = ['']
			if 'R05' in filename:
				supplementary_modules_in_txt = ['IF']
				showc = 'SHOWCARD'
			if 'R06' in filename:
				supplementary_modules_in_txt = ['']
		if '_IE' in language_country:
			if 'R01' in filename:
				supplementary_modules_in_txt = ['I']
			if 'R02' in filename:
				supplementary_modules_in_txt = ['G', 'J']
			if 'R03' in filename:
				supplementary_modules_in_txt = ['']
			if 'R04' in filename:
				supplementary_modules_in_txt = ['']
			if 'R05' in filename:
				supplementary_modules_in_txt = ['']
			if 'R06' in filename:
				supplementary_modules_in_txt = ['IF']
		if '_SOURCE' in language_country:
			if 'R01' in filename:
				supplementary_modules_in_txt = ['I', 'HF']
			if 'R02' in filename:
				supplementary_modules_in_txt = ['I', 'G', 'J']
			if 'R03' in filename:
				supplementary_modules_in_txt = ['HF']
			if 'R04' in filename:
				supplementary_modules_in_txt = ['HF']
			if 'R05' in filename:
				supplementary_modules_in_txt = ['IS']
			if 'R06' in filename:
				supplementary_modules_in_txt = ['']
		if '_LU' in language_country:
			if 'R02' in filename:
				supplementary_modules_in_txt = ['G']


	if 'GER' in language_country:
		refusal =  '(keine Antwort)'
		write_down = "(Aufschreiben)"
		showc = 'Karte'
		abbreviation_interviewer = 'Befr.'
		full_form_interviewer = 'Befrager'
		value_range_pattern = re.compile('(\d+ bis \d+)')

		if '_AT' in language_country:
			dk = '(Weiß nicht)'
			refusal = '(Anwort verweigert)'
			dontapply = '(Trifft nicht zu)'
			write_down = '(Ausfüllen)'
			if 'R01' in filename:
				supplementary_modules_in_txt = ['G', 'H']
			if 'R02' in filename:
				supplementary_modules_in_txt = ['']
			if 'R03' in filename:
				supplementary_modules_in_txt = ['']
			if 'R04' in filename:
				write_down = "(EINTRAGEN)"
				supplementary_modules_in_txt = ['']
			if 'R05' in filename:
				supplementary_modules_in_txt = ['IS']
		if '_CH' in language_country:
			dk = "(Weiss nicht)"
			refusal = '(Keine Antwort)'
			dontapply = '(Trifft nicht zu)'
			write_down = ('(NOTIEREN)')
			if 'R01' in filename:
				supplementary_modules_in_txt = ['G', 'H', 'I']
			if 'R02' in filename:
				write_down = ('(Eingeben)')
				supplementary_modules_in_txt = ['']
			if 'R03' in filename:
				supplementary_modules_in_txt = ['']
			if 'R04' in filename:
				supplementary_modules_in_txt = ['']
			if 'R05' in filename:
				supplementary_modules_in_txt = ['IF']
			if 'R06' in filename:
				supplementary_modules_in_txt = ['']
		if '_DE' in language_country:
			showc = 'Liste'
			dk = '(Weiß nicht)'
			refusal = '(Anwort verweigert)'
			dontapply = '(Trifft nicht zu)'
			abbreviation_interviewer = 'INT.'
			full_form_interviewer = 'Interviewer'
			write_down = "(EINTRAGEN)"
			if 'R01' in filename:
				supplementary_modules_in_txt = ['G', 'N', 'I']
			if 'R02' in filename:
				supplementary_modules_in_txt = ['']
			if 'R03' in filename:
				supplementary_modules_in_txt = ['']
			if 'R04' in filename:
				supplementary_modules_in_txt = ['']
			if 'R05' in filename:
				abbreviation_interviewer = 'INT'
				supplementary_modules_in_txt = ['IF']
			if 'R06' in filename:
				supplementary_modules_in_txt = ['']
		if '_LU' in language_country:
			dk = '(Weiß nicht)'
			refusal = '(Keine Antwort)'
			dontapply = '(Nitch zutreffend)'
			instruction_card = 'Liste'
			write_down = '(Eintragen)'
			if 'R02' in filename:
				supplementary_modules_in_txt = ['']

		
	if 'FRE' in language_country:
		dk = "(Ne sait pas)"
		refusal =  '(Refus)'
		dontapply = "(Ne s'applique pas)"
		write_down = "(NOTER)"
		showc = 'carte No.'
		showc_lower = 'carte numéro'
		abbreviation_interviewer = 'Enq.'
		full_form_interviewer = 'Enquêteur'
		value_range_pattern = re.compile('(\d+ à \d+)')

		if '_BE' in language_country:
			write_down = '(INSCRIVEZ)'
			if 'R01' in filename:
				supplementary_modules_in_txt = ['G', 'H', 'I']
			if 'R02' in filename:
				supplementary_modules_in_txt = ['I']
			if 'R03' in filename:
				supplementary_modules_in_txt = ['']
			if 'R04' in filename:
				write_down = '(NOTEZ)'
				supplementary_modules_in_txt = ['']
			if 'R05' in filename:
				write_down = '(NOTEZ)'
				supplementary_modules_in_txt = ['IF']
			if 'R06' in filename:
				write_down = '(NOTEZ)'
				supplementary_modules_in_txt = ['IF']
		if '_CH' in language_country:
			if 'R01' in filename:
				supplementary_modules_in_txt = ['G', 'H', 'I']
			if 'R02' in filename:
				supplementary_modules_in_txt = ['I']
			if 'R03' in filename:
				write_down = '(NOTEZ)'
				supplementary_modules_in_txt = ['']
			if 'R04' in filename:
				write_down = '(NOTEZ)'
				supplementary_modules_in_txt = ['']
			if 'R05' in filename:
				supplementary_modules_in_txt = ['IF']
			if 'R06' in filename:
				supplementary_modules_in_txt = ['IF']
		if '_FR' in filename:
			if 'R01' in filename:
				supplementary_modules_in_txt = ['']
			if 'R02' in filename:
				supplementary_modules_in_txt = ['IS']
			if 'R03' in filename:
				write_down = '(Écrire)'
				supplementary_modules_in_txt = ['']
			if 'R04' in filename:
				supplementary_modules_in_txt = ['']
			if 'R05' in filename:
				supplementary_modules_in_txt = ['IF']
			if 'R06' in filename:
				supplementary_modules_in_txt = ['']
		if '_LU' in filename:
			if 'R01' in filename or 'R02' in filename:
				write_down = '(NOTEZ)'
				supplementary_modules_in_txt = ['']

	if 'NOR' in language_country:
		dk = "(Vet ikke)"
		refusal = "(Nekter å svare)"
		dontapply =  '(Gjelder ikke)'
		write_down = "(Skriv inn)"
		showc = 'KORT'
		showc_lower = showc.lower()
		abbreviation_interviewer = 'Int.'
		full_form_interviewer = 'Intervjuer'
		value_range_pattern = re.compile('(\d+ til \d+)')
		if 'R01' in filename:
			supplementary_modules_in_txt = ['I']
		if 'R02' in filename:
			supplementary_modules_in_txt = ['']
		if 'R03' in filename:
			supplementary_modules_in_txt = ['']
		if 'R04' in filename:
			supplementary_modules_in_txt = ['']
		if 'R05' in filename:
			supplementary_modules_in_txt = ['I']
		if 'R06' in filename:
			supplementary_modules_in_txt = ['']

	if 'POR' in language_country:
		dk = '(Não sabe)'
		refusal =  '(Recusa)'
		dontapply =  '(Não responde)'
		write_down = "(Escreva)"
		showc = 'MOSTRAR CARTÃO'
		abbreviation_interviewer = 'Ent.'
		full_form_interviewer = 'Entrevistador'
		value_range_pattern = re.compile('(\d+ a \d+)')
		if 'R01' in filename:
				supplementary_modules_in_txt = ['G', 'H', 'I']
		if 'R02' in filename:
				supplementary_modules_in_txt = ['I']
		if 'R03' in filename:
				supplementary_modules_in_txt = ['']
		if 'R04' in filename:
				supplementary_modules_in_txt = ['']
		if 'R05' in filename:
				supplementary_modules_in_txt = ['IF']
		if 'R06' in filename:
				supplementary_modules_in_txt = ['']
	
	if 'RUS' in language_country:
		value_range_pattern = re.compile('(\d+ до \d+)')
		write_down = '(ВПИСАТЬ)'
		dk = '(Не знаю)'
		refusal = '(отказываюсь отвечать)'
		showc = 'КАРТОЧКА'	
		abbreviation_interviewer = 'интервьюер'
		full_form_interviewer = 'интервьюер'
		dontapply =  '(не применяется)'
		
		if '_EE' in language_country:
			dk = '(НЕ ЗНАЮ)'
			refusal = '(ОТКАЗАЛСЯ)'
			write_down = '(ВПИСАТЬ)'
			if 'R02' in filename:
				supplementary_modules_in_txt = ['G']
			if 'R03' in filename:
				supplementary_modules_in_txt = ['']
			if 'R04' in filename:
				supplementary_modules_in_txt = ['']
			if 'R05' in filename:
				supplementary_modules_in_txt = ['IF']
			if 'R06' in filename:
				supplementary_modules_in_txt = ['']

		if '_IL' in language_country:
			dk = '(не знаю)'
			refusal = '(отказываюсь отвечать)'
			dontapply =  '(нет ответа)'
			write_down = '(ЗАПИШИТЕ)'
			showc = 'КАРТОЧКА'

			if 'R01' in filename:
				supplementary_modules_in_txt = ['G', 'H', 'I']
			if 'R04' in filename:
				supplementary_modules_in_txt = ['']	
			if 'R05' in filename:
				supplementary_modules_in_txt = ['I']
			if 'R06' in filename:
				supplementary_modules_in_txt = ['G']
			
		if '_LV' in language_country:
			dk = '(GP)'
			refusal = '(Отказ)'
			write_down = '(ВПИШИТЕ)'
			if 'R03' in filename:
				supplementary_modules_in_txt = ['']
			if 'R04' in filename:
				showc = 'КАРТОЧКА Nr'
				supplementary_modules_in_txt = ['']

		if '_LT' in language_country:
			dk = '(Затрудняюсь ответить)'
			refusal = '(Отказ)'
			write_down = '(ВПИШИТЕ)'
			if 'R04' in filename:
				supplementary_modules_in_txt = ['']
			if 'R05' in filename:
				supplementary_modules_in_txt = ['IS']

		if '_RU' in language_country:
			refusal = '(Отказ от ответа)'
			dk = '(Затрудняюсь ответить)'
			write_down = '(ЗАПИШИТЕ)'
			if 'R03' in filename:
				supplementary_modules_in_txt = ['']
			if 'R04' in filename:
				supplementary_modules_in_txt = ['']
			if 'R05' in filename:
				supplementary_modules_in_txt = ['I']
			if 'R06' in filename:
				supplementary_modules_in_txt = ['']

		if '_UA' in language_country:
			write_down = '(ЗАПИШИТЕ)'
			dk = '(затрудняюсь ответить)'
			refusal = '(отказ от ответа)'
			dontapply = '(не применимо)'
			if 'R02' in filename:
				write_down = '(НАПИШИТЕ)'
				supplementary_modules_in_txt = ['G']
			if 'R03' in filename:
				supplementary_modules_in_txt = ['']
			if 'R04' in filename:
				supplementary_modules_in_txt = ['']
			if 'R05' in filename:
				supplementary_modules_in_txt = ['IF']
			if 'R06' in filename:
				supplementary_modules_in_txt = ['']

	if 'SPA' in language_country:
		value_range_pattern = re.compile('(\d+ a \d+)')
		dk = '(No sabe)'
		refusal =  '(No contesta)'
		dontapply =  "(No se aplica)"
		write_down = "(ANOTAR)"
		showc = 'MOSTRAR TARJETA'
		abbreviation_interviewer = 'Ent.'
		full_form_interviewer = 'Entrevistador'

		if 'R01' in filename:
			write_down = "(Escribir)"
			supplementary_modules_in_txt = ['I']
		if 'R02' in filename:
			supplementary_modules_in_txt = ['I']
		if 'R03' in filename:
			supplementary_modules_in_txt = ['']
			dontapply =  "(No procede)"
		if 'R04' in filename:
			supplementary_modules_in_txt = ['']
		if 'R05' in filename:
			supplementary_modules_in_txt = ['IF']
		if 'R06' in filename:
			supplementary_modules_in_txt = ['']

	showc_lower = showc.lower()
	
	return value_range_pattern, write_down, dk, refusal, dontapply, showc, showc_lower, abbreviation_interviewer, full_form_interviewer, supplementary_modules_in_txt

def test_income_patterns(line):
	j= False
	r= False
	c= False
	m= False
	f= False
	s= False
	k= False
	p= False
	d= False
	h= False
	u= False
	n = False

	income_question_j_pattern = re.compile("(\s?\(J\))")
	income_question_r_pattern = re.compile("(\s?\(R\))")
	income_question_c_pattern = re.compile("(\s?\(C\))")
	income_question_m_pattern = re.compile("(?:\s?\(M\))")
	income_question_f_pattern = re.compile("(?:\s?\(F\))")
	income_question_s_pattern = re.compile("(?:\s?\(S\))")
	income_question_k_pattern = re.compile("(?:\s?\(K\))")
	income_question_p_pattern = re.compile("(?:\s?\(P\))")
	income_question_d_pattern = re.compile("(?:\s?\(D\))")
	income_question_h_pattern = re.compile("(?:\s?\(H\))")
	income_question_u_pattern = re.compile("(?:\s?\(U\))")
	income_question_n_pattern = re.compile("(?:\s?\(N\))")

	if income_question_j_pattern.findall(line):
		j = True
	if income_question_r_pattern.findall(line):
		r = True
	if income_question_c_pattern.findall(line):
		c = True
	if income_question_m_pattern.findall(line):
		m = True
	if income_question_f_pattern.findall(line):
		f = True
	if income_question_s_pattern.findall(line):
		s = True
	if income_question_k_pattern.findall(line):
		k = True
	if income_question_p_pattern.findall(line):
		p = True
	if income_question_d_pattern.findall(line):
		d = True
	if income_question_h_pattern.findall(line):
		h = True
	if income_question_u_pattern.findall(line):
		u = True
	if income_question_n_pattern.findall(line):
		n = True

	return [j,r,c,m,f,s,k,p,d,h,u,n]

def get_question_all_questions(filename, item_name_question_pattern):
	index_questions = []
	print(filename)
	
	with open(filename, 'r') as file:
		lines = file.readlines()

		last_line = len(lines) - 1
		for i, line in enumerate(lines):
			if item_name_question_pattern.match(line) and '€' not in line and 'Kč' not in line and 'pts'  not in line and 'FRANCS' not in line and 'NOK' not in line and 'pta.' not in line:
				ret =  test_income_patterns(line)
				
				if not any(ret):
					question_name = ut.standardize_question_name(line)
					lines[i] = question_name
					index_questions.append(i)
		
		all_questions = get_begin_end_question(index_questions, lines, last_line)
		
		
	file.close()


	return all_questions

def generate_main_questionnaire_df(df_ess, study, prefix, filename, language_country, item_name_question_pattern, all_questions, tokenizer, value_range_pattern, write_down, dk, refusal, dontapply, showc, showc_lower, abbreviation_interviewer, full_form_interviewer, supplementary_modules_in_txt):
	old_item_name = 'A1'
	for a_question in all_questions:
		print(a_question)
		intro = ''
		question_and_answer = split_list(a_question, item_name_question_pattern)
		question = question_and_answer[0]
		answer = question_and_answer[1]
		# if  '{INTRO}' in question:
		# 	intro_and_question = find_intro_in_question(question)
		# 	question = intro_and_question[0]
		# 	intro = intro_and_question[1]
		# 	intro = list(filter(lambda a: a != '{INTRO}', intro))
		if  '{INTRO}' in answer:
			intro_and_answer = find_intro_in_answer(answer)
			answer = intro_and_answer[0]
			intro = intro_and_answer[1]
			intro = list(filter(lambda a: a != '{INTRO}', intro))
			
		question = list(filter(lambda a: a != '{QUESTION}', question))
		answer = list(filter(lambda a: a != '{ANSWERS}', answer))
		
		for item in question[1:]:
			if abbreviation_interviewer in item:
				item = item.replace(abbreviation_interviewer, full_form_interviewer)


			split_into_sentences = tokenizer.tokenize(item)
			for sentence in split_into_sentences:

				if ut.set_of_instructions(sentence.lower(), language_country, filename) == True:

					new_item_name = question[0]
					survey_item_id = decide_on_survey_item_id(prefix, old_item_name, new_item_name)
		
					data = {"survey_item_ID": survey_item_id, 'Study': study, 'module': check_if_module_is_supplementary(question[0],supplementary_modules_in_txt), 
					'item_type': 'INSTRUCTION', 'item_name': new_item_name, 'item_value': None, language_country: ut.clean_text(sentence)}
					df_ess = df_ess.append(data, ignore_index = True)

					old_item_name = new_item_name	
					
				else:						
					new_item_name = question[0]
					survey_item_id = decide_on_survey_item_id(prefix, old_item_name, new_item_name)

					data = {"survey_item_ID": survey_item_id, 'Study': study, 'module': check_if_module_is_supplementary(question[0], supplementary_modules_in_txt), 
					'item_type': 'REQUEST', 'item_name': new_item_name, 'item_value': None, language_country: ut.clean_text(sentence)}
					df_ess = df_ess.append(data, ignore_index = True)

					old_item_name = new_item_name	
										
					

		if not answer or answer[0] == '':
			new_item_name = question[0]
			survey_item_id = decide_on_survey_item_id(prefix, old_item_name, new_item_name)

			data = {"survey_item_ID": survey_item_id, 'Study': study, 'module': check_if_module_is_supplementary(question[0], supplementary_modules_in_txt), 
			'item_type': 'RESPONSE', 'item_name': new_item_name, 'item_value': None, language_country: write_down}
			df_ess = df_ess.append(data, ignore_index = True)

			old_item_name = new_item_name
				

		else:
			flag_is_income = False
			i=0
			income_values = ['J', 'R', 'C', 'M', 'F', 'S', 'K', 'P', 'D', 'H', 'U', 'N']

			if dk.translate(str.maketrans('', '', string.punctuation)) not in str(answer).translate(str.maketrans('', '', string.punctuation)):
				answer.append(dk)

			if re.compile('^00\s').match(answer[0]) or re.compile('^0\s').match(answer[0]):
				item_value = 0
			elif re.compile('^J\s').match(answer[0]):
				item_value = income_values[i]
				flag_is_income = True
			else: 
				item_value = 1
			
			for item in answer:
				t_table = str.maketrans(dict.fromkeys("()"))
				if item == dk or '88 '+dk in item or item == dk.translate(t_table): 
					item = re.sub("\d+", "", item)

					new_item_name = question[0]
					survey_item_id = decide_on_survey_item_id(prefix, old_item_name, new_item_name)

					data = {"survey_item_ID": survey_item_id, 'Study': study, 'module': check_if_module_is_supplementary(question[0], supplementary_modules_in_txt), 
					'item_type': 'RESPONSE', 'item_name': new_item_name, 'item_value': 888, language_country: ut.clean_text(item)}

					old_item_name = new_item_name

				elif item == refusal or '77 '+refusal in item or item == refusal.translate(t_table):
					item = re.sub("\d+", "", item)
					new_item_name = question[0]
					survey_item_id = decide_on_survey_item_id(prefix, old_item_name, new_item_name)

					data = {"survey_item_ID": survey_item_id, 'Study': study, 'module': check_if_module_is_supplementary(question[0], supplementary_modules_in_txt), 
					'item_type': 'RESPONSE','item_name': new_item_name, 'item_value': 777, language_country: ut.clean_text(item)}

					old_item_name = new_item_name

				elif item == dontapply or '99 '+dontapply in item or item == dontapply.translate(t_table): 
					item = re.sub("\d+", "", item)
					new_item_name = question[0]
					survey_item_id = decide_on_survey_item_id(prefix, old_item_name, new_item_name)

					data = {"survey_item_ID": survey_item_id, 'Study': study, 'module':check_if_module_is_supplementary(question[0], supplementary_modules_in_txt), 
					'item_type': 'RESPONSE', 'item_name': new_item_name, 'item_value': 999, language_country: ut.clean_text(item)}

					old_item_name = new_item_name


				else:
					if re.compile('(^00\s+\w)', re.IGNORECASE).match(item) and value_range_pattern.match(item) is None:
						item = re.sub("^00", "", item) 
					elif re.compile('(^10\s+\w)', re.IGNORECASE).match(item) and value_range_pattern.match(item) is None:
						item = re.sub("^10", "", item)
					elif re.compile('(^07\s+\w)', re.IGNORECASE).match(item) and value_range_pattern.match(item) is None:
						item = re.sub("^07", "", item) 
					elif re.compile('(^7\s+\w)', re.IGNORECASE).match(item) and value_range_pattern.match(item) is None:
						item = re.sub("^7", "", item) 
					elif re.compile('(^0\s+\w)', re.IGNORECASE).match(item) and value_range_pattern.match(item) is None:
						item = re.sub("^0", "", item) 
					elif re.compile('(^05\s+\w)', re.IGNORECASE).match(item) and value_range_pattern.match(item) is None:
						item = re.sub("^05", "", item) 
					elif re.compile('(^5\s+\w)', re.IGNORECASE).match(item) and value_range_pattern.match(item) is None:
						item = re.sub("^5", "", item) 
					elif re.compile('(^6\s+\w)', re.IGNORECASE).match(item) and value_range_pattern.match(item) is None:
						item = re.sub("^6", "", item) 
					elif re.compile('(^06\s+\w)', re.IGNORECASE).match(item) and value_range_pattern.match(item) is None:
						item = re.sub("^06", "", item) 
					elif re.compile('(^6\s+\w)', re.IGNORECASE).match(item) and value_range_pattern.match(item) is None:
						item = re.sub("^6", "", item) 
					elif re.compile('(^04\s+\w)', re.IGNORECASE).match(item) and value_range_pattern.match(item) is None:
						item = re.sub("^04", "", item) 
					elif re.compile('(^4\s+\w)', re.IGNORECASE).match(item) and value_range_pattern.match(item) is None:
						item = re.sub("^4", "", item) 

					new_item_name = question[0]
					survey_item_id = decide_on_survey_item_id(prefix, old_item_name, new_item_name)

					data = {"survey_item_ID": survey_item_id, 'Study': study, 'module': check_if_module_is_supplementary(question[0], supplementary_modules_in_txt), 
					'item_type': 'RESPONSE', 'item_name': new_item_name, 'item_value': item_value, language_country: ut.clean_text(item)}
					
					old_item_name = new_item_name
					if flag_is_income == False:
						item_value = item_value + 1 
					else:
						if i < len(income_values)-1:
							i = i+1
							item_value = income_values[i]
							

				df_ess = df_ess.append(data, ignore_index = True)

			#if there is an introduction the intro variable will be different from ''
			if intro != '':
				for item in intro:

					new_item_name = 'INTRO'
					survey_item_id = decide_on_survey_item_id(prefix, old_item_name, new_item_name)

					data = {"survey_item_ID": survey_item_id, 'Study': study, 'module': 'INTRO_MODULE', 'item_type': 'INTRO', 'item_name': 'INTRO', 
					'item_value': None,language_country: ut.clean_text(item)}
						
					old_item_name = new_item_name

					df_ess = df_ess.append(data, ignore_index = True)

	return df_ess

def process_supplementary_df(df_filtered_by_item_name, study, language_country, dk, write_down, prefix, filename):
	aux_df = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', language_country])

	survey_item_id = assign_survey_item_id_to_supplementary(prefix)
	item_type_unique = df_filtered_by_item_name['item_type'].unique()

	for i, row in df_filtered_by_item_name.iterrows():
		if row['item_type'] == 'REQUEST':
			if ut.set_of_instructions(row['text'].lower(), language_country, filename) == True:
				data = {"survey_item_ID": survey_item_id, 'Study': study, 'module': 'SUPP_'+row['module'], 'item_type': 'INSTRUCTION', 'item_name': row['item_name'], 
				'item_value': row['item_value'], language_country: ut.clean_text(row['text'])}
				aux_df = aux_df.append(data, ignore_index = True)
			else:
				data = {"survey_item_ID": survey_item_id, 'Study': study, 'module': 'SUPP_'+row['module'], 'item_type': row['item_type'], 'item_name': row['item_name'], 
				'item_value': row['item_value'], language_country: ut.clean_text(row['text'])}
				aux_df = aux_df.append(data, ignore_index = True)

		else:
			data = {"survey_item_ID": survey_item_id, 'Study': study, 'module': 'SUPP_'+row['module'], 'item_type': row['item_type'], 'item_name': row['item_name'], 
			'item_value': row['item_value'], language_country: ut.clean_text(row['text'])}
			aux_df = aux_df.append(data, ignore_index = True)

	tail = aux_df.tail(1)
	module =  tail.iloc[0]['module']
	item_name = tail.iloc[0]['item_name']
	

	if 'RESPONSE' not in item_type_unique:
		data = {"survey_item_ID": survey_item_id, 'Study': study, 'module': str(module), 'item_type': 'RESPONSE', 'item_name': str(item_name), 
		'item_value': 1, language_country: write_down}
		aux_df = aux_df.append(data, ignore_index = True)

	data = {"survey_item_ID": survey_item_id, 'Study': study, 'module': str(module), 'item_type': 'RESPONSE', 'item_name': str(item_name), 
		'item_value': 888, language_country: dk}
	aux_df = aux_df.append(data, ignore_index = True)

	return aux_df

def main(csv_file, filename, language_country, study):
	reset_initial_sufix()
	
	item_name_question_pattern = re.compile("(?:[A-K][A-Z]?\s?[1-9]{1,3}[a-z]?)+")
	df_ess_all = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', language_country])

	df_ess = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', language_country])
	item_name_old = 'old'
	
	prefix = study+'_'+language_country+'_'
	
	#Punkt Sentence Tokenizer from NLTK	
	sentence_splitter_prefix = 'tokenizers/punkt/'
	sentence_splitter_suffix = ut.determine_sentence_tokenizer(filename)
	sentence_splitter = sentence_splitter_prefix+sentence_splitter_suffix
	tokenizer = nltk.data.load(sentence_splitter)

	#Set up questionnaire params such as dk, resufal, etc
	value_range_pattern, write_down, dk, refusal, dontapply, showc, showc_lower, abbreviation_interviewer, full_form_interviewer, supplementary_modules_in_txt = define_language_country_param(language_country, filename)
	all_questions = get_question_all_questions(filename, item_name_question_pattern)
	

	df_ess = generate_main_questionnaire_df(df_ess, study, prefix, filename, language_country, item_name_question_pattern, all_questions, tokenizer, value_range_pattern, write_down, dk, refusal, dontapply, showc, showc_lower, abbreviation_interviewer, full_form_interviewer, supplementary_modules_in_txt)
	df_ess_all = df_ess_all.append(df_ess, ignore_index = True)

	if csv_file != '':
		df_supplementary = pd.read_csv(csv_file)
		unique_item_names = df_supplementary['item_name'].unique()

		for item in unique_item_names:
			df_filtered_by_item_name = df_supplementary[df_supplementary['item_name'] == item]
			aux_df = process_supplementary_df(df_filtered_by_item_name, study, language_country, dk, write_down, prefix, filename)
			df_ess_all = df_ess_all.append(aux_df, ignore_index = True)

	


	export_filename = study+'_'+language_country+'.csv'
	df_ess_all.to_csv(export_filename, encoding='utf-8', index=False)

	
	



if __name__ == "__main__":
	#Call script using filename, language_country and study parameters. 
	#For instance: reset && python3 txt2spr.py ESS_R01_2002_SOURCE_ENG.txt SOURCE_ENG ESS_R01_2002
	filename = str(sys.argv[1])
	language_country = str(sys.argv[2])
	study = str(sys.argv[3])
	main(filename, language_country, study)