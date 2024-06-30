import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import requests
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyautogui  

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set properties for the TTS engine
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 

user_turn = True
tasks = []

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query.lower()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your assistant. How can I help you today?")

def open_website(url):
    webbrowser.open(url)

def search_wikipedia(query):
    speak('Searching Wikipedia...')
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        print(results)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple options. Please specify.")
    except wikipedia.exceptions.PageError as e:
        speak("Sorry, I could not find any relevant information.")

def get_news():
    api_key = 'YOUR_NEWS_API_KEY'
    url = f"http://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url)
    news = response.json()
    articles = news["articles"]
    speak("Here are the top news headlines")
    for article in articles[:5]:
        speak(article["title"])
        print(article["title"])

def get_weather():
    api_key = 'YOUR_WEATHER_API_KEY'
    city = "YOUR_CITY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather = response.json()
    temperature = weather['main']['temp']
    description = weather['weather'][0]['description']
    speak(f"The current temperature is {temperature} degrees Celsius with {description}")
    print(f"The current temperature is {temperature} degrees Celsius with {description}")

def send_email(to, subject, message):
    try:
        sender_email = "your_email@example.com"
        sender_password = "your_password"
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to, text)
        server.quit()
        
        speak("Email sent successfully")
    except Exception as e:
        speak("Sorry, I couldn't send the email")
        print(f"Error: {str(e)}")

def read_email():
    try:
        email_user = 'your_email@example.com'
        email_password = 'your_password'
        
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_password)
        mail.select("inbox")
        
        result, data = mail.search(None, 'ALL')
        mail_ids = data[0].split()
        speak("Reading your last 5 emails")
        
        for i in range(len(mail_ids)-1, len(mail_ids)-6, -1):
            result, msg_data = mail.fetch(mail_ids[i], '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    email_from = msg['from']
                    email_subject = msg['subject']
                    speak(f"Email from {email_from} with subject {email_subject}")
                    print(f"Email from {email_from} with subject {email_subject}")
        
        mail.close()
        mail.logout()
    except Exception as e:
        speak("Sorry, I couldn't read your emails")
        print(f"Error: {str(e)}")

def manage_tasks():
    global tasks
    speak("What would you like to do? Add a task, remove a task, or list all tasks?")
    action = listen()
    if 'add' in action:
        speak("What task would you like to add?")
        task = listen()
        tasks.append(task)
        speak(f"Task {task} added")
    elif 'remove' in action:
        speak("Which task would you like to remove?")
        task = listen()
        if task in tasks:
            tasks.remove(task)
            speak(f"Task {task} removed")
        else:
            speak("Task not found")
    elif 'list' in action:
        speak("Here are your tasks")
        for task in tasks:
            speak(task)
            print(task)
    else:
        speak("Sorry, I didn't understand that")

def open_camera():
    speak("Opening camera")
    os.system("start microsoft.windows.camera:")

def show_time():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {strTime}")

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    speak("Screenshot taken and saved")

def main():
    wish_me()
    while True:
        query = listen()

        if 'wikipedia' in query:
            query = query.replace("wikipedia", "")
            search_wikipedia(query)
        
        elif 'open youtube' in query:
            open_website("youtube.com")
        
        elif 'open google' in query:
            open_website("google.com")
        
        elif 'play music' in query:
            music_dir = 'C:\Music'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))
        
        elif 'the time' in query:
            show_time()

        elif 'news' in query:
            get_news()
        
        elif 'weather' in query:
            get_weather()

        elif 'send email' in query:
            try:
                speak("What is the recipient's email address?")
                to = listen()
                speak("What is the subject?")
                subject = listen()
                speak("What is the message?")
                message = listen()
                send_email(to, subject, message)
            except Exception as e:
                speak("Sorry, I couldn't send the email")

        elif 'read email' in query:
            read_email()

        elif 'task' in query:
            manage_tasks()

        elif 'exit' in query or 'quit' in query or 'stop' in query:
            speak("Goodbye!")
            break

        elif 'open camera' in query:
            open_camera()

        elif 'search' in query:
            query = query.replace("search", "")
            speak(f"Searching Google for {query}")
            url = f"https://www.google.com/search?q={query}"
            open_website(url)

        elif 'screenshot' in query:
            take_screenshot()

if __name__ == "__main__":
    main()