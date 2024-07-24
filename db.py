import mysql.connector

#connect to local database called security
#Make sure mySQL and Apache are activated on XAMPP Control Panel1
mydb = mysql.connector.connect(
host="localhost",
user="root",
passwd="",
database="security"
)
mycursor=mydb.cursor()

#add a person to 'people' table in local sql database 'security'
def add(id,name):
    sql ="INSERT INTO people(id,name) values(%s,%s)"
    val = (id,name)
    mycursor.execute(sql,val)
    mydb.commit()

