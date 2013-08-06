from simple_rdbms import *

db = Database() #The database

#students table
db.createTable("students",["id","f_name","l_name"])
db.get("students").insert((620024789,"Sean","Wellington"))
db.get("students").insert((620045678,"Crystal","Francis"))
db.get("students").insert((620089945,"Denar","Palmer"))
db.get("students").insert((620034569,"Brian","Long"))

#Shortening the attributes
sid = db.get("students").attr["id"]
f_name = db.get("students").attr["f_name"]
l_name = db.get("students").attr["l_name"]

#The query conditions
q1 = lambda x: x[sid] == 620024789
q2 = lambda x: x[f_name] > "C"
q3 = lambda x: x[l_name][0] == "W"

#The execution of the queries
t1 = db.get("students").select(q1,["id","l_name"])
t2 = db.get("students").select(q2,["id"])
t3 = db.get("students").select(q3,[])  


