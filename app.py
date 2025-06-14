import streamlit as st
import asyncio
from Agents.orchestratorAgent import orchestratorAgent
from Agents.orchestrator2Agent import orchestrator2Agent
import requests
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Ask advices", layout="centered")
# Custom CSS styles
st.markdown("""
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%);
        color: #000000;
    }

    /* Sidebar title */
    .sidebar .css-1d391kg {
        font-size: 24px;
        color: #5B2C6F;
        font-weight: bold;
    }

    /* Buttons */
    .stButton > button {
        background-color: #FF69B4;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: background-color 0.3s;
    }

    .stButton > button:hover {
        background-color: #FF1493;
        color: #fff;
    }

    /* Input boxes */
    .stTextInput > div > div > input {
        background-color: #F0F8FF;
        border: 2px solid #87CEFA;
        border-radius: 8px;
    }

    .stSlider > div > div {
        background-color: #E6E6FA;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)
def display_product_card(product):
    """Display a product card with image and details"""
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            if product.get('image_url'):
                try:
                    response = requests.get(product['image_url'])
                    img = Image.open(BytesIO(response.content))
                    st.image(img, use_column_width=True)
                except:
                    st.error("Could not load image")

        with col2:
            st.subheader(product.get('name', 'Product Name'))
            if product.get('description'):
                st.caption(product['description'])
            
            # Price and Rating
            price_rating = f"**Price:** {product.get('price', 'N/A')}"
            if product.get('rating'):
                price_rating += f" | **Rating:** {product.get('rating')}"
            st.markdown(price_rating)
            
            # Product Link
            if product.get('url'):
                st.markdown(f"[View Product ↗]({product['url']})", unsafe_allow_html=True)
            
            # Reviews
            if product.get('reviews'):
                with st.expander("📝 Reviews (Click to Expand)"):
                    for review in product['reviews']:
                        if review.strip() and review != "no review available":
                            st.markdown(f"<div class='review-box'>🌟 {review}</div>", unsafe_allow_html=True)

        st.markdown("---")

def display_retailer_section(retailer_name, products):
    """Display a section for a retailer's products"""
    if not products:
        return
    
    with st.container():
        st.markdown(f"<div class='retailer-section'>", unsafe_allow_html=True)
        st.header(f"🏬 {retailer_name.capitalize()} Results")
        
        # Create columns for product cards
        cols = st.columns(3)
        product_count = 0
        
        for product_group in products:
            for product in product_group:
                if product_count >= 3:  # Only show 3 products per row
                    break
                with cols[product_count % 3]:
                    display_product_card(product)
                product_count += 1
        
        st.markdown("</div>", unsafe_allow_html=True)
        
#we are setting up the page navigation as there are multiple lages
if "page" not in st.session_state:
    st.session_state.page = "Ask advices"

#orchestrator function async
async def process_query(user_input):
    try:
        orchestrator = orchestratorAgent()
        return await orchestrator.run(user_input)
    except Exception as e:
        return {"error": str(e)}
    
async def process_secondphase(user_input):
    try:
        orchestrator2 = orchestrator2Agent()
        return await orchestrator2.run(user_input)
        
    except Exception as e:
        return {"error" : str(e)}

#sidebar for navigation
with st.sidebar:
    st.title("🧑‍💼 Event Advisor")
    st.write("Get personalized advice for your next event.")
    # Navigation button for this page
    if st.button("Ask advices", key="nav_ask_advices"):
        st.session_state.page = "Ask advices"

#main page
if st.session_state.page == "Ask advices":
    st.header("🎯 Ask for Event Advice")

    #uploading image for similar recommendations
    uploaded_image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"], key="event_image")

    #entering event type
    event_type = st.text_input("What type of event are you going to?", key="event_type")

    #price range slider for selecting outfits
    price_range = st.slider(
        "Select your preferred price range",
        min_value=0,
        max_value=10000,
        value=(1000, 5000),
        step=100,
        key="price_range"
    )

    #gender input 
    gender = st.text_input("What is your gender?", key="gender")

    #submit button
    if st.button("Get Advice", key="submit_advice"):
        if not event_type.strip():
            st.warning("Please specify the event type.")
        else:
            user_input = {
                "event_type": event_type,
                "price_range": price_range,
                "has_image": uploaded_image is not None,
                "gender": gender
            }
            if uploaded_image:
                image_path = f"./userImages/image.jpeg"
                with open(image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                user_input["image_path"] = image_path

            with st.spinner("Fetching advice..."):
                result = asyncio.run(process_query(user_input))

            if "error" in result:
                st.error(result["error"])
            else:
                st.success("Here's your personalized advice!")
                # print("----------------------------------")
                # print(result)
                # print("----------------------------------")
                # st.write(result.get("dresstypes"))
                
                #we saved the results in session state and r switching to next page to show recommendations
                st.session_state.page = "Show Images"
                st.session_state.dress_types = result.get("scraped_content").get("dress_types", [])
                st.session_state.user_gender = result.get("scraped_content").get("gender", gender)
                st.session_state.user_min_range = result.get("scraped_content").get("min_range", price_range[0])
                st.session_state.user_max_range = result.get("scraped_content").get("max_range", price_range[1])
                st.session_state.dress_types = result.get("scraped_content").get("dress_types", [])
                
                # st.session_state.gender = result.get("scraped_content").get("gender", "")
                # st.session_state.min_range = result.get("scraped_content").get("min_range", 0)
                # st.session_state.max_range = result.get("scraped_content").get("max_range", 0)
      
import os
if st.session_state.page == "Show Images":
    st.header("🖼️ Select Your Favorite Outfits")
    selected_images = []
    if "dress_types" in st.session_state:
        for idx, dress_items in enumerate(st.session_state.dress_types):
            item_paths = []
            for item in dress_items:
                item_filename = item.strip().lower().replace(' ', '_') + '.jpg'
                img_path = os.path.join(".", "Outputs", "dress_type_images", item_filename) 
                item_paths.append((item, img_path))
            print('🎀🎀🎀ITEM PATHS',dress_items, "🙏🏻🙏🏻🙏🏻",item_paths)
            if all(os.path.exists(path) for _, path in item_paths):
                st.markdown(f"**Outfit {idx+1}:**")
                checked = st.checkbox(
                    ", ".join(item for item, _ in item_paths),
                    key=f"checkbox_outfit_{idx}"
                )
                cols = st.columns(len(item_paths))
                for col, (item, path) in zip(cols, item_paths):
                    with col:
                        st.image(path, caption=item, width=150)
                if checked:
                    selected_images.append([item for item, _ in item_paths])
        if st.button("Send similar outfits"):
            user_input = {
                "price_range": (st.session_state.get("user_min_range", 0), st.session_state.get("user_max_range", 0)),
                "gender": st.session_state.get("user_gender", ""),
                "selected_dresses": selected_images
            }

            print('🎀🎀🎀SELECTED IMAGES : ',selected_images)

            result2 = asyncio.run(process_secondphase(user_input))
            
            print("💗💗result2💗💗",result2)
            st.json(result2)
            # Display results for each retailer
            if 'myntra' in result2['messages']:
                display_retailer_section("Myntra", result2['messages']['myntra'])
            
            if 'flipkart' in result2['messages']:
                display_retailer_section("Flipkart", result2['messages']['flipkart'])
            
            if 'tata' in result2['messages']:
                display_retailer_section("Tata CLiQ", result2['messages']['tata'])
            
            if st.button("Back to Search"):
                st.session_state.page = "Ask advices"
        else:
            st.warning("No results to display. Please perform a search first.")
            # if "error" in result2:
            #     st.error(result2["error"])
            # else:
            #     st.success("Here are some outfit suggestions based on your choices:")

            #     suggestions = result2.get("suggestions", [])
            #     if suggestions:
            #         for idx, suggestion in enumerate(suggestions, 1):
            #             st.markdown(f"### Suggestion {idx}")
            #             for key, value in suggestion.items():
            #                 st.write(f"{key.capitalize()}:** {value}")
            #     else:
            #         st.info("No specific suggestions were returned.")
            
            # print('🎀🎀🎀RESULT2', result2)
            # st.json(result2["messages"][-1].get("content"))
        
# result 1 format        
# {'messages': [
#     {'role': 'user',
#      'content': 
#          {'event_type': 'birthday party', 
#           'price_range': (1000, 5000), 
#           'has_image': False, 
#           'gender': 'female'}}], 
#  'dresstypes': {'result': 
#      [{'content': '[\n    ["red off-the-shoulder top", "high-waisted black jeans"],\n    ["teal sparkly dress"],\n    ["sunglasses", "pink strappy sandals"],\n    ["Grey wool blazer", "light blue t-shirt"],\n    ["beige culottes", "navy blue crop top"]\n]', 
#        'refusal': None, 
#        'role': 'assistant', 
#        'annotations': None, 
#        'audio': None, 
#        'function_call': None, 
#        'tool_calls': None, 
#        'sender': 'dressType'}], 
#      'min_range': 1000, 'max_range': 5000, 'gender': 'F'}}     