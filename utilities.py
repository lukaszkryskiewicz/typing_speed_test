import requests


def generate_words():
    url =' https://random-word-api.herokuapp.com/word'
    params = {
        'length': 7,
        'number': 25,
    }

    try:
        response = requests.get(url, params)
    except:
        print('No data returned')
        return

    return response.json()

