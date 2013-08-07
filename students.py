from simple_rdbms import *

db = Database() #The database

#students table
db.createTable("students",["sid","f_name","l_name"])
db.createTable("lecturers",["lid","f_name","l_name"])
db.getTable("students").insert((620024789,"Sean","Wellington"))
db.getTable("students").insert((620045678,"Crystal","Francis"))
db.getTable("students").insert((620089945,"Denar","Palmer"))
db.getTable("students").insert((620034569,"Brian","Long"))

#Shortening the attributes
sid = db.getAttr("students","sid")
f_name = db.getAttr("students","f_name")
l_name = db.getAttr("students","l_name")

#The query conditions
q1 = lambda x: x[sid] == 620024789
q2 = lambda x: x[f_name] > "C"
q3 = lambda x: getFirstCharacter(x[l_name]) == "W"

#The execution of the queries and their result tables
t1 = db.select_query("students",q1,["sid","l_name"])
t2 = db.select_query("students",q2,["sid"])
t3 = db.select_query("students",q3,[])  


