import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, RequestException

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
API_Key = os.getenv("COINMARTKETCAP_API") 

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_Key
}

session = Session()
session.headers.update(headers)
session.timeout = 5

def get_crypto_info():
    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        result = {}

        if data['status']['error_code'] == 0 and "data" in data:
            total_cryptocurrencies = str(data['data'].get('total_cryptocurrencies', 'N/A'))
            active_cryptocurrencies = str(data['data'].get('active_cryptocurrencies', 'N/A'))

            result['total_cryptocurrencies'] = total_cryptocurrencies
            result['active_cryptocurrencies'] = active_cryptocurrencies

            if 'quote' in data['data'] and 'USD' in data['data']['quote']:
                market_data = data['data']['quote']['USD']
                total_market_cap = f"$ {market_data.get('total_market_cap', 'N/A')}"
                total_volume_24h = f"$ {market_data.get('total_volume_24h', 'N/A')}"

                result['total_market_cap'] = total_market_cap
                result['total_volume_24h'] = total_volume_24h

        return result

    except ConnectionError:
        print('Error: Failed to connect with the CoinMarketCap API.')
    except Timeout:
        print('Error: Request to the CoinMarketCap API timed out.')
    except TooManyRedirects:
        print('Too many redirects when accessing the API.')
    except RequestException as e:
        print(f'An error occurred while making the request: {e}')
    except json.JSONDecodeError:
        print('Error: Failed to parse JSON response')
    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    try:
        result = get_crypto_info()
        if result:
            for key, value in result.items():
                print(f"{key} : {value}")
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()
