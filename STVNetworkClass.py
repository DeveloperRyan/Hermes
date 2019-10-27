import pyodbc
server = 'stvn.database.windows.net'
database = 'STVNetwork'
username = 'shpeven'
password = 'GOODFITHackGT6'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
class CustomerDataTable:
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#getters
    @staticmethod    
    def getPoints(FaceID):
        cursor.execute("SELECT Points FROM CustomerData WHERE FaceID = "+str(FaceID))
        row = cursor.fetchone()
        return str(row[0]) 

    @staticmethod    
    def getPointsLifetime(FaceID):
        cursor.execute("SELECT PointsLifetime FROM CustomerData WHERE FaceID = "+str(FaceID))
        row = cursor.fetchone()
        return str(row[0]) 
    
    @staticmethod    
    def getPurchases(FaceID):
        cursor.execute("SELECT Purchases FROM CustomerData WHERE FaceID = "+str(FaceID))
        row = cursor.fetchone()
        return str(row[0])

    @staticmethod
    def getMax():
        cursor.execute("SELECT MAX(FaceID)\nFROM CustomerData")
        row = cursor.fetchone()
        return str(row[0])
        
    @staticmethod
    def getAll():
        cursor.execute("SELECT FaceID, Points, Purchases, PointsLifetime FROM CustomerData")
        row = cursor.fetchone()
        while row is not None:
            print (str(row[0])+" "+str(row[1])+" "+str(row[2])+" "+str(row[3]))
            row = cursor.fetchone()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#setters
    @staticmethod
    def updatePoints(FaceID, newpoints):
        cursor.execute("UPDATE CustomerData\nSET Points = "+str(newpoints)+"\nWHERE FaceID = "+str(FaceID))
        cursor.commit()

    @staticmethod
    def addPoints(FaceID, addedPoints):
        cursor.execute("UPDATE CustomerData\nSET Points = "+str(int(CustomerDataTable.getPoints(FaceID))+addedPoints)+"\nWHERE FaceID = "+str(FaceID))
        cursor.execute("UPDATE CustomerData\nSET PointsLifetime = "+str(int(CustomerDataTable.getPointsLifetime(FaceID))+addedPoints)+"\nWHERE FaceID = "+str(FaceID))
        cursor.execute("UPDATE CustomerData\nSET Purchases = "+str(int(CustomerDataTable.getPurchases(FaceID))+1)+"\nWHERE FaceID = "+str(FaceID))
        cursor.commit()

    @staticmethod
    def removePoints(FaceID, removedPoints):
        cursor.execute("UPDATE CustomerData\nSET Points = "+str(int(CustomerDataTable.getPoints(FaceID))-removedPoints)+"\nWHERE FaceID = "+str(FaceID))
        cursor.commit()

    @staticmethod
    def resetPoints(FaceID):
        cursor.execute("UPDATE CustomerData\nSET Points = 0\nWHERE FaceID = "+str(FaceID))
        cursor.commit()

    @staticmethod
    def resetALLPoints():
        cursor.execute("UPDATE CustomerData\nSET Points = 0")
        cursor.commit()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#other
    @staticmethod
    def addFaceID(FaceID):
        cursor.execute("INSERT INTO CustomerData (FaceID, Points, Purchases, PointsLifetime)\nVALUES ("+str(FaceID)+",0,0,0)")
        cursor.commit()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------