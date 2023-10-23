import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import requests
import smtplib

# Initialize the voice recognizer and engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def get_news_headlines():
    news_api_key = '5f26b160558a456ab24a265a767dbbf9'  # Replace with your news API key
    news_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}'

    try:
        response = requests.get(news_url)
        news_data = response.json()

        if news_data.get('status') == 'ok':
            articles = news_data.get('articles')

            if articles:
                headlines = [article['title'] for article in articles]
                talk("Here are the latest news headlines:")
                for idx, headline in enumerate(headlines):
                    talk(f"{idx + 1}. {headline}")
            else:
                talk("I couldn't find any news headlines at the moment.")
        else:
            talk("Sorry, I couldn't fetch the news at this time. Please try again later.")

    except Exception as e:
        print(f"An error occurred while fetching news: {str(e)}")
        talk("Sorry, I encountered an error while fetching news updates.")

def take_command():
    try:
        with sr.Microphone() as source:
            print("Try saying something...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command

def send_email(subject, message, to_email):
    smtp_server = "smtp.gmail.com"  # Replace with your SMTP server address
    smtp_port = 465  # Replace with your SMTP server port (usually 587 for TLS)
    email_address = ""  # Replace with your email address
    email_password = ""  # Replace with your email password

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)
        message_body = f"Subject: {subject}\n\n{message}"
        server.sendmail(email_address, to_email, message_body)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_weather(location):
    if not location:
        talk("Please provide a valid location for the weather.")
        return

    # Replace 'YOUR_WEATHER_API_KEY' with your actual weather API key
    weather_api_key = '9375849fe2f38f02e1a2c70056bd9d94'
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}'

    try:
        response = requests.get(weather_url)
        response.raise_for_status()  # Check for HTTP errors

        weather_data = response.json()

        if response.status_code == 200:
            main_data = weather_data['main']
            weather_description = weather_data['weather'][0]['description']
            temperature = main_data['temp']
            humidity = main_data['humidity']

            weather_info = f"The weather in {location} is {weather_description}. The temperature is {temperature} Kelvin, with a humidity of {humidity}%."

            talk(weather_info)
        else:
            talk(f"Sorry, I couldn't fetch weather information for {location}.")
    except requests.exceptions.RequestException as req_err:
        print(f"Request Error: {req_err}")
        talk("Sorry, the weather server API is down on maintainence. Please try again later.")
    except Exception as e:
        print(f"An error occurred while fetching weather: {str(e)}")
        talk("Sorry, I encountered an error while fetching weather information.")

def get_joke():
    joke_url = 'https://official-joke-api.appspot.com/jokes/random'

    try:
        response = requests.get(joke_url)
        joke_data = response.json()

        if response.status_code == 200:
            setup = joke_data['setup']
            punchline = joke_data['punchline']
            joke = f"{setup} {punchline}"
            talk("Here's a joke for you:")
            talk(joke)
        else:
            talk("Sorry, I couldn't fetch a joke at the moment.")
    except requests.exceptions.RequestException as req_err:
        print(f"Request Error: {req_err}")
        talk("Sorry, there was a problem with the request. Please try again later.")
    except Exception as e:
        print(f"An error occurred while fetching a joke: {str(e)}")
        talk("Sorry, I encountered an error while fetching a joke.")


def run_katana():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('Playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('It\'s ' + time)
    elif 'send email' in command:
        # Extract email details from user's command
        talk('What is the subject of the email?')
        subject = take_command()
        talk('What is the message of the email?')
        message = take_command()
        talk('To whom should I send the email?')
        to_email = take_command()

        # Call the send_email function
        send_email(subject, message, to_email)
    elif 'news' in command:
        get_news_headlines()
    elif 'weather' in command:
        # Extract the location from the user's command
        location = command.replace('weather', '').strip()
        get_weather(location)
    elif 'joke' in command:
        get_joke()
    else:
        talk("I'm not sure what you're asking. Please try again.")

run_katana()
