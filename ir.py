import sqlite3
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,RegexpTokenizer
from nltk.stem import PorterStemmer


def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele + ', '   
    
    # return string   
    str1 = str1 [:-2]
    return str1  

def preprocess(text):
    
    stop_words = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'\w+')
    final = tokenizer.tokenize(text)
    final = ' '.join(final)


    final = word_tokenize(final)
    filtered_sentences = [w.lower() for w in final if not w.lower() in stop_words]

    ps = PorterStemmer()
    # filtered_sentences = []
    # for w in word_tokens: 
    #     if w not in stop_words: 
    #         filtered_sentence.append(w) 

    # print(text2)
    #print(filtered_sentences)
    #print(final)
    updated=[]
    for w in filtered_sentences:
       updated.append(ps.stem(w))

    # print(c.fetchall())
    return updated

conn = sqlite3.connect('books.db')
c=conn.cursor()
# c.execute("""SELECT * FROM 'BX-Users' WHERE "User-ID" = "5";""")


rows = c.execute('SELECT "Book-Title",ISBN FROM "BX-Books" limit 48658;')
data = rows.fetchall()

for i in data:
    toInsert = preprocess(i[0])
    x = listToString(toInsert)
    print(x)
    c=conn.cursor()
    c.execute('UPDATE "BX-Books" SET "Keywords"=? WHERE ISBN=?;', (x,i[1]))
    conn.commit()
    

    
# nltk.download("stopwords")
# nltk.download("punkt")




# text = "Natural language processing (NLP) is a The field "


conn.close()
