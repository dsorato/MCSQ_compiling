# Multilingual Corpus of Survey Questionnaires (MCSQ) Compiling

The Multilingual Corpus of Survey Questionnaires (MCSQ) is a multilingual corpus of survey items from different studies. 
In its first version (Ada Lovelace), it comprises datasets from ESS<sup>[1](#ess)</sup> (rounds 1 to 6) and EVS<sup>[2](#evs)</sup> (rounds 3 and 4) in the English source language and their translations into Catalan, Czech, French (France, Switzerland, Belgium and Luxembourg), German (Austria, Germany, Switzerland and Luxembourg), Norwegian, Portuguese, Spanish and Russian (Israel, Latvia, Lithuania, Russian Confederation, Ukraine, Estonia).

The version 1.1 (Beatrice Worsley) released on 14/10/2020, SHARE COVID questionnaires <sup>[3](#sharecovid)</sup> were included for the following
languages: Czech (Czech Republic), English (Malta and source questionnaire), French (Belgium, Switzerland, Luxembourg, France), German (Austria, Switzerland, Luxembourg, Germany), Portuguese (Portugal), Spanish (Spain) and Russian (Estonia, Israel, Latvia). 

This repository contains several modules that were used in the compilation of MCSQ. 
In the preprocessing directory there are scripts to preprocess EVS and ESS data. 
The scripts differ concerning the format of the input source file. For EVS and and ESS XML inputs please use 'evs_xml_data_extraction.py' and 'ess_xml_data_extraction.py' respectively. For EVS spreadsheet inputs please use 'evs_data_extraction.py'.
txt_to_spreadsheet is a special module to transform ESS plain text files to spreadsheet. 
Many utility functions for the preprocessing step can be found in 'utils.py' (some deprecated).

In the DB directory there are the files concerning the database structure. It is a PostgreSQL Entity-Relationship (ER) database implemented using SQLAlchemy and Python. The script 'populate_tables.py' takes the preprocessed spreadsheets as inputs and populated the database tables. Data manipulation for the population of the  MCSQ ER model is done in 'ess_data_inclusion.py'.

Alignment folder has the script to align two given files regarding its metadata information.

<a name="ess">1</a>: https://www.europeansocialsurvey.org/
<a name="evs">2</a>: https://europeanvaluesstudy.eu/
<a name="sharecovid">3</a>: http://www.share-project.org/special-data-sets/share-covid-19-questionnaire.html


* Visit the MCSQ official website https://www.upf.edu/web/mcsq/
* MCSQ interface prototype http://easy.mcsq.upf.edu/
* For more implementation details, see code documentation in: https://mcsq-compiling.readthedocs.io/en/latest/