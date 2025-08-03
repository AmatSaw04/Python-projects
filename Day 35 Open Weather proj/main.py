import requests

from twilio.rest import Client

account_sid = 'AC71a050977a5e6bd5ad1f49e5b048bfeb'
auth_token = '5fec0a16ae77d1921ce08136710d9234'
api_key = "cb660c5e86048bcbe58cfd311a1e561f"
my_data ={"coord":{"lon":79.1,"lat":21.15},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],"base":"stations","main":{"temp":299.49,"feels_like":299.49,"temp_min":299.49,"temp_max":299.49,"pressure":1001,"humidity":69,"sea_level":1001,"grnd_level":966},"visibility":10000,"wind":{"speed":5.67,"deg":245,"gust":8.12},"clouds":{"all":100},"dt":1750743560,"sys":{"country":"IN","sunrise":1750723405,"sunset":1750771707},"timezone":19800,"id":1262180,"name":"Nagpur","cod":200}

api_data = "https://api.openweathermap.org/data/2.5/forecast"
parameter = {"lat": 21.15,
             "lon": 79.1,
             "appid": api_key,
             "cnt": 4,
             }
response = requests.get(api_data, params=parameter)
weather_data = response.json()
response.raise_for_status()

will_rain = False
for hour_data in weather_data["list"]:
    cond_code = hour_data["weather"][0]["id"]
    if int(cond_code) < 700:
        will_rain = True
account_sid = 'AC71a050977a5e6bd5ad1f49e5b048bfeb'
auth_token = '5fec0a16ae77d1921ce08136710d9234'
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body='It is going to Rain, Bring an Umbrella',
        from_='(229) 360-7063',
        to='+919518718012',

    )
    print(message.sid)

