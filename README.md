# Event‑Aware Dress Recommender 👗

An AI‑powered event advisor that recommends complete outfits for your next occasion and finds real products from Myntra, Flipkart and Tata Cliq.  
The app combines LLM “agents” with live web scraping and a Streamlit UI.

---

## 1. Features

- **Event‑aware suggestions**  
  - User specifies event type, budget range and gender.  
  - An LLM agent proposes multiple complete outfits (top, bottom, accessories, etc.).

- **Multi‑site product search**  
  - Selenium scrapers for **Myntra**, **Flipkart** and **Tata Cliq** fetch real products that match the generated outfits.  
  - Product cards show title, price, rating and a “View Product” link.

- **Interactive Streamlit UI**  
  - Step 1: Fill the event form and get personalized advice.  
  - Step 2: Select favourite outfits from a gallery of images.  
  - Step 3: View ranked product results from each e‑commerce site.
<img width="1920" height="1080" alt="Screenshot (1089)" src="https://github.com/user-attachments/assets/fc92c2da-dc67-4493-aad9-356111d7137b" />

---

## 2. Tech Stack

- **Frontend / App**: Streamlit  
- **Language**: Python 3.10+  
- **LLM Layer**:  
  - Local Ollama server exposing an OpenAI‑compatible API  
  - [`swarm`](https://pypi.org/project/swarm/) agents on top of `llama3.2:latest`
- **Web Scraping**: Selenium WebDriver + `requests`  
- **Logging**: Python `logging` → `bot_log.log`

---

## 3. Project Structure
dress_recommender/
├── Agents/
│ └── baseAgent.py # Base class for all LLM agents
├── WebScraping/
│ ├── baseScraper.py # Common Selenium + image download logic
│ ├── myntraScraper.py # Myntra‑specific scraping
│ ├── flipkartScraper.py # Flipkart‑specific scraping
│ ├── tatacliqScraper.py # Tata Cliq‑specific scraping
│ └── reviewScraper.py # Optional review / rating scraping
├── Models/ # Trained models or embeddings (if any)
├── Outputs/
│ └── dress_type_images/ # Scraped outfit images (runtime artefacts)
├── userImages/ # Uploaded user photos (runtime artefacts)
├── app.py # Streamlit entry point
├── bot_log.log # Application + scraping logs
└── dress_venv/ # Local virtual environment (ignored by git)

## 4. Typical flow:

1. **Event form**  
   - Inputs: optional image upload, event type text, budget slider, gender dropdown.  
   - Button “Get Advice” triggers the LLM agent.

2. **Outfit proposal + selection**  
   - The agent returns several outfit descriptions.  
   - For each outfit, the app shows one or more images from `Outputs/dress_type_images` plus captions.  
   - User can tick checkboxes to mark favourite outfits.

3. **Product scraping & display**  
   - For each selected outfit, call the relevant scrapers (Myntra / Flipkart / Tata Cliq).  
   - Display products in responsive columns with title, description snippet, price, rating and a clickable external link.

<img width="1920" height="1080" alt="Screenshot (1089)" src="https://github.com/user-attachments/assets/5f667bfc-cb96-4216-91f2-11ea358b916c" />
<img width="1920" height="1080" alt="Screenshot (1090)" src="https://github.com/user-attachments/assets/21b0fd8b-12ec-4b2e-b6b0-ca4637b52579" />
<img width="1920" height="1080" alt="Screenshot (1092)" src="https://github.com/user-attachments/assets/3254805c-34d8-42b5-8856-151b3aea44ce" />
<img width="1920" height="1080" alt="Screenshot (1097)" src="https://github.com/user-attachments/assets/e4c4f181-68ac-4f4f-b929-166e022af916" />
<img width="1920" height="1080" alt="Screenshot (1098)" src="https://github.com/user-attachments/assets/66a22fb7-2c4b-4122-8410-f1671933f30d" />




