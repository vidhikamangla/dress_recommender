from .baseAgent import baseAgent
from .multiScraperAgent import multiScraperAgent

class orchestrator2Agent(baseAgent):
    
    def __init__(self):
        super().__init__(name="secondPhase", instructions="""                   
                         """)
        self.multi_scraper = multiScraperAgent()
        
    async def run(self,messages : list):

        print('🎀🎀MESSAGES new o2',messages)
        scraped1 = await self.multi_scraper.run(messages)
        print('SCRAPED--=CONTENT', scraped1)
    
        return {
            "messages" : messages
        }
    