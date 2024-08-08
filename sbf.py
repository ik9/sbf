from concurrent.futures import ThreadPoolExecutor
from termcolor import colored
import requests

url = input("url : ")

sublist = "sublist.txt"
f = open(sublist, 'r', encoding='utf-8').readlines()

count = 0
def fetch(session, url):
    global count
    
    sub = f[count].replace('\n', '')+"."
    if 'https://' in url:
        url = "https://"+sub+url[8:]
    elif 'http://' in url:
        url = "http://"+sub+url[7:]
    else:
        url = "https://"+sub+url
    
    count+=1

    response = session.get(url)

    if response.status_code == 200:
        print(colored(url+" - SC : 200", 'green'))
    else:
        print(colored(url+" - with SC : "+str(response.status_code), 'yellow'))


with ThreadPoolExecutor(max_workers=50) as executor:
    with requests.Session() as session:
        executor.map(fetch, [session] * len(f), [url] * len(f))
        executor.shutdown(wait=True)



