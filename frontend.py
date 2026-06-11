import streamlit as st
import requests

# Configure the Streamlit page
st.set_page_config(
    page_title="Hardware Architect Agent",
    page_icon="🤖",
    layout="wide"
)

# Backend API URL
API_URL = "http://localhost:8000/architect-project"

# UI Header
st.title("🤖 Hardware Project Architect")
st.markdown("Instantly generate System Architecture, Bill of Materials, Wiring Guides, and Code for your electronics prototypes.")

# User Inputs
with st.form("hardware_form"):
    project_idea = st.text_area(
        "Describe your project idea in detail", 
        placeholder="e.g., An eye-blinking and drowsiness detection system using an IR sensor and a buzzer..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        microcontroller = st.selectbox(
            "Preferred Microcontroller / Board", 
            ["Arduino Uno", "Arduino Nano", "ESP32", "ESP8266", "Raspberry Pi Pico", "Raspberry Pi 4"]
        )
        
    with col2:
        experience_level = st.selectbox(
            "Your Experience Level", 
            ["Beginner", "Intermediate (Familiar with basic circuits)", "Advanced (Custom PCBs & complex logic)"]
        )

    submit_button = st.form_submit_button("Generate Architecture ⚡")

# Handle Submission
if submit_button:
    if not project_idea:
        st.warning("Please describe your project idea first.")
    else:
        with st.spinner(f"Architecting system for {microcontroller}..."):
            try:
                # Call the FastAPI Backend
                payload = {
                    "project_idea": project_idea,
                    "microcontroller": microcontroller,
                    "experience_level": experience_level
                }
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    result = response.json()["data"]
                    
                    st.success("Architecture Generated Successfully!")
                    
                    # Display the result
                    st.markdown("---")
                    st.markdown(result)
                    
                else:
                    st.error(f"Error from server: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend. Ensure the FastAPI server is running on port 8000.")
                