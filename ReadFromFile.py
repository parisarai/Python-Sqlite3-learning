from itertools import *
import sqlite3, csv, logging, sys, ConfigParser, time
 
def my_generator():
	yield '7','Parisa','Mumbai','50','50'
	yield '8','Rai','Pune','50','50'
def ReadFromFile():
	try:
		config= ConfigParser.ConfigParser()
		config.read('try.ini')
		except:
		print 'Please check for error in Configuration File.'
		return	

	try:
		dbname=config.get('Section1','dbase')
		filename=config.get('Section1','fname1')
		conn = sqlite3.connect(dbname)	
		conn.text_factory = str
		c = conn.cursor()
	except:
		print 'Error connecting with the database. Insert not possible'
		return

	ml=list()
	sroll=list()
	sname=list()
	saddr=list()
	sfinal=list()
	count = 0
	
	try:
		c.execute("Drop table if exists Table1;");
		c.execute('CREATE TABLE IF NOT EXISTS Table1 (Roll int, Name char, Address char(50), MarksI real, MarksII real);');
	except:
		print 'Create Table Error'

	try:
		file1=open(filename,"rb")
		reader = csv.reader(file1, delimiter = ' ')
	except:
		print 'Unable to open file for reading. Either look into the Configuration file or location of files.'

	try:
		for row in reader:
			c.execute('INSERT INTO Table1 values (?,?,?,?,?);',(row[0], row[1], row[2], row[3], row[4]));	
	except:
		print 'Insert into Table Error'

	try:
		for row in my_generator():
			c.execute('INSERT INTO Table1 values (?,?,?,?,?);',(row[0], row[1], row[2], row[3], row[4]));
	except:
		print 'Insert using Generator error'

	try:
		c.execute('PRAGMA TABLE_INFO(Table1);');
		names = [tup[1] for tup in c.fetchall()]	
		print names
	except:
		print 'Table info read error'

	db=c.execute("SELECT * from Table1;");
	for row in db:
		print row[0],row[1],row[2],row[3],row[4],'\n'
		sroll.append(row[0])
		sname.append(row[1])
		saddr.append(row[2])
		sfinal.append(row[3]+row[4])
	
	for i in izip(sroll,sname,saddr,sfinal):
		ml.append(i)
		count += 1
	print 'Rows read:', count
	
	conn.commit()
	conn.close()
	return ml

def WriteToFile(ml):
	
	try:
		config=ConfigParser.ConfigParser()
		config.read('try.ini')
		dbname=config.get('Section1','dbase')
		filename=config.get('Section2','fname2')
	except:
		print 'Please check for error in the Configuration File.'
		return	

	try:
		file1=open(filename,"w")
		writes=csv.writer(file1,delimiter=' ')
	except:
		print 'Unable to open file for writing. Either look into the Configuration file or location of files.'
		return

	try:
		conn1 = sqlite3.connect(dbname)
		conn1.text_factory = str
		final= conn1.cursor()
	except:
		print 'Error connecting with the database. Read not possible'
		return
	
	count = 0
	
	final.execute("Drop table if exists Table2;");
	final.execute('CREATE TABLE IF NOT EXISTS Table2 (Roll int, Name char, Address char(50), Totalmarks real);');
	
	for row in ml:
		final.execute('INSERT INTO Table2 values (?,?,?,?);',(row[0],row[1],row[2],row[3]));
		count +=1
	rows=final.fetchall()    
	
	writes.writerows(rows)	
	
	final.execute("PRAGMA TABLE_INFO(Table2);")
	names=[tup[1] for tup in final.fetchall()]
	print names
	
	prevtime=time.time()
	dbfinal=final.execute("SELECT * FROM Table2;");
	curtime=time.time()
	totaltime=round(curtime - prevtime)
	print 'No of rows extracted:', count
	print 'Time taken to extract the rows:', totaltime
	
	for row in dbfinal:
		print row[0],row[1],row[2],row[3],'\n'
	
	conn1.commit()
	conn1.close()
	return count

try:
	ml=ReadFromFile()
	cnt = len(ml)
	try:
		count=WriteToFile(ml)
		if count == cnt :
			print 'Success Rate: 100%'
		else :
			rate = 100 * (cnt / count)
			print 'Success Rate:', rate
	except:
		print 'Write to file Operation Aborted.'
except:
	print 'File Read Operation Aborted.'
