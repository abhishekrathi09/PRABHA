import requests

def weather(lon,lat):
    url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"

    querystring = {"lon":str(lon),"lat":str(lat)}

    headers = {
        "X-RapidAPI-Key": "2c62e920bbmshd3f39ed86555fa6p17b12cjsn32d762a8acd3",
        "X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response

result = weather(29.3,72.5)
print(result.text)