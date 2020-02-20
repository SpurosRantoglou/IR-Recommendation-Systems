import nltk
import random
import sqlite3
import string
from collections import defaultdict
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


# nltk.download("stopwords")
# nltk.download("punkt")


# Function to convert list to String  
def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1  

def overlap(recJaccard, recDice):
    JS = 0
    DC = 0

    for i in recJaccard:
        JS = JS + float(i['similarity'])
    for i in recDice:
        DC = DC + float(i['similarity'])

    Overlap = float((JS + DC)/20)
    #print(JS)
    #print(DC)
    #print("\nOverlap is: ")
    print(Overlap)

def goldenStandard(recJaccard, recDice):
    
    #We use the lists as parametres but we keep the same ones
    #With ISBN and Book-Title and similarity
    #But im gonna use similarity as the column of freq
 
    #Combine the 2 list(Jaccard, Dice) and create one new with the most 10 frequent movies
    for i in recJaccard:
        Count = 0
        
        for j in recJaccard:
            if i['ISBN']==j['ISBN']:
                Count = Count + 1
        for j in recDice:
            if i['ISBN']==j['ISBN']:
                Count = Count + 1
        i['similarity'] = Count   

    for i in recDice:
        Count = 0
        for j in recDice:
            if i['ISBN']==j['ISBN']:
                Count = Count + 1        
        for j in recJaccard:
            if i['ISBN']==j['ISBN']:
                Count = Count + 1

    sorted(recJaccard, key=lambda k: k['similarity'], reverse=True)[:10]
    sorted(recDice, key=lambda k: k['similarity'], reverse=True)[:10]
    goldenStandard = []
    goldenStandard = recDice + recJaccard
    sorted(goldenStandard, key=lambda k: k['similarity'], reverse=True)[:10]
    for i in goldenStandard[:10]:
        print(i)
   
   
   
   
    
 
  

def RecommendedForDice(profile):   
    #Finding non rated books
    c=conn.cursor()
    unrated = c.execute('SELECT Keywords,"Book-Author","Year-Of-Publication",ISBN,"Book-Title" FROM "BX-Books" WHERE ISBN NOT IN (SELECT ISBN FROM "BX-Book-Ratings" WHERE "User-ID" = \'' + profile['userId'] + '\');')
    unrated = unrated.fetchall()
   
    recommendedBooks = []
    for i in unrated:
        bookSimilarity = {'ISBN': '', 'bookTitle': '', 'similarity': ''}

        author_similarity = 0
        keyword_similarity = 0
        years_similarity = []
        #year_weight = 0.4

        bookSimilarity['ISBN'] = i[3]
        bookSimilarity['bookTitle'] = i[4]

    



        if(i[1] in profile['authors'].split(',')):
            author_similarity = 0.3
        
        arrayKeywords = profile['keywords'].split(', ')
        keyword_similarity = Dice_Coefficient(arrayKeywords, i[0].split(', '))
      
        try:
            int(i[2])
        except ValueError:
            continue
        for j in profile['year'].split(','):

            try:
                int(j)
            except ValueError:
                continue

            a = i[2]
            a = int(a)
            b = j
            b = int(b)
            years_similarity.append(1-(abs(a - b)/2005))

        
        try:
            (min(years_similarity)*0.2)
        except ValueError:
            continue

        #tries/excepets because of some error of data
        
        bookSimilarity['similarity'] = (keyword_similarity * 0.5) + (author_similarity) + (min(years_similarity)*0.2)
        recommendedBooks.append(bookSimilarity)
        
    jaccardSimilar = sorted(recommendedBooks, key=lambda k: k['similarity'], reverse=True)[:10]
    for i in jaccardSimilar:
        print(i)
    return jaccardSimilar

def RecommendedForJaccard(profile):   

    #Finding non rated books
    c=conn.cursor()
    unrated = c.execute('SELECT Keywords,"Book-Author","Year-Of-Publication",ISBN,"Book-Title" FROM "BX-Books" WHERE ISBN NOT IN (SELECT ISBN FROM "BX-Book-Ratings" WHERE "User-ID" = \'' + profile['userId'] + '\');')
    unrated = unrated.fetchall()
   
    recommendedBooks = []
    for i in unrated:
        bookSimilarity = {'ISBN': '', 'bookTitle': '', 'similarity': ''}

        author_similarity = 0
        keyword_similarity = 0
        years_similarity = []
        #year_weight = 0.4

        bookSimilarity['ISBN'] = i[3]
        bookSimilarity['bookTitle'] = i[4]

    

        if(i[1] in profile['authors'].split(',')):
            author_similarity = 0.4
        arrayKeywords = profile['keywords'].split(', ')
      
        keyword_similarity = jaccard(arrayKeywords, i[0].split(', '))

        try:
            int(i[2])
        except ValueError:
            continue
        for j in profile['year'].split(','):
            
            try:
                int(j)
            except ValueError:
                continue
                
            a = i[2]
            a = int(a)
            b = j
            b = int(b)
            years_similarity.append(1-(abs(a - b)/2005))

        try:
            (min(years_similarity)*0.4)
        except ValueError:
            continue 
        
        #tries/excepets because of some error of data
        bookSimilarity['similarity'] = (keyword_similarity * 0.2) + (author_similarity) + (min(years_similarity)*0.4)

        recommendedBooks.append(bookSimilarity)
        
    jaccardSimilar = sorted(recommendedBooks, key=lambda k: k['similarity'], reverse=True)[:10]
    for i in jaccardSimilar:
        print(i)
    return jaccardSimilar

def randomUser():

    #Return 5 random ID's to run recommendation
    c=conn.cursor()
    random = c.execute('SELECT "User-ID" FROM "BX-Users" ORDER BY RANDOM() LIMIT 5')
    random = random.fetchall()
    #print(random)
    #print("Users that will recommend books for: ")
    randomUsers = []
    for i in random:
        randomUsers.append(i[0])
        #print(i[0])
    #print(randomUsers)

    return randomUsers
    
def writeToFileJaccard(user, info):
   with open("User" + user + "Jaccard.txt", "w",encoding='utf-8') as file_handler:
       file_handler.write("Jaccard similarity \n\n")
       for item in info:
           file_handler.write("{}\n".format(item))
        
def writeToFileDice(user, info):
   with open("User" + user + "Dice.txt", "w",encoding='utf-8') as file_handler:
       file_handler.write("Dice Coefficient \n\n")
       for item in info:
           file_handler.write("{}\n".format(item))
           

        
    
       
    

    


   


def createProfile(userID, listOfIsbn):
    #Creating all the keywords union for a specific user
    
    
    profile = {'userId': '', 'keywords': '', 'authors': '', 'year': ''}

    for i in listOfIsbn:
        c=conn.cursor()
        data = c.execute('SELECT Keywords, "Book-Author","Year-Of-Publication" FROM "BX-Books" WHERE ISBN = \'' + i[0] + '\';')
        data = data.fetchall()
        #print(i[0])
        print(data)
        
        #Union at profile of user
        profile['userId'] = userID
        profile['keywords'] += listToString(data[0][0]) + ', '
        profile['authors'] += data[0][1] + ','
        profile['year'] += str(data[0][2]) + ','
        
    
    
    
    
    #print(profile['keywords'])
    profile['keywords'] = profile['keywords'][:-2]
    #print(profile['keywords'])
    profile['authors'] = profile['authors'][:-1]
    profile['year'] = profile['year'][:-1] 
    return profile



#Jaccard Similarity function
def jaccard(a, b):
    
    userA = set(a)
    userB = set(b)
    JS = float(len(userA.intersection(userB))/len(userA.union(userB)))
    return JS


#Dice Coefficient function
def Dice_Coefficient(a, b):
    userA = set(a)
    userB = set(b)
    DC = float(len(userA.intersection(userB)) * 2.0) / (len(userA) + len(userB))
    return DC
conn = sqlite3.connect('books.db')


####### MAIN #######

rand = randomUser()
print("\n")
print("The random users that selected: " )
print(rand)
print("\n")

for randUser in rand:
    c=conn.cursor()
    book = c.execute('SELECT ISBN FROM "BX-Book-Ratings" WHERE "User-ID" =\'  '+ str(randUser) +'  \'ORDER BY "Book-Rating" DESC LIMIT 3;')
    books = book.fetchall()
    print("\n")
    print("\n")
    print("User: " + str(randUser) + " ,top 3 rated books") 
    print("\n")
    
    id = str(randUser)

    aUser = createProfile(id,books)
    print("\n\n")
    print("For those books we recommend you: ")
    print("\n")
    print("With Jaccard Similarity \n")
    JS = RecommendedForJaccard(aUser)
    print("################################################################################################################################# \n\n\n")
    print("With Dice Coefficient \n")
    DC = RecommendedForDice(aUser)
    print("################################################################################################################################# \n\n")
    print("Combine both recommenders")
    writeToFileJaccard(id,RecommendedForJaccard(aUser))
    writeToFileDice(id,RecommendedForDice(aUser))

    print("\n\n\n")
    print("The overlap between Jaccard Similarity and Dice Coefficient: ")
    overlap(JS,DC)
    print("\n")
    print("The final Golden Standard list is: ")
    goldenStandard(JS,DC)
    print("\n")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

   
    
###TEST USER###

print("################### TEST USER ###################")
# Finding 3 top-rated books of user 276746
c=conn.cursor()
book = c.execute('SELECT ISBN FROM "BX-Book-Ratings" WHERE "User-ID" ="276746" ORDER BY "Book-Rating" DESC LIMIT 3;')
books = book.fetchall()



#Creating a list of user's book
listOfBooks = []
for i in books:
    listOfBooks.append(i[0])
userID = "276746"

user = createProfile(userID,books)
JS = RecommendedForJaccard(user)
DC = RecommendedForDice(user)


writeToFileJaccard(userID,RecommendedForJaccard(user))
writeToFileDice(userID,RecommendedForDice(user))

print("\n")
print("Recomended books with Jaccard Similarity: \n")
RecommendedForJaccard(user)
print("################################################################################################################################# \n\n\n")
print("Recomended books with Dice Coefficient: \n")
RecommendedForDice(user)
print("################################################################################################################################# \n\n")
overlap(JS,DC)
#goldenStandard(JS,DC)


conn.close()























