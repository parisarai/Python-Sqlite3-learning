import sqlite3, csv, logging, ConfigParser, time

def mygen(reader):
	for row in reader:
        	yield row[0],row[1],row[2],row[3],row[4]

def writedb(reader,db):
	conn=sqlite3.connect(db)
	conn.text_factory = str
	c = conn.cursor()
	c.execute('drop table if exists try;')
	c.execute('create table try (Roll int, Name txt, Addr char(50), MarksI int, MarksII int);')
	c.executemany('Insert into try values (?,?,?,?,?);',mygen(reader))
	conn.commit()
	conn.close()

def writefile(reader,f2):
	with open(f2,"w") as file1:
		writes=csv.writer(file1, delimiter=' ', quoting=csv.QUOTE_ALL)
		writes.writerows(mygen(reader))
	
config= ConfigParser.ConfigParser()
config.read('try.ini')
dbname=config.get('Section1','dbase')
filename1=config.get('Section1','fname1')
filename2=config.get('Section2','fname2')
file1=open(filename1,"rb")
reader = csv.reader(file1, delimiter = ' ')
writedb(reader,dbname)
file1.seek(0)
writefile(reader,filename2)
