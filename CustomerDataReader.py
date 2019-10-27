import pyodbc
server = 'stvn.database.windows.net'
database = 'STVNetwork'
username = 'shpeven'
password = 'GOODFITHackGT6'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("SELECT FaceID, Points FROM CustomerData")
row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()