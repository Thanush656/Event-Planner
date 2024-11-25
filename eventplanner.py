import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API
genai.configure(api_key=os.environ["google_api_key"])

# Create the model with desired generation settings
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Function to generate an event plan
def generate_event_plan(event_details):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "Create a detailed plan for the following event:",
                ],
            },
        ]
    )
    
    response = chat_session.send_message(event_details)
    return response.text

# Streamlit app
def main():
    st.title("Event Planner")

    # Collect event details
    st.subheader("Enter Event Details")
    event_type = st.text_input("Event Type (e.g., Wedding, Conference, Birthday Party)")
    event_date = st.date_input("Event Date")
    event_time = st.time_input("Event Time")
    location = st.text_input("Event Location")
    number_of_guests = st.number_input("Number of Guests", min_value=1, step=1)
    specific_requests = st.text_area("Special Requests or Theme")

    # Generate event plan
    if st.button("Generate Event Plan"):
        with st.spinner("Planning your event..."):
            # Prepare the event details as input for the model
            event_details = f"Type: {event_type}\nDate: {event_date}\nTime: {event_time}\nLocation: {location}\nGuests: {number_of_guests}\nSpecial Requests: {specific_requests}"
            
            event_plan = generate_event_plan(event_details)
            st.subheader("Event Plan")
            st.write(event_plan)

if __name__ == "__main__":
    main()
