# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #

import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db
NoneType = type(None)

import gensim
from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS
from gensim.parsing.preprocessing import strip_punctuation

import random

def connection():
    ''' User this function to create your connections '''
    # con = db.connect(
    #     settings.mysql_host, 
    #     settings.mysql_user, 
    #     settings.mysql_passwd, 
    #     settings.mysql_schema)

    con = db.connect(host='localhost', user='root', password='uBuntu@20.', db = 'sys') 
    return con

# Python3 code to convertcur.execute( tuple 
# into string
def convertTuple(tup):
    str =  ''.join(tup)
    return str

#delete stopwords
def delete_stopwords( text):
    # take stopwords
    all_stopwords = gensim.parsing.preprocessing.STOPWORDS
    all_stopwords = list( all_stopwords)
    result = create_ngrams( text, 1)
    j = 0
    while  j < len( result):
        find = False
        for i in range( len( all_stopwords)):
            
            if result[j] == all_stopwords[i]:
                result.pop(j)
                find = True
                break
        
        if find == False:
            j = j + 1

    #create string again
    new_text = " ".join(result)                     
    return new_text

#create ngrams
def create_ngrams( text, num):
    res = text.split()
    if num == 1:
        return res
    elif num == 2:
        result = []

        for r in range(len(res)-1):
            result.append(res[r] + " " + res[r+1])

        return result
    else:
        result = []
        
        for r in range(len(res)-2):
            result.append(res[r] + " " + res[r+1] + " " + res[r+2])

        return result

#class Word for list with words
class Word:
    
    def __init__(self, str, num):
        self.str = str
        self.num = num


def get( w):
    return w.num

def mostcommonsymptoms(vax_name):
    
    # Create a new connection
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()

    cur.execute(f"SELECT v.symptoms FROM vaccination v WHERE (v.vaccines_vax_name = '{vax_name}')")

    #num ngrams for fuctions create_ngrams
    num_ngrams = 1
    #rows where return the cur.execute from select 
    rows = cur.fetchall()
    #list with words
    result = []

    for row in rows:

        #we take the string and all character change in lower after we remove punct and stopwards and finally call 
        #create_ngrams where she create one list with words
        text = convertTuple(row)
        new_text = text.lower()
        new_text = strip_punctuation(new_text)
        new_text = delete_stopwords(new_text)
        res = create_ngrams( new_text, num_ngrams)
        
        #forloop for list res where return the function create_ngrams
        for j in range(len(res)):
            
            i = -1
            for k in range(len(result)):
                if result[k].str == res[j]:
                   i = k 

            if i == -1:
                w = Word( res[j], 1)
                result.append(w)
            else:
                w = result[i]
                w.num +=1

    #sort the table    
    result = sorted( result, key = get)
    result_finally = []
    for i in range(len(result)):
        if i >=15:
            break
        word = result[i]
        result_finally.append(word.str)
    
    #print results
    print([vax_name] + result_finally)
    
    #return results
    return [vax_name] + result_finally


def buildnewblock(blockfloor):
    
   # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    
    #if the blockfloor have free ward
    cur.execute(f"SELECT count(*) FROM block bl WHERE bl.BlockFloor = {blockfloor}")
    x = cur.fetchone()
    count = int(x[0])
    if count == 9:
        print("error")
        return "error"
    
    cur = con.cursor()
    cur.execute(f"SELECT bl.BlockCode FROM block bl WHERE bl.BlockFloor = {blockfloor}")

    c = cur.fetchone()
    new_code = 1

    #i find this ward and i crete this ward in blockfloor from input
    while new_code < 10:
        
        try:
            count_ = int(c[0])

            if count_ == new_code:
                new_code += 1
            else:
                break
        
            c = cur.fetchone()
        except TypeError:
            break

    #i add this new_code in table block
    cur = con.cursor()
    sql = f"""INSERT INTO block VALUES ({blockfloor},{new_code})"""
    try:
        # Execute the SQL command
        cur.execute(sql)
        # Commit your changes in the database
        con.commit()
    except:
        # Rollback in case there is any error
        con.rollback()
    try:
        con.commit()
    except:
        con.rollback()

    #room count
    room_num = random.randint(1,5)
    for i in range(1,room_num + 1):
        code_room = blockfloor*1000 + new_code*100 + room_num
        #i create room and i add in table room
        sql = f"""INSERT INTO room VALUES ({code_room},'NON-TYPE', {blockfloor}, {new_code} ,0)"""

        try:
            # Execute the SQL command
            cur.execute(sql)
            # Commit your changes in the database
            con.commit()
        except: 
            # Rollback in case there is any error
            con.rollback()
        try:
            con.commit()
        except:
            con.rollback() 
    
    #results
    print("ok")
    return [("result",),("ok",)] 

def findnurse(x,y):

    # Create a new connection
    
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    cur.execute(f"SELECT N.Name, N.EmployeeID, (SELECT count( distinct v.patient_SSN) AS num FROM vaccination v WHERE( v.nurse_EmployeeID = N.EmployeeID)) AS NUM_PATIENT_VACCINATION FROM nurse N WHERE( N.EmployeeID IN ( SELECT oc.Nurse FROM on_call oc WHERE (oc.BlockFloor = {x}) GROUP BY oc.Nurse HAVING ( count( distinct oc.BlockCode) = (	SELECT count(*) FROM block bl WHERE (bl.BlockFloor = {x}) ) ) ) AND {y} <= ( SELECT count(distinct ap.Patient) FROM appointment ap WHERE (ap.PrepNurse = N.EmployeeID) ) ) GROUP BY N.Name, N.EmployeeID")

    
    table = cur.fetchall()

    #print because with have ERROR 500
    print([("Nurse", "ID", "Number of patients"),] + list(table) )
    #return
    return [("Nurse", "ID", "Number of patients"),] + list(table)

def patientreport(patientName):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
    cur.execute(f"SELECT s.StayEnd, t.Name, t.Cost, ph.Name, n.Name, r.BlockFloor, r.BlockCode, r.RoomNumber FROM patient p,room r,stay s,undergoes u ,treatment t ,physician ph , nurse n WHERE (u.Physician = ph.EmployeeID AND u.AssistingNurse = n.EmployeeID AND u.stay = s.StayID AND u.Treatment = t.Code AND s.Room = r.RoomNumber AND s.Patient = p.SSN AND p.Name = '{patientName}')")
    
    table = cur.fetchall()
    
    #results
    print([("Patient","Physician", "Nurse", "Date of release", "Treatement going on", "Cost", "Room", "Floor", "Block"),] + list(table))
    return [("Patient","Physician", "Nurse", "Date of release", "Treatement going on", "Cost", "Room", "Floor", "Block"),]

# for test

patientreport("Kirlin Taylor")
# patientreport("Nicolas Craig")
# mostcommonsymptoms('PFIZER')
# findnurse(1,2)
# buildnewblock(5)
