"""
Utility functions for the text to spreadsheet transformation algorithm
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
"""

import re
import string

def intersection(iterableA, iterableB, key=lambda x: x):
    """Return the intersection of two iterables with respect to `key` function.

    """
    def unify(iterable):
        d = {}
        for item in iterable:
            d.setdefault(key(item), []).append(item)
        return d

    A, B = unify(iterableA), unify(iterableB)

    return [(A[k], B[k]) for k in A if k in B]

def standardize_question_name(question_name):
	question_name = re.sub('\.', "",question_name)

	return "".join(question_name.split())



def check_if_sentence_is_uppercase(text):
	is_uppercase = False
	if isinstance(text, str):
		text = text.translate(str.maketrans('', '', string.punctuation))
		"".join(text)
		text = re.sub('\s+', '', text)
		text = re.sub('\d+', '', text)
		for word in text:
			if word.isupper():
				is_uppercase = True
			else:
				is_uppercase = False
		# print(text, is_uppercase)

	return is_uppercase

def percentage_of_intersection(text, intersection):
	text_size = len(text)
	
	
	return len(intersection)/text_size
				

#a strategy to identify instructions based on regex
def set_of_instructions(text, language_country, filename):
	is_instruction = False

	if 'CAT_' in language_country:
		programmer_pattern = re.compile("(Programador:)", re.IGNORECASE)
		full_form_interviewer_pattern = re.compile("(Entrevistador:)", re.IGNORECASE)
		use_card_pattern = re.compile("(us|plau|utilitzi|aquesta|targeta|respondre)", re.IGNORECASE)
		use_card_again_pattern = re.compile("(us|plau|utilitzi|mateixa|targeta|respondre|altra|vegada)", re.IGNORECASE)
		continue_using_card_pattern = re.compile("(us|plau|Continuï|segueixi|utilitzant|mateixa|targeta|aquesta|respondre)", re.IGNORECASE)
		showc_pattern = re.compile("(mostrar|targeta)", re.IGNORECASE)
		choose_answer_in_card_pattern = re.compile("(Triï|resposta|d'aquesta|targeta)", re.IGNORECASE)
		new_card_pattern = re.compile("(dummy value)", re.IGNORECASE)
		other_variations_card_pattern = re.compile("(CONTINUÏ|MOSTRANT|targeta)", re.IGNORECASE)
		read_pattern = re.compile("(llegir|alta)", re.IGNORECASE)
		prompt_pattern = re.compile("(dummy value)", re.IGNORECASE)
		note_for_interviewer_pattern = re.compile("(nota per entrevistador codificar)", re.IGNORECASE)
		code_all_pattern = re.compile("(dummy value)", re.IGNORECASE)
		ask_all_pattern = re.compile("(preguntar|tothom)", re.IGNORECASE)
		tick_box_or_choose_one_pattern = re.compile("(Si|us|plau|encercli|una|opció)", re.IGNORECASE)
		choose_multiple_pattern = re.compile("(MARQUEU|TOTS|QUE|CORRESPONGUIN)", re.IGNORECASE)
		choose_closest_to_opinion_pattern = re.compile("(Si|us|plau|encercli|l'opció|més|propera|seva|opinió)", re.IGNORECASE)
		list_and_code_pattern = re.compile("(Codificar|totes|que|calgui)", re.IGNORECASE)
		list_and_code_organization_pattern =  re.compile("(LLEGIR|CADA|ORGANITZACIÓ|PER|TORNS)", re.IGNORECASE)
		insist_pattern =  re.compile("(insistiu)", re.IGNORECASE)
		suggest_answer_cattegories_pattern = re.compile("(suggerir|categories|resposta)", re.IGNORECASE)
		note_with_details_pattern = re.compile("(ANOTEU|AMB|TOTS|DETALLS)", re.IGNORECASE)
		new_card_pattern = re.compile("(dummy value)", re.IGNORECASE)
		only_one_answer_possible_pattern = re.compile("(dummy value)", re.IGNORECASE)

		only_one_answer_possible = ['(dummy value)']
		prompt = ['(dummy value)']
		new_card = ['(dummy value)']
		use_card = ['us', 'plau',  'utilitzi', 'aquesta', 'targeta', 'respondre']
		use_card_again = ['us', 'plau', 'utilitzi','mateixa','targeta','respondre','altra','vegada']
		continue_using_card = ['us', 'plau', 'Continuï', 'segueixi','utilitzant','mateixa','aquesta', 'targeta','respondre']
		show_card = ['mostrar', 'targeta']
		choose_answer_in_card = ['Triï', 'resposta', "d'aquesta", 'targeta']
		other_card = ['CONTINUÏ', 'MOSTRANT','targeta']
		read = ['llegir', 'alta']
		note_for_interviewer  = ['nota','per', 'entrevistador', 'codificar']
		code_all = ['(dummy value)']
		choose_multiple = ['MARQUEU','TOTS','QUE','CORRESPONGUIN']
		ask_all = ['preguntar', 'tothom']
		tick_box = ['Si','us','plau','encercli','una','opció']
		choose_closest = ['Si','us','plau','encercli',"l'opció",'més','propera','seva','opinió']
		list_and_code = ['Codificar', 'totes','que','calgui']
		list_and_code_organization = ['LLEGIR','CADA','ORGANITZACIÓ','PER','TORNS']
		insist = ['insistiu']
		suggest_answer_cattegories = ['suggerir', 'categories', 'resposta']
		note_with_details = ['ANOTEU','AMB','TOTS','DETALLS']
		

		if 'R01' in filename:
			read_pattern = re.compile("(LLEGIR|EN|VEU|ALTA)", re.IGNORECASE)
			read = ['LLEGIR','EN','VEU','ALTA']

		if 'R02' in filename:
			ask_all_pattern = re.compile("(A|TOTHOM)", re.IGNORECASE) 
			choose_answer_in_card_pattern = re.compile("(Si|us|plau|esculli|resposta|d'aquesta|targeta)")
			showc_pattern = re.compile("(mostrar|CONTINUÏ|MOSTRANT|targeta)", re.IGNORECASE)

			show_card = ['CONTINUÏ','MOSTRANT', 'mostrar', 'targeta']
			ask_all = ['a', 'tothom']
			choose_answer_in_card = ['Si','us','plau', 'esculli', 'resposta', "d'aquesta", 'targeta']

		if 'R03' in filename:
			showc_pattern = re.compile("(SEGUIR AMB|targeta)", re.IGNORECASE)
			show_card = ['SEGUIR', 'AMB', 'targeta']

		if 'R04' in filename or 'R05' in filename:
			showc_pattern = re.compile("(CONTINUEU MOSTRANT|MOSTREU|TARGETA)", re.IGNORECASE)
			show_card = ['CONTINUEU', 'MOSTRANT', 'MOSTREU', 'targeta']

		if 'R06' in filename:
			showc_pattern = re.compile("(CONTINUEU MOSTRANT|MOSTREU|TARGETA)", re.IGNORECASE)
			read_pattern = re.compile("(LLEGIU)", re.IGNORECASE)
			list_and_code_pattern = re.compile("(LLEGIU|CADA|AFIRMACIÓ|MARQUEU-HO|LA|GRAELLA)", re.IGNORECASE)
			choose_closest_to_opinion_pattern = re.compile("(Si|us|plau|MIRI|TRIAR|RESPOSTA|D'AQUESTA|TARGETA|QUE|S'AJUSTI|MILLOR|seva|opinió)", re.IGNORECASE)

			read = ['LLEGIU']
			show_card = ['CONTINUEU', 'MOSTRANT', 'MOSTREU', 'targeta']
			list_and_code = ['LLEGIU','CADA','AFIRMACIÓ','MARQUEU-HO','LA','GRAELLA']
			choose_closest = ['Si','us','plau','MIRI','TRIAR','RESPOSTA',"D'AQUESTA", 'TARGETA','QUE',"S'AJUSTI", 'MILLOR','seva','opinió']

	if 'CZE' in language_country:
		programmer_pattern = re.compile("(tazatele)", re.IGNORECASE)
		#this one actually means instruction
		full_form_interviewer_pattern = re.compile("(Pokyn:)", re.IGNORECASE)
		use_card_pattern = re.compile("(odpovědi|Nyní|prosím|použijte|tuto|kartu|karta)", re.IGNORECASE)
		use_card_again_pattern = re.compile("(použijte|tuto|Předložte|opět|karta|kartu)", re.IGNORECASE)
		continue_using_card_pattern = re.compile("('Při|odpovědích|Použijte|stejnou|znovu|tuto|kartu|karta)", re.IGNORECASE)
		showc_pattern = re.compile("(KARTU|KARTA)", re.IGNORECASE)
		choose_answer_in_card_pattern = re.compile("(Vyberte|svou|prosím|jednu|odpověď|této|karty)", re.IGNORECASE)
		new_card_pattern = re.compile("(dummy value)", re.IGNORECASE)
		other_variations_card_pattern = re.compile("(Prohlédněte|si|karta|kartu)", re.IGNORECASE)
		read_pattern = re.compile("(přečtěte|varianty|odpovědí)", re.IGNORECASE)
		prompt_pattern = re.compile("(dummy value)", re.IGNORECASE)
		note_for_interviewer_pattern = re.compile("(poznámka pro tazatele)", re.IGNORECASE)
		code_all_pattern = re.compile("(dummy value)", re.IGNORECASE)
		ask_all_pattern = re.compile("(ptejte|Přejte|se|všech)", re.IGNORECASE)
		tick_box_or_choose_one_pattern = re.compile("(NA|KAŽDÉM|ŘÁDKU|MOŽNÁ|POUZE|JEDNA|ODPOVĚĎ)", re.IGNORECASE)
		choose_multiple_pattern = re.compile("(zakroužkujte|všechny|odpovědi)", re.IGNORECASE)
		choose_closest_to_opinion_pattern = re.compile("()", re.IGNORECASE)
		list_and_code_pattern = re.compile("(ČTĚTE|NAHLAS|KAŽDÝ|VÝROK|ZAZNAMENEJTE|ODPOVĚĎ|TABULKY)", re.IGNORECASE)
		list_and_code_organization_pattern =  re.compile("(Čtěte|postupně|všechny|organizace)", re.IGNORECASE)
		insist_pattern =  re.compile("(SONDUJTE)", re.IGNORECASE)
		suggest_answer_cattegories_pattern = re.compile("(dummy value)", re.IGNORECASE)
		note_with_details_pattern = re.compile("(dummy value)", re.IGNORECASE)
		only_one_answer_possible_pattern = re.compile("(dummy value)", re.IGNORECASE)

		only_one_answer_possible = ['dummy value']
		use_card = ['odpovědi','Nyní','prosím','použijte','kartu','tuto','karta']
		use_card_again = ['Předložte','použijte', 'tuto', 'opět','karta','kartu']
		continue_using_card = ['Při', 'odpovědích', 'Použijte','stejnou','znovu','tuto','kartu','karta']
		show_card = ['KARTU','KARTA']
		choose_answer_in_card = ['Vyberte','svou','prosím','jednu','odpověď','této','karty']
		new_card = ['(dummy value)']
		other_card = ['Prohlédněte','si','karta','kartu']
		read = ['přečtěte','varianty','odpovědí']
		prompt = ['(dummy value)']
		note_for_interviewer  = ['poznámka', 'pro', 'tazatele']
		code_all = ['(dummy value)']
		ask_all = ['ptejte', 'Přejte', 'se','všech']
		tick_box = ['NA','KAŽDÉM','ŘÁDKU', 'MOŽNÁ','POUZE','JEDNA','ODPOVĚĎ']
		choose_closest = ['']
		choose_multiple = ['zakroužkujte','všechny','odpovědi']
		list_and_code = ['ČTĚTE','NAHLAS','KAŽDÝ','VÝROK','ZAZNAMENEJTE','ODPOVĚĎ','TABULKY']
		list_and_code_organization = ['Čtěte','postupně','všechny','organizace']
		insist = ['SONDUJTE']
		suggest_answer_cattegories = ['(dummy value)']
		note_with_details = ['(dummy value)']


		if 'R02' in filename:
			read_pattern = re.compile("(ČTĚTE NAHLAS)", re.IGNORECASE)
			showc_pattern = re.compile("(opět|KARTA)", re.IGNORECASE)
			other_variations_card_pattern = re.compile("(Prohlédněte|si|karta|kartu)", re.IGNORECASE)

			other_card = ['Prohlédněte','si','karta','kartu']
			show_card = ['opět','karta']
			read = ['ČTĚTE','NAHLAS']
		
		if 'R04' in filename:
			read_pattern = re.compile("(ČTĚTE NAHLAS)", re.IGNORECASE)
			showc_pattern = re.compile("(opět|KARTU)", re.IGNORECASE)
			note_for_interviewer_pattern = re.compile("(POZNÁMKA PRO TAZATELE:)", re.IGNORECASE)
			choose_answer_in_card = re.compile("(Vyberte|vaší|prosím|odpověď|této|z|karty)", re.IGNORECASE)

			choose_answer_in_card = ['Vyberte', 'vaší', 'prosím','odpověď','z','této','karty']
			show_card = ['opět','kartu']
			read = ['ČTĚTE','NAHLAS']

		if 'R05' in filename:
			read_pattern = re.compile("(ČTĚTE NAHLAS)", re.IGNORECASE)
			showc_pattern = re.compile("(PŘEDLOŽTE|KARTU)", re.IGNORECASE)
			note_for_interviewer_pattern = re.compile("(POZNÁMKA PRO TAZATELE:)", re.IGNORECASE)
			choose_answer_in_card = re.compile("(Vyberte|odpověď|této|z|karty)", re.IGNORECASE)
			use_card_pattern = re.compile("(Nyní|prosím|použijte|tuto|kartu|stejnou)", re.IGNORECASE)
			

			use_card = ['Nyní','prosím','použijte','tuto','kartu','stejnou']
			choose_answer_in_card = ['Vyberte','odpověď','z','této','karty']
			show_card = ['PŘEDLOŽTE','kartu']
			read = ['ČTĚTE','NAHLAS']
		
		if 'R06' in filename:
			programmer_pattern = re.compile("TAZ", re.IGNORECASE)
			read_pattern = re.compile("(ČTĚTE NAHLAS)", re.IGNORECASE)
			showc_pattern = re.compile("(STÁLE|KARTA)", re.IGNORECASE)
			other_variations_card_pattern = re.compile("(PŘEDLOŢTE|KARTU)", re.IGNORECASE)
			note_for_interviewer_pattern = re.compile("(POZNÁMKA PRO TAZATELE:)", re.IGNORECASE)
			choose_answer_in_card = re.compile("(Vyberte|odpověď|této|z|karty)", re.IGNORECASE)
			use_card_pattern = re.compile("(Nyní|prosím|použijte|tuto|kartu|stejnou)", re.IGNORECASE)
			

			use_card = ['Nyní','prosím','použijte','tuto','kartu','stejnou']
			choose_answer_in_card = ['Vyberte','odpověď','z','této','karty']
			show_card = ['STÁLE','karta']
			other_card = ['PŘEDLOŢTE','kartu']
			read = ['ČTĚTE','NAHLAS']
		


		

	if 'ENG' in language_country:
		programmer_pattern = re.compile("(Programmer:)", re.IGNORECASE)
		full_form_interviewer_pattern = re.compile("(Interviewer)", re.IGNORECASE)
		use_card_pattern = re.compile("(please|use|this|card|answer)", re.IGNORECASE)
		use_card_again_pattern = re.compile("(please|use|this|card|again)", re.IGNORECASE)
		continue_using_card_pattern = re.compile("(please|still|use|this|same|card|answer)", re.IGNORECASE)
		showc_pattern = re.compile("(show card)", re.IGNORECASE)
		choose_answer_in_card_pattern = re.compile("(please|Choose|one|your|answer|from|this|card)", re.IGNORECASE)
		new_card_pattern = re.compile("", re.IGNORECASE)
		other_variations_card_pattern = re.compile("(card|again|still)", re.IGNORECASE)
		read_pattern = re.compile("(read out)", re.IGNORECASE)
		prompt_pattern = re.compile("(prompt|relation|precodes)", re.IGNORECASE)
		note_for_interviewer_pattern = re.compile("(note for the Interviewer)", re.IGNORECASE)
		code_all_pattern = re.compile("(code|all|applies)", re.IGNORECASE)
		ask_all_pattern = re.compile("(ask all|interviewers)", re.IGNORECASE)
		tick_box_or_choose_one_pattern = re.compile("(Please|tick|one|box)", re.IGNORECASE)
		choose_multiple_pattern = re.compile("(Select|all|that|apply)", re.IGNORECASE)
		choose_closest_to_opinion_pattern = re.compile("(Please|tick|box|closest|your|opinion)", re.IGNORECASE)
		list_and_code_pattern = re.compile("(READ|OUT|EACH|STATEMENT|CODE|GRID)", re.IGNORECASE)
		list_and_code_organization_pattern =  re.compile("", re.IGNORECASE)
		insist_pattern =  re.compile("(INSIST)", re.IGNORECASE)
		suggest_answer_cattegories_pattern = re.compile("", re.IGNORECASE)
		note_with_details_pattern = re.compile("(IN|GRID|COLLECT|DETAILS|RESPONDENT)", re.IGNORECASE)
		only_one_answer_possible_pattern = re.compile("(Please|select|only|one)", re.IGNORECASE)
		
		only_one_answer_possible = ['Please','select','only','one']
		use_card = ['please','use', 'this', 'card', 'answer']	
		use_card_again = ['please','use', 'this', 'card', 'again']
		continue_using_card = ['please','still','use','this','same','card','answer']
		show_card = ['show', 'card']
		choose_answer_in_card = ['please','Choose','one', 'your','answer','from','this','card']
		new_card = ['']
		other_card = ['card','again','still']
		read = ['read', 'out']
		prompt = ['prompt', 'relation', 'precodes']
		note_for_interviewer = ['note', 'for', 'interviewer']
		code_all = ['code', 'all']
		ask_all = ['ask', 'all']
		tick_box = ['Please','tick','one','box']
		choose_multiple = ['Select','all','that','apply']
		choose_closest = ['Please','tick','box','closest','your','opinion']
		list_and_code = ['READ','OUT','EACH','STATEMENT','CODE','GRID']
		list_and_code_organization = ['']
		insist = ['INSIST']
		suggest_answer_cattegories = ['']
		note_with_details = ['IN','GRID','COLLECT','DETAILS','RESPONDENT']
		
		if '_GB' in filename:
			if 'R03' in filename or 'R04' in filename:
				full_form_interviewer_pattern = re.compile("(Interviewer)", re.IGNORECASE)

			if 'R05' in filename:
				other_variations_card_pattern = re.compile("(showcard|still|again)", re.IGNORECASE)
				other_card = ['again','still', 'showcard']

		if '_IE' in filename:
			if 'R01' in filename:
				showc_pattern = re.compile("(interviewer show card)", re.IGNORECASE)
				show_card = ['interviewer', 'show', 'card']
			else:
				full_form_interviewer_pattern = re.compile("(Interviewer)", re.IGNORECASE)
				other_variations_card_pattern = re.compile("(card|still card)", re.IGNORECASE)
				tick_box_or_choose_one_pattern = re.compile("(Please|code|select|only|one)", re.IGNORECASE)
				tick_box = ['Please','select','code','only','one']
				other_card = ['still', 'card']
			
		if '_SOURCE' in filename:
			full_form_interviewer_pattern = re.compile("(Interviewer)", re.IGNORECASE)
			other_variations_card_pattern = re.compile("(card|still card)", re.IGNORECASE)
			tick_box_or_choose_one_pattern = re.compile("(Please|code|select|only|one)", re.IGNORECASE)
			tick_box = ['Please','select','code','only','one']
			other_card = ['still', 'card']
			


	if 'FRE' in language_country:
		programmer_pattern = re.compile("(Programmeur)", re.IGNORECASE)
		full_form_interviewer_pattern = re.compile("(Enquêteur)", re.IGNORECASE)
		use_card_pattern = re.compile("(S'il|vous|plaît|utilisez|cette|carte)", re.IGNORECASE)
		use_card_again_pattern = re.compile("(S'il|vous|plaît|utilisez|nouveau|cette|même|carte)", re.IGNORECASE)
		continue_using_card_pattern = re.compile("(S'il|vous|plaît|utilisez|encore|cette|carte)", re.IGNORECASE)
		showc_pattern = re.compile("(carte)", re.IGNORECASE)
		choose_answer_in_card_pattern = re.compile("(Veuillez utiliser|carte|pour répondre)")
		new_card_pattern = re.compile("()", re.IGNORECASE)
		other_variations_card_pattern = re.compile("(carte|toujours carte)", re.IGNORECASE)
		read_pattern = re.compile("(lisez|lire)", re.IGNORECASE)
		prompt_pattern = re.compile("()", re.IGNORECASE)
		note_for_interviewer_pattern = re.compile("(NOTE A L'ENQUETEUR)", re.IGNORECASE) 
		code_all_pattern = re.compile("(codez|tout)", re.IGNORECASE)
		ask_all_pattern = re.compile("(demandez|tous)", re.IGNORECASE)
		tick_box_or_choose_one_pattern = re.compile("(Veuillez|choisir|une|seule|réponses|figurant|sur|cette|carte)", re.IGNORECASE)
		choose_multiple_pattern = re.compile("(CHOIX|MULTIPLE|POSSIBLE)", re.IGNORECASE)
		choose_closest_to_opinion_pattern = re.compile("", re.IGNORECASE)
		list_and_code_pattern = re.compile("(LISEZ|CHAQUE|POINT|VUE|ENCODEZ-LE|DANS|GRILLE)", re.IGNORECASE)
		list_and_code_organization_pattern =  re.compile("(LISEZ|CHAQUE|ORGANISATION|SON|TOUR)", re.IGNORECASE)	
		insist_pattern =  re.compile("(RELANCER:)", re.IGNORECASE)
		suggest_answer_cattegories_pattern = re.compile("()", re.IGNORECASE)
		note_with_details_pattern = re.compile("()", re.IGNORECASE)
		only_one_answer_possible_pattern = re.compile("(dummy value)", re.IGNORECASE)
		
		only_one_answer_possible = ['(dummy value)']
		use_card = ["S'il",'vous','plaît','utilisez','cette','carte']
		use_card_again = ["S'il",'vous','plaît','utilisez', 'nouveau','même', 'cette','carte']
		continue_using_card = ["S'il",'vous','plaît','utilisez','encore','cette','carte']
		show_card = ['carte']
		choose_answer_in_card = ['Veuillez', 'utiliser', 'carte', 'pour', 'répondre']
		new_card = []
		other_card = ['carte', 'toujours']
		read = ['lisez', 'lire']
		prompt = ['']
		note_for_interviewer = ['NOTE', "L'ENQUETEUR"]
		code_all = ['codez']
		ask_all = ['demandez', 'tous']
		tick_box = ['Veuillez','choisir','une','seule','réponses','figurant','sur','cette','carte']
		choose_multiple = ['CHOIX', 'MULTIPLE', 'POSSIBLE']
		choose_closest = []
		list_and_code = ['LISEZ','CHAQUE','POINT','VUE','ENCODEZ-LE','DANS','GRILLE']
		list_and_code_organization = ['LISEZ','CHAQUE','ORGANISATION','SON','TOUR']
		insist = []
		suggest_answer_cattegories = []
		note_with_details = []

		if '_BE' in filename:
			showc_pattern = re.compile("(montrez carte|montrez encore carte)", re.IGNORECASE)
			use_card_pattern = re.compile("(Veuillez|utiliser|cette|carte|pour répondre)")
			choose_multiple_pattern = re.compile("(CHOIX|MULTIPLE|POSSIBLE)", re.IGNORECASE)
			
			choose_multiple = ['CHOIX', 'MULTIPLE', 'POSSIBLE']
			use_card = ['Veuillez', 'utiliser', 'cette', 'carte', 'pour', 'répondre']		
			show_card = ['montrez', 'encore', 'carte']

			if 'R01' in filename:
				showc_pattern = re.compile("(Toujours|l'aide|de|cette|carte)", re.IGNORECASE)
				code_all_pattern = re.compile("(CODEZ|TOUT|CE|QUI|S'APPLIQUE)", re.IGNORECASE)

				code_all = ['CODEZ','TOUT','CE','QUI',"S'APPLIQUE"]
				show_card = ['Toujours', "l'aide", 'de', 'cette', 'carte']
			if 'R02' in filename:
				choose_answer_in_card_pattern = re.compile("Choisissez|votre|réponse|sur|cette|carte")
				use_card_pattern = re.compile("(utilisez|nouveau|cette|même|carte|pour répondre)", re.IGNORECASE)
				other_variations_card_pattern = re.compile("(Je vous prie d'utiliser|cette|carte|pour répondre)")
			
				other_card = ['je', 'vous', 'prie', "d'utiliser", 'cette','carte', 'pour', 'répondre']
				choose_answer_in_card = ['Choisissez', 'votre', 'réponse', 'sur', 'cette', 'carte']
				use_card = ['utilisez','nouveau','cette','même','carte','pour', 'répondre']
			if 'R04' in filename or 'R05' in filename:
				full_form_interviewer_pattern = re.compile("(ENQUETEUR)", re.IGNORECASE)
				choose_answer_in_card_pattern = re.compile("Choisissez|votre|réponse|sur|cette|carte")
				list_and_code_pattern = re.compile("(LIRE|HAUTE|VOIX|CHAQUE|PHRASE|CODER|DANS|GRILLE)", re.IGNORECASE)
				note_for_interviewer_pattern = re.compile("(INSTRUCTION POUR L'ENQUETEUR:)", re.IGNORECASE) 
				
				list_and_code = ['LIRE','HAUTE','VOIX', 'CHAQUE','PHRASE','CODER','DANS','GRILLE']
				choose_answer_in_card = ['Choisissez', 'votre', 'réponse', 'sur', 'cette', 'carte']
			if 'R05' in filename:
				showc_pattern = re.compile("(toujours|carte)", re.IGNORECASE)
				other_variations_card_pattern = re.compile("(Veuillez répondre|moyen|l'aide|cette|carte)")
				
				other_card = ['Veuillez', 'répondre','moyen', "l'aide", 'cette','carte']
				show_card = ['toujours', 'carte']
			if 'R06' in filename:
				ask_all_pattern = re.compile("(poser|a|tous)", re.IGNORECASE)
				read_pattern = re.compile("(lire|PROPOSITIONS)", re.IGNORECASE)
	
				ask_all = ['poser', 'a','tous']
				read = ['lire', 'PROPOSITIONS']
				

		if '_CH' in filename:
			use_card_pattern = re.compile("(Je vous prie d'utiliser|cette|carte|pour répondre)")
			use_card = ['je', 'vous', 'prie', "d'utiliser", 'cette','carte', 'pour', 'répondre']

			if 'R02' in filename or 'R04' in filename or 'R06' in filename:
				continue_using_card_pattern = re.compile("(Continuez|utiliser|cette|carte)", re.IGNORECASE)
				other_variations_card_pattern = re.compile("(Veuillez répondre|l'aide|cette|carte)")
				choose_answer_in_card_pattern = re.compile("(Choisissez|votre|réponse|sur|cette|carte)")
				
				choose_answer_in_card = ['Choisissez', 'votre', 'réponse', 'sur', 'cette', 'carte']
				other_card = ['Veuillez', 'répondre', "l'aide", 'cette','carte']
				continue_using_card = ['Continuez','utiliser','encore','cette','carte']

			if 'R03' in filename:
				showc_pattern = re.compile("(montrez|la carte|montrez|encore)", re.IGNORECASE)
				continue_using_card_pattern = re.compile("(Continuez|utiliser|cette|carte)", re.IGNORECASE)
				other_variations_card_pattern = re.compile("(carte)")
				choose_answer_in_card_pattern = re.compile("(Choisissez|votre|réponse|sur|cette|carte)")
				
				show_card = ['montrez', 'encore', 'la', 'carte']
				choose_answer_in_card = ['Choisissez', 'votre', 'réponse', 'sur', 'cette', 'carte']
				other_card = ['carte']
				continue_using_card = ['Continuez','utiliser','encore','cette','carte']

			if 'R04' in filename:
				continue_using_card_pattern = re.compile("(Continuez|utiliser|cette|carte)", re.IGNORECASE)
				other_variations_card_pattern = re.compile("(Je vous prie|choisir|votre réponse|sur|cette carte)")
				choose_answer_in_card_pattern = re.compile("(Choisissez|votre|réponse|sur|cette|carte)")
				# use_card_again_pattern = re.compile("(Veuillez|utiliser|cette|noveau|même|carte|pour|répondre)", re.IGNORECASE)
				
				# use_card_again = ['Veuillez', 'utiliser', 'cette', 'noveau','même','carte', 'pour', 'répondre']
				choose_answer_in_card = ['Choisissez', 'votre', 'réponse', 'sur', 'cette', 'carte']
				other_card = ['Je', 'vous', 'prie','choisir','votre', 'réponse','sur', 'cette','carte']
				continue_using_card = ['Continuez','utiliser','encore','cette','carte']

			if 'R05' in filename:
				continue_using_card_pattern = re.compile("(Continuez|utiliser|cette|carte)", re.IGNORECASE)
				other_variations_card_pattern = re.compile("(Je vous prie|choisir|votre réponse|sur|cette carte)")
				choose_answer_in_card_pattern = re.compile("(Choisissez|votre|réponse|sur|cette|carte)")
				showc_pattern = re.compile("(toujours|carte)", re.IGNORECASE)
				
				show_card = ['toujours', 'carte']
				choose_answer_in_card = ['Choisissez', 'votre', 'réponse', 'sur', 'cette', 'carte']
				other_card = ['Je', 'vous', 'prie','choisir','votre', 'réponse','sur', 'cette','carte']
				continue_using_card = ['Continuez','utiliser','encore','cette','carte']

		if '_FR' in filename:
			full_form_interviewer_pattern = re.compile("(ENQUETEUR)", re.IGNORECASE)
			use_card_pattern = re.compile("(Je vous prie d'utiliser|Veuillez utiliser|carte|pour répondre)", re.IGNORECASE)
			showc_pattern = re.compile("(montrez carte \d+|montrez encore carte \d+|carte \d+)", re.IGNORECASE)
			choose_multiple_pattern = re.compile("(PLUSIEURS|REPONSES|POSSIBLES)", re.IGNORECASE)
			
			choose_multiple = ['PLUSIEURS', 'REPONSES', 'POSSIBLE']
			use_card = ['vous', 'prie', "d'utiliser", 'Veuillez', 'utiliser', 'carte', 'pour', 'répondre']
			show_card = ['montrez', 'encore', 'carte']

			if 'R03' in filename or 'R04' in filename or 'R05' in filename:
				continue_using_card_pattern = re.compile("(Continuez|utiliser|cette|carte)", re.IGNORECASE)
				choose_answer_in_card_pattern = re.compile("(Choisissez|votre|réponse|sur|cette|carte)", re.IGNORECASE)
				other_variations_card_pattern = re.compile("(Répondez|utilisant|cette|carte)", re.IGNORECASE)
				
				choose_answer_in_card = ['Choisissez', 'votre', 'réponse', 'sur', 'cette', 'carte']
				continue_using_card = ['Continuez','utiliser','encore','cette','carte']
				other_card = ['Répondez','utilisant','cette','carte']

			if 'R06' in filename:
				continue_using_card_pattern = re.compile("(Continuez|utiliser|cette|carte)", re.IGNORECASE)
				choose_answer_in_card_pattern = re.compile("(Choisissez|votre|réponse|sur|cette|carte)", re.IGNORECASE)
				other_variations_card_pattern = re.compile("(Je vous prie d'utiliser|cette|carte|pour répondre)", re.IGNORECASE)
				ask_all_pattern = re.compile("(poser|a tous)", re.IGNORECASE)
				showc_pattern = re.compile("(laisser|carte)", re.IGNORECASE)
				
				choose_answer_in_card = ['Choisissez', 'votre', 'réponse', 'sur', 'cette', 'carte']
				continue_using_card = ['Continuez','utiliser','encore','cette','carte']
				other_card = ['je', 'vous', 'prie', "d'utiliser", 'cette','carte', 'pour', 'répondre']
				ask_all = ['poser', 'a', 'tous']
				show_card = ['laisser', 'carte']

		if '_LU' in filename:
			list_and_code_organization_pattern =  re.compile("(ENONCEZ|UNE|ORGANISATION|LA|FOIS)", re.IGNORECASE)
			choose_multiple_pattern = re.compile("(VOUS|POUVEZ|COCHER|PLUSIEURS|CASES|POUR|CHAQUE|ORGANISATION)", re.IGNORECASE)
			
			choose_multiple = ['VOUS','POUVEZ','COCHER','PLUSIEURS','CASES','POUR','CHAQUE','ORGANISATION']	
			list_and_code_organization = ['ENONCEZ','UNE','ORGANISATION','LA','FOIS']

			if 'R02' in filename:
				tick_box_or_choose_one_pattern = re.compile("(Cerclez|code|correspondant|votre|réponse)", re.IGNORECASE)
				choose_multiple_pattern = re.compile("(PLUSIEURS|REPONSES|POSSIBLES)", re.IGNORECASE)
			
				choose_multiple = ['PLUSIEURS', 'REPONSES', 'POSSIBLE']
				tick_box = ['Cerclez','code','correspondant','votre','réponse']
	
	if 'GER' in language_country:
		programmer_pattern = re.compile("(Befrager)", re.IGNORECASE)
		full_form_interviewer_pattern = re.compile("(Befrager)", re.IGNORECASE)
		use_card_pattern = re.compile("(Verwenden|Sie|Karte|Nr)", re.IGNORECASE)
		use_card_again_pattern = re.compile("(Bitte sagen Sie|bitte|nochmals|mir|anhand|von|Liste)", re.IGNORECASE)
		continue_using_card_pattern = re.compile("(Bitte sagen Sie|es|mir|noch|einmal|anhand|von|karte)", re.IGNORECASE)
		showc_pattern = re.compile("(Karte)", re.IGNORECASE)
		choose_answer_in_card_pattern = re.compile("(Bitte|verwenden|Sie|diese|Karte|für|Ihre|Antwort)", re.IGNORECASE)
		only_one_answer_possible_pattern = re.compile("(NUR|EINE|ANTWORT|MÖGLICH)", re.IGNORECASE)
		new_card_pattern = re.compile("(neue|Karte)", re.IGNORECASE)
		other_variations_card_pattern = re.compile("(Bitte|benutzen|Sie|Liste|karte)", re.IGNORECASE)
		read_pattern = re.compile("(BITTE|VORLESEN)", re.IGNORECASE)
		prompt_pattern = re.compile("(Prompt)", re.IGNORECASE)
		note_for_interviewer_pattern = re.compile("(Hinweis für den Interviewer:)", re.IGNORECASE)
		code_all_pattern = re.compile("(code)", re.IGNORECASE)
		ask_all_pattern = re.compile("(an alle)", re.IGNORECASE)
		#GER_DE
		tick_box_or_choose_one_pattern = re.compile("(Bitte|kreuzen|Sie|ein|Kästchen|an)", re.IGNORECASE)
		choose_multiple_pattern = re.compile("", re.IGNORECASE)
		choose_closest_to_opinion_pattern = re.compile("(Bitte sagen Sie|jene|Zahl|die|Ihrer|Meinung|besten|entspricht)", re.IGNORECASE)
		list_and_code_pattern = re.compile("", re.IGNORECASE)
		list_and_code_organization_pattern =  re.compile("", re.IGNORECASE)
		insist_pattern =  re.compile("(NACHFRAGEN)", re.IGNORECASE)
		suggest_answer_cattegories_pattern = re.compile("", re.IGNORECASE)
		note_with_details_pattern = re.compile("", re.IGNORECASE)

		use_card = ['verwenden', 'sie', 'karte', 'nr']
		use_card_again = ['bitte', 'sagen', 'sie', 'bitte','nochmals', 'mir', 'anhand', 'von', 'liste']
		continue_using_card = ['Bitte', 'sagen', 'Sie', 'es', 'mir', 'noch', 'einmal', 'anhand', 'von','karte']
		show_card = ['karte']
		choose_answer_in_card = ['Bitte','verwenden','Sie','diese','Karte','für','Ihre','Antwort']
		new_card = ['neue', 'Karte']
		other_card = ['Bitte', 'benutzen', 'Sie','Liste','karte']
		read =['BITTE','vorlesen']
		prompt = ['null']
		note_for_interviewer = ['null']
		code_all = ['null']
		ask_all = ['an', 'alle']
		tick_box = ['Bitte','kreuzen','Sie','ein','Kästchen','an']
		choose_multiple = ['null']
		choose_closest = ['Bitte', 'sagen', 'Sie','jene','Zahl','die','Ihrer','Meinung','besten','entspricht']
		list_and_code = ['null']
		list_and_code_organization = ['null']
		insist = ['NACHFRAGEN']
		suggest_answer_cattegories = ['null']
		note_with_details = ['null']
		only_one_answer_possible = ['NUR','EINE','ANTWORT','MÖGLICH']

		if '_AT' in language_country:
			showc_pattern = re.compile("(karte|Weiter karte)", re.IGNORECASE)
			continue_using_card_pattern = re.compile("(Bitte|verwenden|Sie|weiterhin|diese|dieselbe|karte)", re.IGNORECASE)
			use_card_again_pattern = re.compile("(Verwenden|Sie|wieder|wiederum|jetzt|bitte|diese|karte)", re.IGNORECASE)
			choose_answer_in_card_pattern = re.compile("(Bitte|wählen|Sie|eine|Antwort|Karte)", re.IGNORECASE)

			show_card = ['karte', 'Weiter']
			continue_using_card = ['Bitte', 'verwenden', 'sie', 'weiterhin','diese', 'dieselbe', 'karte']
			use_card_again = ['verwenden', 'sie', 'karte', 'wieder', 'wiederum', 'diese', 'jetzt', 'bitte']
			choose_answer_in_card = ['Bitte','wählen','Sie','eine','Antwort','Karte']

			if 'R02' in filename:
				full_form_interviewer_pattern = re.compile("(Interviewer)", re.IGNORECASE)
			
			if 'R04' in filename:
				choose_answer_in_card_pattern = re.compile("(Wählen|Sie|Antwort|von|dieser|Karte)", re.IGNORECASE)
				use_card_pattern = re.compile("(Verwenden|Sie|die|gleiche|Karte)", re.IGNORECASE)
				tick_box_or_choose_one_pattern = re.compile("(Nur|eine|Antwort)", re.IGNORECASE)
				other_variations_card_pattern = re.compile("(Und|nun|Bitte|benutzen|Sie|dazu|wieder|Karte|Liste)", re.IGNORECASE) 

				choose_answer_in_card = ['Wählen','Sie','Antwort','von','dieser','Karte']
				use_card = ['Verwenden','Sie','die','gleiche','Karte']
				tick_box = ['Nur', 'eine', 'Antwort']
				other_card = ['Und','nun','Bitte','benutzen','Sie','dazu','wieder','Karte', 'Liste']
			
			if 'R05' in filename:
				choose_answer_in_card_pattern = re.compile("(Wählen|Sie|Antwort|von|dieser|Karte)", re.IGNORECASE)
				tick_box_or_choose_one_pattern = re.compile("(Bitte|ringeln|Sie|eine|Antwortzahl)", re.IGNORECASE)
				
				choose_answer_in_card = ['Wählen','Sie','Antwort','von','dieser','Karte']
				tick_box = ['Bitte','ringeln','Sie','eine','Antwortzahl']

		if '_CH' in language_country:
			choose_answer_in_card_pattern = re.compile("(Bitte|wählen|verwenden|Sie|für|eine|Antwort|dafür|diese|dieser|karte)", re.IGNORECASE)
			showc_pattern = re.compile("(karte \d+|IMMER NOCH karte \d+)", re.IGNORECASE)
			use_card_again_pattern = re.compile("(Verwenden|Sie|die|gleiche|karte|nochmals)", re.IGNORECASE)
			other_variations_card_pattern = re.compile("(Und|nun|Bitte|benutzen|Sie|dazu|wieder|Karte|Liste)", re.IGNORECASE) 

			choose_answer_in_card = ['Bitte', 'wählen', 'verwenden', 'sie', 'für','eine', 'Antwort', 'dafür', 'diese','dieser', 'karte']
			show_card = ['karte', 'IMMER', 'NOCH']
			use_card_again = ['verwenden', 'sie', 'die', 'gleiche', 'karte', 'nochmals']
			other_card = ['Und','nun','Bitte','benutzen','Sie','dazu','wieder','Karte', 'Liste']

			if 'R02':
				other_variations_card_pattern = re.compile("(Geb|Bitte|verwenden|Sie|Ihre|Antwort|anhand|dieser|Beantwortung|Frage|diese|Karte)", re.IGNORECASE) 
				other_card = ['Geb','Bitte','verwenden','Sie','Ihre','Antwort','anhand','dieser','Beantwortung','Frage','diese','Karte']

		if '_DE' in language_country:
			full_form_interviewer_pattern = re.compile("(Interviewer)", re.IGNORECASE)
			showc_pattern = re.compile("(Liste \d+)", re.IGNORECASE)
			use_card_again_pattern = re.compile("(Bitte benutzen Sie|jetzt|dazu|dafür|wieder|die|Liste)", re.IGNORECASE)

			show_card = ['liste']
			use_card_again = ['bitte', 'benutzen', 'sie', 'dazu', 'dafür', 'wieder', 'jetzt', 'die', 'liste']

			if 'R04' in filename:
				choose_answer_in_card_pattern = re.compile("(Wählen|Sie|Antwort|von|dieser|Liste)", re.IGNORECASE)
				choose_answer_in_card = ['Wählen','Sie','Antwort','von','dieser','Liste']
			
			if 'R05' in filename or 'R06' in filename:
				choose_answer_in_card_pattern = re.compile("(Wählen|Sie|Antwort|von|dieser|Liste)", re.IGNORECASE)
				use_card_pattern = re.compile("(Bitte|benutzen|Sie|diese|Liste|antworten)", re.IGNORECASE)
				use_card_again_pattern = re.compile("(Bitte benutzen Sie|jetzt|dazu|dafür|wieder|Antwort|nochmals|Liste)", re.IGNORECASE)
				
				choose_answer_in_card = ['Wählen','Sie','Antwort','von','dieser','Liste']
				use_card = ['Bitte','benutzen','Sie','diese','Liste','antworten']
				se_card_again = ['bitte', 'benutzen', 'sie', 'dazu', 'dafür', 'wieder', 'jetzt', 'Antwort','nochmals', 'liste']

	if 'NOR' in language_country:
		programmer_pattern = re.compile("(programmerer)", re.IGNORECASE)
		full_form_interviewer_pattern = re.compile("(Intervjuer)", re.IGNORECASE)
		use_card_pattern = re.compile("(Se|på|Bruk|det|dette|kortet|til|å|svare)", re.IGNORECASE)
		use_card_again_pattern = re.compile("(Bruk|fortsatt|kortet)", re.IGNORECASE)
		showc_pattern = re.compile("(FORTSATT|KORT)", re.IGNORECASE)
		continue_using_card_pattern = re.compile("(fortsatt|kort|igjen|titt|på|dette|kortet)", re.IGNORECASE)
		choose_answer_in_card_pattern = re.compile("(Velg|et|svaralternativ|ett|svaralternativene|alternativene|fra|dette|kortet)", re.IGNORECASE)
		new_card_pattern = re.compile("(Her|et|nytt|kort)", re.IGNORECASE)
		other_variations_card_pattern = re.compile("(Svar|med|utgangspunkt|dette|kortet)", re.IGNORECASE)
		read_pattern = re.compile("(les|høyt|opp|alternativene)", re.IGNORECASE)
		prompt_pattern = re.compile("", re.IGNORECASE)
		note_for_interviewer_pattern = re.compile("(notat til intervjueren)", re.IGNORECASE)
		code_all_pattern = re.compile("(kod|alt|som|passer)", re.IGNORECASE)
		ask_all_pattern = re.compile("(stilles|til|alle)", re.IGNORECASE)
		tick_box_or_choose_one_pattern = re.compile("(Vennligst|sett|ett|kryss)", re.IGNORECASE)
		choose_multiple_pattern = re.compile("(LES|HØYT|OG|MARKER|ETT|ALTERNATIV|HVER|LINJE)", re.IGNORECASE)
		choose_closest_to_opinion_pattern = re.compile("(Kryss|av|ruta|som|stemmer|best|med|din|mening)", re.IGNORECASE)
		list_and_code_pattern = re.compile("(LES|HØYT|HVER|PÅSTAND|KOD|BOKSEN)", re.IGNORECASE)
		list_and_code_organization_pattern =  re.compile("(Les|opp|ulike|institusjonene)", re.IGNORECASE)
		insist_pattern =  re.compile("(insistere)", re.IGNORECASE)
		suggest_answer_cattegories_pattern = re.compile("(Bruk|kategoriene|på|kortet)", re.IGNORECASE)
		note_with_details_pattern = re.compile("", re.IGNORECASE)
		only_one_answer_possible_pattern  = re.compile("", re.IGNORECASE)
		
		use_card = ['Se', 'på','Bruk','det','dette','kortet','til','å','svare']
		use_card_again = ['Bruk','fortsatt','kortet']
		continue_using_card = ['fortsatt','kort','igjen','titt','på','dette','kortet']
		show_card = ['FORTSATT','kort']
		choose_answer_in_card = ['Velg','et','svaralternativ','ett','alternativene','svaralternativene','fra','dette','kortet']
		new_card = ['Her','et','nytt','kort']
		other_card = ['svar', 'med', 'utgangspunkt', 'dette', 'kortet']	
		read = ['les', 'høyt', 'opp', 'alternativene']
		prompt = ['']
		note_for_interviewer = ['']
		code_all = ['kod', 'alt', 'som', 'passer']
		ask_all = ['stilles', 'til', 'alle']
		tick_box = ['Vennligst','sett','ett','kryss']
		choose_multiple = ['LES','HØYT','OG','MARKER','ETT','ALTERNATIV','HVER','LINJE']	
		choose_closest = ['Kryss','av','ruta','som','stemmer','best','med','din','mening']
		list_and_code = ['LES','HØYT','HVER','PÅSTAND','KOD','BOKSEN']
		list_and_code_organization = ['Les','opp','ulike','institusjonene']
		insist = ['insistere']
		suggest_answer_cattegories = ['Bruk','kategoriene','på','kortet']
		note_with_details = ['']
		only_one_answer_possible = ['']


		if 'R02' in filename:
			choose_closest_to_opinion_pattern = re.compile("(Vennligst|sett|kryss|ruten|nærmest|din|mening)", re.IGNORECASE)
			showc_pattern = re.compile("(vis|FORSATT|KORT)", re.IGNORECASE)

			show_card = ['Vis','FORSATT','kort']
			choose_closest = ['Kryss','Vennligst','ruten','Vennligst','nærmest','med','din','mening']


	if 'POR' in language_country:
		programmer_pattern = re.compile("(Programador)", re.IGNORECASE)
		full_form_interviewer_pattern = re.compile("(Entrevistador:)", re.IGNORECASE)
		use_card_pattern = re.compile("(utilize|este|cartão|para|responder)", re.IGNORECASE)
		use_card_again_pattern = re.compile("(mostrar|utilize|este|mesmo|cartão|novamente)", re.IGNORECASE)
		continue_using_card_pattern = re.compile("(continue|mostrando|utilizando|este|cartão)", re.IGNORECASE)
		showc_pattern = re.compile("(mostrar|cartão)", re.IGNORECASE)
		choose_answer_in_card_pattern = re.compile("(escolha|respostas|deste|cartão)", re.IGNORECASE)
		new_card_pattern = re.compile("(dummy value)", re.IGNORECASE)
		other_variations_card_pattern = re.compile("(mostrar|manter|novamente|cartão)", re.IGNORECASE)
		read_pattern = re.compile("(ler|pausadamente|voz|alta)", re.IGNORECASE)
		prompt_pattern = re.compile("(pedir|ao|entrevistado|escrever)", re.IGNORECASE)
		note_for_interviewer_pattern = re.compile("(nota para entrevistador)", re.IGNORECASE)
		code_all_pattern = re.compile("(entrevistador|codifica)", re.IGNORECASE)
		ask_all_pattern = re.compile("(perguntar|a|todos)", re.IGNORECASE)
		tick_box_or_choose_one_pattern = re.compile("(dummy value)", re.IGNORECASE)
		choose_multiple_pattern = re.compile("(dummy value)", re.IGNORECASE)
		choose_closest_to_opinion_pattern = re.compile("(Por|favor|escolha|afirmação|que|mais|se|aproxima|da sua opinião)", re.IGNORECASE)
		list_and_code_pattern = re.compile("(dummy value)", re.IGNORECASE)
		list_and_code_organization_pattern =  re.compile("(LER|UMA|ORGANIZAÇãO|DE|CADA|VEZ|ASSINALAR|RESPOSTA)", re.IGNORECASE)
		insist_pattern =  re.compile("(insistir)", re.IGNORECASE)
		suggest_answer_cattegories_pattern = re.compile("(sugerir|categorias)", re.IGNORECASE)
		note_with_details_pattern = re.compile("(DESCREVER DETALHADAMENTE)", re.IGNORECASE)
		only_one_answer_possible_pattern  = re.compile("(CODIFICAR SÓ UMA RESPOSTA)", re.IGNORECASE)

		use_card = ['utilize','este','cartão','para','responder']
		use_card_again = ['mostrar','utilize','este','mesmo','cartão','novamente']
		continue_using_card = ['continue','mostrando','utilizando','este','cartão']
		show_card = ['mostrar','cartão']
		choose_answer_in_card = ['escolha','respostas','deste','cartão']
		new_card = ['(dummy value)']
		other_card = ['mostrar', 'manter', 'novamente', 'cartão']
		read = ['ler', 'pausadamente', 'voz', 'alta']
		prompt = ['pedir', 'ao', 'entrevistado', 'escrever']
		note_for_interviewer = ['nota',  'para', 'entrevistador']
		code_all = ['entrevistador', 'codifica']
		ask_all = ['perguntar', 'a','todos']
		tick_box = ['(dummy value)']
		choose_multiple = ['(dummy value)']
		choose_closest = ['Por','favor','escolha','afirmação','que','mais','se','aproxima','da','sua','opinião']
		list_and_code = ['(dummy value)']
		list_and_code_organization = ['LER','UMA','ORGANIZAÇãO','DE','CADA','VEZ','ASSINALAR','RESPOSTA']
		insist = ['insistir']
		suggest_answer_cattegories = ['sugerir','categorias']
		note_with_details = ['DESCREVER', 'DETALHADAMENTE']
		only_one_answer_possible = ['CODIFICAR', 'SÓ', 'UMA', 'RESPOSTA']

		if 'R04' in filename or 'R05' in filename:
			other_variations_card_pattern = re.compile("(Responda|utilizando|mesma|mesmo|escala|cartão)", re.IGNORECASE)
			choose_answer_in_card_pattern = re.compile("(escolha|sua|resposta|a|partir|do|seguinte|cartão)", re.IGNORECASE)

			other_card = ['Responda','utilizando','mesma','escala', 'mesmo', 'cartão']
			choose_answer_in_card = ['escolha','sua','resposta','a','partir','do','seguinte','cartão']
		if 'R06' in filename:
			choose_answer_in_card_pattern = re.compile("(escolha|sua|resposta|a|partir|do|seguinte|cartão)", re.IGNORECASE)
			showc_pattern = re.compile("(MOSTRAR|MANTER|CARTÃO)", re.IGNORECASE)
			other_variations_card_pattern = re.compile("(use|por favor|este|cartão)", re.IGNORECASE)

			show_card = ['MOSTRAR','MANTER','CARTÃO']
			other_card = ['use','por', 'favor','este', 'cartão']
			choose_answer_in_card = ['escolha','sua','resposta','a','partir','do','seguinte','cartão']


	if 'SPA' in language_country:
		programmer_pattern = re.compile("(Programador:)", re.IGNORECASE)
		full_form_interviewer_pattern = re.compile("(Entrevistador:)", re.IGNORECASE)
		use_card_pattern = re.compile("(Por favor|utilice|esta|tarjeta|para|responder)", re.IGNORECASE)
		use_card_again_pattern = re.compile("(Por favor|utilice|otra|vez|misma|esta|tarjeta|para|responder)", re.IGNORECASE)
		continue_using_card_pattern = re.compile("(Por favor|siga|utilizando|misma|esta|tarjeta|para|responder)", re.IGNORECASE)
		showc_pattern = re.compile("(mostrar|tarjeta)", re.IGNORECASE)
		choose_answer_in_card_pattern = re.compile('(Por favor|escoja|elija|su|respuesta|TARJETA)')
		other_variations_card_pattern = re.compile("(SEGUIR|CON|LA|TARJETA)", re.IGNORECASE)
		read_pattern = re.compile("(leer|alto)", re.IGNORECASE)
		prompt_pattern = re.compile("(dummy value)", re.IGNORECASE)
		note_for_interviewer_pattern = re.compile("(nota para el entrevistador codificar)", re.IGNORECASE)
		code_all_pattern = re.compile("(dummy value)", re.IGNORECASE)
		ask_all_pattern = re.compile("(preguntar|todos)", re.IGNORECASE)
		tick_box_or_choose_one_pattern = re.compile("(Por favor|marque|una|casilla)", re.IGNORECASE)
		choose_multiple_pattern = re.compile("(dummy value)", re.IGNORECASE)
		choose_closest_to_opinion_pattern = re.compile("(Por favor|marque|casilla|que|mejor|represente|su|opinión)", re.IGNORECASE)
		list_and_code_pattern = re.compile("(LEER|UNA|A|UNA|ANOTAR|CÓDIGO|TABLA)", re.IGNORECASE)
		list_and_code_organization_pattern =  re.compile("(LEER|CADA|ORGANIZACIÓN|ALTO|DE|FORMA|PAUSADA)", re.IGNORECASE)
		insist_pattern =  re.compile("(INSISTIR)", re.IGNORECASE)
		suggest_answer_cattegories_pattern = re.compile("(sugerir|categorías|respuesta)", re.IGNORECASE)
		note_with_details_pattern = re.compile("(dummy value)", re.IGNORECASE)
		new_card_pattern = re.compile("(dummy value)", re.IGNORECASE)
		only_one_answer_possible_pattern = re.compile("(dummy value)", re.IGNORECASE)

		only_one_answer_possible = ['(dummy value)']
		choose_multiple = ['(dummy value)']
		new_card = ['(dummy value)']
		prompt = ['(dummy value)']
		use_card = ['Por', 'favor','utilice','esta','tarjeta','para','responder']
		use_card_again = ['Por', 'favor', 'utilice','otra','vez','misma','esta','tarjeta','para','responder']
		continue_using_card = ['Por', 'favor', 'siga','utilizando','misma','esta','tarjeta','para','responder']
		show_card = ['mostrar', 'tarjeta']
		choose_answer_in_card = ['Por', 'favor','escoja','elija','su','respuesta','TARJETA']
		other_card = ['SEGUIR','CON','LA','TARJETA']
		read = ['leer', 'alto']
		note_for_interviewer  = ['nota','para', 'entrevistador', 'codificar']
		code_all = ['']
		ask_all = ['preguntar', 'todos']
		tick_box = ['Por', 'favor', 'marque','una','casilla']
		choose_closest = ['Por', 'favor', 'marque','casilla', 'que','mejor','represente','su','opinión']
		list_and_code = ['LEER','UNA','A','UNA','ANOTAR','CÓDIGO','TABLA']
		list_and_code_organization = ['LEER','CADA','ORGANIZACIÓN','ALTO','DE','FORMA','PAUSADA']
		insist = ['INSISTIR']
		suggest_answer_cattegories = ['sugerir', 'categorías', 'respuesta']
		note_with_details = ['']
		
		

		if 'R01' in filename:
			read_pattern = re.compile("(LEER|EN|ALTO)", re.IGNORECASE)
			read = ['LEER','EN','ALTO']

		elif 'R05' in filename or 'R06' in filename:
			use_card_pattern = re.compile("(Por favor|use|utilice|esta|tarjeta)", re.IGNORECASE)
			use_card_again_pattern = re.compile("(Por favor|use|otra|vez|misma|esta|tarjeta|para|responder)", re.IGNORECASE)
			continue_using_card_pattern = re.compile("(Por favor|siga|usando|misma|esta|tarjeta|para|responder)", re.IGNORECASE)
			
			use_card = ['Por', 'favor','use', 'utilice', 'esta','tarjeta']
			use_card_again = ['Por', 'favor', 'use','otra','vez','misma','esta','tarjeta','para','responder']
			continue_using_card = ['Por', 'favor', 'siga','usando','misma','esta','tarjeta','para','responder']

	if 'RUS' in language_country:
		programmer_pattern = re.compile("(программист)", re.IGNORECASE)
		full_form_interviewer_pattern = re.compile("(ИНТЕРВЬЮЕР:)", re.IGNORECASE)
		use_card_pattern = re.compile("(Для ответа|пожалуйста|используйте|эту|карточку)", re.IGNORECASE)
		use_card_again_pattern = re.compile("(ПОПРОСИТЕ|РЕСПОНДЕНТА|ОТКРЫТЬ|СНОВА|ВОСПОЛЬЗОВАТЬСЯ|КАРТОЧКУ)", re.IGNORECASE)
		continue_using_card_pattern = re.compile("(Для|ответа|снова|воспользуйтесь|этой|карточкой)", re.IGNORECASE)
		showc_pattern = re.compile("(КАРТОЧКА)", re.IGNORECASE)
		choose_answer_in_card_pattern = re.compile("(Выберите|ответ|этой|карточки)", re.IGNORECASE)
		new_card_pattern = re.compile("(Теперь|используйте|эту|карточку)", re.IGNORECASE)
		other_variations_card_pattern = re.compile("(ОТВЕЧАЮТ ВСЕ РЕСПОНДЕНТЫ)", re.IGNORECASE)
		read_pattern = re.compile("(ПРОЧИТАТЬ ВСЛУХ)", re.IGNORECASE)
		prompt_pattern = re.compile("(ИНТЕРВЬЮЕР|ОТМЕЧАЕТ|КОД)", re.IGNORECASE)
		note_for_interviewer_pattern = re.compile("(ДЛЯ ИНТЕРВЬЮЕРА)", re.IGNORECASE)
		code_all_pattern = re.compile("(ОТМЕТЬТЕ ВСЕ ПОДХОДЯЩИЕ ОТВЕТЫ)", re.IGNORECASE)
		ask_all_pattern = re.compile("(СПРАШИВАТЬ|ВСЕХ)", re.IGNORECASE)
		tick_box_or_choose_one_pattern = re.compile("(Отметьте|пожалуйста|одну|клетку)", re.IGNORECASE)
		choose_multiple_pattern = re.compile("(МОЖНО|ОТМЕТИТЬ|БОЛЬШЕ|ЧЕМ|ОДИН|ОТВЕТ)", re.IGNORECASE)
		choose_closest_to_opinion_pattern = re.compile("(Заполните|пожалуйста|только|одну|ячейку)", re.IGNORECASE)
		list_and_code_pattern = re.compile("(ПРОЧИТАЙТЕ|КАЖДОЕ|УТВЕРЖДЕНИЕ|ОТМЕТЬТЕ|ТАБЛИЦЕ)", re.IGNORECASE)
		list_and_code_organization_pattern =  re.compile("(ОТМЕТЬТЕ|ВСЕ|ПОДХОДЯЩИЕ|ОТВЕТЫ|ДЛЯ|КАЖДОЙ|ОРГАНИЗАЦИИ)", re.IGNORECASE)
		insist_pattern =  re.compile("(СПРОСИТЕ)", re.IGNORECASE)
		suggest_answer_cattegories_pattern = re.compile("()", re.IGNORECASE)
		only_one_answer_possible_pattern = re.compile("(ОТМЕТЬТЕ|ТОЛЬКО|ОДИН|ВАРИАНТ)", re.IGNORECASE)
		#read in each line 
		note_with_details_pattern = re.compile("(ЗАЧИТЫВАЙТЕ|ПО|КАЖДОЙ|СТРОКЕ)", re.IGNORECASE)
	
		use_card = ['Для', 'ответа','пожалуйста','используйте','эту','карточку']
		use_card_again = ['ПОПРОСИТЕ','РЕСПОНДЕНТА','ОТКРЫТЬ','СНОВА','ВОСПОЛЬЗОВАТЬСЯ','КАРТОЧКУ']
		continue_using_card = ['Для','ответа','снова','воспользуйтесь','этой','карточкой']
		show_card = ['КАРТОЧКА']
		choose_answer_in_card = ['Выберите','ответ','этой','карточки']
		new_card = ['Теперь','используйте','эту','карточку']
		other_card = ['ОТВЕЧАЮТ', 'ВСЕ', 'РЕСПОНДЕНТЫ']
		read = ['ПРОЧИТАТЬ', 'ВСЛУХ']
		prompt = ['ИНТЕРВЬЮЕР', 'ОТМЕЧАЕТ', 'КОД']
		note_for_interviewer = ['ДЛЯ ИНТЕРВЬЮЕРА']
		code_all = ['ОТМЕТЬТЕ', 'ВСЕ', 'ПОДХОДЯЩИЕ', 'ОТВЕТЫ']
		ask_all = ['СПРАШИВАТЬ', 'ВСЕХ']
		tick_box = ['Отметьте', 'пожалуйста', 'одну', 'клетку']
		choose_multiple = ['МОЖНО','ОТМЕТИТЬ','БОЛЬШЕ','ЧЕМ','ОДИН','ОТВЕТ']
		choose_closest = ['Заполните',  'пожалуйста','только','одну','ячейку']
		list_and_code = ['ПРОЧИТАЙТЕ','КАЖДОЕ','УТВЕРЖДЕНИЕ','ОТМЕТЬТЕ','ТАБЛИЦЕ']
		list_and_code_organization = ['ОТМЕТЬТЕ','ВСЕ','ПОДХОДЯЩИЕ','ОТВЕТЫ','ДЛЯ','КАЖДОЙ','ОРГАНИЗАЦИИ']
		insist = ['СПРОСИТЕ']
		suggest_answer_cattegories = ['']
		note_with_details = ['ЗАЧИТЫВАЙТЕ','ПО','КАЖДОЙ','СТРОКЕ']
		only_one_answer_possible = ['ОТМЕТЬТЕ','ТОЛЬКО','ОДИН','ВАРИАНТ']

		if '_EE' in filename:
			if 'R04' in filename:
				use_card_pattern = re.compile("(Для ответа|пожалуйста|используйте|эту|карточку)", re.IGNORECASE)
				showc_pattern = re.compile("(КАРТА|ПРОДОЛЖАЕТСЯ)", re.IGNORECASE)
				read_pattern = re.compile("(ЗАЧИТАТЬ)", re.IGNORECASE)
				list_and_code_pattern = re.compile("(ЗАЧИТАТЬ|КАЖДОЕ|УТВЕРЖДЕНИЕ|ОТМЕТИТЬ|ОТВЕТ|ПО|ШКАЛЕ)", re.IGNORECASE)
				ask_all_pattern = re.compile("(СПРОСИТЬ|ВСЕХ)", re.IGNORECASE)
				choose_answer_in_card_pattern = re.compile("(Выберите|свой|ответ|из|карты)", re.IGNORECASE)

				use_card = ['Для',  'ответа', ',', 'пожалуйста', 'используйте', 'эту', 'карточку']
				show_card = ['КАРТА', 'ПРОДОЛЖАЕТСЯ']
				read = ['ЗАЧИТАТЬ']
				list_and_code = ['ЗАЧИТАТЬ','КАЖДОЕ','УТВЕРЖДЕНИЕ','ОТМЕТИТЬ','ОТВЕТ','ПО','ШКАЛЕ']
				ask_all = ['СПРОСИТЬ', 'ВСЕХ']
				choose_answer_in_card = ['Выберите','свой','ответ','из','карты']
			
			if 'R05' in filename or 'R06' in filename:
				use_card_pattern = re.compile("(Для ответа|пожалуйста|используйте|эту|карточку)", re.IGNORECASE)
				read_pattern = re.compile("(ЗАЧИТАЙТЕ)", re.IGNORECASE)
				list_and_code_pattern = re.compile("(ЗАЧИТАТЬ|КАЖДОЕ|УТВЕРЖДЕНИЕ|ОТМЕТИТЬ|ОТВЕТ|ПО|ШКАЛЕ)", re.IGNORECASE)
				ask_all_pattern = re.compile("(СПРОСИТЕ|У|ВСЕХ)", re.IGNORECASE)
				choose_answer_in_card_pattern = re.compile("(Выберите|свой|ответ|на|карточке)", re.IGNORECASE)

				use_card = ['Для',  'ответа', 'пожалуйста', 'используйте', 'эту', 'карточку']
				read = ['ЗАЧИТАЙТЕ']
				list_and_code = ['ЗАЧИТАТЬ','КАЖДОЕ','УТВЕРЖДЕНИЕ','ОТМЕТИТЬ','ОТВЕТ','ПО','ШКАЛЕ']


				ask_all = ['СПРОСИТЕ','У','ВСЕХ']
				choose_answer_in_card = ['Выберите','свой','ответ','на','карточке']

			if 'R06' in filename:
				full_form_interviewer_pattern = re.compile("(ИНТЕРВЬЮЕР)", re.IGNORECASE)
				list_and_code_pattern = re.compile("(ЗАЧИТАЙТЕ|КАЖДОЕ|УТВЕРЖДЕНИЕ|ОТМЕТЬТЕ|ОТВЕТ|В|СТРОКЕ)", re.IGNORECASE)
				code_all_pattern = re.compile("(ОТМЕЧАТЬ|ВСЕ|КОТОРЫЕ|ПОДХОДЯТ)", re.IGNORECASE)
				other_variations_card_pattern = re.compile("(СНОВА|КАРТА)", re.IGNORECASE)
				use_card_again_pattern = re.compile("(Используйте|ту|же|самую|карту)", re.IGNORECASE)

				list_and_code = ['ЗАЧИТАЙТЕ','КАЖДОЕ','УТВЕРЖДЕНИЕ','ОТМЕТЬТЕ','ОТВЕТ','В','СТРОКЕ']
				code_all = ['ОТМЕЧАТЬ','ВСЕ','КОТОРЫЕ','ПОДХОДЯТ']
				other_card = [ 'СНОВА', 'КАРТА']
				use_card_again = ['Используйте','ту','же','самую','карту']

		if '_IL' in filename:
			programmer_pattern = re.compile("(РЕСПОНДЕНТ:)", re.IGNORECASE)
			note_for_interviewer_pattern = re.compile('(ДЛЯ ИНТЕРВЬЮЕРА)', re.IGNORECASE)
			tick_box_or_choose_one_pattern = re.compile("(Пожалуйста|отметьте|один|квадрат)", re.IGNORECASE)
			
			tick_box = ['Пожалуйста','отметьте','один','квадрат']
			
			if 'R04' in filename or 'R06' in filename:
				showc_pattern = re.compile("(ИСПОЛЬЗУЙТЕ|КАРТОЧКУ)", re.IGNORECASE)
				ask_all_pattern = re.compile("(ОТВЕЧАЮТ|ВСЕ|РЕСПОНДЕНТЫ)", re.IGNORECASE)
				
				ask_all = ['ОТВЕЧАЮТ','ВСЕ','РЕСПОНДЕНТЫ']
				show_card = ['ИСПОЛЬЗУЙТЕ', 'КАРТОЧКУ']
		
		if '_LV' in filename:
			if 'R03' in filename or 'R04' in filename:
				use_card_pattern = re.compile("(Используйте|пожалуйста|эту|карточку)", re.IGNORECASE)
				showc_pattern = re.compile("(КАРТОЧКА|Nr)", re.IGNORECASE)
				read_pattern = re.compile("(ЗАЧИТАЙТЕ)", re.IGNORECASE)
				ask_all_pattern = re.compile("(СПРАШИВАЙТЕ|ВСЕХ)", re.IGNORECASE)
				tick_box_or_choose_one_pattern = re.compile("(ОТМЕТЬТЕ|ТОЛЬКО|ОДИН|КОД)", re.IGNORECASE)

				tick_box = ['ОТМЕТЬТЕ','ТОЛЬКО','ОДИН','КОД']
				use_card = ['Используйте', ',','пожалуйста','эту','карточку']
				show_card = ['КАРТОЧКА', 'Nr']
				read = ['ЗАЧИТАЙТЕ']
				ask_all = ['СПРАШИВАЙТЕ', 'ВСЕХ']

		if '_LT' in filename:
			if 'R04' in filename or 'R05' in filename:
				other_variations_card_pattern = re.compile("(ПОДАЙТЕ|РЕСПОНДЕНТУ|КАРТОЧКУ)", re.IGNORECASE)
				showc_pattern = re.compile("(ТА|ЖЕ|карточка)", re.IGNORECASE)
				tick_box_or_choose_one_pattern = re.compile("(Отметьте|пожалуйста|одну|клетку)", re.IGNORECASE)
				ask_all_pattern = re.compile("(ЭТОТ|ВОПРОС|ЗАДАЙТЕ|ВСЕМ|РЕСПОНДЕНТАМ)", re.IGNORECASE)
			
				other_card = ['ПОДАЙТЕ', 'РЕСПОНДЕНТУ', 'КАРТОЧКУ']
				show_card = ['ТА', 'ЖЕ','карточка']
				tick_box = ['Отметьте','пожалуйста','одну', 'клетку']
				ask_all = ['ЭТОТ','ВОПРОС','ЗАДАЙТЕ','ВСЕМ','РЕСПОНДЕНТАМ']
			
		if '_RU' in filename:
			if 'R03' in filename:
				read_pattern = re.compile("(ЗАЧИТАЙТЕ)", re.IGNORECASE)
				read = ['ЗАЧИТАЙТЕ']

			if 'R04' in filename:
				showc_pattern = re.compile("(ПОПРОСИТЕ|РЕСПОНДЕНТА|ОТКРЫТЬ|КАРТОЧКУ|СНОВА|ВОСПОЛЬЗОВАТЬСЯ|КАРТОЧКОЙ)", re.IGNORECASE)
				ask_all_pattern = re.compile("(СПРОСИТЕ|ВСЕХ)", re.IGNORECASE)
				choose_answer_in_card_pattern = re.compile("Для ответа|используйте|пожалуйста|карточку")
				use_card_pattern = re.compile("(Для ответа|снова|воспользуйтесь|этой|той|же|карточкой)", re.IGNORECASE)

				show_card = ['ПОПРОСИТЕ','РЕСПОНДЕНТА','ОТКРЫТЬ','КАРТОЧКУ','СНОВА','ВОСПОЛЬЗОВАТЬСЯ','КАРТОЧКОЙ']
				use_card = ['Для', 'ответа','снова','воспользуйтесь','этой','той','же','карточкой']
				ask_all = ['СПРОСИТЕ', 'ВСЕХ']
				choose_answer_in_card = ['Для', 'ответа','используйте','пожалуйста','карточку']

			if 'R05' in filename or 'R06' in filename:
				showc_pattern = re.compile("(ПОПРОСИТЕ|РЕСПОНДЕНТА|ОТКРЫТЬ|КАРТОЧКУ|СНОВА|ВОСПОЛЬЗОВАТЬСЯ|КАРТОЧКОЙ)", re.IGNORECASE)
				ask_all_pattern = re.compile("(СПРОСИТЕ|ВСЕХ)", re.IGNORECASE)
				choose_answer_in_card_pattern = re.compile("(Выберите|ответ|из|предложенных|на|карточке)")
				list_and_code_pattern = re.compile("(ЗАЧИТЫВАЙТЕ|ВОПРОСЫ|ОТМЕЧАЙТЕ|ОТВЕТ|ПО|КАЖДОМ)", re.IGNORECASE)
				read_pattern = re.compile("(ЗАЧИТАЙТЕ)", re.IGNORECASE)

				show_card = ['ПОПРОСИТЕ','РЕСПОНДЕНТА','ОТКРЫТЬ','КАРТОЧКУ','СНОВА','ВОСПОЛЬЗОВАТЬСЯ','КАРТОЧКОЙ']
				ask_all = ['СПРОСИТЕ', 'ВСЕХ']
				choose_answer_in_card = ['Выберите','ответ','из','предложенных','на','карточке']
				list_and_code = ['ЗАЧИТЫВАЙТЕ','ВОПРОСЫ','ОТМЕЧАЙТЕ','ОТВЕТ','ПО','КАЖДОМ']
				read = ['ЗАЧИТАЙТЕ']

				if 'R06' in filename:
					tick_box_or_choose_one_pattern = re.compile("(ОТМЕТЬТЕ|ОДНО|ЧИСЛО)", re.IGNORECASE)
					read_pattern = re.compile("(ЗАЧИТАЙТЕ|ЗАЧИТАЙТ)", re.IGNORECASE)

					read = ['ЗАЧИТАЙТЕ','ЗАЧИТАЙТ']
					tick_box = ['ОТМЕТЬТЕ','ОДНО','ЧИСЛО']

					


		if '_UA' in filename:
			choose_answer_in_card_pattern = re.compile("(Пожалуйста|выберите|один|ответ|на|этой|карточке)", re.IGNORECASE)
			choose_answer_in_card = ['Пожалуйста','выберите','один','ответ','на','этой','карточке']
			if 'R04' in filename :
				use_card_pattern = re.compile("(Для ответа|пожалуйста|используйте|эту|карточку)", re.IGNORECASE)
				use_card = ['Для',  'ответа', 'пожалуйста', 'используйте', 'эту', 'карточку']
			if 'R05' in filename or 'R06' in filename:
				use_card_pattern = re.compile("(Для ответа|пожалуйста|используйте|эту|карточку)", re.IGNORECASE)
				read_pattern = re.compile("(ЗАЧИТАЙТЕ)", re.IGNORECASE)
				showc_pattern = re.compile("(КАРТОЧКА)", re.IGNORECASE)
				choose_answer_in_card_pattern = re.compile("(Ваш|ответ|из|этой|карточки)", re.IGNORECASE)
				list_and_code_pattern = re.compile("(ПРОЧИТАЙТЕ|КАЖДОЕ|УТВЕРЖДЕНИЕ|ОТМЕТЬТЕ|В|ТАБЛИЦЕ)", re.IGNORECASE)
					
				use_card = ['Для',  'ответа', 'пожалуйста', 'используйте', 'эту', 'карточку']
				read = ['ЗАЧИТАЙТЕ']
				show_card = ['КАРТОЧКА']
				choose_answer_in_card = ['Ваш','ответ','из','этой','карточки']
				list_and_code = ['ПРОЧИТАЙТЕ','КАЖДОЕ','УТВЕРЖДЕНИЕ','ОТМЕТЬТЕ','В','ТАБЛИЦЕ']

			
	
	text = text.translate(str.maketrans(' ', ' ', string.punctuation))
	split_text = text.split()

	if split_text == []:
		return is_instruction
	else:
		intersection_use_card = intersection(split_text, use_card, key=str.lower)
		intersection_use_card_again = intersection(split_text, use_card_again, key=str.lower)
		intersection_continue_using_card = intersection(split_text, continue_using_card, key=str.lower)
		intersection_show_card = intersection(split_text, show_card, key=str.lower)
		intersection_choose_answer_in_card = intersection(split_text, choose_answer_in_card, key=str.lower)
		intersection_new_card = intersection(split_text, new_card, key=str.lower)
		intersection_other_variations_card = intersection(split_text, other_card, key=str.lower)
		intersection_read = intersection(split_text, read, key=str.lower)
		intersection_prompt = intersection(split_text, prompt, key=str.lower)
		intersection_note_for_interviewer = intersection(split_text, note_for_interviewer, key=str.lower)
		intersection_code_all = intersection(split_text, code_all, key=str.lower)
		intersection_ask_all = intersection(split_text, ask_all, key=str.lower)
		intersection_tick_box = intersection(split_text, tick_box, key=str.lower)
		intersection_choose_multiple = intersection(split_text, choose_multiple, key=str.lower)
		intersection_choose_closest_to_opinion = intersection(split_text, choose_closest, key=str.lower)
		intersection_list_and_code = intersection(split_text, list_and_code, key=str.lower)
		intersection_list_and_code_organization = intersection(split_text, list_and_code_organization, key=str.lower)
		intersection_insist = intersection(split_text, insist, key=str.lower)
		intersection_suggest_answer_cattegories = intersection(split_text, suggest_answer_cattegories, key=str.lower)
		intersection_note_with_details = intersection(split_text, note_with_details, key=str.lower)
		intersection_only_one_answer_possible = intersection(split_text, only_one_answer_possible, key=str.lower)

		if check_if_sentence_is_uppercase(text) == True:
			is_instruction = True
			return is_instruction
		if full_form_interviewer_pattern.search(text):
			is_instruction = True
			return is_instruction
		if note_for_interviewer_pattern.search(text):
			is_instruction = True
			return is_instruction
		if programmer_pattern.search(text):
			is_instruction = True
			return is_instruction
		# if insist_pattern.search(text):
		# 	is_instruction = True
		# 	return is_instruction
		if use_card_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_use_card) >= 0.5:
				is_instruction = True
				return is_instruction
		if use_card_again_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_use_card_again) >= 0.5:
				is_instruction = True
				return is_instruction
		if continue_using_card_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_continue_using_card) >= 0.5:
				is_instruction = True
				return is_instruction
		if showc_pattern.search(text):
			if percentage_of_intersection(split_text, intersection_show_card)  >= 0.5:
				is_instruction = True
				return is_instruction
		if choose_answer_in_card_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_choose_answer_in_card)  >= 0.5:
				is_instruction = True
				return is_instruction
		if new_card_pattern.findall(text):
			print(split_text, intersection_new_card)
			if percentage_of_intersection(split_text, intersection_new_card)  >= 0.5:
				is_instruction = True
				return is_instruction
		if other_variations_card_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_other_variations_card) >= 0.5:
				is_instruction = True
				return is_instruction
		if read_pattern.search(text):
			if percentage_of_intersection(split_text, intersection_read)  >= 0.5:
				is_instruction = True
				return is_instruction
		if prompt_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_prompt)  >= 0.5:
				is_instruction = True
				return is_instruction
		if code_all_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_code_all)  >= 0.5:
				is_instruction = True
				return is_instruction
		if ask_all_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_ask_all)  >= 0.5:
				is_instruction = True
				return is_instruction
		if tick_box_or_choose_one_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_tick_box)  >= 0.5:
				is_instruction = True
				return is_instruction
		if choose_multiple_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_choose_multiple)  >= 0.5:
				is_instruction = True
				return is_instruction
		if choose_closest_to_opinion_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_choose_closest_to_opinion)  >= 0.5:
				is_instruction = True
				return is_instruction
		if list_and_code_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_list_and_code)  >= 0.5:
				is_instruction = True
				return is_instruction
		if list_and_code_organization_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_list_and_code_organization)  >= 0.5:
				is_instruction = True
				return is_instruction
		if insist_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_insist)  >= 0.5:
				is_instruction = True
				return is_instruction
		if suggest_answer_cattegories_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_suggest_answer_cattegories)  >= 0.5:
				is_instruction = True
				return is_instruction
		if note_with_details_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_note_with_details)  >= 0.5:
				is_instruction = True
				return is_instruction
		if only_one_answer_possible_pattern.findall(text):
			if percentage_of_intersection(split_text, intersection_only_one_answer_possible)  >= 0.5:
				is_instruction = True
				return is_instruction
		
	return is_instruction





def clean_text(text):
	if isinstance(text, str):
		text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)
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
		# text = re.sub('^[A-Z]\s', "",text)
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

def standartize_item_name(item_name):
	item_name = re.sub("\.", "", item_name)
	item_name = item_name.lower()
	item_name = re.sub("q", "Q", item_name)

	if '_'  in item_name:
		item_name = item_name.split('_')
		item_name = item_name[0]

	return item_name

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
	if '_FR' in filename:
		country = 'France'
	if '_GE' in filename:
		country = 'Georgia'
	if '_GB' in filename or 'SOURCE' in filename:
		country = 'Great Britain'
	if '_GR' in filename:
		country = 'Greece'
	if '_IE' in filename:
		country = 'Ireland'	
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
	if '_MT' in filename:
		country = 'Malta'
	if '_NO' in filename:
		country = 'Norway'
	if '_PT' in filename:
		country = 'Portugal'
	if '_RU' in filename:
		country = 'Russian Federation'
	if '_UA' in filename:
		country = 'Ukraine'


	return country


def determine_sentence_tokenizer(filename):
	if 'ENG_' in filename:
		sentence_splitter_suffix = 'english.pickle'
	if 'FRE_' in filename:
		sentence_splitter_suffix = 'french.pickle'
	if 'GER_' in filename:
		sentence_splitter_suffix = 'german.pickle'
	if 'CZE_' in filename:
		sentence_splitter_suffix = 'czech.pickle'
	if 'POR_' in filename:
		sentence_splitter_suffix = 'portuguese.pickle'
	if 'ITA_' in filename:
		sentence_splitter_suffix = 'italian.pickle'
	if 'RUS_' in filename:
		sentence_splitter_suffix = 'russian.pickle'
	if 'SPA_' in filename or 'CAT_' in filename:
		sentence_splitter_suffix = 'spanish.pickle'
	if 'DAN_' in filename:
		sentence_splitter_suffix = 'danish.pickle'
	if 'DUT_' in filename:
		sentence_splitter_suffix = 'dutch.pickle'
	if 'SLO_' in filename:
		sentence_splitter_suffix = 'slovene.pickle'
	if 'EST_' in filename:
		sentence_splitter_suffix = 'estonian.pickle'
	if 'FIN_' in filename:
		sentence_splitter_suffix = 'finnish.pickle'
	if 'GRE_' in filename:
		sentence_splitter_suffix = 'greek.pickle'
	if 'POL_' in filename:
		sentence_splitter_suffix = 'polish.pickle'
	if 'NOR_' in filename:
		sentence_splitter_suffix = 'norwegian.pickle'
	if 'SWE_' in filename:
		sentence_splitter_suffix = 'swedish.pickle'
	if 'TUR_' in filename:
		sentence_splitter_suffix = 'turkish.pickle'
	if 'HUN_' in filename:
		sentence_splitter_suffix = 'hungarian.pickle'

	return sentence_splitter_suffix