import json
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from wsgiref.simple_server import make_server


def get_exchange_rate(currency_code):
    api_url = f"https://api.exchangerate-api.com/v4/latest/{currency_code.upper()}"
    try:
        req = Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            return json.load(response)
    except HTTPError as e:
        if e.code == 400:
            return {"error": "Invalid currency code"}
        else:
            return {"error": f"API request failed with status code: {e.code}"}
    except Exception as e:
        return {"error": f"Failed to fetch data from API: {e}"}


def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    if not path:
        status = '404 Not Found'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps({"error": "Currency code is missing"}).encode('utf-8')]

    currency_code = path.upper()

    exchange_data = get_exchange_rate(currency_code)

    if "error" in exchange_data:
        status_code = '400 Bad Request' if exchange_data["error"] == "Invalid currency code" else '500 Internal Server Error'
        status = status_code
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps({"error": exchange_data["error"]}).encode('utf-8')]
    else:
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps(exchange_data).encode('utf-8')]


if __name__ == '__main__':
    httpd = make_server('0.0.0.0', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()