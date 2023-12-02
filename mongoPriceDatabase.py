
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from datetime import timedelta
from cryptoPrice import *
from loggerConfig import setup_logger

logger = setup_logger()

class mongoPriceDatabase():

    client : MongoClient
    currencies : []
    cryptos : []
    priceInterface : priceInterface
    
    #constructor
    #**************************************************************+
    def __init__(self, uri : str, currencies: [],cryptos : [], priceInterface : priceInterface ):
        self.cryptos = cryptos
        self.currencies = currencies
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.priceInterface = priceInterface
        
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
            logger.info( "Pinged your deployment. You successfully connected to MongoDB!") 
        except Exception as e:
            logger.error( e)

    # method to run database in thread
    #**************************************************************
    def run(self):
        self.initDatabase()
        while 1:
            self.checkForNewPrice()
            
    #get a single price
    #**************************************************************
    def getPrice(self, coin : str, currency : str, date : str ):
        myDB = self.client[coin]
        myCollection = myDB[currency]
        findDocument = { "_id": date }
        foundDocument = myCollection.find_one( findDocument )
        if foundDocument:
            logger.info(  "%s %s %s Document found: %s", coin, currency, date, foundDocument ) 
            field_value = foundDocument.get('Price')
            return field_value
        else:
            logger.info(  "%s %s %s Document not found ", coin, currency, date ) 
            return '0'
            
            
    # check database if coin price exists and update if not
    #**************************************************************
    def initDatabase(self):
        #log update time
        updateBeginTime = datetime.now()
        logger.info( "Start initialise database %s", updateBeginTime  )
        
        
        startDate = datetime(2023, 12 ,1 )
        endDate = datetime.now()
        delta = timedelta(days=1)
        currentDate = startDate

        #check 1.1.2022 until now
        while currentDate <= endDate: 
            self.checkDatabase( currentDate.strftime( "%d-%m-%Y" ) )   
            currentDate += delta
            
            
        updateEndTime = datetime.now()
        logger.info( "Finished initialise database: %s", updateEndTime  )
        logger.info( "Required initialise time: %s", updateEndTime-updateBeginTime )


    #wait one day then check for prices
    #**************************************************************
    def checkForNewPrice(self):
        logger.info( "Waiting..." )
        time.sleep(3600*12)
        logger.info( "Updating database" )
        self.checkDatabase( datetime.now().strftime( "%d-%m-%Y" ) )  


    # check single day of database if coin prices exists and update if not
    #**************************************************************
    def checkDatabase(self, date : str):
            #check all cryptos
            for i in self.cryptos:
                myDB = self.client[i]
                #check all currencies
                for j in self.currencies:
                    myCollection = myDB[j]
                    findDocument = { "_id": date }
                    foundDocument = myCollection.find_one( findDocument )
                    if foundDocument:
                        logger.debug( "%s, %s, Document found: %s", i, j, foundDocument ) 
                        field_value = foundDocument.get('Price')
                        if field_value == '0':
                            newPrice = self.priceInterface.getPrice( date=date, coinId=i, currency=j )
                            if newPrice > 0:
                                newValues = { "$set": { "_id": date, "Price" : str(newPrice) }}
                                myCollection.update_one(foundDocument, newValues)
                                logger.info( "%s %s Updated Document: %s", i, j, newValues )
                    else:
                        logger.info("%s %s Document not found: %s", i, j, findDocument  )
                        newPrice = self.priceInterface.getPrice( date=date, coinId=i, currency=j )
                        if newPrice > 0:
                            newDocument = { "_id": date, "Price" : str(newPrice) }
                            myCollection.insert_one( newDocument )
                            logger.info( "%s %s Added Document: %s", i, j, newDocument )
                            
                            
                            
                            
                            
                            
                            
            
            
 
            
            
        

            

    
    