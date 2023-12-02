import requests
import time


debugMsgOn = False



# interface    
############################################################################
class priceInterface():
    
    def __init__(self ):
        pass
    
    def getPrice(self, date : str, coinId : str ):
        pass    
         
         
# coingecko    
############################################################################
class priceCoingecko(priceInterface):  
    
    coins = {   "Azero": "aleph-zero",
                "Fort" : "forta",
                "Tara" : "taraxa"
                }
    
    def getPrice(self, date : str, coinId : str, currency : str ):
        #get price of a coin at a time
        url = f'https://api.coingecko.com/api/v3/coins/{self.coins[coinId]}/history/?date={date}'
        if debugMsgOn:
            print(url)
        y = requests.get(url).json()
        
        time.sleep(7)
        
        if 'market_data' in y:
            price = y['market_data']['current_price'][currency.lower()]
        else:
            price = 0
            print( coinId, currency, date, ': no price found'  )
        
        return price
    
    
    
    