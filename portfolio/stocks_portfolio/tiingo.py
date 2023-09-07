import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token 627c0e183dc6dc87ddace6b95993ef99b1c02f9b'
}


def get_price_data(ticker):
    url = 'https://api.tiingo.com/tiingo/daily/{}/prices'.format(ticker)
    response = requests.get(url, headers=headers)
    return response.json()[0]
