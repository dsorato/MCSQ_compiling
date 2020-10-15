class EVSModules2008():
	"""
	Class encapsulating variables that compose the following modules in EVS 2008:
	Perceptions of life, Politics and society, Environment, Family, Work, Religion and morale, 
	National Identity, Life Experiences, Socio demographics, Respondent Parents, Respondent Partner,
	Administrative.
	"""

	perceptions_of_life = ['V2','V3','V4','V5','V1','V6','V8','V9','V167','V168','V169','V170','V171','V172',
	'V173','V174','V175','V176','V177','V178','V179','V180','V181','V184','V185','V97','V98','V99',
	'V100','V7','V10','V11','V12','V13','V14','V15','V16','V17','V18','V19','V20','V21','V22','V23','V24','V25',
	'V28','V29','V30','V31','V32','V33','V34','V35','V36','V37','V38','V39','V40','V41','V42','V43','V46'
	,'V47','V49','V52','V53','V54','V55','V56','V57','V58','V59','V60','V48','V50','V51','V62','V64','V63','V66','V65']
	perceptions_of_life = [x.lower() for x in perceptions_of_life]

	politics_and_society = ['V201','V202','V203','V204','V186','V187','V188','V189','V190','V191','V192','V193',
	'V200','V198','V199','V194','V195','V196','V197','V205','V206','V207','V208','V209','V210','V211','V212','V213',
	'V222','V221','V219','V220','V217','V218','V214','V215','V216','V223','V224','V225','V226','V227','V228','V230',
	'V231','V232','V229','V266','V281','V282','V283','V284','V285','V286','V287','V288','V289','V290','V291','V292',
	'V293','V294','V263','V264','V264_LR','V265','V265_LR','V67','V68','V267','V202_4']
	politics_and_society = [x.lower() for x in politics_and_society]

	environment = ['v295', 'v296', 'v297', 'v298', 'v299', 'v300', 'v301']

	family = ['V148','V149','V152','V150','V151','V153','V154','V155','V156','V157','V158','V136','V137','V138','V139',
	'V140','V141','V142','V143','V144','V145','V146','V147','V159','V162','V164','V160','V161','V163','V165','V166']
	family = [x.lower() for x in family]

	work = ['V103','V102','V69','V71','V72','V73','V74','V76','V78','V79','V80','V81','V70','V75','V77','V82','V83',
	'V84','V85','V86','V89','V90','V91','V92','V93','V94','V95','V96','V101']
	work = [x.lower() for x in work]

	religion_and_morale = ['V104','V105','V106','V106_cs','V107','V108','V108_cs','V109','V110','V111','V112',
	'V113','V114','V115','V116','V117','V118','V119','V120','V121','V122','V123','V124','V125','V126','V127',
	'V128','V129','V130','V131','V132','V133','V134','V135','V233','V247','V234','V239','V240','V248','V241',
	'V242','V243','V244','V235','V236','V237','V238','V245','V246','V249','V250','V251','V252']
	religion_and_morale = [x.lower() for x in religion_and_morale]

	national_identity = ['V253','V254','V255','V256','V276','V277','V278','V279','V280','V268','V269',
	'V270','V271','V272','V273','V274','V275','V257','V258','V259','V260','V261','V262']
	national_identity = [x.lower() for x in national_identity]

	life_experiences = ['V329a','V329b','V330a','V330b','V331a','V331b','V332a','V332b','V333a','V333b',
	'V334a','V334b']
	life_experiences = [x.lower() for x in life_experiences]

	socio_demographics = ['V302','V303','V304','V305b','V306','V307b','V308','AGE','AGE_r','AGE_r2',
	'V316','V317','V318','V319','V313','V314','V315','V320','V321','V322','V323','V324a','V324b',
	'V325a','V325b','V326a','V326b','V327a','V327b','V328a','V328b','V335','V335_r','V336_4','V336',
	'V336_2','V336_3','v336_cs','V336_r','V337','V338','V341','V341a','V340','V339_2','V339_3',
	'V339ISCO','v339SIOPS','v339ISEI','v339egp','v339ESeC','V349','V351','v353WK','v353W_cs','v353MM',
	'v353M_cs','v353YR','v353Y_cs','V353M_ppp','V353_r','v371b_N1','v371b_N2','v371b_N3','v368b_CC',
	'v368b_N1','v368b_N2','V368b_N3','V370']
	socio_demographics = [x.lower() for x in socio_demographics]

	respondent_parents = ['V309','V310b','V311','V312b','V354','V355','v355_2','v355_3','v355_cs',
	'V355_4','V355_r','V356','V357_2','V357_3','V357ISCO','v357SIOPS','v357ISEI','v357ESeC','v357egp',
	'V358','V359','V359a','V360','V361','V362','V363','V364','V365','V366','V367']
	respondent_parents = [x.lower() for x in respondent_parents]

	respondent_partner = ['V342','V343b','V344','v344_2','v344_3','v344_cs','V344_4','V344_r','V345',
	'V345a','V346_2','V346_3','V346ISCO','v346SIOPS','v346ISEI','v346ESeC','v346egp','V347','V348',
	'V348a','V350','V352']
	respondent_partner = [x.lower() for x in respondent_partner]

	administrative = ['V374','V373a','V373b','V374a','V374b','V374c','V372','V375','V376','V377','V378']
	administrative = [x.lower() for x in administrative]

class EVSModules1999():
	"""
	Class encapsulating variables that compose the following modules in EVS 1999:
	Perceptions of life, Politics and society, Environment, Family, Work, Religion and morale, 
	National Identity, Life Experiences, Socio demographics, Administrative.
	"""
	perceptions_of_life = ['V2','V3','V4','V5','V1','V6','V11','V162','V163','V164','V165','V166','V167','V168',
	'V169','V170','V171','V172','V173','V174','V177','V178','V48','V49','V50','V51','V7','V12','V13','V14',
	'V15','V16','V17','V18','V19','V20','V21','V22','V23','V24','V25','V26','V27','V30','V31','V32','V33','V34',
	'V35','V36','V37','V38','V39','V40','V41','V42','V43','V44','V45','V52','V53','V55','V58','V59','V60','V61',
	'V62','V63','V64','V65','V59_TR','V54','V56','V57','O1','V66','V68','V67',
	'v10', 'v11_gb', 'v6a_gb', 'v6a_ua','v6b_ua', 'v6c_ua,' 'v65a_gb', 'v65a_pt', 'v178a_pt', 'v178a_at']
	perceptions_of_life = [x.lower() for x in perceptions_of_life]

	politics_and_society = ['V190','V191','O24','V192','V193','V194','V195','V196','V197','V198','V199','O25',
	'O17','V179','V180','V181','V182','V183','V184','V185','O23','O18','O19','V186','V187','V188','V189',
	'O20','O21','O22','V200','V201','V202','V203','V204','V205','V206','V207','V208','O27','V211','V212',
	'V209','O26','V210','V213','V214','V215','V216','V217','V218','V219','O31','O32','V221','V222','V223',
	'V220','V224','O28','O29','O30','V258','O47','V259','V260','V261','V262','O48','V263','V264','V265','V266',
	'V267','V268','V269','V270','V271','V272','V273','V274','V275','V276','V277','V278','V279','V280','V281',
	'V282','V283','V284','V285','V286','V287','V288','V289','V290','V256','V257','V69','V70','V191_4',
	'c1','c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c29', 'c30', 'c31', 'c32', 'c33', 'c34',
	'c35', 'v189a_gb', 'v189b_gb', 'v199a_gb', 'v199b_gb', 'v199c_gb', 'v212a_gb', 'v212b_gb', 'v183a_pt',
	'v183b_pt', 'v183c_pt', 'v183d_pt', 'v183e_pt', 'v190_gb', 'v191_gb', 'v212a_cz', 'o22_01', 
	'v212a_at', 'v278a_de', 'v279a_de', 'v290a_de', 'v290b_de', 'v290c_de', 'v290d_de', 'v184_2c',
	'v212a_ua', 'v212b_ua', 'v260_ua', 'v261_ua', 'v262_ua', 'o48_ua']
	politics_and_society = [x.lower() for x in politics_and_society]

	environment = ['v10', 'v8', 'v9']

	family = ['V148','V149','V152','V150','V151','V153','V133','V134','V135','V136','V137','V138','V139',
	'V140','V141','V142','V143','V144','V145','V146','V147','O16','V154','V157','V159','V155','V156','V158',
	'V160','V161',
	'v147a_gb', 'v154_5c', 'v155_5c', 'v156_5c', 'v157_5c', 'v158_5c', 'v159_5c', 'v160_5c', 'v161_5c',
	'v153a_at']
	family = [x.lower() for x in family]

	work = ['V99','V98','O5','V71','V73','V74','V76','V77','V78','V80','V82','V83','V84','V85','V72','V75',
	'V79','V81','O2','O3','V86','V87','V88','V89','O4','V90','V91','V92','V93','V94','V95','V96','V97',
	'v90a_gb', 'v85a_pt', 'o5_lu', 'v90_at', 'v91_at', 'v92_at', 'v93_at', 'v94_at', 'v95_at']
	work = [x.lower() for x in work]

	religion_and_morale = ['O6','V100','V101','V102','V103','V103r_gb','V104','V104r_gb','V105','V106','V107',
	'V108','V109','V110','V111','V112','V113','V114','V115','V116','V117','V118','V119','V120','V121','O8',
	'O7','V122','V123','V124','V125','V126','V126_SI','O9','V127','V128','O10','O11','V129','V130','V131',
	'V132','O12','O13','O14','O15','V225','O33','V226','V231','V232','O35','V233','V234','V235','V236',
	'V227','V228','V229','V230','V237','V238','V239','V240','V241','V242','O34','O36','O37','O38','V243',
	'V244','V245','V246','V247','V248','V249','V250','O39','O40','O41','O42','O43','O44',
	'v242a_gb', 'v243_lu', 'v244_lu', 'v245_lu', 'v246_lu', 'v247_lu', 'v248_lu','v249_lu','v250_lu', 'o39_lu',
	'o40_lu','o41_lu', 'o44a_de', 'v124_de', 'v102_by', 'v104_by', 'v102_ee', 'v104_ee', 'v102_ua', 'v104_ua']
	religion_and_morale = [x.lower() for x in religion_and_morale]

	national_identity = ['V251','V251_MT','V252','V252_MT','V253','V253_MT','V254','V255','O45','O46',
	'v254_nir']
	national_identity = [x.lower() for x in national_identity]

	socio_demographics = ['V291','V292','AGE','AGE_r','AGE_r2','V293','V294','V295','V296','V297','V298',
	'V299','V300','V301','V302','V303','V303_r','V304','V304_r','V305','V306','V307','V308','V308_r','V309',
	'V309_r','V310','V310_r','V310_r2','V311_2','V311_3','V311','V312','V314','V315','V316','V317_2',
	'V317_3','V317','V318','O49','V320','V320_CS','V320_ppp','V320_r','V323','V322', 'c36', 'c39',
	'v320_pt', 'v320_at', 'v292a_de', 'v292b_de', 'v292c_de', 'v292z_de', 'v302a_de', 'v304_de', 'v316a_de',
	'v320_de', 'v322a_ua']
	socio_demographics = [x.lower() for x in socio_demographics]

	administrative = ['O52_r','O50','O53','V324','V325']
	administrative = [x.lower() for x in administrative]


	





