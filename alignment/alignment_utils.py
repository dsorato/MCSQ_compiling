from countryspecificrequest import *
import nltk
from nltk.corpus import stopwords

def convert_iso_code(lang):
	if lang == 'FRE':
		return 'fr'
	if lang == 'GER':
		return 'de'
	if lang == 'CAT':
		return 'ca'
	if lang == 'CZE':
		return 'cz'
	if lang == 'NOR':
		return 'no'
	if lang == 'RUS':
		return 'ru'
	if lang == 'SPA':
		return 'es'
	if lang == 'POR':
		return 'pt'

def instantiate_country_specific_request_object(study):
	"""
	Instantiates the appropriate set of country-specific requests according to the study.
	Country-specific requests are deleted from alignment by design because the answer categories
	frequently change from country to country.

	Args:
		param1 study (string): study metadata, embedded in filenames.

	Returns:
		country_specific_requests (Python object). Instance of python object that encapsulates the item names of 
		the country specific questions.
	"""
	if 'ESS_R01' in study:
		country_specific_requests = ESSCountrySpecificR01()
	elif 'ESS_R02' in study:
		country_specific_requests = ESSCountrySpecificR02()
	elif 'ESS_R03' in study:
		country_specific_requests = ESSCountrySpecificR03()
	elif 'ESS_R04' in study:
		country_specific_requests = ESSCountrySpecificR04()
	elif 'ESS_R05' in study:
		country_specific_requests = ESSCountrySpecificR05()
	elif 'ESS_R06' in study:
		country_specific_requests = ESSCountrySpecificR06()
	elif 'ESS_R07' in study:
		country_specific_requests = ESSCountrySpecificR07()
	elif 'ESS_R08' in study:
		country_specific_requests = ESSCountrySpecificR08()
	elif 'ESS_R09' in study:
		country_specific_requests = ESSCountrySpecificR09()
	elif 'EVS_R03' in study:
		country_specific_requests = EVSCountrySpecificR03()
	elif 'EVS_R04' in study:
		country_specific_requests = EVSCountrySpecificR04()
	elif 'EVS_R05' in study:
		country_specific_requests = EVSCountrySpecificR05()

	return country_specific_requests

def instantiate_language_stopwords_set(language):
	"""
	Instantiates the appropriate list of language-specific stopwords.
	These lists were taken from https://github.com/stopwords-iso.

	Args:
		param1 study (string): study metadata, embedded in filenames.

	Returns:
		country_specific_requests (Python object). Instance of python object that encapsulates the item names of 
		the country specific questions.
	"""
	
	if 'SPA' in language:
		spanish_stopwords = ["actualmente","acuerdo","adelante","ademas","además","adrede","afirmó","agregó","ahi","ahora","ahí",
		"al","algo","alguna","algunas","alguno","algunos","algún","alli","allí","alrededor","ambos","ampleamos","antano","antaño",
		"ante","anterior","antes","apenas","aproximadamente","aquel","aquella","aquellas","aquello","aquellos","aqui","aquél","aquélla",
		"aquéllas","aquéllos","aquí","arriba","arribaabajo","aseguró","asi","así","atras","aun","aunque","ayer","añadió","aún","bajo",
		"bastante","bien","breve","buen","buena","buenas","bueno","buenos","cada","casi","cerca","cierta","ciertas","cierto","ciertos",
		"cinco","claro","comentó","como","con","conmigo","conocer","conseguimos","conseguir","considera","consideró","consigo","consigue",
		"consiguen","consigues","contigo","contra","cosas","creo","cual","cuales","cualquier","cuando","cuanta","cuantas","cuanto","cuantos",
		"cuatro","cuenta","cuál","cuáles","cuándo","cuánta","cuántas","cuánto","cuántos","cómo","da","dado","dan","dar","de","debajo","debe",
		"deben","debido","decir","dejó","del","delante","demasiado","demás","dentro","deprisa","desde","despacio","despues","después",
		"detras","detrás","dia","dias","dice","dicen","dicho","dieron","diferente","diferentes","dijeron","dijo","dio","donde","dos","durante",
		"día","días","dónde","ejemplo","el","ella","ellas","ello","ellos","embargo","empleais","emplean","emplear","empleas","empleo","en",
		"encima","encuentra","enfrente","enseguida","entonces","entre","era","erais","eramos","eran","eras","eres","es","esa","esas","ese",
		"eso","esos","esta","estaba","estabais","estaban","estabas","estad","estada","estadas","estado","estados","estais","estamos","estan",
		"estando","estar","estaremos","estará","estarán","estarás","estaré","estaréis","estaría","estaríais","estaríamos","estarían","estarías",
		"estas","este","estemos","esto","estos","estoy","estuve","estuviera","estuvierais","estuvieran","estuvieras","estuvieron","estuviese",
		"estuvieseis","estuviesen","estuvieses","estuvimos","estuviste","estuvisteis","estuviéramos","estuviésemos","estuvo","está","estábamos",
		"estáis","están","estás","esté","estéis","estén","estés","ex","excepto","existe","existen","explicó","expresó","fin","final","fue",
		"fuera","fuerais","fueran","fueras","fueron","fuese","fueseis","fuesen","fueses","fui","fuimos","fuiste","fuisteis","fuéramos",
		"fuésemos","general","gran","grandes","gueno","ha","haber","habia","habida","habidas","habido","habidos","habiendo","habla","hablan",
		"habremos","habrá","habrán","habrás","habré","habréis","habría","habríais","habríamos","habrían","habrías","habéis","había","habíais",
		"habíamos","habían","habías","hace","haceis","hacemos","hacen","hacer","hacerlo","haces","hacia","haciendo","hago","han","has","hasta",
		"hay","haya","hayamos","hayan","hayas","hayáis","he","hecho","hemos","hicieron","hizo","horas","hoy","hube","hubiera","hubierais",
		"hubieran","hubieras","hubieron","hubiese","hubieseis","hubiesen","hubieses","hubimos","hubiste","hubisteis","hubiéramos","hubiésemos",
		"hubo","igual","incluso","indicó","informo","informó","intenta","intentais","intentamos","intentan","intentar","intentas","intento","ir",
		"junto","lado","largo","las","le","lejos","les","llegó","lleva","llevar","lo","los","luego","lugar","mal","manera","manifestó","mas",
		"mayor","me","mediante","medio","mejor","mencionó","menos","menudo","mi","mia","mias","mientras","mio","mios","mis","misma","mismas",
		"mismo","mismos","modo","momento","mucha","muchas","mucho","muchos","muy","más","mí","mía","mías","mío","míos","nada","nadie",
		"ni","ninguna","ningunas","ninguno","ningunos","ningún","no","nos","nosotras","nosotros","nuestra","nuestras","nuestro","nuestros",
		"nueva","nuevas","nuevo","nuevos","nunca","ocho","os","otra","otras","otro","otros","pais","para","parece","parte","partir","pasada",
		"pasado","paìs","peor","pero","pesar","poca","pocas","poco","pocos","podeis","podemos","poder","podria","podriais","podriamos",
		"podrian","podrias","podrá","podrán","podría","podrían","poner","por","por qué","porque","posible","primer","primera","primero",
		"primeros","principalmente","pronto","propia","propias","propio","propios","proximo","próximo","próximos","pudo","pueda",
		"puede","pueden","puedo","pues","qeu","que","quedó","queremos","quien","quienes","quiere","quiza","quizas","quizá","quizás","quién",
		"quiénes","qué","raras","realizado","realizar","realizó","repente","respecto","sabe","sabeis","sabemos","saben","saber","sabes","sal",
		"salvo","se","sea","seamos","sean","seas","segun","segunda","segundo","según","seis","ser","sera","seremos","será","serán","serás",
		"seré","seréis","sería","seríais","seríamos","serían","serías","seáis","señaló","si","sido","siempre","siendo","siete","sigue",
		"siguiente","sin","sino","sobre","sois","sola","solamente","solas","solo","solos","somos","son","soy","soyos","su","supuesto",
		"sus","suya","suyas","suyo","suyos","sé","sí","sólo","tal","tambien","también","tampoco","tan","tanto","tarde","te","temprano",
		"tendremos","tendrá","tendrán","tendrás","tendré","tendréis","tendría","tendríais","tendríamos","tendrían","tendrías","tened",
		"teneis","tenemos","tener","tenga","tengamos","tengan","tengas","tengo","tengáis","tenida","tenidas","tenido","tenidos",
		"teniendo","tenéis","tenía","teníais","teníamos","tenían","tenías","tercera","ti","tiempo","tiene","tienen","tienes","toda",
		"todas","todavia","todavía","todo","todos","total","trabaja","trabajais","trabajamos","trabajan","trabajar","trabajas",
		"trabajo","tras","trata","través","tres","tu","tus","tuve","tuviera","tuvierais","tuvieran","tuvieras","tuvieron","tuviese",
		"tuvieseis","tuviesen","tuvieses","tuvimos","tuviste","tuvisteis","tuviéramos","tuviésemos","tuvo","tuya","tuyas","tuyo",
		"tuyos","tú","ultimo","un","una","unas","uno","unos","usa","usais","usamos","usan","usar","usas","uso","usted","ustedes",
		"va","vais","valor","vamos","van","varias","varios","vaya","veces","ver","verdad","verdadera","verdadero","vez","vosotras",
		"vosotros","voy","vuestra","vuestras","vuestro","vuestros","y","ya","yo","él","éramos","ésa","ésas","ése","ésos","ésta",
		"éstas","éste","éstos","última","últimas","último","últimos"]

		return spanish_stopwords
		
	elif 'ENG' in language:

		return stopwords.words('english')

	elif 'RUS' in language:
		russian_stopwords = ["c","а","алло","без","белый","близко","более","больше","большой","будем","будет",
		"будете","будешь","будто","буду","будут","будь","бы","бывает","бывь","был","была","были","было","быть","в","важная",
		"важное","важные","важный","вам","вами","вас","ваш","ваша","ваше","ваши","вверх","вдали","вдруг","ведь","везде","вернуться",
		"весь","вечер","взгляд","взять","вид","видел","видеть","вместе","вне","вниз","внизу","во","вода","война","вокруг",
		"вон","вообще","вопрос","восемнадцатый","восемнадцать","восемь","восьмой","вот","впрочем","времени","время","все",
		"все еще","всегда","всего","всем","всеми","всему","всех","всею","всю","всюду","вся","всё","второй","вы","выйти","г",
		"где","главный","глаз","говорил","говорит","говорить","год","года","году","голова","голос","город","да","давать","давно",
		"даже","далекий","далеко","дальше","даром","дать","два","двадцатый","двадцать","две","двенадцатый","двенадцать","дверь",
		"двух","девятнадцатый","девятнадцать","девятый","девять","действительно","дел","делал","делать","делаю","дело","день","деньги",
		"десятый","десять","для","до","довольно","долго","должен","должно","должный","дом","дорога","друг","другая","другие","других",
		"друго","другое","другой","думать","душа","е","его","ее","ей","ему","если","есть","еще","ещё","ею","её","ж","ждать","же","жена",
		"женщина","жизнь","жить","за","занят","занята","занято","заняты","затем","зато","зачем","здесь","земля","знать","значит","значить",
		"и","иди","идти","из","или","им","имеет","имел","именно","иметь","ими","имя","иногда","их","к","каждая","каждое","каждые","каждый",
		"кажется","казаться","как","какая","какой","кем","книга","когда","кого","ком","комната","кому","конец","конечно","которая","которого",
		"которой","которые","который","которых","кроме","кругом","кто","куда","лежать","лет","ли","лицо","лишь","лучше","любить","люди","м",
		"маленький","мало","мать","машина","между","меля","менее","меньше","меня","место","миллионов","мимо","минута","мир","мира","мне",
		"много","многочисленная","многочисленное","многочисленные","многочисленный","мной","мною","мог","могу","могут","мож","может","может быть",
		"можно","можхо","мои","мой","мор","москва","мочь","моя","моё","мы","на","наверху","над","надо","назад","наиболее","найти","наконец","нам",
		"нами","народ","нас","начала","начать","наш","наша","наше","наши","не","него","недавно","недалеко","нее","ней","некоторый","нельзя","нем","немного",
		"нему","непрерывно","нередко","несколько","нет","нею","неё","ни","нибудь","ниже","низко","никакой","никогда","никто","никуда","ним","ними",
		"них","ничего","ничто","но","новый","нога","ночь","ну","нужно","нужный","нх","о","об","оба","обычно","один","одиннадцатый","одиннадцать","однажды",
		"однако","одного","одной","оказаться","окно","около","он","она","они","оно","опять","особенно","остаться","от","ответить","отец","откуда","отовсюду",
		"отсюда","очень","первый","перед","писать","плечо","по","под","подойди","подумать","пожалуйста","позже","пойти","пока","пол","получить","помнить",
		"понимать","понять","пор","пора","после","последний","посмотреть","посреди","потом","потому","почему","почти","правда","прекрасно","при","про","просто",
		"против","процентов","путь","пятнадцатый","пятнадцать","пятый","пять","работа","работать","раз","разве","рано","раньше","ребенок","решить","россия",
		"рука","русский","ряд","рядом","с","с кем","сам","сама","сами","самим","самими","самих","само","самого","самой","самом","самому","саму","самый",
		"свет","свое","своего","своей","свои","своих","свой","свою","сделать","сеаой","себе","себя","сегодня","седьмой","сейчас","семнадцатый","семнадцать",
		"семь","сидеть","сила","сих","сказал","сказала","сказать","сколько","слишком","слово","случай","смотреть","сначала","снова","со","собой","собою",
		"советский","совсем","спасибо","спросить","сразу","стал","старый","стать","стол","сторона","стоять","страна","суть","считать",
		"т","та","так","такая","также","таки","такие","такое","такой","там","твои","твой","твоя","твоё","те","тебе","тебя",
		"тем","теми","теперь","тех","то","тобой","тобою","товарищ","тогда","того","тоже","только","том","тому","тот","тою","третий",
		"три","тринадцатый","тринадцать","ту","туда","тут","ты","тысяч","у","увидеть","уж","уже","улица","уметь","утро",
		"хороший","хорошо","хотел бы","хотеть","хоть","хотя","хочешь","час","часто","часть","чаще","чего","человек","чем",
		"чему","через","четвертый","четыре","четырнадцатый","четырнадцать","что","чтоб","чтобы","чуть","шестнадцатый","шестнадцать","шестой",
		"шесть","эта","эти","этим","этими","этих","это","этого","этой","этом","этому","этот","эту","я","являюсь"]

		return russian_stopwords
	elif 'FRE' in language:
		french_stopwords = ["abord","absolument","afin","ah","ai","aie","aient","aies","ailleurs","ainsi","ait","allaient","allo","allons",
		"allô","alors","anterieur","anterieure","anterieures","apres","après","as","assez","attendu","au","aucun","aucune","aucuns","aujourd",
		"aujourd'hui","aupres","auquel","aura","aurai","auraient","aurais","aurait","auras","aurez","auriez","aurions","aurons","auront","aussi",
		"autant","autre","autrefois","autrement","autres","autrui","aux","auxquelles","auxquels","avaient","avais","avait","avant","avec","avez",
		"aviez","avions","avoir","avons","ayant","ayez","ayons","bah","bas","basee","bat","beau","beaucoup","bien","bigre","bon","boum","bravo",
		"car","ce","ceci","cela","celle","celle-ci","celle-là","celles","celles-ci","celles-là","celui","celui-ci","celui-là","celà","cent",
		"cependant","certain","certaine","certaines","certains","certes","ces","cet","cette","ceux","ceux-ci","ceux-là","chacun","chacune","chaque",
		"cher","chers","chez","chiche","chut","chère","chères","ci","cinq","cinquantaine","cinquante","cinquantième","cinquième","clac","clic","combien",
		"comme","comment","comparable","comparables","compris","concernant","contre","couic","crac","da","dans","de","debout","dedans","dehors","deja",
		"delà","depuis","dernier","derniere","derriere","derrière","des","desormais","desquelles","desquels","dessous","dessus","deux","deuxième",
		"deuxièmement","devant","devers","devra","devrait","different","differentes","differents","différent","différente","différentes","différents",
		"dire","directe","directement","dit","dite","dits","divers","diverse","diverses","dix","dix-huit","dix-neuf","dix-sept","dixième","doit","doivent",
		"donc","dont","dos","douze","douzième","dring","droite","du","duquel","durant","dès","début","désormais","effet","egale","egalement","egales",
		"eh","elle","elle-même","elles","elles-mêmes","en","encore","enfin","entre","envers","environ","es","essai","est","et","etant","etc","etre",
		"eu","eue","eues","euh","eurent","eus","eusse","eussent","eusses","eussiez","eussions","eut","eux","eux-mêmes","exactement","excepté","extenso",
		"exterieur","eûmes","eût","eûtes","fais","faisaient","faisant","fait","faites","façon","feront","fi","flac","floc","fois","font","force","furent",
		"fus","fusse","fussent","fusses","fussiez","fussions","fut","fûmes","fût","fûtes","gens","ha","haut","hein","hem","hep","hi","ho","holà","hop",
		"hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","hé","hélas","ici","il","ils","importe","je","jusqu","jusque","juste",
		"la","laisser","laquelle","las","le","lequel","les","lesquelles","lesquels","leur","leurs","longtemps","lors","lorsque","lui","lui-meme",
		"lui-même","là","lès","ma","maint","maintenant","mais","malgre","malgré","maximale","me","meme","memes","merci","mes","mien","mienne","miennes",
		"miens","mille","mince","mine","minimale","moi","moi-meme","moi-même","moindres","moins","mon","mot","moyennant","multiple","multiples","même",
		"mêmes","na","naturel","naturelle","naturelles","ne","neanmoins","necessaire","necessairement","neuf","neuvième","ni","nombreuses",
		"nombreux","nommés","non","nos","notamment","notre","nous","nous-mêmes","nouveau","nouveaux","nul","néanmoins","nôtre","nôtres","oh",
		"ohé","ollé","olé","on","ont","onze","onzième","ore","ou","ouf","ouias","oust","ouste","outre","ouvert","ouverte","ouverts","où","paf",
		"pan","par","parce","parfois","parle","parlent","parler","parmi","parole","parseme","partant","particulier","particulière","particulièrement",
		"pas","passé","pendant","pense","permet","personne","personnes","peu","peut","peuvent","peux","pff","pfft","pfut","pif","pire","pièce","plein",
		"plouf","plupart","plus","plusieurs","plutôt","possessif","possessifs","possible","possibles","pouah","pour","pourquoi","pourrais","pourrait",
		"pouvait","prealable","precisement","premier","première","premièrement","pres","probable","probante","procedant","proche","près","psitt","pu",
		"puis","puisque","pur","pure","qu","quand","quant","quant-à-soi","quanta","quarante","quatorze","quatre","quatre-vingt","quatrième",
		"quatrièmement","que","quel","quelconque","quelle","quelles","quelqu'un","quelque","quelques","quels","qui","quiconque","quinze",
		"quoi","quoique","rare","rarement","rares","relative","relativement","remarquable","rend","rendre","restant","reste","restent",
		"restrictif","retour","revoici","revoilà","rien","sa","sacrebleu","sait","sans","sapristi","sauf","se","sein","seize","selon",
		"semblable","semblaient","semble","semblent","sent","sept","septième","sera","serai","seraient","serais","serait","seras",
		"serez","seriez","serions","serons","seront","ses","seul","seule","seulement","si","sien","sienne","siennes","siens","sinon",
		"six","sixième","soi","soi-même","soient","sois","soit","soixante","sommes","son","sont","sous","souvent","soyez","soyons","specifique","specifiques",
		"speculatif","stop","strictement","subtiles","suffisant","suffisante","suffit","suis","suit","suivant","suivante","suivantes","suivants","suivre",
		"sujet","superpose","sur","surtout","ta","tac","tandis","tant","tardive","te","tel","telle","tellement","telles","tels","tenant","tend","tenir",
		"tente","tes","tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous","tout","toute","toutefois",
		"toutes","treize","trente","tres","trois","troisième","troisièmement","trop","très","tsoin","tsouin","tu","té","un","une","unes",
		"uniformement","unique","uniques","uns","va","vais","valeur","vas","vers","via","vif","vifs","vingt","vivat","vive","vives","vlan",
		"voici","voie","voient","voilà","voire","vont","vos","votre","vous","vous-mêmes","vu","vé","vôtre","vôtres","zut","à","â","ça",
		"ès","étaient","étais","était","étant","état","étiez","étions","été","étée","étées","étés","êtes","être","ô"]

		return french_stopwords

	elif 'GER' in language:
		german_stopwords = ["ab","aber","ach","acht","achte","achten","achter","achtes","ag","alle","allein","allem","allen","aller",
		"allerdings","alles","allgemeinen","als","also","am","an","ander","andere","anderem","anderen","anderer","anderes","anderm",
		"andern","anderr","anders","au","auch","auf","aus","ausser","ausserdem","außer","außerdem","bald","bei","beide","beiden","beim",
		"beispiel","bekannt","bereits","besonders","besser","besten","bin","bis","bisher","bist","d.h","da","dabei","dadurch","dafür",
		"dagegen","daher","dahin","dahinter","damals","damit","danach","daneben","dank","dann","daran","darauf","daraus","darf","darfst",
		"darin","darum","darunter","darüber","das","dasein","daselbst","dass","dasselbe","davon","davor","dazu","dazwischen","daß","dein",
		"deine","deinem","deinen","deiner","deines","dem","dementsprechend","demgegenüber","demgemäss","demgemäß","demselben","demzufolge",
		"den","denen","denn","denselben","der","deren","derer","derjenige","derjenigen","dermassen","dermaßen","derselbe","derselben","des",
		"deshalb","desselben","dessen","deswegen","dich","die","diejenige","diejenigen","dies","diese","dieselbe","dieselben","diesem",
		"diesen","dieser","dieses","dir","doch","dort","drei","drin","dritte","dritten","dritter","drittes","du","durch","durchaus",
		"durfte","durften","dürfen","dürft","eben","ebenso","ehrlich","ei","eigen","eigene","eigenen","eigener","eigenes","ein","einander",
		"eine","einem","einen","einer","eines","einig","einige","einigem","einigen","einiger","einiges","einmal","eins","elf","en","ende",
		"endlich","entweder","er","ernst","erst","erste","ersten","erster","erstes","es","etwa","etwas","euch","euer","eure","eurem",
		"euren","eurer","eures","folgende","früher","fünf","fünfte","fünften","fünfter","fünftes","für","gab","ganz","ganze","ganzen",
		"ganzer","ganzes","gar","gedurft","gegen","gegenüber","gehabt","gehen","geht","gekannt","gekonnt","gemacht","gemocht","gemusst",
		"genug","gerade","gern","gesagt","geschweige","gewesen","gewollt","geworden","gibt","ging","gleich","gott","gross","grosse","grossen",
		"grosser","grosses","groß","große","großen","großer","großes","gut","gute","guter","gutes","hab","habe","haben","habt","hast",
		"hat","hatte","hatten","hattest","hattet","heisst","her","heute","hier","hin","hinter","hoch","hätte","hätten","i","ich","ihm",
		"ihn","ihnen","ihr","ihre","ihrem","ihren","ihrer","ihres","im","immer","in","indem","infolgedessen","ins","irgend","ist","ja",
		"jahr","jahre","jahren","je","jede","jedem","jeden","jeder","jedermann","jedermanns","jedes","jedoch","jemand","jemandem","jemanden",
		"jene","jenem","jenen","jener","jenes","jetzt","kam","kann","kannst","kaum","kein","keine","keinem","keinen","keiner","keines",
		"kleine","kleinen","kleiner","kleines","kommen","kommt","konnte","konnten","kurz","können","könnt","könnte","lang","lange",
		"leicht","leide","lieber","los","machen","macht","machte","mag","magst","mahn","mal","man","manche","manchem","manchen","mancher",
		"manches","mann","mehr","mein","meine","meinem","meinen","meiner","meines","mensch","menschen","mich","mir","mit","mittel",
		"mochte","mochten","morgen","muss","musst","musste","mussten","muß","mußt","möchte","mögen","möglich","mögt","müssen","müsst",
		"müßt","na","nach","nachdem","nahm","natürlich","neben","nein","neue","neuen","neun","neunte","neunten","neunter","neuntes",
		"nicht","nichts","nie","niemand","niemandem","niemanden","noch","nun","nur","ob","oben","oder","offen","oft","ohne","ordnung",
		"recht","rechte","rechten","rechter","rechtes","richtig","rund","sa","sache","sagt","sagte","sah","satt","schlecht","schluss",
		"schon","sechs","sechste","sechsten","sechster","sechstes","sehr","sei","seid","seien","sein","seine","seinem","seinen","seiner",
		"seines","seit","seitdem","selbst","sich","sie","sieben","siebente","siebenten","siebenter","siebentes","sind","so","solang",
		"solche","solchem","solchen","solcher","solches","soll","sollen","sollst","sollt","sollte","sollten","sondern","sonst","soweit",
		"sowie","später","startseite","statt","steht","suche","tag","tage","tagen","tat","teil","tel","tritt","trotzdem","tun","uhr","um",
		"und","uns","unse","unsem","unsen","unser","unsere","unserer","unses","unter","vergangenen","viel","viele","vielem","vielen",
		"vielleicht","vier","vierte","vierten","vierter","viertes","vom","von","vor","wahr","wann","war","waren","warst","wart","warum",
		"was","weg","wegen","weil","weit","weiter","weitere","weiteren","weiteres","welche","welchem","welchen","welcher","welches","wem",
		"wen","wenig","wenige","weniger","weniges","wenigstens","wenn","wer","werde","werden","werdet","weshalb","wessen","wie","wieder",
		"wieso","will","willst","wir","wird","wirklich","wirst","wissen","wo","woher","wohin","wohl","wollen","wollt","wollte","wollten",
		"worden","wurde","wurden","während","währenddem","währenddessen","wäre","würde","würden","z.b","zehn","zehnte","zehnten","zehnter",
		"zehntes","zeit","zu","zuerst","zugleich","zum","zunächst","zur","zurück","zusammen","zwanzig","zwar","zwei","zweite","zweiten",
		"zweiter","zweites","zwischen","zwölf","über","überhaupt","übrigens"]

		return german_stopwords

	elif language == 'NOR_NO':
		norwegian_stopwords = ["alle","andre","arbeid","at","av","bare","begge","ble","blei","bli","blir","blitt","bort","bra","bruke",
		"både","båe","da","de","deg","dei","deim","deira","deires","dem","den","denne","der","dere","deres","det","dette","di","din","disse",
		"ditt","du","dykk","dykkar","då","eg","ein","eit","eitt","eller","elles","en","ene","eneste","enhver","enn","er","et","ett","etter",
		"folk","for","fordi","forsûke","fra","få","før","fûr","fûrst","gjorde","gjûre","god","gå","ha","hadde","han","hans","har","hennar",
		"henne","hennes","her","hjå","ho","hoe","honom","hoss","hossen","hun","hva","hvem","hver","hvilke","hvilken","hvis","hvor","hvordan",
		"hvorfor","i","ikke","ikkje","ingen","ingi","inkje","inn","innen","inni","ja","jeg","kan","kom","korleis","korso","kun","kunne","kva",
		"kvar","kvarhelst","kven","kvi","kvifor","lage","lang","lik","like","makt","man","mange","me","med","medan","meg","meget","mellom",
		"men","mens","mer","mest","mi","min","mine","mitt","mot","mye","mykje","må","måte","navn","ned","nei","no","noe","noen","noka","noko",
		"nokon","nokor","nokre","ny","nå","når","og","også","om","opp","oss","over","part","punkt","på","rett","riktig","samme","sant","seg",
		"selv","si","sia","sidan","siden","sin","sine","sist","sitt","sjøl","skal","skulle","slik","slutt","so","som","somme","somt","start",
		"stille","så","sånn","tid","til","tilbake","tilstand","um","under","upp","ut","uten","var","vart","varte","ved","verdi","vere","verte",
		"vi","vil","ville","vite","vore","vors","vort","vår","være","vært","vöre","vört","å"]

		return norwegian_stopwords

	elif 'POR' in language:
		portuguese_stopwords = ["a","acerca","adeus","agora","ainda","alem","algmas","algo","algumas","alguns","ali",
		"além","ambas","ambos","ano","anos","antes","ao","aonde","aos","apenas","apoio","apontar","apos","após","aquela","aquelas",
		"aquele","aqueles","aqui","aquilo","as","assim","através","atrás","até","aí","baixo","bastante","bem","boa","boas","bom",
		"bons","breve","cada","caminho","catorze","cedo","cento","certamente","certeza","cima","cinco","coisa","com","como","comprido",
		"conhecido","conselho","contra","contudo","corrente","cuja","cujas","cujo","cujos","custa","cá","da","daquela","daquelas",
		"daquele","daqueles","dar","das","de","debaixo","dela","delas","dele","deles","demais","dentro","depois","desde","desligado",
		"dessa","dessas","desse","desses","desta","destas","deste","destes","deve","devem","deverá","dez","dezanove","dezasseis",
		"dezassete","dezoito","dia","diante","direita","dispoe","dispoem","diversa","diversas","diversos","diz","dizem","dizer",
		"do","dois","dos","doze","duas","durante","dá","dão","dúvida","e","ela","elas","ele","eles","em","embora","enquanto","entao",
		"entre","então","era","eram","essa","essas","esse","esses","esta","estado","estamos","estar","estará","estas","estava",
		"estavam","este","esteja","estejam","estejamos","estes","esteve","estive","estivemos","estiver","estivera","estiveram",
		"estiverem","estivermos","estivesse","estivessem","estiveste","estivestes","estivéramos","estivéssemos","estou","está",
		"estás","estávamos","estão","eu","exemplo","falta","fará","favor","faz","fazeis","fazem","fazemos","fazer","fazes","fazia",
		"faço","fez","fim","final","foi","fomos","for","fora","foram","forem","forma","formos","fosse","fossem","foste","fostes",
		"fui","fôramos","fôssemos","geral","grande","grandes","grupo","ha","haja","hajam","hajamos","havemos","havia","hei",
		"hoje","hora","horas","houve","houvemos","houver","houvera","houveram","houverei","houverem","houveremos","houveria","houveriam",
		"houvermos","houverá","houverão","houveríamos","houvesse","houvessem","houvéramos","houvéssemos","há","hão","iniciar","inicio",
		"ir","irá","isso","ista","iste","isto","já","lado","lhe","lhes","ligado","local","logo","longe","lugar","lá","maior","maioria",
		"maiorias","mais","mal","mas","me","mediante","meio","menor","menos","meses","mesma","mesmas","mesmo","mesmos","meu","meus",
		"mil","minha","minhas","momento","muito","muitos","máximo","mês","na","nada","nao","naquela","naquelas","naquele","naqueles",
		"nas","nem","nenhuma","nessa","nessas","nesse","nesses","nesta","nestas","neste","nestes","no","noite","nome","nos","nossa","nossas",
		"nosso","nossos","nova","novas","nove","novo","novos","num","numa","numas","nunca","nuns","não","nível","nós","número","o","obra",
		"obrigada","obrigado","oitava","oitavo","oito","onde","ontem","onze","os","ou","outra","outras","outro","outros","para","parece",
		"parte","partir","paucas","pegar","pela","pelas","pelo","pelos","perante","perto","pessoas","pode","podem","poder","poderá","podia",
		"pois","ponto","pontos","por","porque","porquê","portanto","posição","possivelmente","posso","possível","pouca","pouco","poucos",
		"povo","primeira","primeiras","primeiro","primeiros","promeiro","propios","proprio","própria","próprias","próprio","próprios",
		"próxima","próximas","próximo","próximos","puderam","pôde","põe","põem","quais","qual","qualquer","quando","quanto","quarta",
		"quarto","quatro","que","quem","quer","quereis","querem","queremas","queres","quero","questão","quieto","quinta","quinto",
		"quinze","quáis","quê","relação","sabe","sabem","saber","se","segunda","segundo","sei","seis","seja","sejam","sejamos",
		"sem","sempre","sendo","ser","serei","seremos","seria","seriam","será","serão","seríamos","sete","seu","seus","sexta","sexto",
		"sim","sistema","sob","sobre","sois","somente","somos","sou","sua","suas","são","sétima","sétimo","só","tal","talvez","tambem","também",
		"tanta","tantas","tanto","tarde","te","tem","temos","tempo","tendes","tenha","tenham","tenhamos","tenho","tens","tentar","tentaram",
		"tente","tentei","ter","terceira","terceiro","terei","teremos","teria","teriam","terá","terão","teríamos","teu","teus",
		"teve","tinha","tinham","tipo","tive","tivemos","tiver","tivera","tiveram","tiverem","tivermos","tivesse","tivessem",
		"tiveste","tivestes","tivéramos","tivéssemos","toda","todas","todo","todos","trabalhar","trabalho","treze","três","tu",
		"tua","tuas","tudo","tão","tém","têm","tínhamos","um","uma","umas","uns","usa","usar","vai","vais","valor","veja","vem",
		"vens","ver","verdade","verdadeiro","vez","vezes","viagem","vindo","vinte","você","vocês","vos","vossa","vossas","vosso",
		"vossos","vários","vão","vêm","vós","zero","à","às","área","é","éramos","és","último"]

		return portuguese_stopwords

	elif 'CAT' in language:
		catalan_stopwords = ["a","abans","ací","ah","així","això","al","aleshores","algun",
		"alguna","algunes","alguns","alhora","allà","allí","allò","als","altra","altre",
		"altres","amb","ambdues","ambdós","anar","ans","apa","aquell","aquella","aquelles",
		"aquells","aquest","aquesta","aquestes","aquests","aquí","baix","bastant","bé","cada",
		"cadascuna","cadascunes","cadascuns","cadascú","com","consegueixo","conseguim","conseguir",
		"consigueix","consigueixen","consigueixes","contra","d'un","d'una","d'unes","d'uns","dalt","de",
		"del","dels","des","des de","després","dins","dintre","donat","doncs","durant","e","eh","el",
		"elles","ells","els","em","en","encara","ens","entre","era","erem","eren","eres","es","esta",
		"estan","estat","estava","estaven","estem","esteu","estic","està","estàvem","estàveu","et","etc",
		"ets","fa","faig","fan","fas","fem","fer","feu","fi","fins","fora","gairebé","ha","han","has","haver",
		"havia","he","hem","heu","hi","ho","i","igual","iguals","inclòs","ja","jo","l'hi","la","les","li",
		"li'n","llarg","llavors","m'he","ma","mal","malgrat","mateix","mateixa","mateixes","mateixos","me",
		"mentre","meu","meus","meva","meves","mode","molt","molta","moltes","molts","mon","mons","més","n'he",
		"n'hi","ne","ni","no","nogensmenys","només","nosaltres","nostra","nostre","nostres","o","oh","oi","on",
		"pas","pel","pels","per","per que","perquè","però","poc","poca","pocs","podem","poden","poder","podeu",
		"poques","potser","primer","propi","puc","qual","quals","quan","quant","que","quelcom","qui","quin","quina",
		"quines","quins","què","s'ha","s'han","sa","sabem","saben","saber","sabeu","sap","saps","semblant",
		"semblants","sense","ser","ses","seu","seus","seva","seves","si","sobre","sobretot","soc","solament",
		"sols","som","son","sons","sota","sou","sóc","són","t'ha","t'han","t'he","ta","tal","també","tampoc",
		"tan","tant","tanta","tantes","te","tene","tenim","tenir","teniu","teu","teus","teva","teves","tinc","ton",
		"tons","tot","tota","totes","tots","un","una","unes","uns","us","va","vaig","vam","van","vas","veu","vosaltres",
		"vostra","vostre","vostres","érem","éreu","és","éssent","últim","ús"]

		return catalan_stopwords

	elif 'CZE_CZ' in language:

		czech_stopwords= ["a","aby","ahoj","aj","ale","anebo","ani","aniž","ano","asi","aspoň","atd","atp","az","ačkoli","až",
		"bez","beze","blízko","bohužel","brzo","bude","budem","budeme","budes","budete","budeš","budou",
		"budu","by","byl","byla","byli","bylo","byly","bys","byt","být","během","chce","chceme","chcete",
		"chceš","chci","chtít","chtějí","chut'","chuti","ci","clanek","clanku","clanky","co","coz","což",
		"cz","daleko","dalsi","další","den","deset","design","devatenáct","devět","dnes","do","dobrý",
		"docela","dva","dvacet","dvanáct","dvě","dál","dále","děkovat","děkujeme","děkuji","email","ho","hodně","i",
		"jak","jakmile","jako","jakož","jde","je","jeden","jedenáct","jedna","jedno","jednou","jedou","jeho","jehož",
		"jej","jeji","jejich","její","jelikož","jemu","jen","jenom","jenž","jeste","jestli","jestliže","ještě",
		"jež","ji","jich","jimi","jinak","jine","jiné","jiz","již","jsem","jses","jseš","jsi","jsme","jsou","jste",
		"já","jí","jím","jíž","jšte","k","kam","každý","kde","kdo","kdy","kdyz","když","ke","kolik","kromě","ktera","ktere",
		"kteri","kterou","ktery","která","které","který","kteři","kteří","ku","kvůli","ma","mají","mate","me","mezi","mi","mit",
		"mne","mnou","mně","moc","mohl","mohou","moje","moji","možná","muj","musí","muze","my","má","málo","mám","máme","máte",
		"máš","mé","mí","mít","mě","můj","může","na","nad","nade","nam","napiste","napište","naproti","nas","nasi","načež","naše",
		"naši","ne","nebo","nebyl","nebyla","nebyli","nebyly","nechť","nedělají","nedělá","nedělám","neděláme","neděláte","neděláš",
		"neg","nejsi","nejsou","nemají","nemáme","nemáte","neměl","neni","není","nestačí","nevadí","nez","než","nic","nich","nimi",
		"nove","novy","nové","nový","nula","ná","nám","námi","nás","náš","ní","ním","ně","něco","nějak","někde","někdo","němu",
		"němuž","o","od","ode","on","ona","oni","ono","ony","osm","osmnáct","pak","patnáct","po","pod","podle","pokud","potom",
		"pouze","pozdě","pořád","prave","pravé","pred","pres","pri","pro","proc","prostě","prosím","proti","proto","protoze",
		"protože","proč","prvni","první","práve","pta","pět","před","přede","přes","přese","při","přičemž","re","rovně",
		"s","se","sedm","sedmnáct","si","sice","skoro","smí","smějí","snad","spolu","sta","sto","strana","sté","sve","svych",
		"svym","svymi","své","svých","svým","svými","svůj","ta","tady","tak","take","takhle","taky","takze","také","takže",
		"tam","tamhle","tamhleto","tamto","tato","te","tebe","tebou","ted'","tedy","tema","ten","tento","teto","ti","tim",
		"timto","tipy","tisíc","tisíce","to","tobě","tohle","toho","tohoto","tom","tomto","tomu","tomuto","toto","trošku",
		"tu","tuto","tvoje","tvá","tvé","tvůj","ty","tyto","téma","této","tím","tímto","tě","těm","těma","těmu","třeba",
		"tři","třináct","u","určitě","uz","už","v","vam","vas","vase","vaše","vaši","ve","vedle","večer","vice","vlastně",
		"vsak","vy","vám","vámi","vás","váš","více","však","všechen","všechno","všichni","vůbec","vždy","z","za","zatímco",
		"zač","zda","zde","ze","zpet","zpravy","zprávy","zpět","čau","či","článek","článku","články","čtrnáct","čtyři","šest","šestnáct","že"]

		return czech_stopwords