# discord.gg/clown
# github.com/kuzey1337
import os
import concurrent.futures
import time
import threading
import requests
import socks
import socket
from colorama import Fore, Style


# colors
red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
magenta = Fore.MAGENTA
reset = Style.RESET_ALL

output_lock = threading.Lock()

def get_time_now():
    return time.strftime("%H:%M:%S")

def scrape_proxies(url):
    global proxies_scraped
    response = requests.get(url)
    if response.status_code == 200:
        with output_lock:
            print(f"[{get_time_now()}] | ({green}SUCCESS{reset}) {magenta}Scraped --> {url}\n")
        proxies = response.text.splitlines()
        return proxies
    else:
        with output_lock:
            print(f"[{get_time_now()}] | ({magenta}ERROR{reset}) Failed to scrape proxies from {url}\n")
        return []

def scrape_and_save_proxies(url, filename):
    proxies = scrape_proxies(url)
    with open(filename, "w") as file:
        for proxy in proxies:
            file.write(proxy + '\n')

def run(num_threads):
    global http_checked, socks4_checked, socks5_checked
    http_checked = 0
    socks4_checked = 0
    socks5_checked = 0

    # HTTPS proxy
    https_urls = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=10000&country=all&ssl=all&anonymity=all"
    ]

    # HTTP proxy
    http_urls = [
        "https://rootjazz.com/proxies/proxies.txt",
        "https://spys.me/proxy.txt",
        "https://proxyspace.pro/http.txt"
    ]

    # SOCKS4 proxy
    socks4_urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all",
        "https://api.openproxylist.xyz/socks4.txt",
        "https://proxyspace.pro/socks4.txt",
        "https://www.proxy-list.download/api/v1/get?type=socks4"
    ]

    # SOCKS5 proxy
    socks5_urls = [
        "https://api.openproxylist.xyz/socks5.txt",
        "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5",
        "https://proxyspace.pro/socks5.txt",
        "https://spys.me/socks.txt"
    ]

    # ALL PROXY
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(scrape_and_save_proxies, https_urls, ["https_proxies.txt"] * len(https_urls))
        executor.map(scrape_and_save_proxies, http_urls, ["http_proxies.txt"] * len(http_urls))
        executor.map(scrape_and_save_proxies, socks4_urls, ["socks4_proxies.txt"] * len(socks4_urls))
        executor.map(scrape_and_save_proxies, socks5_urls, ["socks5_proxies.txt"] * len(socks5_urls))

    time.sleep(5)  

    total_https_proxies = sum(len(scrape_proxies(url)) for url in https_urls)
    total_http_proxies = sum(len(scrape_proxies(url)) for url in http_urls)
    total_socks4_proxies = sum(len(scrape_proxies(url)) for url in socks4_urls)
    total_socks5_proxies = sum(len(scrape_proxies(url)) for url in socks5_urls)

    print(f"\nTotal proxies scraped:")
    print(f"HTTPS proxies: {total_https_proxies}")
    print(f"HTTP proxies: {total_http_proxies}")
    print(f"SOCKS4 proxies: {total_socks4_proxies}")
    print(f"SOCKS5 proxies: {total_socks5_proxies}")

if __name__ == "__main__":
    num_threads = int(input("Enter number of threads: "))
    run(num_threads)
