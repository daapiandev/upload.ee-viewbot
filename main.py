# made with love ❤
import requests
import threading
import random
from colorama import Fore, Style, init
from termcolor import colored


init(autoreset=True)

def get_user_agents_from_file(filename):
    with open(filename, 'r') as file:
        user_agents = file.readlines()
    return [user_agent.strip() for user_agent in user_agents if user_agent.strip()]

def get_proxies_from_file(filename):
    with open(filename, 'r') as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies if proxy.strip()]

def get_proxies_from_apis(api_urls):
    proxies = []
    for url in api_urls:
        try:
            response = requests.get(url)
            proxies.extend(response.text.split('\n'))
        except requests.RequestException:
            pass
    return [proxy.strip() for proxy in proxies if proxy.strip()]

def check_proxy(proxy, test_url, user_agents):
    try:
        user_agent = random.choice(user_agents)
        headers = {'User-Agent': user_agent}
        response = requests.get(test_url, proxies={'http': proxy, 'https': proxy}, headers=headers, timeout=5)
        if response.status_code == 200:
            print(colored(f"{proxy} view sent ({user_agent})", 'green', attrs=['bold']))
            with open('working.txt', 'a') as file:
                file.write(f"{proxy}\n")
    except requests.RequestException:
        pass

def print_ascii_art():
    ascii_art = r"""
          _______   _______      ___      ___  ____  ____   _______  __   __  ___  _______     ______  ___________  
         /"     "| /"     "|    |"  \    /"  |("  _||_ " | /"     "||"  |/  \|  "||   _  "\   /    " \("     _   ") 
        (: ______)(: ______)     \   \  //  / |   (  ) : |(: ______)|'  /    \:  |(. |_)  :) // ____  \)__/  \\__/  
         \/    |   \/    |        \\  \/. ./  (:  |  | . ) \/    |  |: /'        ||:     \/ /  /    ) :)  \\_ /     
  _____  // ___)_  // ___)_        \.    //    \\ \__/ //  // ___)_  \//  /\'    |(|  _  \\(: (____/ //   |.  |     
 ))_  ")(:      "|(:      "|        \\   /     /\\ __ //\ (:      "| /   /  \\   ||: |_)  :)\        /    \:  |     
(_____(  \_______) \_______)         \__/     (__________) \_______)|___/    \___|(_______/  \"_____/      \__|     
    """
    gradient_colors = [Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX]
    for line in ascii_art.split('\n'):
        for i, char in enumerate(line):
            color = gradient_colors[i % len(gradient_colors)]
            print(f"{color}{char}", end='')
        print()

def main():
    print_ascii_art()
    user_agents = get_user_agents_from_file('useragents.txt')
    choice = input("Do you want to test proxies from a file (f) or from APIs (a)? (f/a): ").strip().lower()
    
    if choice == 'f':
        proxies = get_proxies_from_file('proxies.txt')
    elif choice == 'a':
        api_urls = [
            'https://www.proxy-list.download/api/v1/get?type=https',
            'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all',
            'https://spys.me/proxy.txt',
            'https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=lastChecked&sort_type=desc&protocols=http,https',
            'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/http/data.txt',
            'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt',
            'http://pubproxy.com/api/proxy',
            'https://openproxylist.com/',
            'https://api.getproxylist.com/proxy',
            'https://www.freeproxy.world/?type=https',
            'https://www.proxy-list.download/api/v1/get?type=http',
            'https://www.proxy-list.download/api/v1/get?type=socks4',
            'https://www.proxy-list.download/api/v1/get?type=socks5',
            'https://www.proxy-list.download/api/v1/get?type=https&anon=elite',
            'https://www.proxy-list.download/api/v1/get?type=https&anon=anonymous'
        ]
        proxies = get_proxies_from_apis(api_urls)
    else:
        return

    test_url = input("Enter the upload.ee HTML URL: ").strip()

    threads = []
    for proxy in proxies:
        thread = threading.Thread(target=check_proxy, args=(proxy, test_url, user_agents))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
