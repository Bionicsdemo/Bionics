import streamlit as st
import requests
import json
import uuid

# API Key, endpoint, and channel token
API_KEY = "qfG4uJoG.SHh6xinGrkYGIBKanHNGFdvguic1tYaq"  # Replace with your actual API Key
ENDPOINT_ID = "Q30XVFX5UU"  # Replace with your actual endpoint ID
CHANNEL_TOKEN = str(uuid.uuid4())  # Generate a unique token for each user or session

# Base URL of the endpoint
BASE_URL = f"https://payload.vextapp.com/hook/{ENDPOINT_ID}/catch/{CHANNEL_TOKEN}"

# Function to send the POST request
def send_request(message):
    headers = {
        "Content-Type": "application/json",
        "Apikey": f"Api-Key {API_KEY}"
    }
    payload = {
        "payload": message
    }
    
    # Send the POST request
    response = requests.post(BASE_URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Function to send the request with long polling
def send_long_polling_request(message):
    headers = {
        "Content-Type": "application/json",
        "Apikey": f"Api-Key {API_KEY}"
    }
    payload = {
        "payload": message,
        "long_polling": True
    }
    
    response = requests.post(BASE_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        result = response.json()
        return result.get("request_id")
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Function to check the request status for long polling
def check_request_status(request_id):
    headers = {
        "Content-Type": "application/json",
        "Apikey": f"Api-Key {API_KEY}"
    }
    payload = {"request_id": request_id}
    is_processing = True
    
    while is_processing:
        response = requests.post(BASE_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            result = response.json()
            if "processing" in result.get("text", "").lower():
                st.write("Processing... please wait.")
            else:
                return result
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            is_processing = False
        return None

# Streamlit UI setup
st.title("Bionics 1.0")
user_message = st.text_area("Enter your message:", placeholder="Type your message here")

# Option to choose between normal request or long polling
option = st.radio("Choose request type:", ("Normal Request", "Long Polling"))

if st.button("Send"):
    if user_message:
        if option == "Normal Request":
            st.write("Sending message...")
            # Send normal request
            response = send_request(user_message)
            if response:
                st.write("Response:")
                st.json(response)
            else:
                st.write("No response received.")
        elif option == "Long Polling":
            st.write("Sending message with long polling...")
            # Send the initial request with long polling
            request_id = send_long_polling_request(user_message)
            
            if request_id:
                # Check the request status until it's ready
                final_result = check_request_status(request_id)
                
                if final_result:
                    st.write("Response:")
                    st.json(final_result)
                else:
                    st.write("No response received.")
            else:
                st.write("No response received.")
    else:
        st.warning("Please enter a message before sending.")