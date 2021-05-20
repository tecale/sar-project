import json
from nltk.stem.snowball import SnowballStemmer
import os
import re


class SAR_Project:
    """
    Prototipo de la clase para realizar la indexacion y la recuperacion de noticias

        Preparada para todas las ampliaciones:
          parentesis + multiples indices + posicionales + stemming + permuterm + ranking de resultado

    Se deben completar los metodos que se indica.
    Se pueden añadir nuevas variables y nuevos metodos
    Los metodos que se añadan se deberan documentar en el codigo y explicar en la memoria
    """

    # lista de campos, el booleano indica si se debe tokenizar el campo
    # NECESARIO PARA LA AMPLIACION MULTIFIELD
    fields = [("title", True), ("date", False),
              ("keywords", True), ("article", True),
              ("summary", True)]
    fields_names = {x[0] for x in fields}
    normalized_fields = {x[0] for x in fields if x[1]}

    # numero maximo de documento a mostrar cuando self.show_all es False
    SHOW_MAX = 10

    def __init__(self):

        """
        Constructor de la classe SAR_Indexer.
        NECESARIO PARA LA VERSION MINIMA

        Incluye todas las variables necesaria para todas las ampliaciones.
        Puedes añadir más variables si las necesitas

        """
        self.index = {k[0]: {} for k in SAR_Project.fields}  # hash para el indice invertido de terminos --> clave: termino, valor: posting list.
        # Si se hace la implementacion multifield, se pude hacer un segundo nivel de hashing de tal forma que:
        # self.index['title'] seria el indice invertido del campo 'title'.
        self.sindex = {}  # hash para el indice invertido de stems --> clave: stem, valor: lista con los terminos que tienen ese stem
        self.ptindex = {}  # hash para el indice permuterm.
        self.docs = {}  # diccionario de documentos --> clave: entero(docid),  valor: ruta del fichero.
        self.weight = {}  # hash de terminos para el pesado, ranking de resultados. puede no utilizarse
        self.news = {}  # hash de noticias --> clave entero (newid), valor: la info necesaria para diferenciar la noticia dentro de su fichero (doc_id y posición dentro del documento)
        self.tokenizer = re.compile("\W+")  # expresion regular para hacer la tokenizacion
        self.stemmer = SnowballStemmer('spanish')  # stemmer en castellano
        self.show_all = False  # valor por defecto, se cambia con self.set_showall()
        self.show_snippet = False  # valor por defecto, se cambia con self.set_snippet()
        self.use_stemming = False  # valor por defecto, se cambia con self.set_stemming()
        self.use_ranking = False  # valor por defecto, se cambia con self.set_ranking()

        self.total_doc = 0  # contador de número de documentos, usado para asignar docid
        self.total_news = 0  # contador de número de noticias, usado para asignar newid


    ###############################
    ###                         ###
    ###      CONFIGURACION      ###
    ###                         ###
    ###############################


    def set_showall(self, v):
        """

        Cambia el modo de mostrar los resultados.

        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_all es True se mostraran todos los resultados el lugar de un maximo de self.SHOW_MAX, no aplicable a la opcion -C

        """
        self.show_all = v

    def set_snippet(self, v):
        """

        Cambia el modo de mostrar snippet.

        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_snippet es True se mostrara un snippet de cada noticia, no aplicable a la opcion -C

        """
        self.show_snippet = v

    def set_stemming(self, v):
        """

        Cambia el modo de stemming por defecto.

        input: "v" booleano.

        UTIL PARA LA VERSION CON STEMMING

        si self.use_stemming es True las consultas se resolveran aplicando stemming por defecto.

        """
        self.use_stemming = v

    def set_ranking(self, v):
        """

        Cambia el modo de ranking por defecto.

        input: "v" booleano.

        UTIL PARA LA VERSION CON RANKING DE NOTICIAS

        si self.use_ranking es True las consultas se mostraran ordenadas, no aplicable a la opcion -C

        """
        self.use_ranking = v

    ###############################
    ###                         ###
    ###   PARTE 1: INDEXACION   ###
    ###                         ###
    ###############################


    def index_dir(self, root, **args):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Recorre recursivamente el directorio "root" e indexa su contenido
        los argumentos adicionales "**args" solo son necesarios para las funcionalidades ampliadas

        """

        self.multifield = args['multifield']
        self.positional = args['positional']
        self.stemming = args['stem']
        self.permuterm = args['permuterm']


        for dir, subdirs, files in os.walk(root):
            for filename in files:
                if filename.endswith('.json'):
                    fullname = os.path.join(dir, filename)
                    self.index_file(fullname)

                    ##########################################
                    ## COMPLETAR PARA FUNCIONALIDADES EXTRA ##
                    ##########################################

    def index_file(self, filename):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Indexa el contenido de un fichero.

        Para tokenizar la noticia se debe llamar a "self.tokenize"

        Dependiendo del valor de "self.multifield" y "self.positional" se debe ampliar el indexado.
        En estos casos, se recomienda crear nuevos metodos para hacer mas sencilla la implementacion

        input: "filename" es el nombre de un fichero en formato JSON Arrays (https://www.w3schools.com/js/js_json_arrays.asp).
                Una vez parseado con json.load tendremos una lista de diccionarios, cada diccionario se corresponde a una noticia

        """

        with open(filename) as fh:
            jlist = json.load(fh)

            #
            # "jlist" es una lista con tantos elementos como noticias hay en el fichero,
            # cada noticia es un diccionario con los campos:
            #      "title", "date", "keywords", "article", "summary"
            #
            # En la version basica solo se debe indexar el contenido "article"
            #
            #
            #
            
        position = 0
        for news in jlist:
            for field in self.fields:
                if not self.multifield and field[0] != 'article':
                    # Si no estamos procesando para múltiples campos y el campo actual no es artículo, pasamos al siguiente campo
                    continue
                if field[1]: #tokenize
                    tokens = self.tokenize(news[field[0]])
                    for i in range(len(tokens)):
                        # Para cada token de cada campo, lo intoroducimos en el índice
                        token = tokens[i]
                        if token not in self.index[field[0]]:
                            # Si no hemos visto el token antes, creamos una entrada nueva en el índice, con número de aparaciones a 0 y lista de noticias en las que aparece vacía
                            self.index[field[0]][token] = (0,[])
                        index_entry = self.index[field[0]][token]
                        posting_list = index_entry[1]
                        if self.positional:
                            #Si estamos construyendo el índice posicioanl
                            if len(posting_list) > 0 and posting_list[-1][0] == self.total_news:
                                # Si ya habíamos nos habíamos encotrado con este token en esta noticia, solamente añadimos la posición
                                # a la lista de posiciones para el token en esa noticia. Comprobamos solo la última posición de la lista
                                # de noticias porque al tratarlas secuencialmente, si buscamos la noticia actual, solamente sería posible
                                # que estuviese en la última posición, no es posible que hayamos tratado otra distinta de por medio
                                posting_list[-1][1].append(i)
                            else:
                                #Si el token no había aparecido antes en la noticia, creamos una nueva entrada con el id de la noticia
                                # y la lista de apariciones con la posición del token
                                posting_list.append((self.total_news, [i]))
                        else:
                            # Si no estamos construyendo el índice posicional
                            if len(posting_list) == 0 or posting_list[-1] != self.total_news:
                                # Si no nos habíamos encotrado antes el token en la noticia, añadimos el id de la noticia a lista de 
                                # de documentos para ese token
                                posting_list.append(self.total_news)
                        #Actualizamos la entrada en el índice para el token, incrementando el número total de apariciones y con la lista de documentos actaulizada
                        self.index[field[0]][token] = (index_entry[0] + 1, posting_list)
                else: #not tokenize
                    token = news[field[0]]
                    if token not in self.index[field[0]]:
                        # Si no hemos visto el token antes, creamos una entrada nueva en el índice, con número de aparaciones a 0 y lista de noticias en las que aparece vacía
                        self.index[field[0]][token] = (0,[])
                    index_entry = self.index[field[0]][token]
                    posting_list = index_entry[1]
                    if self.positional:
                        # Si es posicional, añadimos a la lista de aparciones el id de la noticia. Como solo hay un token de este campo por 
                        # noticia, no es posible que el id de noticia ya esté en la lista, así que no hay que comprobarlo. Y como todo el
                        # texto va a ser el token, la posición siempre será 0
                        posting_list.append((self.total_news,[0]))
                    else:
                        # Si no es posicional, añadimos a la lista de apariciones el id de la noticia. Como solo hay un token de este campo
                        # por noticia, no es posible que el id de noticia ya esté en la lista, así que no hay que comprobarlo.
                        posting_list.append(self.total_news)
                    #Actualizamos la entrada en el índice para el token, incrementando el número total de apariciones y con la lista de documentos actaulizada
                    self.index[field[0]][token] = (index_entry[0] + 1, posting_list)
            #Registramos la noticia con el documento en el que está y su posición dentro de él
            self.news[self.total_news] = (self.total_doc, position)
            self.total_news += 1
            position +=1
        # Registramos el documento con su ruta
        self.docs[self.total_doc] = filename
        self.total_doc += 1


    def tokenize(self, text):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Tokeniza la cadena "texto" eliminando simbolos no alfanumericos y dividientola por espacios.
        Puedes utilizar la expresion regular 'self.tokenizer'.

        params: 'text': texto a tokenizar

        return: lista de tokens

        """
        return self.tokenizer.sub(' ', text.lower()).split()

    def make_stemming(self):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING.

        Crea el indice de stemming (self.sindex) para los terminos de todos los indices.

        self.stemmer.stem(token) devuelve el stem del token

        """

        pass
        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################

    def make_permuterm(self):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM

        Crea el indice permuterm (self.ptindex) para los terminos de todos los indices.

        """
        pass
        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################

    def show_stats(self):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Muestra estadisticas de los indices

        """
        print("========================================")
        print("Number of indexed days: " +  str(len(self.index['date'])))
        print("----------------------------------------")
        print("Number of indexed news: " +  str(len(self.news)))
        print("----------------------------------------")
        print("TOKENS:")
        if self.multifield:
            for field in self.fields:
                print("\t# of tokens in \'"+ field[0] +"\': " + str(len(self.index[field[0]])))
        else:
            print("\t# of tokens in \'article\': " + str(len(self.index['article'])))
        print("----------------------------------------")
        if self.positional:
            print("Positional queries are allowed.")
        else:
            print("Positional queries are NOT allowed.")
        print("========================================")

    ###################################
    ###                             ###
    ###   PARTE 2.1: RECUPERACION   ###
    ###                             ###
    ###################################


    def solve_query(self, query, prev={}):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una query.
        Debe realizar el parsing de consulta que sera mas o menos complicado en funcion de la ampliacion que se implementen


        param:  "query": cadena con la query
                "prev": incluido por si se quiere hacer una version recursiva. No es necesario utilizarlo.


        return: posting list con el resultado de la query

        """

        if query is None or len(query) == 0:
            return []
        
        query = query.lower()
        i = 0
        p = []
        #Limpiamos el posible espacio blanco al principio
        while i < len(query) and query[i].isspace():
            i += 1

        # Procesamos el primer token, que puede ser o una subconsulta entre paréntesis,
        # o un término negado, o un término simple
        if query[i] == '(':
            # Si es una subconsulta, búscamos el paréntesis de cierre
            matching_pos = self.get_matching_parenthesis(query, i)
            # Obtenemos la posting list de la subconsulta
            p = self.solve_query(query[i+1: matching_pos])
            # Avanzamos el índice hasta después de la consulta
            i = matching_pos + 1
        elif query[i:i+4] == 'not ' or query[i:i+4] == 'not(':
            # Si es un término negado, lo delegamos a la método para calcular posting lists
            # de negaciones
            (p,i) = self.solve_reversed_query(query, i)
        else:
            # Si es un token normal, buscamos hasta dónde llega
            token_end = self.get_token_end(query, i)
            # Calculamos la posting list del término
            p = self.get_posting(query[i:token_end])
            #Avanzamos el índice hasta después del token
            i = token_end

        # Mientras la consulta continue, la seguimos procesando de izquierda a derecha
        while i < len(query):
            if query[i].isspace():
                i += 1
                continue
            # Obtenemos el tipo de operación, y salimos si no se corresponde con el formato
            if query[i:i+2] == 'or':
                operation = self.or_posting
                i += 2
            elif query[i:i+3] == 'and':
                operation = self.and_posting
                i += 3
            else:
                break
            
            while i < len(query) and query[i].isspace():
                i += 1

            # El otro operando puede ser también o una subconsulta, o un término
            # negado, o un término normal, y se tratarán de la misma manera
            if query[i] == '(':
                matching_pos = self.get_matching_parenthesis(query, i)
                p2 = self.solve_query(query[i+1: matching_pos])
                i = matching_pos + 1
            elif query[i:i+4] == 'not ' or query[i:i+4] == 'not(':
                (p2,i) = self.solve_reversed_query(query, i)
            else:
                token_end = self.get_token_end(query, i)
                p2 = self.get_posting(query[i:token_end])
                i = token_end
            
            # Calculamos el resultado de la operación, y continuamos si es necesario
            p = operation(p, p2)
        
        return p
        



    def get_token_end(self, query, start):
        """
        A partir de una query y la posición en la que comienza un token que se corresponde con el operando para
        una operación AND, OR o NOT, devuelve la posición del siguiente carácter después del token sobre el que
        se opera. El token puede ser o bien una cadena entre comillas para búsqueda, o bien una palabra suelta, 
        que puede incluir un especificador de campo. También podría ser una subconsulta entre paréntesis. No 
        se considera la opción de que sea una consulta negada, ese caso se trata externamente

        param:  "query" Cadena con la query
                "start" Posición del primer carácter del token
        return: posición del siguiente carácter posterior al token
        """ 
        pos = start
        while pos < len(query) and not (query[pos] == ' ' or query[pos] == ')'):
            # Generalmente, sabremos que hemos llegado al final del token si hemos alcanzado el final del input, 
            # si nos encotramos un espacio en blanco, o un paréntesis que cierre
            if query[pos] == '"':
                #Si encontramos comillas, token acabará únicamente cuando nos encontremos las comillas de cierre
                pos += 1
                while pos < len(query) and query[pos] != '"':
                    pos += 1
                if pos >= len(query):
                    print("ERROR: No se han cerrado comillas")
                    exit()
            pos += 1
        return pos


    def get_matching_parenthesis(self, query, start):
        """
        A partir de una query y la posición de un paréntisis inicial, devuelve la posición del
        paréntesis que lo cierra. Se asume que la query está construida correctamente

        param:  "query": query de la que se quiere extraer la posición del paréntesis de cierre
                "start": posición del paréntisis de abertura

        return: posición del paréntesis de cierre
        """
        pos  = start + 1
        inner_parenthesis = 0
        while pos < len(query):
            if query[pos] == ')':
                if inner_parenthesis == 0:
                    # Si se corresponde con el paréntesis inicial, devolvemos la posición
                    return pos
                else:
                    # Si no, descontamos del número de pares de paréntesis internos
                    inner_parenthesis -= 1
            elif query[pos] == '(':
                # Si nos encontramos con otro paréntesis de apertura, tendremos que asegurarnos de que
                # estos se cierran antes de que podamos cerrar en nuestro
                inner_parenthesis += 1
            pos += 1


    def solve_reversed_query(self, query, start):
        """
        Resuelve las queries del tipo NOT, devolviendo la posting list y la posición donde termina la query. Tiene 
        en cuenta los casos de que el operando sea a su vez una query NOT, como que sea una subconsulta entre 
        paréntesis, como que sea un término normal

        param:  "query": query de la que se quiere extrar la query NOT
                "start": posición donde comienza la query NOT
        
        return: (end, posting_list) La posición donde acaba la query NOT, y la posting list resultante de la query
        """
        # Pasamos el NOT inicial
        pos = start + 3
        while pos < len(query):
            # Limpiamos los posibles espacios
            if query[pos].isspace():
                pos += 1
                continue
            elif query [pos] == '(':
                #Si nos encontramos un paréntesis, obtenemos la posting list de la subconsulta, 
                # y calculamos el NOT de esa
                matching_pos = self.get_matching_parenthesis(query, pos)
                posting_list = self.solve_query(query[pos+1:matching_pos])
                return (self.reverse_posting(posting_list), matching_pos + 1)
            elif query[pos: pos+4] == 'not ' or query[pos:pos+4] == 'not(':
                # Si nos econtramos otra query NOT dentro, calculamos esa recursivamente, y devolvemos su negación
                (posting_list, pos) = self.solve_reversed_query(query, pos)
                return (self.reverse_posting(posting_list), pos)
            else:
                # Si es un término normal, calculamos su posting list, y devolvemos la negación
                token_start = pos
                token_end = self.get_token_end(query, token_start)
                posting_list = self.get_posting(query[token_start:token_end])
                return (self.reverse_posting(posting_list), token_end)
        return []

    def get_posting(self, term, field='article'):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Devuelve la posting list asociada a un termino.
        Dependiendo de las ampliaciones implementadas "get_posting" puede llamar a:
            - self.get_positionals: para la ampliacion de posicionales
            - self.get_permuterm: para la ampliacion de permuterms
            - self.get_stemming: para la amplaicion de stemming


        param:  "term": termino del que se debe recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """
        #Si encontramos el separador de campo, especificamos el campo, si no, ponemos article por defecto
        separator_pos = term.find(':')
        if separator_pos == -1:
            field = 'article'
        else:
            field = term[:separator_pos]
        if term[separator_pos + 1] == '"':
            # Si es una búsqueda posicional, obtendremos la posting list de la secuencia, tokenizada o no
            # dependiendo de si lo requiere, delegando en get_positionals
            if not self.positional:
                print("ERROR: La indexación no se realizó con soporte para búsquedas posicionales")
                exit()
            if field in SAR_Project.normalized_fields:
                terms = self.tokenize(term[separator_pos + 2:-1])
            else:
                terms = term[separator_pos + 2:-1].split()
            return self.get_positionals(terms, field)
        else:
            # Si no es una búsquesa posicional
            if self.stemming and field in SAR_Project.normalized_fields:
                # Si utilizamos stemming, delegamos
                return self.get_stemming(term[separator_pos+1:], field)

            #Tokenizamos si es necasrio
            if field in SAR_Project.normalized_fields:
                token = self.tokenize(term[separator_pos+1:])[0]
            else:
                token = term[separator_pos+1:]
            if self.positional:
                # Si es el índice es posicional, tendremos que extraer de cada entrada de la posting list únicamente el id de noticia,
                # e ignorar las listas de posiciones que acompañan en una tupla al id. 
                # Ej: posting_list: [(new1, [2,4]), (new7, [0]), (new10,[1,2]), ...]
                return [x[0] for x in self.index.get(field, {}).get(token, (0,[]))[1]]
            else:
                # Si el índice no es posicional, bastará con obtener la posting list, que solo consistirá en una lista de id de noticias.
                # Ej: posting_list: [new1, new7, new10...]
                return self.index.get(field, {}).get(token, (0,[]))[1]


    def get_positionals(self, terms, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE POSICIONALES

        Devuelve la posting list asociada a una secuencia de terminos consecutivos.

        param:  "terms": lista con los terminos consecutivos para recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """
        # Aquí utilizamos una modificación de una operación AND, solo que en lugar de hacerla con solo 2 elementos, se
        # hace con una cantidad arbitraria, y además de comprobar si están en el mismo documento, se comprueba si su 
        # posición es secuencial
        result = []
        posting_lists = [self.index.get(field, {}).get(term, (0, []))[1] for term in terms]
        positions = [0] * len(posting_lists)
        n_terms = len(posting_lists)
        if n_terms == 0:
            return []
        while all([positions[i] < len(posting_lists[i]) for i in range(n_terms)]):
            # Mientras no hayamos llegado al final de la posting list de ninguno de los elementos
            same_doc = True
            doc = posting_lists[0][positions[0]]
            #Comprobamos si estamos en todas las posting list apuntando al mismo documento
            for j in range(1,n_terms):
                if posting_lists[j][positions[j]][0] != doc[0]:
                    same_doc = False
                    break
            if same_doc:
                # Si aparecen todos los términos en el mismo documento, comprobamos si aparecen secuencialmente
                if self.check_sequential_in_document([posting_lists[j][positions[j]][1] for j in range(n_terms)]):
                    # Si aparecen secuencialmente, añadimos la noticia a la posting list de resultado
                    result.append(doc[0])
                # Avanzamos todas las posting list de los términos a la siguiente posición
                for j in range(n_terms):
                    positions[j] += 1
            else:
                # Si no es la misma noticia, búscamos el término con la noticia más baja, y la avanzamos a la siguiente
                min_pos = min([(j, posting_lists[j][positions[j]]) for j in range(n_terms)], key= lambda x: x[1])[0]
                positions[min_pos] += 1
        return result

    def check_sequential_in_document(self, term_positions):
        """
        Dada una lista de n listas correspondientes con las posiciones de n términos en una noticia, devuelve true
        si los términos aparecen en la noticia consecutivamente, en el orden en el que se han pasado las listas

        param:  "term_positions": lista de n listas con las posiciones de los n términos en la noticia

        return: true si los términos aparecen consecutivamente en el orden de las listas
        """
        n_terms = len(term_positions)
        positions = [0]*n_terms
        while positions[0] < len(term_positions[0]):
            start_pos = term_positions[0][positions[0]]
            for i in range(1,n_terms):
                #Para cada término, mientras su posición no sea posterior a la del término posterior, lo avanzamos
                while positions[i] < len(term_positions[i]) and term_positions[i][positions[i]] < start_pos+i:
                    positions[i] += 1
                if positions[i] >= len(term_positions[i]):
                    #Si alguna lista se sale, no puede estar la secuencia
                    return False
                
            # Si las posiciones de cada término son secuenciales, devolvemos true
            if all([term_positions[i][positions[i]] == start_pos + i for i in range(n_terms)]):
                return True
            # Si no, incrementamos la posición del primer término, y lo seguimos intentando, hasta llegar al final o encontrarlo
            positions[0] += 1
        return False

    def get_stemming(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING

        Devuelve la posting list asociada al stem de un termino.

        param:  "term": termino para recuperar la posting list de su stem.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """

        stem = self.stemmer.stem(term)

        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################

    def get_permuterm(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM

        Devuelve la posting list asociada a un termino utilizando el indice permuterm.

        param:  "term": termino para recuperar la posting list, "term" incluye un comodin (* o ?).
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """

        ##################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA PERMUTERM ##
        ##################################################

    def reverse_posting(self, p):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Devuelve una posting list con todas las noticias excepto las contenidas en p.
        Util para resolver las queries con NOT.


        param:  "p": posting list


        return: posting list con todos los newid exceptos los contenidos en p

        """

        i = 0
        result = []
        for docid in p:
            #Añadimos al resultado todos los docuemntos que hay entre cada uno de los que nos han pasado, 
            # sin incluir esos
            result += range(i, docid)
            i = docid + 1
        #Añadimos todos los que pueda haber desde el último que se debe excluir hasta el final
        result += range(i, self.total_news)
        return result

        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################

    def and_posting(self, p1, p2):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Calcula el AND de dos posting list de forma EFICIENTE

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newid incluidos en p1 y p2

        """
        result = []
        i = 0
        j = 0
        #Vamos avanzando sobre la lista mientras aún queden en las dos
        while i < len(p1) and j < len(p2):
            if p1[i] == p2[j]:
                # Si la noticia está en las dos, la incuimos en el resultado y pasamos a las siguientes
                result.append(p1[i])
                i += 1
                j += 1
            else:
                # Si no, avanzamos el que tenga la noticia más baja
                if p1[i] < p2[j]:
                    i += 1
                else:
                    j += 1

        return result

    def or_posting(self, p1, p2):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Calcula el OR de dos posting list de forma EFICIENTE

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newid incluidos de p1 o p2

        """
        result = []
        i = 0
        j = 0
        while i < len(p1) and j < len(p2):
            #Mientreas queden noticias en los dos
            if p1[i] == p2[j]:
                #Si está en los dos, la incluimos y avanzamos los dos
                result.append(p1[i])
                i += 1
                j += 1
            else:
                # Si solo está en una, la incluimos y avanzamos a la siguiente. 
                if p1[i] < p2[j]:
                    result.append(p1[i])
                    i += 1
                else:
                    result.append(p2[j])
                    j += 1
        # Añadimos todas las que pueden haber quedado de lo que sobre en una u otra de las lista,
        # ya que habremos salido del bucle porque una o las dos listas se habían agotado
        while i < len(p1):
            result.append(p1[i])
            i += 1
        while j < len(p2):
            result.append(p2[j])
            j += 1
        return result

    def minus_posting(self, p1, p2):
        """
        OPCIONAL PARA TODAS LAS VERSIONES

        Calcula el except de dos posting list de forma EFICIENTE.
        Esta funcion se propone por si os es util, no es necesario utilizarla.

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newid incluidos de p1 y no en p2

        """

        pass
        ########################################################
        ## COMPLETAR PARA TODAS LAS VERSIONES SI ES NECESARIO ##
        ########################################################

    #####################################
    ###                               ###
    ### PARTE 2.2: MOSTRAR RESULTADOS ###
    ###                               ###
    #####################################


    def solve_and_count(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una consulta y la muestra junto al numero de resultados

        param:  "query": query que se debe resolver.

        return: el numero de noticias recuperadas, para la opcion -T

        """
        result = self.solve_query(query)
        print("%s\t%d" % (query, len(result)))
        return len(result)  # para verificar los resultados (op: -T)

    def solve_and_show(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una consulta y la muestra informacion de las noticias recuperadas.
        Consideraciones:

        - En funcion del valor de "self.show_snippet" se mostrara una informacion u otra.
        - Si se implementa la opcion de ranking y en funcion del valor de self.use_ranking debera llamar a self.rank_result

        param:  "query": query que se debe resolver.

        return: el numero de noticias recuperadas, para la opcion -T

        """
        result = self.solve_query(query)
        if self.use_ranking:
            result = self.rank_result(result, query)   
        
        multifield_tokenizer = re.compile(r"(?:\w+:)?(?:\w+|(?:\".*?\"))")

        print('='*40)
        print('Query: \'' + query + '\'')
        print('Number of results: %d' % len(result))
        for i in range(len(result)):
            newid = result[i-1]
            (docId, pos) = self.news[newid]
            filepath = self.docs[docId]
            with open(filepath) as f:
                jlist = json.load(f)
                new = jlist[pos]

            print('#%d' % (i+1))
            print('Score: 0')
            print(str(newid))
            print("Date: " + new['date'])
            print('Title: ' + new['title'])
            print('Keywords: ' + new['keywords'])

            if (self.show_snippet):
                tokenized_query = multifield_tokenizer.findall(query.lower())
                normalized_new = {}
                ocurrences = {}
                for (key, value) in SAR_Project.fields:
                    if value:
                        normalized_new[key] = self.tokenize(new[key])
                    else:
                        normalized_new[key] = [new[key]]
                    ocurrences[key] = []

                j = 0
                while (j < len(tokenized_query)):
                    token = tokenized_query[j]
                    if (token == 'and' or token == 'or' or token == 'not'):
                        j+=1
                        continue
                    separator_pos = token.find(':')
                    if separator_pos == -1:
                        field =  'article'
                    else:
                        field = token[:separator_pos]
                        token = token[separator_pos+1:]
                    if token[0] == '"':
                        if field in SAR_Project.normalized_fields:
                            terms = self.tokenize(token[1:-1])
                        else:
                            terms = token.trim('"').split()
                        for k in range(len(normalized_new[field]) - len(terms) + 1):
                            found = True
                            for h in range(len(terms)):
                                if normalized_new[field][k + h] != terms[h]:
                                    found = False
                                    break
                            if found:
                                left_pos = max(0, k - 6)
                                right_pos = min(len(normalized_new[field]) - 1, k + len(terms) + 5)
                    else:
                        pos = normalized_new[field].index(token)
                        left_pos = max(0, pos - 6)
                        right_pos = min(len(normalized_new[field])-1, pos + 6)
                        
                    ocurrences[field].append((left_pos, right_pos))
                    j+=1
                
                for (field, _) in SAR_Project.fields:
                    field_ocurrences = ocurrences[field]
                    field_ocurrences.sort(key=lambda x: x[0])

                    j=0
                    while (j < len(field_ocurrences) - 1):
                        if field_ocurrences[j][1] >= field_ocurrences[j+1][0]:
                            field_ocurrences = field_ocurrences[:j] + [(field_ocurrences[j][0],field_ocurrences[j+1][1])] + field_ocurrences[j+2:]
                        else:
                            j+=1
                
                print("...", end="")
                for (field,_) in SAR_Project.fields:
                    for snippet in ocurrences[field]:
                        for j in range(snippet[0], snippet[1] + 1):
                            print(normalized_new[field][j], end=" ")
                        print("... ", end="")
                print()
                    



            if (i < len(result)-1):
                print('-'*20)
        print('='*40)

    def rank_result(self, result, query):
        """
        NECESARIO PARA LA AMPLIACION DE RANKING

        Ordena los resultados de una query.

        param:  "result": lista de resultados sin ordenar
                "query": query, puede ser la query original, la query procesada o una lista de terminos


        return: la lista de resultados ordenada

        """

        pass

        ###################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE RANKING ##
        ###################################################