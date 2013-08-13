import itertools
import pickle

#Get the first character in a string
def getFirstCharacter(string):
    return string[0]

#Returns the element at the specified index in the list
def getElement(iset,index):
    lst = list(iset)
    return lst[index]

#Determines if an iterable has duplicate elements
def hasDups(lst):
    spotDup = False
    lst = list(lst)
    for x in lst:
        if lst.count(x) > 1:
            spotDup = True
    return spotDup
            

#Removes duplicate entries in the list
def removeDups(lst):
    lst = list(lst)
    for x in lst:
        if lst.count(x) > 1:
            x = ''
    lst = filter(lambda x: not x == '',lst)
    return lst

#Determines if two lists have an intersection
def hasCommon(lst,lst1):
    set1,set2 = set(lst),set(lst1)
    return not set1.isdisjoint(set2)
    
#Returns the Cartesian Product of two sets
def cartesian_product(set1,set2):
    lst1, lst2 = list(set1), list(set2)
    res = [(x,y) for x in lst1 for y in lst2]
    result = set(res)
    return result
    

#Represents a table in a database
class Table:
    def __init__(self,name,headings,table=set()):
        self.__table = table
        self.__ncols = len(headings)
        self.__headings = headings
        self.__seq = [x for x in range(len(self.__headings))]
        self.__name = name  
        self.attr = dict(zip(self.__headings,self.__seq))

    #Returns the underlying set structure in the table
    def getInnerTable(self):
        return self.__table

    #Returns the name of the table
    def getName(self):
        return self.__name

    #Returns the names of the columns 
    def getHeadings(self):
        return self.__headings

    #Returns the number of columns in the table
    def getNumCols(self):
        return self.__ncols

    #Allows one to view the table
    def display(self):
        lst = list(self.__table)
        print lst

    #Inserts a record in the table
    def insert(self,row):
        if not len(row) == self.__ncols:
            print "Record is not of the correct length"
        else:
            lst = list(self.__table)
            lst.append(row)
            self.__table = set(lst)

    
    def delete(self,cond):
        lst = list(self.__table)
        lst1 = filter(cond,lst)
        s, s1 = set(lst),set(lst1)
        result = list(s.difference(s1))
        self.__table = set(result)

    #Sets up and "runs" a select query
    def select(self,cond,cols,name="select_query"):
        lst = list(self.__table)
        result = filter(cond,lst)
        if not cols == []:
            result = [tuple([x[self.attr[r]] for r in cols]) for x in result]
        sel = Table(name,cols,set(result))
        return sel

    #Sets up and "runs" a simple full join
    def full_join(self,t,name="full_join_query"):
        tab,tab1 = self.__table,t.getInnerTable()
        headings = self.__headings + t.getHeadings()
        result = cartesian_product(tab,tab1)
        res_lst = list(result)
        res_lst = [x[0] + x[1] for x in res_lst]
        result = set(res_lst)
        result = Table(name,headings,result)
        return result


    #Sets up and "runs" a simple inner join
    def inner_join(self,t,name="inner_join_query"):
        isEligible, final_lst = False,[]
        lst1, lst2 = list(self.__table), list(t.getInnerTable())
        headings = self.__headings + t.getHeadings()
        result = cartesian_product(lst1,lst2)
        res_lst = list(result)
        res_lst = [x[0] + x[1] for x in res_lst]
        for row in res_lst:
            if hasDups(row):
                final_lst.append(row)
        result = set(final_lst)
        result = Table(name,headings,result)
        return result
            
    #Sets up and "runs" a union on two tables
    def union(self,t,name="union_query"):
        tab,tab1 = self.__table,t.getInnerTable()
        if not self.getHeadings() == t.getHeadings():
            return Table(name,self.__headings,set())
        result = tab.union(tab1)
        result = Table(name,self.__headings,result)
        return result

#Represents a view that would be found in standard RDBMS's
class View:
    def __init__(self,name,table):
        self.__table = table #The table or query this view references
        self.__name = name

    def display(self):
        self.__table.display()

#Constants for views
TABLE_VIEW = 0
QUERY_VIEW = 1

#Represents a database in the Simple_RDBMS system
class Database:
    def __init__(self,name,tables=dict()):
        self.__name = name
        self.__tables = tables
        self.__queries = dict()
        self.__views = dict()

    #Returns the name of the database
    def getName(self):
        return self.__name

    #Create a new table
    def createTable(self,name,headings):
        if not self.hasTable(name):
            tab = Table(name,headings)
            self.__tables[name] = tab
        else:
            print "A table with that name already exists."


    #Create a new view that references a table or query with table_name
    def createView(self,name,table_type,table_name):
        if table_type == TABLE_VIEW:
            if self.hasTable(table_name):
                view = View(name,self.getTable(table_name))
                self.__views[name] = view
            else:
                print "Table does not exist: ",table_name
        elif table_type == QUERY_VIEW:
            if self.hasQuery(table_name):
                view = View(name,self.getQuery(table_name))
                self.__views[name] = view
            else:
                print "Query does not exist: ",table_name
        else:
            print "Invalid flag"
            

    #Determines if database has the specified table
    def hasTable(self,table_name):
        return self.__tables.has_key(table_name)

    #Determines if database has the specified query
    def hasQuery(self,query_name):
        return self.__queries.has_key(query_name)

    #Determines if database has the specified view
    def hasView(self,view_name):
        return self.__views.has_key(view_name)

    #Return the table in the database with the specified name
    def getTable(self,name):
        if self.hasTable(name):
            return self.__tables[name]
        return -1

    #Return the query in the database with the specified name
    def getQuery(self,name):
        if self.hasQuery(name):
            return self.__queries[name]
        return -1


    #Return the view in the database with the specified name
    def getView(self,name):
        if self.hasView(name):
            return self.__views[name]
        return -1

    #Get the index of the specified attribute in the table
    def getAttr(self,table_name,attr_name):
        if self.hasTable(table_name):
            return self.getTable(table_name).attr[attr_name]
        return "Table does not exist: ",table_name
    
    #Run a select query on the table
    def select_query(self,table_name,cond,heading_lst,name="select_query"):
        if self.hasTable(table_name):
            tab = self.getTable(table_name).select(cond,heading_lst,name)
            self.__queries[name] = tab
            return tab
        return "Table does not exist: ",table_name

    #Run an insert query on the table
    def insert_query(self,table_name,row):
        if self.hasTable(table_name):
            self.getTable(table_name).insert(row)
        else:
            print "Table does not exist: ",table_name


    #Run a full join query on two tables in the database
    def full_join_query(self,table1_name,table2_name,name):
        if self.hasTable(table1_name):
            if self.hasTable(table2_name):
                join_tab = self.getTable(table1_name).full_join(self.getTable(table2_name))
                self.__queries[name] = join_tab
                return join_tab
            return "Table does not exist: ",table2_name
        return "Table does not exist: ",table1_name


    #Run an inner join query on two tables in the database
    def inner_join_query(self,table1_name,table2_name,name):
        if self.hasTable(table1_name):
            if self.hasTable(table2_name):
                join_tab = self.getTable(table1_name).inner_join(self.getTable(table2_name))
                self.__queries[name] = join_tab
                return join_tab
            return "Table does not exist: ",table2_name
        return "Table does not exist: ",table1_name

    #Run a union query on two tables in the database
    def union_query(self,table1_name,table2_name,name):
        if self.hasTable(table1_name):
            if self.hasTable(table2_name):
                union_tab = self.getTable(table1_name).union(self.getTable(table2_name))
                self.__queries[name] = union_tab
                return union_tab
            return "Table does not exist: ",table2_name
        return "Table does not exist: ",table1_name
        

    #Returns a list of the names of all the tables in the database
    def getTableNames(self):
        return self.__tables.keys()

    #Returns a list of the names of all the queries in the database
    def getQueryNames(self):
        return self.__queries.keys()

    #Returns a list of the names of all the views in the database
    def getViewNames(self):
        return self.__views.keys()
    
    #Drops the table with the specified name
    def dropTable(self,table_name):
        if self.hasTable(table_name):
            self.__tables.pop(table_name)
            print "Table dropped: ",table_name
        else:
            print "Table does not exist: ",table_name


    #Drops the view with the specified name
    def dropView(self,view_name):
        if self.hasView(view_name):
            self.__views.pop(view_name)
            print "View dropped: ",view_name
        else:
            print "View does not exist: ",view_name

    #Display the table with the specified name
    def displayTable(self,table_name):
        if self.hasTable(table_name):
            self.getTable(table_name).display()
        else:
            print "Table does not exist: ",table_name
        
    #Display the specified view's table/query
    def displayView(self,view_name):
        self.__views[view_name].display()


#Represents the system itself
class SimpleRDBMS:
    def __init__(self):
        self.__databases = dict()

    #Determines if the system has the specified database
    def hasDB(self,db_name):
        return self.__databases.has_key(db_name)

    #Returns the database with the specified 
    def getDatabase(self,db_name):
        if self.hasDB(db_name):
            return self.__databases[db_name]
        return -1

    #Returns a list of the names of all databases in the system
    def getDBNames(self):
        return self.__databases.keys()

    #Creates a new database
    def createDB(self,db_name):
        if not self.hasDB(db_name):
            db = Database(db_name)
            self.__databases[db_name] = db
        else:
            print "A database with that name already exists."
        

    #Drops the specified database
    def dropDB(self,db_name):
        if not self.hasDB(db_name):
            self.__databases.pop(db_name)
            print "Database dropped: ",db_name
        else:
            print "Database does not exist: ",db_name

    #Saves the database management system object 
    def save(self,file_name):
        path = "C:/Users/SWELL/Desktop/"
        path = path + file_name
        pickle.dump(self, open(path,"wb"))
                    
        
