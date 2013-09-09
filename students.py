from simple_rdbms import *

'''
This is a script to test some of the major parts of the system.
This is not meant to be used for serious work using this system.
If you wish to do something halfway serious with this, use the interpeter provided.
'''

sdb = SimpleRDBMS() #Singleton RDBMS 

sdb.createDB("UWI_DB") #Creating a new database
db = sdb.getDatabase("UWI_DB")

#students table
db.createTable("students",[("sid",int),("f_name",str),("l_name",str),("lid",int)])
db.createTable("lecturers",[("lid",int),("f_name",str),("l_name",str)])


db.insert_query("students",(620034567,"Sean","Wellington",'45039456'))
db.insert_query("students",(620045678,"Crystal","Francis",242235245))
db.insert_query("students",(620089945,"Denar","Palmer",542323323))
db.insert_query("students",(620034569,"Brian","Long",3543545))
db.insert_query("lecturers",(45039456,"Daniel","Coore"))
db.insert_query("lecturers",(3543545,"Daniel","Fokum"))

#Shortening the attributes
sid = db.getAttr("students","sid")
f_name = db.getAttr("students","f_name")
l_name = db.getAttr("students","l_name")

#The query conditions
q1 = lambda x: x[sid] == 620034567
q2 = lambda x: x[f_name] > "C"
q3 = lambda x: getFirstCharacter(x[l_name]) == "W"

#The execution of the queries and their result tables
t1 = db.select_query("students",["sid","l_name"],q1,"query_1")
t2 = db.select_query("students",["sid"],q2,"query_2")
t3 = db.select_query("students",[],q3,"query_3")  

#Creating a view
db.createView("sample_view",QUERY_VIEW,"query_3")

#Doing a full join
j1 = db.full_join_query("students","lecturers","join_query_1")

#Doing an inner join
j2 = db.inner_join_query("students","lecturers","join_query_2")


#Doing a union
u1 = db.union_query("students","lecturers","union_query_1")

