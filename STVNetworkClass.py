import pyodbc
server = 'stvn.database.windows.net'
database = 'STVNetwork'
username = 'shpeven'
password = 'GOODFITHackGT6'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
class CustomerDataTable:
    @staticmethod
    def updatePoints(FaceID, newpoints):
        cursor.execute("UPDATE CustomerData\nSET Points = "+str(newpoints)+"\nWHERE FaceID = "+str(FaceID))
        cursor.commit()

    @staticmethod    
    def getPoints(FaceID):
        cursor.execute("SELECT Points FROM CustomerData WHERE FaceID = "+str(FaceID))
        row = cursor.fetchone()
        return str(row[0]) 

    @staticmethod
    def addPoints(FaceID, addedPoints):
        cursor.execute("UPDATE CustomerData\nSET Points = "+str(int(CustomerDataTable.getPoints(FaceID))+addedPoints)+"\nWHERE FaceID = "+str(FaceID))
        cursor.commit()

    @staticmethod
    def resetPoints(FaceID):
        cursor.execute("UPDATE CustomerData\nSET Points = 0\nWHERE FaceID = "+str(FaceID))
        cursor.commit()

    @staticmethod
    def resetALLPoints():
        cursor.execute("UPDATE CustomerData\nSET Points = 0")
        cursor.commit()

    @staticmethod
    def addFaceID(points):
        cursor.execute("INSERT INTO CustomerData (FaceID, Points)\nVALUES ("+str(int(CustomerDataTable.getMax())+1)+", "+str(points)+")")
        cursor.commit()

    @staticmethod
    def getMax():
        cursor.execute("SELECT MAX(FaceID)\nFROM CustomerData")
        row = cursor.fetchone()
        return str(row[0])
        
    @staticmethod
    def getAll():
        cursor.execute("SELECT FaceID, Points FROM CustomerData")
        row = cursor.fetchone()
        print ("Facial ID"+" "+"Points")
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()