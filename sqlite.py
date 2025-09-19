import sqlite3

#connect to database
connection = sqlite3.connect("student.db")

#cursor object to insert and create table
cursor = connection.cursor()

#create table
table_info = """  
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25), MARKS INT)
"""

cursor.execute(table_info)

#insert record in table
cursor.execute('''insert into  STUDENT values("krish","devops","A",90)''')
cursor.execute('''Insert Into STUDENT values('John','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT values('Mukesh','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('Jacob','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''')

#display all records
print("inserted records are")
data = cursor.execute("""select * from STUDENT""")
for row in data:
    print(row)


#commit changes in db
connection.commit()
connection.close()