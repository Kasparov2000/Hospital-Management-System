import requests

try:
    response = requests.get('https://api.freegeoip.app/json/?apikey=294835e0-5ad7-11ec-b103-d7197c67950f').json()
    time_zone = response['time_zone']
except Exception:
    time_zone = "Africa/Harare"

