from pymongo import MongoClient, errors
import json
import bcrypt

#connessione al DB
try:
    client = MongoClient("mongodb://root:Latitante@localhost:27017/")
    db = client.GymDB
except errors.ConnectionError as e:
    print("Errore di connessione:", e)    
else:
    print("Connessione al database:", db.name)

#verifica collection users ed eventuale caricamento json
collection = db.users    
try:
    users_count = collection.count_documents({})
except errors.PyMongoError as e:    
    print("Errore count users:", e)  
else:
    print ("\nDocumenti presenti in users:", users_count)
    
if users_count == 0:
    print ("Inizio caricamento JSON users")
    with open('users.json','r') as f:
        users_data = json.load(f)
        # hash password
        for user in users_data:
            user['password_hash'] = bcrypt.hashpw(user['password_hash'].encode('utf-8'), bcrypt.gensalt())        
 #       print (users_data)   
    
    try:
       result = collection.insert_many(users_data)
    except errors.PyMongoError as e:    
        print("Errore caricamento users:", e)  
    else:
       print (f"Caricamento json users terminato correttamente, {collection.count_documents({})} documenti caricati") #", result.inserted_ids) 

#verifica collection exercises ed eventuale caricamento json
collection = db.exercises    
try:
    exercises_count = collection.count_documents({})
except errors.PyMongoError as e:    
    print("Errore count exercises:", e)  
else:
    print ("\nDocumenti presenti in exercises:", exercises_count)
    
if exercises_count == 0:
    print ("Inizio caricamento JSON exercises")
    with open('exercises.json','r') as f:
        exercises_data = json.load(f)   
 #       print (exercises_data)   
    
    try:
       result = collection.insert_many(exercises_data)
    except errors.PyMongoError as e:    
        print("Errore caricamento exercises:", e)  
    else:
       print (f"Caricamento json exercises terminato correttamente, {collection.count_documents({})} documenti caricati") #, result.inserted_ids) 
       
client.close
   
   