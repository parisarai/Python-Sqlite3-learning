import sqlite3
from itertools import *

#Database 1 will be provideed by user, I didn't have it right now so I created one.
#Database1 is a Student's database, records, name, roll no, address, Marks in Sem1, Marks in Sem2 out of 50.
conn = sqlite3.connect('Student.db')
c = conn.cursor()
#created 4 lists to later incorporate them in the final database.
roll = list();
name = list();
addr = list();
avg=list();
#list ml[] will serve as the parameter to inserting rows in final database.
ml=list();
c.execute("DROP TABLE Student1");
#creating a table Student1 and inserting values in 3 rows
c.execute(''' CREATE TABLE Student1 (Roll int Primary key, Name char, Address char(50), MarksI real, MArksII real);''');
c.execute(''' INSERT INTO Student1 values (1, "Aaron","Florida",34,43),(2,"Ashish","California",45,46),(3,"Aashna","Malibu",43,42);''');
#Reading values and storing each column value in separate list. roll[] for roll no, name[] for name and so on.
db=c.execute("SELECT * FROM Student1");
for row in db:
	roll.append(row[0]);
	name.append(str(row[1]));
	addr.append(str(row[2]));
	avg.append((row[3]+row[4])/2);
#Since the length of all lists are going to be same, we need only length of only 1 list created in the prvious for loop
#Creating the list of tuples, ml[]
#for i in range(0,len(roll),1):
#	x=(roll[i],name[i],addr[i],avg[i])
#	ml.append(x)
for i in izip(roll,name,addr,avg):
	ml.append(i)
#dropping the original table so that we can rename the new rable by this one
c.execute("DROP TABLE Student1");
conn.commit()
conn.close()
# 2nd database being manipulated
conn=sqlite3.connect('Student.db')
conn.text_factory = str
c = conn.cursor()
#creating a table with only 4 columns as compared to 5 columns in the previous database.
c.execute(' Create table Student1 (Roll int Primary key, Name text, Address char(50), FinalMarks int);')
#inserting from ml list of tuples
c.executemany('Insert into Student1 Values (?,?,?,?)',ml)
#viewing the final database
db1 = c.execute("SELECT * FROM Student1");
for row in db1:
#	print row[0],'\t',row[1],'\t',row[2],'\t',row[3],"\n"
	print row
conn.commit()
conn.close()
