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
        self.index = {} # hash para el indice invertido de terminos --> clave: termino, valor: posting list.
                        # Si se hace la implementacion multifield, se pude hacer un segundo nivel de hashing de tal forma que:
                        # self.index['title'] seria el indice invertido del campo 'title'.
        self.sindex = {} # hash para el indice invertido de stems --> clave: stem, valor: lista con los terminos que tienen ese stem
        self.ptindex = {} # hash para el indice permuterm.
        self.docs = {} # diccionario de documentos --> clave: entero(docid),  valor: ruta del fichero.
        self.weight = {} # hash de terminos para el pesado, ranking de resultados. puede no utilizarse
        self.news = {} # hash de noticias --> clave entero (newid), valor: la info necesaria para diferenciar la noticia dentro de su fichero (doc_id y posición dentro del documento)
        self.tokenizer = re.compile("\W+") # expresion regular para hacer la tokenizacion
        self.stemmer = SnowballStemmer('spanish') # stemmer en castellano
        self.show_all = False # valor por defecto, se cambia con self.set_showall()
        self.show_snippet = False # valor por defecto, se cambia con self.set_snippet()
        self.use_stemming = False # valor por defecto, se cambia con self.set_stemming()
        self.use_ranking = False  # valor por defecto, se cambia con self.set_ranking()

        self.total_doc = 0 # contador de número de documentos, usado para asignar docid
        self.total_news = 0 # contador de número de noticias, usado para asignar newid


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
        #################
        ### COMPLETAR ###
        #################



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
        pass
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################

        








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
        while i < len(query) and query[i].isspace():
            i += 1

        if query[i] == '(':
            matching_pos = self.get_matching_parenthesis(query, i)
            p = self.solve_query(query[i+1: matching_pos])
            i = matching_pos + 1
        elif query[i:i+4] == 'not ' or query[i:i+4] == 'not(':
            (p,i) = self.solve_reversed_query(query, i)
        else:
            token_end = self.get_token_end(query, i)
            p = self.get_posting(query[i:token_end])
            i = token_end

        while i < len(query):
            if query[i].isspace():
                i += 1
                continue
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
            
            p = operation(p, p2)
        
        return p
        



    def get_token_end(self, query, start):
        pos = start
        while pos < len(query) and not (query[pos] == ' ' or query[pos] == '(' or query[pos] == ')'):
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
                    return pos
                else:
                    inner_parenthesis -= 1
            elif query[pos] == '(':
                inner_parenthesis += 1
            pos += 1


    def solve_reversed_query(self, query, start):
        pos = start + 3
        while pos < len(query):
            if query[pos].isspace():
                pos += 1
                continue
            elif query [pos] == '(':
                matching_pos = self.get_matching_parenthesis(query, pos)
                posting_list = self.solve_query(query[pos+1:matching_pos])
                return (self.reverse_posting(posting_list), matching_pos + 1)
            elif query[pos: pos+4] == 'not ' or query[pos:pos+4] == 'not(':
                (posting_list, pos) = self.solve_reversed_query(query, pos)
                return (self.reverse_posting(posting_list), pos)
            else:
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
        if self.positional:
            return [x[0] for x in self.index[field][term[1]]]
        else:
            return self.index[field][term][1]
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################



    def get_positionals(self, terms, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE POSICIONALES

        Devuelve la posting list asociada a una secuencia de terminos consecutivos.

        param:  "terms": lista con los terminos consecutivos para recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """
        pass
        ########################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE POSICIONALES ##
        ########################################################


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
            # for j in range(i,docid):
            #     result.append(j)
            result += range(i,docid)
            i = docid + 1
        # while i < self.total_news:
        #     result.append(i)
        #     i+=1
        result += range(i,self.total_news)
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
        while i < len(p1) and j < len(p2):
            if p1[i] == p2[j]:
                result.append(p1[i])
                i += 1
                j += 1
            else:
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
            if p1[i] == p2[j]:
                result.append(p1[i])
                i += 1
                j += 1
            else:
                if p1[i] < p2[j]:
                    result.append(p1[i])
                    i += 1
                else:
                    result.append(p2[j])
                    j+=1
        while i < len(p1):
            result.append(p1[i])
            i+=1
        while j < len(p2):
            result.append(p2[j])
            j+=1
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
                tokenized_query = self.tokenize(query)
                normalized_new = self.tokenize(new['article'])
                ocurrences = []
                j = 0
                while (j < len(tokenized_query)):
                    token = tokenized_query[j]
                    if (token == 'and' or token == 'or'):
                        j+=1
                        continue
                    if (token == 'not'):
                        j+=2
                        continue
                    pos = normalized_new.index(token)
                    left_pos = max(0, pos - 6)
                    right_pos = min(len(normalized_new)-1, pos + 6)
                    ocurrences.append((left_pos, right_pos))
                    j+=1
                
                ocurrences.sort(key=lambda x: x[0])

                j=0
                while (j < len(ocurrences) - 1):
                    if ocurrences[j][1] >= ocurrences[j+1][0]:
                        ocurrences = ocurrences[:j] + [(ocurrences[j][0],ocurrences[j+1][1])] + ocurrences[j+2:]
                    else:
                        j+=1
                
                print("...", end="")
                for snippet in ocurrences:
                    for j in range(snippet[0], snippet[1] + 1):
                        print(normalized_new[j], end=" ")
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
