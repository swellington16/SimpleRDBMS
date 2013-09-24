import re
from simple_rdbms import *


#-------------terminals-------------
NAME = "[a-zA-Z0-9_\*]+"
ENTRY = "[a-zA-Z0-9_\'\*]+"
TYPE = "(INT|STR|FLOAT|LONG)"
FILENAME = "([a-zA-Z]:)*[a-zA-Z0-9_/-]+(\.[a-zA-Z]+)"
SDB_FILENAME = "([a-zA-Z]:)*[a-zA-Z0-9_/-]+(\.sdb)"


#COMMAND KEYWORDS
CALL_OP = "(CALL)"
CREATE_OP = "(CREATE)"
INSERT_OP = "(INSERT)"
SELECT_OP = "(SELECT)"
DELETE_OP = "(DELETE)"
FROM_OP = "(FROM)"
WHERE_OP = "(WHERE)"
INTO_OP = "(INTO)"
JOIN_OP = "(FULL|INNER) (JOIN)"
UPDATE_OP = "(UPDATE)"
SET_OP = "(SET)"
TO_OP = "(TO)"
SHOW_OP = "(SHOW ALL)"
DISPLAY_OP = "(DISPLAY)"
COND_OP = "(EQUALS|GREATER|LESS|GREATER_EQUAL|LESS_EQUAL)"
DUMP_OP = "(DUMP)"
EXIT = "(EXIT)"

#OBJECT KEYWORDS
DB_OBJECT = "(DATABASE|TABLE|VIEW|QUERY)"
DB_OP = "(USE|CREATE|DROP)"
DB_OBJ_TABLE = "(TABLE)"
DB_OBJ_VIEW = "(VIEW)"




#-------------non-terminals--------------------
column = "(\["+NAME+","+TYPE+"\])"
call_stmt = CALL_OP+" "+SDB_FILENAME
db_obj_stmt = DB_OP+" "+DB_OBJECT+" "+NAME
show_obj_stmt = SHOW_OP+" "+DB_OBJECT
create_tab_stmt = CREATE_OP+" "+DB_OBJ_TABLE+" "+NAME+" ("+column+" )*"+column
create_view_stmt = CREATE_OP+" "+DB_OBJ_VIEW+" "+NAME+" "+NAME+" "+NAME
insert_tab_stmt = INSERT_OP+" "+INTO_OP+" "+NAME+" ("+ENTRY+" )*"+ENTRY
select_tab_stmt = SELECT_OP+" ("+NAME+" )*"+FROM_OP+" "+NAME+"( "+WHERE_OP+" "+NAME+" "+COND_OP+" "+NAME+")*"
delete_stmt = DELETE_OP+" "+FROM_OP+" "+NAME+" "+WHERE_OP+" "+NAME+" "+COND_OP+" "+NAME
update_stmt = UPDATE_OP+" "+DB_OBJ_TABLE+" "+NAME+" "+SET_OP+" "+NAME+" "+TO_OP+" "+NAME+"( "+WHERE_OP+" "+NAME+" "+COND_OP+" "+NAME+")*"
join_stmt = JOIN_OP+" "+NAME+" "+NAME+" "+NAME
dump_stmt = DUMP_OP+" "+SDB_FILENAME

stmt = "("+call_stmt+"|"+db_obj_stmt+"|"+show_obj_stmt+"|"+create_tab_stmt+\
       "|"+create_view_stmt+"|"+insert_tab_stmt+"|"+select_tab_stmt+"|"+join_stmt+\
       "|"+delete_stmt+"|"+update_stmt+"|"+dump_stmt+")(;)"


SELECT_QUERY_ID_NUM = 0

#Abstract Syntax Tree classes
class ASTNode:
    def __init__(self,exp):
        self.exp = exp

    def getExp(self):
        return self.exp

    def accept(self,visitor):
        visitor.visit(self)

class ASTProgram(ASTNode):
    def accept(self,visitor):
        visitor.visitProgram(self)

class ASTStmt(ASTNode):
    def accept(self,visitor):
        visitor.visitStmt(self)

class ASTCallStmt(ASTNode):
    def accept(self,visitor):
        visitor.visitCallStmt(self)

class ASTCreateTabStmt(ASTNode):
    def accept(self,visitor):
        visitor.visitCreateTabStmt(self)
        
class ASTCreateViewStmt(ASTNode):
    def accept(self,visitor):
        visitor.visitCreateViewStmt(self)

class ASTShowObjStmt(ASTNode):
    def accept(self,visitor):
        visitor.visitShowStmt(self)

class ASTDBObjStmt(ASTNode):
    def accept(self,visitor):
        visitor.visitDBObjStmt(self)

class ASTInsertTabStmt(ASTNode):
    def accept(self,visitor):
        visitor.visitInsertTabStmt(self)

class ASTSelectTabStmt(ASTNode):
    def accept(self,visitor):
        visitor.visitSelectTabStmt(self)

class ASTDeleteStmt(ASTNode):
    def accept(self,visitor):
        visitor.visitDeleteStmt(self)

class ASTUpdateStmt(ASTNode):
    def accept(self,visitor):
        visitor.visitUpdateStmt(self)

class ASTJoinStmt(ASTNode):
    def accept(self,visitor):
        visitor.visitJoinStmt(self)

class ASTDumpStmt(ASTNode):
    def accept(self,visitor):
        visitor.visitDumpStmt(self)

class ASTExitStmt(ASTNode):
    def accept(self,visitor):
        visitor.visitExitStmt(self)
    

#Visitor for the Abstract Syntax Tree
class Visitor:
    def __init__(self,sdb,bc):
        self.__status = 1
        self.sdb = sdb
        self.bc = bc
        self.db = Database("dummy_database")

    #Determines if the visitor is still "visiting"
    def getStatus(self):
        return self.__status

    #Shows that the visitor is "visiting"
    def changeStatus(self):
        self.__status = 1

    #Saves the commands entered into the interpreter for later dumping
    def preserve(self,command):
        self.bc.append(command)

    def visit(self,node):
        pass

    def visitProgram(self,node):
        exp = node.getExp()
        #print exp #debugging
        stmts = exp.split(";")
        #print "Statements: ",stmts #debugging
        true_stmts = filter(lambda x: not x == '' and not hasLastChar(x,'\n'),stmts)
        #print "Number of semicolons: ",exp.count(";") #debugging
        #print "Number of statements: ",len(true_stmts) #debugging
        if (not exp.count(";") == len(true_stmts)):
            print "Syntax error"
        else:
            for i in range(len(stmts)):
                stmts[i] = stmts[i].strip()
            stmts = filter(lambda x: not x == '', stmts)
            #print "Statements in program: ",stmts #debugging
            for stmt in stmts:
                #print "Program statement: ",stmt #debugging
                ASTStmt(stmt).accept(self)


    def visitStmt(self,node):
        stmt_input = node.getExp()
        node = stmt_input.split(" ")
        #print "Statement input: ",stmt_input #debugging
        #print "Nodes: ",node #debugging
        
        #Matches the entered string with any known pattern
        call_stmt_matcher = re.match(call_stmt,stmt_input)
        db_obj_stmt_matcher = re.match(db_obj_stmt,stmt_input)
        show_stmt_matcher = re.match(show_obj_stmt,stmt_input)
        create_tab_stmt_matcher = re.match(create_tab_stmt,stmt_input)
        create_view_stmt_matcher = re.match(create_view_stmt,stmt_input)
        insert_tab_stmt_matcher = re.match(insert_tab_stmt,stmt_input)
        select_tab_stmt_matcher = re.match(select_tab_stmt,stmt_input)
        delete_stmt_matcher = re.match(delete_stmt,stmt_input)
        update_stmt_matcher = re.match(update_stmt,stmt_input)
        join_stmt_matcher = re.match(join_stmt,stmt_input)
        dump_stmt_matcher = re.match(dump_stmt,stmt_input)
        exit_matcher = re.match(EXIT,stmt_input)

        if not call_stmt_matcher is None:
            ASTCallStmt(node).accept(self)
        elif not dump_stmt_matcher is None:
            ASTDumpStmt(node).accept(self)
        elif not create_tab_stmt_matcher is None:
            ASTCreateTabStmt(node).accept(self)
        elif not create_view_stmt_matcher is None:
            ASTCreateViewStmt(node).accept(self)
        elif not insert_tab_stmt_matcher is None:
            ASTInsertTabStmt(node).accept(self)
        elif not select_tab_stmt_matcher is None:
            ASTSelectTabStmt(node).accept(self)
        elif not delete_stmt_matcher is None:
            ASTDeleteStmt(node).accept(self)
        elif not update_stmt_matcher is None:
            ASTUpdateStmt(node).accept(self)
        elif not join_stmt_matcher is None:
            ASTJoinStmt(node).accept(self)
        elif not show_stmt_matcher is None:
            ASTShowObjStmt(node).accept(self)
        elif not db_obj_stmt_matcher is None:
            ASTDBObjStmt(node).accept(self)
        elif not exit_matcher is None:
            ASTExitStmt(node).accept(self)
        else:
            print "Syntax error"


    def visitCallStmt(self,node):
        exp = node.getExp()
        filename = exp[1]
        print "File name: ",filename
        try:
            code_file = open(filename)
            code_string = code_file.read()
            code_file.close()
            ASTProgram(code_string).accept(self)
        except IOError:
            print "File does not exist: ",filename
        
        
    def visitCreateTabStmt(self,node):
        exp = node.getExp()
        name, cols = exp[2], exp[3:]
        for i in range(len(cols)):
            lst = cols[i]
            lst1 = lst.split('[')
            lst2 = lst1[1].split(']')
            cols[i] = lst2[0].split(',')
            data_name = cols[i][0]
            data_type = cols[i][1]
            if data_type == "INT":
                cols[i] = (data_name,int)
            elif data_type == "STR":
                cols[i] = (data_name,str)
            elif data_type == "FLOAT":
                cols[i] = (data_name,float)
            elif data_type == "LONG":
                cols[i] = (data_name,long)
        self.db.createTable(name,cols)
        print "Headings of table: ",name
        print self.db.getTable(name).getHeadingsRef()
        print "\n"
        #print self.db.getTableNames()

    def visitCreateViewStmt(self,node):
        exp = node.getExp()
        name, num, view_name = exp[2], int(exp[3]), exp[4]
        self.db.createView(name,num,view_name)


    def visitInsertTabStmt(self,node):
        exp = node.getExp()
        name, values = exp[2], exp[3:]
        headingTypes = self.db.getTable(name).getHeadingTypes()

        #Accounting for spaces in string values
        for i in range(len(values)-1):
            isPartialFirst = hasFirstChar(values[i],"\'") and not hasLastChar(values[i],"\'")
            isPartialLast = hasLastChar(values[i+1],"\'") and not hasFirstChar(values[i+1],"\'")
            if isPartialFirst and isPartialLast:
                values[i] = values[i] + " " + values[i+1]
                values[i+1] = "\t"

        values = filter(lambda x: not x == "\t",values)

        for i in range(len(values)):
            isString = hasFirstChar(values[i],"\'") and hasLastChar(values[i],"\'")
            if not isString:
                if headingTypes[i] == float:
                    values[i] = float(values[i])
                elif headingTypes[i] == int:
                    values[i] = int(values[i])
                elif headingTypes[i] == long:
                    values[i] = long(values[i])
            else:
                size = len(values[i])-1
                values[i] = values[i][1:size]
                        
        values = tuple(values)
        
        print "Name: ",name
        print "Values: ",values

        self.db.insert_query(name, values)


    def visitSelectTabStmt(self,node):
        exp = node.getExp()
        columns, index = [], 1
        while not exp[index] == "FROM":
            columns.append(exp[index])
            index += 1
        tab_name = exp[index+1]
        if not exp[index+2:] == []:
            param1 = exp[index+3]
            cond = exp[index+4]
            param2 = reduce(lambda x,y: x+" "+y,exp[index+5:])
        
            attr1 = self.db.getAttr(tab_name,param1)
            if self.db.getTableHeadingType(tab_name,param1) == int:
                param2 = int(param2)
            elif self.db.getTableHeadingType(tab_name,param1) == float:
                param2 = float(param2)
            elif self.db.getTableHeadingType(tab_name,param1) == long:
                param2 = long(param2)
        
            if cond == "EQUALS":
                condition = lambda x: x[attr1] == param2
            elif cond == "GREATER":
                condition = lambda x: x[attr1] > param2
            elif cond == "LESS":
                condition = lambda x: x[attr1] < param2
            elif cond == "GREATER_EQUAL":
                condition = lambda x: x[attr1] >= param2
            elif cond == "LESS_EQUAL":
                condition = lambda x: x[attr1] <= param2
        else:
            condition = None
            
        if columns[0] == "*":
            columns = self.db.getColumnNames(tab_name)

        global SELECT_QUERY_ID_NUM

        q = self.db.select_query(tab_name,columns,condition,"select_query_"+str(SELECT_QUERY_ID_NUM))

        try:
            self.db.getQuery("select_query_"+str(SELECT_QUERY_ID_NUM)).display()
        except AttributeError:
            print "Select query had failed, or the query you are attempting to display has a different name..."
        
        SELECT_QUERY_ID_NUM += 1


    def visitDeleteStmt(self,node):
        exp = node.getExp()
        tab_name, param1, cond= exp[2], exp[4], exp[5]
        param2 = reduce(lambda x,y: x+" "+y,exp[6:])
        attr1 = self.db.getAttr(tab_name,param1)
        if self.db.getTableHeadingType(tab_name,param1) == int:
            param2 = int(param2)
        elif self.db.getTableHeadingType(tab_name,param1) == float:
            param2 = float(param2)
        elif self.db.getTableHeadingType(tab_name,param1) == long:
            param2 = long(param2)
        
        if cond == "EQUALS":
            condition = lambda x: x[attr1] == param2
        elif cond == "GREATER":
            condition = lambda x: x[attr1] > param2
        elif cond == "LESS":
            condition = lambda x: x[attr1] < param2
        elif cond == "GREATER_EQUAL":
            condition = lambda x: x[attr1] >= param2
        elif cond == "LESS_EQUAL":
            condition = lambda x: x[attr1] <= param2

        self.db.delete_query(tab_name,condition)


    def visitUpdateStmt(self,node):
        exp = node.getExp()
        tab_name,col,val = exp[2],exp[4],exp[6]
        if self.db.getTableHeadingType(tab_name,col) == int:
            val = int(val)
        elif self.db.getTableHeadingType(tab_name,col) == float:
            val = float(val)
        elif self.db.getTableHeadingType(tab_name,col) == long:
            val = long(val)

        condition = None
        
        if not exp[7:] == []:
            param1,cond = exp[8],exp[9]
            param2 = reduce(lambda x,y: x+" "+y,exp[10:])
            attr1 = self.db.getAttr(tab_name,param1)
            if self.db.getTableHeadingType(tab_name,param1) == int:
                param2 = int(param2)
            elif self.db.getTableHeadingType(tab_name,param1) == float:
                param2 = float(param2)
            elif self.db.getTableHeadingType(tab_name,param1) == long:
                param2 = long(param2)
            if cond == "EQUALS":
                condition = lambda x: x[attr1] == param2
            elif cond == "GREATER":
                condition = lambda x: x[attr1] > param2
            elif cond == "LESS":
                condition = lambda x: x[attr1] < param2
            elif cond == "GREATER_EQUAL":
                condition = lambda x: x[attr1] >= param2
            elif cond == "LESS_EQUAL":
                condition = lambda x: x[attr1] <= param2

        self.db.update_query(tab_name,col,val,condition)
        

    def visitDBObjStmt(self,node):
        exp = node.getExp()
        command, obj, name = exp[0], exp[1], exp[2]
        if command == "USE":
            self.db = self.sdb.getDatabase(name)
        elif command == "CREATE":
            if obj == "DATABASE":
                self.sdb.createDB(name)
        elif command == "DROP":
            if obj == "DATABASE":
                self.sdb.dropDB(name)
            elif obj == "TABLE":
                self.db.dropTable(name)
            elif obj == "VIEW":
                self.db.dropView(name)

    def visitShowStmt(self,node):
        exp = node.getExp()
        obj = exp[2]
        if obj == "DATABASE":
            print self.sdb.getDBNames()
        elif obj == "TABLE":
            print "Current database: ",self.db.getName()
            print self.db.getTableNames()
        elif obj == "VIEW":
            print self.db.getViewNames()
        elif obj == "QUERY":
            print self.db.getQueryNames()
        

    def visitJoinStmt(self,node):
        exp = node.getExp()
        jq = None
        command,tab1,tab2,join_name = exp[0],exp[2],exp[3],exp[4]
        if command == "FULL":
            jq = self.db.full_join_query(tab1,tab2,join_name)
        elif command == "INNER":
            jq = self.db.inner_join_query(tab1,tab2,join_name)
        jq.display()
        return jq


    def visitDumpStmt(self,node):
        exp = node.getExp()
        filename = exp[1]
        self.bc.save(filename)
        print "Interpreter input dumped to file: ",filename


    def visitExitStmt(self,node):
        exp = node.getExp()
        self.__status = 0
        print "Bye"

#Saves the string of entered interpreter commands to be "dumped"
class BackupCreator:
    def __init__(self):
        self.__commands = ""

    def append(self,command):
        self.__commands = self.__commands + command + "\n"

    def getCommands(self):
        return self.__commands

    def save(self,filename):
        f = open(filename,"a+")
        f.write(self.__commands)
        f.close()


#Interpreter program
def interpreter(visitor):
    visitor.changeStatus()
    code_input = raw_input(">>> ")
    ASTProgram(code_input).accept(visitor)

    visitor.preserve(code_input)
    
    if visitor.getStatus() == 1:
        interpreter(visitor)
