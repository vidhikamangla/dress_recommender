from .baseAgent import baseAgent
from .dressTypeAgent import dressType
from .scraperAgent import scraperAgent

class orchestratorAgent(baseAgent):
    
    def __init__(self):
        super().__init__(name="orchestrator", instructions="""
                                 
                         """)
        
        self.dressType = dressType()
        self.scraper = scraperAgent()
        
    async def run(self,messages:list):
        #our input message collected from user
        print('MESSAGES',messages)
        
        #getting the dress types after running dress type agent
        dress_types = await self.dressType.run(messages)
        print('DRESS TYPES',dress_types)
        
        scraped_content = await self.scraper.run(dress_types)
        print('SCRAPED CONTENT', scraped_content)
        
        
        return {
            "messages" : messages,
            "dresstypes" : dress_types,
            "scraped_content" : scraped_content
        }
        
        
        
        