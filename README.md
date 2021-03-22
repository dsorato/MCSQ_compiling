# Multilingual Corpus of Survey Questionnaires (MCSQ) Compiling
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4572930.svg)](https://doi.org/10.5281/zenodo.4572930)
[![DOI](https://zenodo.org/badge/206563769.svg)](https://zenodo.org/badge/latestdoi/206563769)

The Multilingual Corpus of Survey Questionnaires (MCSQ) is a multilingual corpus of survey items from different studies. 
It comprises datasets from ESS<sup>[1](#ess)</sup> (rounds 1 to 9), EVS<sup>[2](#evs)</sup> (waves 3, 4 and 5) and SHARE<sup>[3](#share)</sup> (waves 7, 8 and COVID questionnaires) in the English source language and their translations into Catalan, Czech, French (France, Switzerland, Belgium and Luxembourg), German (Austria, Germany, Switzerland and Luxembourg), Norwegian, Portuguese (Portugal and Luxembourg), Spanish (Spain) and Russian (Azerbaijan, Belarus, Israel, Latvia, Lithuania, Russian Federation, Ukraine, Estonia, Moldavia and Georgia).

This repository contains several modules that were used in the compilation of MCSQ. 
In the preprocessing directory there are scripts to preprocess data
The scripts differ concerning the format of the input source file.

In the DB directory there are the files concerning the database structure. It is a PostgreSQL Entity-Relationship (ER) database implemented using SQLAlchemy and Python. 

Alignment folder has the script to align two given files regarding its metadata information.

The [MCSQ]: Multilingual Corpus of Survey Questionnaires is an open-access research resource. 
If you use part of the code, datasets, and/or findings to inspire your own scientific work, please cite the article:

Zavala-Rojas, D., Sorato, D., Hareide, L., & Hofland, K. (forthcoming 2021). [MCSQ] Multilingual Corpus of Survey Questionnaires. Meta: Journal Des Traducteurs.
@article{Zavala-Rojas,author = {Zavala-Rojas, Diana and Sorato, Danielly and Hareide, Lidun and Hofland, Knut},journal = {Meta: Journal des traducteurs},title = {{[MCSQ] Multilingual Corpus of Survey Questionnaires}}}


<a name="ess">1</a>: https://www.europeansocialsurvey.org/
<a name="evs">2</a>: https://europeanvaluesstudy.eu/
<a name="share">3</a>: http://www.share-project.org/home0.html


* Visit the MCSQ official website https://www.upf.edu/web/mcsq/
* MCSQ interface prototype http://easy.mcsq.upf.edu/
* For more implementation details, see code documentation in: https://mcsq-compiling.readthedocs.io/en/latest/