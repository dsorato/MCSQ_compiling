# Multilingual Corpus of Survey Questionnaires (MCSQ) Compiling

This repository contains several modules necessary to compile the Multilingual Corpus of Survey Questionnaires (MCSQ).

In the preprocessing directory there are the scripts to preprocess EVS and ESS data. The scripts differ concerning the format of the input source file. For EVS and and ESS XML inputs please use evs_xml_data_extraction.py and ess_xml_data_extraction.py respectively. 
txt_to_spreadsheet is a special module to transform ESS plain text files to spreadsheet. 
Many functions for preprocessing can be found in utils.py (some deprecated).

In the DB directory there are the files concerning the database structure.

Data inclusion scripts refer to inclusion of datasets in the MCSQ database. 
