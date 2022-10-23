import requests
import random
import json

def get_rand_gif(search_term, api_key, lmt):
    response = requests.get(
        "https://g.tenor.com/v2/search?q=%s&key=%s&limit=%s" 
        % (search_term, api_key, lmt))
    data = response.json()
    
    gif = random.choice(data["results"])
    return gif["media_formats"]["gif"]["url"]
