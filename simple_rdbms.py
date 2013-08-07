#Get the first character in a string
def getFirstCharacter(string):
    return string[0]

#Returns the element at the specified index in the list
def getElement(iset,index):
    lst = list(iset)
    return lst[index]

#Removes duplicate entries in the list
def removeDups(lst):
    lst = list(lst)
    for x in lst:
        if lst.count(x) > 1:
            x = ''
    lst = filter(lambda x: not x == '',lst)

#Determines if two lists have an intersection
def hasCommon(lst,lst1):
    set1,set2 = set(lst),set(lst1)
    return not set1.isdisjoint(set2)
    
#Returns the Cartesian Product of two sets
def cartesian_product(set1,set2):
    lst1,lst2 = list(set1),list(set2)
    result = [x + y for x in lst1 for y in lst2 if hasCommon(x,y)]
    for x in result:
        removeDups(x)
    result = set([tuple(x) for x in result])
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
    def getTable(self):
        return self.__table

    #Returns the name of the table
    def getName(self):
        return self.__name

    #Returns the names of the columns 
    def getHeadings(self):
        return self.__headings

    #Allows one to view the table
    def display(self):
        lst = list(self.__table)
        print lst

    #Inserts a record in the table
    def insert(self,row):
        if not len(row) == self.__ncols:
            print "Tuple is not of the correct length"
        else:
            self.__table.add(row)

    
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

    #Sets up and "runs" a simple join
    def join(self,t,name="join_query"):
        tab,tab1 = self.__table,t.getTable()
        headings = self.__headings + t.getHeadings()
        result = cartesian_product(tab,tab1)
        result = Table(name,headings,result)
        return result

    def union(self,t,name="union_query"):
        tab,tab1 = self.__table,t.getTable()
        if not tab.getHeadings() == tab1.getHeadings():
            return "Cannot union these tables"
        result = tab.union(tab1)
        result = Table(name,self.__headings,result)
        return result

#Represents a view that would be found in standard RDBMS's
class View:
    def __init__(self,name,table):
        self.__table = table
        self.__name = name

    def display(self):
        self.__table.display()



#Represents the Simple_RDBMS system
class Database:
    def __init__(self,tables=dict()):
        self.__tables = tables
        self.__queries = dict()
        self.__views = dict()

    #Create a new table
    def createTable(self,name,headings):
        tab = Table(name,headings)
        self.__tables[name] = tab

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

    #Get the index of the specified attribute in the table
    def getAttr(self,table_name,attr_name):
        if not self.getTable(table_name) == -1:
            return self.getTable(table_name).attr[attr_name]
        return "Table does not exist: ",table_name
    
    #Run a select query on the table
    def select_query(self,table_name,cond,heading_lst,name="select_query"):
        if not self.getTable(table_name) == -1:
            tab = self.getTable(table_name).select(cond,heading_lst,name)
            self.__queries[name] = tab
            return tab
        return "Table does not exist: ",table_name

    #Run an insert query on the table
    def insert_query(self,table_name,row):
        if not self.getTable(table_name) == -1:
            self.getTable(table_name).insert(row)
        else:
            print "Table does not exist: ",table_name

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
        if not self.getTable(table_name) == -1:
            self.__tables.pop(table_name)
            print "Table dropped: ",table_name
        else:
            print "Table does not exist: ",table_name
        
