from .baseAgent import baseAgent
import ast
from WebScraping.myntraScraper import executeMyntraBase
from WebScraping.flipkartScraper import executeFlipkartBase
from WebScraping.tatacliqScraper import executeTatacliqBase

class multiScraperAgent(baseAgent):
    def __init__(self):
        super().__init__(name="multi_craper", instructions="""                                
                         """)
 
    async def run(self,messages : list):
        content = messages
        # print("💗 rcd msgs: ",messages)
        min_range = content["price_range"][0]
        max_range = content["price_range"][1]
        gender = content["gender"]
        selected_list = content["selected_dresses"]
        
        text = {
            "dress_types": selected_list,
            "price_range": {
                "min_range": min_range,
                "max_range": max_range
            },
            "gender": gender
        }
        print("💗formed text: ",text)
        flipkart_results=executeFlipkartBase(text)
        myntra_results=executeMyntraBase(text)
        tata_results=executeTatacliqBase(text)
        
        print("---------------------------------------------")
        print("💗getting the results: ")
        print("---------------------------------------------")
        print('🛍️MYNTRA. RESULTS',myntra_results)
        print('🛍️FLIPKART. RESULTS',flipkart_results)
        print('🛍️TATACLIQ. RESULTS',tata_results)
        print("got the results: ",text)
        
        # return(myntra_results)
        return({
            "myntra" : myntra_results,
            "flipkart" : flipkart_results,
            "tata" : tata_results
            
        })
        # return {
        #     "dress_types" : selected_list,
        #     "gender" : gender,
        #     "min_range" : min_range,
        #     "max_range" : max_range
        # }
        
        
        

        
        