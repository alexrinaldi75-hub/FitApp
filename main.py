from pymongo import MongoClient, errors
from datetime import datetime
import bcrypt
import getpass

# classe per gestione DB
class DatabaseManager:
    def __init__(self, uri, db_name):
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
        except errors.ConnectionError as e:   
            print("Errore di connessione:", e) 
  
    def close(self):
        self.client.close() 

    def change_collection(self, collection_name):
        try:
            self.collection = self.db[collection_name]   
        except errors.PyMongoError as e:   
            print("Errore cambio collection:", e)  

    def read_single_document(self, query):
        try:
            documents = self.collection.find_one(query)
        except errors.PyMongoError as e:   
            print("Errore di lettura:", e)   
        else:
            return documents      
        
    def read_multiple_document(self, query, projection=None):
        try:
            documents = self.collection.find(query, projection)
        except errors.PyMongoError as e:   
            print("Errore di lettura:", e)   
        else:
            return documents             

    def update_one_document(self, query, update):
        try:
            result = self.collection.update_one(query, update)
        except errors.PyMongoError as e:   
            print("Errore in update:", e)             
       # print("Documenti modificati:", result.modified_count)    
        else:
            print ("Modifica effettuata")
       
    def insert_one_document(self, document):
        try:
            result = self.collection.insert_one(document)
        except errors.PyMongoError as e:   
            print("Errore in insert:", e) 
        else:
            print ("Inserimento effettuato")        

    def delete_one_document(self, query):
        try:
            result = self.collection.delete_one(query)
        except errors.PyMongoError as e:   
            print("Errore in delete:", e) 
        else:
            print ("Cancellazione effettuata")      

    def read_aggregate_document(self, pipeline):
        try:
            documents = self.collection.aggregate(pipeline)
        except errors.PyMongoError as e:   
            print("Errore di lettura aggregate:", e)   
        else:
            return documents                                 
       
       
class Menu:  
    def __init__(self, DB): 
        self.DB = DB
    def menu_admin(self):
        print ("\n         Menu Admin   ")
        print ("1 - Inserisci nuovo utente")
        print ("2 - Elimina utente")
        print ("3 - Reset password")
        print ("0 - Esci")
        scelta = input ("Scegli un'operazione: ")
        return scelta
    def menu_new_user(self):
        print ("")
        #u = input ("Inserisci username: ")
        u_ko = True
        while u_ko:       
            u = input ("Inserisci username: ")
            us = self.DB.read_single_document({"username":u})
            if us == None:
                u_ko = False
            else:                
                print("Username già presente")

        #p = input ("inserisci la password: ")
        n = input ("inserisci il nome: ")
        ruolo_ko = True
        while ruolo_ko:
            ruoli = {"admin", "trainer", "athlete"}
            r = input ("inserisci il ruolo (admin/trainer/athlete): ")
            if r in ruoli:
                ruolo_ko = False
            else:
                print("Ruolo non previsto")    
        return u, n, r 
    def menu_username(self):
        print ("")
        u = input ("Inserisci username: ")
        return u

    def menu_trainer(self):
        print ("\n       Menu Trainer   ")
        print ("1 - Visualizza atleti")
        print ("2 - Crea scheda")
        print ("3 - Assegna scheda")
        print ("0 - Esci")
        scelta = input ("Scegli un'operazione: ")
        return scelta    
        
    def menu_new_workout(self):
        print ("")
        self.DB.change_collection('exercises')
        exercise_ko = True
        while exercise_ko:
            e = input ("Inserisci l'esercizio: ")
            exercise = self.DB.read_single_document({"name":e})
            if exercise == None:
                print ("Esercizio non presente")
            else:
                exercise_ko = False    
        serie_ko = True        
        while serie_ko:        
            s = input ("inserisci le serie: ")
            if s.isdigit():
                s = int(s)
                serie_ko = False
            else:
                print ("Sono ammessi solo valori numerici")   
        rip_ko = True
        while rip_ko:         
            r = input ("inserisci le ripetizioni: ")
            if r.isdigit():
                r = int(r)
                rip_ko = False
            else:
                print ("Sono ammessi solo valori numerici") 
        rec_ko = True
        while rec_ko:        
            rc = input ("inserisci il recupero (in secondi): ")
            if rc.isdigit():
                rc = int(rc)
                rec_ko = False
            else:
                print ("Sono ammessi solo valori numerici")
        return e,s, r, rc, exercise['_id']
    
    def menu_assign_workout(self):
        print ("")
        self.DB.change_collection('workout_plans')
        sk_ko = True
        while sk_ko:
            sk = input("inserisci il nome della scheda: ")
            scheda = self.DB.read_single_document({"name":sk})
            if scheda == None:
                print("Scheda non trovata")
            else:
                sk_ko = False    
        self.DB.change_collection('users') 
        u_ko = True
        while u_ko:       
            u = input ("Inserisci username dell'atleta: ")
            us = self.DB.read_single_document({"username":u, "role": "athlete"})
            if us == None:
                print("Atleta non trovato")
            else:
                u_ko = False
        return scheda['_id'], us['_id']
    
    def menu_athlete(self):
        print ("\n       Menu Atleta   ")
        print ("1 - Lista schede assegnate")
        print ("2 - Visualizza scheda")
        print ("3 - Inizia allenamento")
        print ("4 - Visualizza storico allenamento")
        print ("0 - Esci")
        scelta = input ("Scegli un'operazione: ")
        return scelta    
    

class userGym: 
    def __init__(self, DB, M): 
        self.DB = DB
        self.M = M

    def admin_new_user(self):
        userm, name, role = self.M.menu_new_user()
        pwd = 'pwd' #imposto una password di default per i nuovi utenti
        self.DB.insert_one_document({"username": userm, "password_hash": bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()), "change_pwd": True,"role":role, "name": name })  

    def admin_del_user(self):
        userm = self.M.menu_username()    
        doc = self.DB.read_single_document({"username":userm})
        if doc == None:
            print ("User non trovata")
        else:
            self.DB.delete_one_document({"username": userm})     

    def admin_reset_pwd(self):
        userm = self.M.menu_username()
        doc = self.DB.read_single_document({"username":userm})
        #print(doc)
        if doc == None:
            print ("User non trovata")   
        else:    
            pwd = 'pwd' #imposto una password di default
            self.DB.update_one_document({"username":userm}, {"$set":{"password_hash":bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()),"change_pwd": True }})            

    def lista_athlete(self):
        self.DB.change_collection('users')
        docsAthl = self.DB.read_multiple_document({"role":"athlete"})
        print ("\nAtleti:")
        i = 0
        for docA in docsAthl:
            if i == 0:
                i = 1
            print (f"nome: {docA['name']} - user {docA['username']}")

        if i == 0:
            print("Non ci sono atleti")    

    def trainer_new_workout(self):
        self.DB.change_collection('workout_plans')
        sk_ko = True
        while sk_ko:
            wk_name = input ("\nInserisci un nome per la scheda: ")
            sk = self.DB.read_single_document({'name': wk_name})
            if sk == None:
                sk_ko = False
            else:    
                print("Nome scheda già esitente")

        new_workout = {"name": wk_name, "created_by": user['_id'], "assigned_to": [], "exercises": []}
        continua = 'S'
        while continua.upper() == 'S':
            exercise, sets, reps, rest, ex_id = self.M.menu_new_workout()
            esercizio = {"exercise_id": ex_id, "sets": sets, "reps": reps, "rest": rest}
            new_workout['exercises'].append(esercizio)   
            continua_ko = True
            while continua_ko:        
                continua = input("Vuoi inserire un'altro esercizio? (S/N): ")
                if continua.upper() in {"S", "N"}:
                    continua_ko = False
                else:
                    print("Sono ammessi solo i valori S/N")    

        self.DB.change_collection('workout_plans')
        self.DB.insert_one_document(new_workout)            
        #print(new_workout)

    def trainer_assign_workout(self):
            wk_id, ath_id = self.M.menu_assign_workout()
            self.DB.change_collection('workout_plans')
            self.DB.update_one_document({"_id": wk_id}, {"$push":{"assigned_to": ath_id }}) 

    def lista_workout(self, id_athl):
        self.DB.change_collection('workout_plans')
        docswk = self.DB.read_multiple_document({"assigned_to": id_athl}, {"_id":0, "name": 1})       
        i = 0
        for docW in docswk:
            if i == 0:
                print ("\nSchede:")
                i = 1
            print (docW['name'])

        if i == 0:
            print ("Non sono presenti schede assegnate a te") 

    def view_workout(self, id_athl):
        self.DB.change_collection('workout_plans')
        wkname = input ("\nInserisci il nome della scheda: ")
        pipeline = [
                    {
                            '$match': {
                                'assigned_to': {
                                    '$elemMatch': {
                                        '$eq': id_athl
                                    }
                                }, 
                                'name': wkname
                            }
                        }, {
                            '$unwind': {
                                'path': '$exercises'
                            }
                        }, {
                            '$lookup': {
                                'from': 'exercises', 
                                'localField': 'exercises.exercise_id', 
                                'foreignField': '_id', 
                                'as': 'esercizio'
                            }
                        }, {
                            '$lookup': {
                                'from': 'users', 
                                'localField': 'created_by', 
                                'foreignField': '_id', 
                                'as': 'trainer'
                            }
                        }, {
                            '$project': {
                                '_id': 0,
                                'name': 1, 
                                'trainer.name': 1, 
                                'esercizio': 1, 
                                'exercises': 1
                            }
                        }
                    ]
        schede = self.DB.read_aggregate_document(pipeline) 
        i = 0
        for scheda in schede:
            if i == 0:
                print ("\nNome Scheda: ", scheda['name'])
                print ("Assegnata da: ", scheda['trainer'][i]['name'])
                i = 1

            print ("\nEsercizio: ", scheda['esercizio'][0]['name'] ) 
            print ("Gruppo muscolare: ", scheda['esercizio'][0]['muscle_group'] )   
            print ("Tipo: ", scheda['esercizio'][0]['type'] ) 
            print ("Serie: ", scheda['exercises']['sets'])
            print ("Ripetizioni: ", scheda['exercises']['reps'])
            print ("Recupero (in secondi): ", scheda['exercises']['rest'])
            #print(scheda)

        if i == 0:
            print("Scheda non trovata")

    def start_training(self, id_athl):
        self.DB.change_collection('workout_plans')
        wkname = input ("\nInserisci il nome della scheda: ")
        pipeline = [
                    {
                            '$match': {
                                'assigned_to': {
                                    '$elemMatch': {
                                        '$eq': id_athl
                                    }
                                }, 
                                'name': wkname
                            }
                        }, {
                            '$unwind': {
                                'path': '$exercises'
                            }
                        }, {
                            '$lookup': {
                                'from': 'exercises', 
                                'localField': 'exercises.exercise_id', 
                                'foreignField': '_id', 
                                'as': 'esercizio'
                            }
                        }, {
                            '$project': {
                                'name': 1, 
                                'esercizio': 1, 
                                'exercises': 1
                            }
                        }
                    ]
        schede = self.DB.read_aggregate_document(pipeline) 
        i = 0
        for scheda in schede:
            if i == 0:
                print ("\nNome Scheda: ", scheda['name'])
                print ("Inizio allenamento!")
                i = 1
                continua = 'S'
                current_date = datetime.now()
                session = {"user_id": id_athl, "date": current_date, "plan_id": scheda['_id'], "logs": []}
                #print(session)
            else:
                continua_ko = True
                while continua_ko:        
                    continua = input ("\nVuoi proseguire con il prossimo esercizio? (S/N): ")  
                    if continua.upper() in {"S", "N"}:
                        continua_ko = False
                    else:
                        print("Sono ammessi solo i valori S/N")   

            if continua.upper() == 'N':
                break              

            print ("\nEsercizio: ", scheda['esercizio'][0]['name'] ) 
            print ("Gruppo muscolare: ", scheda['esercizio'][0]['muscle_group'] )   
            print ("Tipo: ", scheda['esercizio'][0]['type'] ) 
            print ("Serie: ", scheda['exercises']['sets'])
            print ("Ripetizioni: ", scheda['exercises']['reps'])
            print ("Recupero (in secondi): ", scheda['exercises']['rest'])
            #print(scheda)
            for j in range(1,scheda['exercises']['sets'] + 1):
                print("\nSerie: ",j)
                reps_ko = True
                while reps_ko:        
                    inp_reps = input("Inserisci il numero di ripetizioni: ")
                    if inp_reps.isdigit():
                        inp_reps = int(inp_reps)
                        reps_ko = False
                    else:
                        print ("Sono ammessi solo valori numerici")

                kg_ko = True
                while kg_ko:        
                    inp_kg = input("Inserisci il numero di kg sollevati: ")
                    if inp_kg.isdigit():
                        inp_kg = int(inp_kg)
                        kg_ko = False
                    else:
                        print ("Sono ammessi solo valori numerici")

                log = {"exercise_id": scheda['exercises']['exercise_id'], "set_index": j, "reps_performed": inp_reps, "load_kg": inp_kg}
                session['logs'].append(log)  
                #print(session)                 

        if i == 0:
            print("Scheda non trovata")
        else:
            print ("\nAllenamento terminato!")   
            self.DB.change_collection('sessions')
            self.DB.insert_one_document(session)     

    def log_training(self, id_athl, tms):
        max_tms = tms.replace(hour=23,minute=59,second=59,microsecond=999999)
        self.DB.change_collection('sessions')
        pipeline = [
                        {
                            '$match': {
                                'date': {
                                    '$gte': tms, 
                                    '$lte': max_tms
                                }, 
                                'user_id': id_athl
                            }
                        }, {
                            '$unwind': {
                                'path': '$logs'
                            }
                        }, {
                            '$lookup': {
                                'from': 'workout_plans', 
                                'localField': 'plan_id', 
                                'foreignField': '_id', 
                                'as': 'scheda'
                            }
                        }, {
                            '$lookup': {
                                'from': 'exercises', 
                                'localField': 'logs.exercise_id', 
                                'foreignField': '_id', 
                                'as': 'esercizio'
                            }
                        }, {
                            '$project': {
                                '_id': 0, 
                                'scheda.name': 1, 
                                'esercizio': 1, 
                                'logs': 1
                            }
                        }
                    ]
        logs = self.DB.read_aggregate_document(pipeline) 
        name_sk = None
        for log in logs:
            #print(log)
            if name_sk != log['scheda'][0]['name']:
                print ("\nNome Scheda: ", log['scheda'][0]['name'])
                name_sk = log['scheda'][0]['name']

            if log['logs']['set_index'] == 1:
                print ("\nEsercizio: ", log['esercizio'][0]['name'] ) 
                print ("Gruppo muscolare: ", log['esercizio'][0]['muscle_group'] )   
                print ("Tipo: ", log['esercizio'][0]['type'] ) 

            print ("Serie: ", log['logs']['set_index'])
            print ("Ripetizioni effettuate: ", log['logs']['reps_performed'])
            print ("kg sollevati: ", log['logs']['load_kg'])
            

        if name_sk == None:
            print("Nessun allenamento trovato in quella data")


def acquisisci_data():   
    while True:
        data_str = input("Inserisci la data dell'allenamento nel formato (GG/MM/AAAA): ")
        
        try:
            # Conversione
            data_tms = datetime.strptime(data_str, "%d/%m/%Y")           
            return data_tms
            
        except ValueError:
            print("\nIl formato inserito non è valido. Formato data(GG/MM/AAAA)")
             

#-----------------------------------------------------------------------------------------------------------------------

dbGYM = DatabaseManager('mongodb://root:Latitante@localhost:27017/','GymDB') 
dbGYM.change_collection('users')

print ("Benvenuto in FitApp\nper iniziare fai il login")
# controllo utenza e password
login_ok = False
for i in range(3):
    username = input ("\nInserisci la tua user: ")
    pwd = getpass.getpass ("Inserisci la password: ") # la password digitata non è visibile a video

    user = dbGYM.read_single_document({"username":username})
    #print (user)
    if user == None:
        print ("User non trovata")
    else:
        if bcrypt.checkpw(pwd.encode('utf-8'), user['password_hash']):
           # print ("pwd ok")
            print ('\nCiao', user['name'])
            login_ok = True
            # se primo accesso chiedo di modificare la password
            if user['change_pwd']:
                pwd = getpass.getpass ("Primo accesso, modifica la password: ") # la password digitata non è visibile a video
                dbGYM.update_one_document({"username":username}, {"$set":{"password_hash":bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()),"change_pwd": False }})

            break
        else:
            print("Password errata")

if login_ok:
    m = Menu(dbGYM)
    while True:
        # gestione Menu admin
        if user['role'] == 'admin':
            dbGYM.change_collection('users')
            s = m.menu_admin()
            userA = userGym(dbGYM, m)
            #inserimeto nuovo utente
            if s == '1':
                userA.admin_new_user()
            #cancellazione utente
            elif s == '2':
                userA.admin_del_user()
             #reset password       
            elif s == '3':
                userA.admin_reset_pwd()     
            elif s == '0':
                print ("Esco")
                break
            else:
                print ("Scelta errata")
        # gestione Menu trainer        
        elif user['role'] == 'trainer':  
            userA = userGym(dbGYM, m)
            s = m.menu_trainer()  
            if s == '1':    
                #lista atleti     
                userA.lista_athlete()
            elif s == '2':
                #creazione nuova scheda
                userA.trainer_new_workout()
            elif s == '3':
                #assegnazione scheda
                userA.trainer_assign_workout()
            elif s == '0':
                print ("Esco")
                break
            else:
                print ("Scelta errata")
        # gestione Menu athlete
        elif user['role'] == 'athlete':  
            userA = userGym(dbGYM, m)
            s = m.menu_athlete()  
            if s == '1':
                #lista schede
                userA.lista_workout(user['_id'])
            elif s == '2':
                #visualizza dettaglio scheda
                userA.view_workout(user['_id'])
            elif s == '3':
                #inizia allenamento
                userA.start_training(user['_id'])    
            elif s == '4':
                #Visualizza storico allenamento
                dtms = acquisisci_data()    
                userA.log_training(user['_id'], dtms)
            elif s == '0':
                print ("Esco")
                break
            else:
                print ("Scelta errata")    
        else:
            print (f"Ruolo {user['role']} non gestito")       
            break

dbGYM.close()