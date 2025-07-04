from flask import Flask, render_template, request
import requests
import os
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY') 

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city'].strip()
        city_encoded = quote(city)
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid={API_KEY}&units=metric'

        print(" URL:", url)
        response = requests.get(url)
        print(" Status Code:", response.status_code)
        print(" Response:", response.text)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon']
            }
        else:
            try:
                error_message = response.json().get('message', 'City not found')
            except:
                error_message = 'City not found'
            weather_data = {'error': error_message}

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
