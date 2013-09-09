from simple_rdbms import *
from interpreter import *

sdb = SimpleRDBMS() #Singleton RDBMS
bc = BackupCreator()
visitor = Visitor(sdb,bc)

#Start up the interpreter
interpreter(visitor)
