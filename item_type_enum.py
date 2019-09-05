from enum import Enum 

class ItemType(Enum):
    question = 1
    question_instruction = 2
    question_text = 3
    question_coding_instruction = 4
    response = 5
    response_option = 6
    fill = 7
    translator_note = 8 
    header = 9
    iwer = 10
