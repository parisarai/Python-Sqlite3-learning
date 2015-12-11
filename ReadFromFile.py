import sqlite3, csv
#connecting with database,creating string (NOT unicode) and creating a cursor 
conn = sqlite3.connect('Student.db')
conn.text_factory = str
c = conn.cursor()
#creating a table Student with 5 columns
c.execute(''' CREATE TABLE IF NOT EXISTS Student (Roll int Primary key, Name char, Address char(50), MarksI real, MArksII real);''');
#Reading Student.csv file 
reader = csv.reader(open('Student.csv',"rb"),delimiter=' ')
#inserting every row as a tuple in the table Student
for row in reader:
    c.execute('INSERT INTO Student values (?,?,?,?,?)',(row[0],row[1],row[2],row[3],row[4]));
#Printing the rows
db=c.execute("SELECT * FROM Student");
for row in db:
    print row[0],' ',row[1],' ',row[2],' ',row[3],' ',row[4],'\n'

conn.commit()
conn.close()
