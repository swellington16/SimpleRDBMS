from simple_rdbms import *

db = Database() #The database

#students table
db.createTable("students",["sid","f_name","l_name"])
db.createTable("lecturers",["lid","f_name","l_name"])
db.insert_query("students",(620024789,"Sean","Wellington"))
db.insert_query("students",(620045678,"Crystal","Francis"))
db.insert_query("students",(620089945,"Denar","Palmer"))
db.insert_query("students",(620034569,"Brian","Long"))
db.insert_query("lecturers",(45039456,"Daniel","Coore"))

#Shortening the attributes
sid = db.getAttr("students","sid")
f_name = db.getAttr("students","f_name")
l_name = db.getAttr("students","l_name")

#The query conditions
q1 = lambda x: x[sid] == 620024789
q2 = lambda x: x[f_name] > "C"
q3 = lambda x: getFirstCharacter(x[l_name]) == "W"

#The execution of the queries and their result tables
t1 = db.select_query("students",q1,["sid","l_name"],"query_1")
t2 = db.select_query("students",q2,["sid"],"query_2")
t3 = db.select_query("students",q3,[],"query_3")  

#Creating a view
db.createView("sample_view",QUERY_VIEW,"query_3")

#Doing a full join
j1 = db.full_join_query("students","lecturers","join_query_1")

