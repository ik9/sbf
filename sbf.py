
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored
import requests, pyfiglet, argparse
from os import system
from sys import platform

if "linux" in platform:
    system("clear")
else:
    system("cls")

# Processing command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help='url', dest='target')
parser.add_argument('-s', '--subdomains', help='subdomains brute force', dest='subdomains', action="store_true")
parser.add_argument('-p', '--paths', help='paths brute force', dest='paths', action="store_true")
parser.add_argument('-sl', '--subdomains-file-list', help='list of subdomains - there is a ready list', dest='slist')
parser.add_argument('-pl', '--paths-file-list', help='list of paths - there is a ready list', dest='plist')
args = parser.parse_args()

target = args.target
subdomains = args.subdomains
paths = args.paths
slist = args.slist
plist = args.plist

NAME = pyfiglet.figlet_format("SBF")
COLORED_NAME = colored(NAME, 'green')

print(COLORED_NAME) 
print(colored('Created by : @izox99\n', 'blue'))
if target == None:
    print(colored("url target required try again with sbf.py --help", 'red'))
    exit()



def log(response, url):
    if response.status_code <= 299:
        print(colored("[+]"+url+" - with SC : "+str(response.status_code), 'green'))
    elif response.status_code <= 399:
        print(colored("[+]"+url+" - with SC : "+str(response.status_code), 'yellow'))
    else:
        print(colored("[-]"+url+" - with SC : "+str(response.status_code), 'red'))


count = 0
def subdomains_bf(session, url):
    global count
    
    if subdomains == True:
        s = l1[count].replace('\n', '')+"."
        if 'https://' in url:
            url = "https://"+s+url[8:]
        elif 'http://' in url:
            url = "http://"+s+url[7:]
        else:
            url = "https://"+s+url
    
    count+=1

    response = session.get(url)

    log(response, url)

count = 0
def paths_bf(session, url):
    global count
    if "://" not in url:
        url = "https://"+url
    if l2 != None:
        s = l2[count].replace('\n', '')
        if url[-1] != '/':
            url = url+"/"+s
        else:
            url = url+s
        
    else: 
        print("exit")
        exit()
    count+=1
    response = session.get(url)
    
    log(response, url)
    

if subdomains == True:
    if slist != None:
        l1 = open(slist, 'r', encoding='utf-8').readlines()
    else:
        l1 = open("sublist.txt", 'r', encoding='utf-8').readlines()

    print("start")
    with ThreadPoolExecutor(max_workers=50) as executor:
        with requests.Session() as session:
            executor.map(subdomains_bf, [session] * len(l1), [target] * len(l1))
            executor.shutdown(wait=True)
if paths == True:
    if plist != None:
        l2 = open(plist, 'r', encoding='utf-8').readlines()
    else:
        l2 = None
        print("list is null")
        exit()
    print("start")
    with ThreadPoolExecutor(max_workers=50) as executor:
        with requests.Session() as session:
            executor.map(paths_bf, [session] * len(l2), [target] * len(l2))
            executor.shutdown(wait=True)

