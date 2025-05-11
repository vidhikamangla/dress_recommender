from .baseAgent import baseAgent
import ast
from WebScraping.baseScraper import executeBase

class scraperAgent(baseAgent):
    def __init__(self):
        super().__init__(name="scraper", instructions="""                                
                         """)
 
    async def run(self,messages : list):
        content = messages
        min_range = content["min_range"]
        max_range = content["max_range"]
        gender = content["gender"]
        dress_types_list = ast.literal_eval(content["result"][0]["content"])
        text = {
            "dress types" : dress_types_list,
            "price range" : {
                "min_range" : min_range,
                "max_range" : max_range
            },
            "gender" : gender
        }
        
        dressResults = executeBase(text)
        # print('DRESS RESULTS',dressResults)
        return {
            "dress_types" : dress_types_list,
            "gender" : gender,
            "min_range" : min_range,
            "max_range" : max_range
        }
        
        

        
        