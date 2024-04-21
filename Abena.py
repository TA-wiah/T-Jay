import pyttsx3
import speech_recognition as sr
import wikipedia
import os
import requests
import json
import datetime
import cv2
import threading
import webbrowser
import smtplib
import openai

# import sys
# Add the path to the libraries directory
# sys.path.append('C:\Users\aryeh\OneDrive\Desktop\Abena\Libraries')

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Define the directory to store voice recordings
VOICE_DIR = "voices"

# Ensure the directory exists
if not os.path.exists(VOICE_DIR):
    os.makedirs(VOICE_DIR)

# Set the OpenAI API key
# Replace with your actual OpenAI API key
openai.api_key = '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'

# Function to speak with visual line
def speak(text):
    # Use the text-to-speech engine to speak the text
    engine.say(text)
    engine.runAndWait()

    # Display a visual line while speaking
    line_thread = threading.Thread(target=display_line)
    line_thread.start()

# Function to display visual line
def display_line():
    # Display a visual line while speaking
    line_length = 50
    line_char = "-"
    for _ in range(line_length):
        print(line_char, end="", flush=True)
        cv2.waitKey(50)  # Adjust the delay as needed for the desired speed
    print("")

# Set the voice properties
def set_voice_properties(language, speed):
    # Get the list of available voices
    voices = engine.getProperty('voices')

    # Select a young female voice
    for voice in voices:
        if "female" in voice.name.lower() and "young" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    # Set the speed
    engine.setProperty('rate', speed)


# Function to listen to the user's voice input
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            user_input = recognizer.recognize_google(audio)
            print("User Input:", user_input)
            return user_input
        except Exception as e:
            print("Error:", str(e))
            speak("Sorry, I couldn't understand what you said. Can you please repeat?")
            return ""


# Function to set a reminder
def set_reminder():
    speak("What would you like me to remind you about?")
    reminder_text = listen()
    if reminder_text:
        speak("When should I remind you?")
        reminder_time = listen()
        # Additional logic to set the reminder (e.g., store in a database or schedule task)

# Function to perform OSINT search
def perform_osint_search(query):
    # Example: Use DuckDuckGo search API
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        search_results = response.json()
        if search_results.get("AbstractText"):
            return search_results["AbstractText"]
        elif search_results.get("RelatedTopics"):
            return search_results["RelatedTopics"][0]["Text"]
        else:
            return "No relevant information found."
    else:
        return "Failed to perform the search."


# Function to interact with Abena
def interact_with_abena():
    set_voice_properties("english", 150)  # Set default voice properties
    user_info = load_user_info()
    current_time = datetime.datetime.now().strftime("%H:%M")
    
    # If user information is not found, prompt the user to add their voice
    if not user_info:
        speak("It seems I couldn't find your user information. Would you like to add your voice?")
        response = listen()
        if response.lower() in ["yes", "yeah", "ok"]:
            add_a_voice()
            user_info = load_user_info()
        else:
            speak("No problem. Let me know if you need anything.")
    
    # Main interaction loop
    while True:
        user_input = listen().lower()

        if "exit" in user_input:
            speak("Goodbye! Take care.")
            break
        elif "abena"in user_input:
            speak(f"Hello {user_info['name']},. How can I assist you")
        elif "search" in user_input:
            query = user_input.replace("search", "").strip()
            response = perform_osint_search(query)
            speak(response)
        elif "who is" in user_input:
            query = user_input.replace("who is", "").strip()
            response = perform_osint_search(query)
            speak(response)
        elif "what" in user_input:
            query = user_input.replace("what", "").strip()
            response = search_with_chatgpt(query)
            speak(response)
        elif "if" in user_input:
            query = user_input.replace("if", "").strip()
            response = search_with_chatgpt(query)
            speak(response)
        elif "change voice" in user_input:
            set_voice_properties("english", 150)  # Change voice properties as needed
            speak("Voice changed successfully.")
        elif "analyze file" in user_input:
            speak("Please provide the path to the file you want to analyze.")
            file_path = input("File Path: ")
            analyze_file(file_path)
        elif "analyze picture" in user_input:
            speak("Please provide the path to the picture you want to analyze.")
            picture_path = input("Picture Path: ")
            analyze_picture(picture_path)
        elif "analyze video" in user_input:
            speak("Please provide the path to the video you want to analyze.")
            video_path = input("Video Path: ")
            analyze_video(video_path)
        elif "access mobile settings" in user_input:
            access_mobile_settings()
        elif "access pc settings" in user_input:
            access_pc_settings()
        elif "access contacts" in user_input:
            access_contacts()
        elif "access photos" in user_input:
            access_photos()
        elif "access networks" in user_input:
            access_networks()
        elif "who created you" in user_input or "who is your creator" in user_input or "who brought you into existence" in user_input:
            speak("I was created by Tottimeh Jeffrey. Would you like to know more about Tottimeh Jeffrey?")
            response = listen()
            if "yes" or "ok" or "yeah" in response:
                speak(personal_information())
        else:
            speak("I'm sorry, I didn't understand that command.")


# Function to analyze a file
def analyze_file(file_path):
    # Add your file analysis code here
    speak("File analysis is not implemented yet. Sorry for the inconvenience.")

# Function to analyze a picture
def analyze_picture(picture_path):
    # Add your picture analysis code here
    speak("Picture analysis is not implemented yet. Sorry for the inconvenience.")

# Function to analyze a video
def analyze_video(video_path):
    # Add your video analysis code here
    speak("Video analysis is not implemented yet. Sorry for the inconvenience.")

# Function to access mobile settings
def access_mobile_settings():
    # Add your code to access mobile settings here
    speak("Accessing mobile settings is not implemented yet. Sorry for the inconvenience.")

#Function to access PC settings
def access_pc_settings():
    # Add your code to access PC settings here
    speak("Accessing PC settings is not implemented yet. Sorry for the inconvenience.")

# Function to access contacts
def access_contacts():
    # Add your code to access contacts here
    speak("Accessing contacts is not implemented yet. Sorry for the inconvenience.")

# Function to access photos
def access_photos():
    # Add your code to access photos here
    speak("Accessing photos is not implemented yet. Sorry for the inconvenience.")

# Function to access networks
def access_networks():
    # Add your code to access networks here
    speak("Accessing networks is not implemented yet. Sorry for the inconvenience.")

# Function to provide personal information about the creator
def personal_information():
    info = """
    Personal Information:

    Name: Tottimeh Jeffrey
    Age: 19
    Education: Completed Apam Senior High School in 2023
    Location: Kasoa, Ghana

    Summary:
    Tottimeh Jeffrey is a determined and ambitious young individual with a keen interest in both aviation and 
    information and communication technology (ICT). With a solid foundation in IT and a dream of becoming a pilot, 
    Jeffrey is driven by a desire to excel in both fields, showcasing a unique blend of technical expertise and aviation 
    aspirations.

    Education:
    Apam Senior High School (Graduated 2023):
    Completed high school education with a focus on science and technology subjects.
    Engaged in extracurricular activities related to computer science robotics and IT.

    Skills:
    Information Technology Expertise:
    Proficient in programming languages such as Python, Java, and HTML/CSS.
    Experienced in system administration, troubleshooting, and network management, ethcal hacking.
    Skilled in software development, web development and database management.

    Aviation Aspirations:
    Possesses a strong passion for aviation and dreams of becoming a pilot.
    Actively engages with flight simulators and aviation software to enhance flying skills.
    Actively seeks out knowledge about the aviation industry, flight operations, and regulations.

    Projects:
    IT Projects:
    Developed a web-based application for local businesses to manage inventory and sales efficiently.
    Contributed to open-source projects, demonstrating coding expertise and collaboration skills.
    Created a personal website/portfolio showcasing skills and projects to potential employers.
    He has also created a delivery app to improve delivery system in Ghana

    Aviation Exploration:
    Regularly participates in flight simulation sessions to improve flying skills and understanding of aircraft operations.
    Actively engages in online aviation communities, discussing industry news, technology, and career paths.
    Seeks out opportunities for flight training and learning about aviation regulations and procedures.

    Goals:
    My master (Jeffrey's) ultimate goal is to pursue a career as a pilot while leveraging his expertise in ICT to contribute to the aviation 
    industry. He aims to continue his education, potentially pursuing a degree in aviation or a related field, while gaining 
    hands-on experience in both IT and aviation. Tottimeh is committed to integrating his passions and skills to make a significant 
    impact in the worlds of technology and aviation.
    """
    return info


# Function to access the device camera
def access_camera():
    cap = cv2.VideoCapture(0)  # 0 for the default camera, change it if needed

    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord(listen("stop")):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to perform internet-dependent task
def perform_internet_task():
    # Perform internet-dependent task here
    speak("Performing internet task")

# Function to detect emotions using camera
def detect_emotions():
    # Load the pre-trained Haar cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Prompt the user if a face is detected
            speak("Face Detected")
            speak("What's wrong?")

        # Display the frame
        cv2.imshow('Emotion Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

# Function to perform search using ChatGPT
def search_with_chatgpt(query):
    # Call the OpenAI ChatGPT API to generate a response
    response = openai.Completion.create(
        engine="davinci",  # Use the Davinci engine for natural language understanding
        prompt=query,
        max_tokens=100  # Adjust the maximum number of tokens for the response
    )
    return response.choices[0].text.strip()

# Function to interact with Abena using ChatGPT for search
def interact_with_abena_chatgpt():
    # Set initial voice properties
    language = "english"
    speed = 150  # Normal speed
    set_voice_properties(language, speed)


def check_wifi_status():
    # Check if wifi is available  (offline simulator)
    return False

def connect_to_wifi(network):
    # Connect to WiFi using the provided password (offline simulator)
    speak(f"Available network: {network}")
    speak("Please enter the password for the network.")
    password = listen()
    if password:
        speak("Connecting to WiFi...")
        # Simulate connection process
        speak("WiFi connected.")
 


# Function to save the conversation
def save_conversation(speaker, message):
    with open("conversation_log.txt", "a") as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - {speaker}: {message}\n")

def add_a_voice():
    speak("Please speak a passphrase to add your voice.")
    passphrase = listen()
    if passphrase:
        file_path = os.path.join(VOICE_DIR, f"{passphrase}.txt")  # Change file extension to '.txt'
        speak("Please your name.")
        name = listen()
        speak("Please your age.")
        age = listen()
        speak("Please provide any additional information about yourself.")
        additional_info = listen()
        with open(file_path, "w") as file:  # Open file in text mode ('w')
            file.write(passphrase + "\n")  # Write passphrase as text
            file.write(name + "\n")  # Write name as text
            file.write(age + "\n")  # Write age as text
            file.write(additional_info)  # Write additional_info as text
        # Store user information in a JSON file
        user_info = {"name": name, "age": age, "additional_info": additional_info}
        with open("user_info.json", "w") as json_file:
            json.dump(user_info, json_file)
        speak("Voice added successfully!")



# Function to load user information
def load_user_info():
    try:
        with open("user_info.json", "r") as file:
            user_info = json.load(file)
        return user_info
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Add this function to the main program to initialize the conversation
def main():
    speak("Initializing Abena...")
    interact_with_abena()


# Execute the main function
if __name__ == "__main__":
    main()
