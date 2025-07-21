#!/usr/bin/env python3
try:
    import requests, time, os, re, json, sys
    from rich import print as println
    from rich.console import Console
    from rich.panel import Panel
    from fake_useragent import UserAgent
except ModuleNotFoundError:
    print("Required modules are not installed. Please run 'pip install -r requirements.txt'.")
    sys.exit(1)

BASE_URL = "https://socioblend.com"
SUCCESS, FAILED, DELAY = [], [], {
    "TIME": 0
}
CONSOLE = Console()

def Banner() -> None:
    """Display the banner for the script."""
    CONSOLE.print(
        Panel(
            r"""[bold red]   _____            _      ______ _                _ 
  /  ___|          (_)     | ___ \ |              | |
  \ `--.  ___   ___ _  ___ | |_/ / | ___ _ __   __| |
   `--. \/ _ \ / __| |/ _ \| ___ \ |/ _ \ '_ \ / _` |
  /\__/ / (_) | (__| | (_) | |_/ / |  __/ | | | (_| |
[bold white]  \____/ \___/ \___|_|\___/\____/|_|\___|_| |_|\__,_|
            [underline red]Free Tiktok Views - by Rozhak""", width=59, style="bold bright_black"
        )
    )
    return None

class SubmitTikTokViews:

    def __init__(self, video_url: str) -> None:
        """Initialize the SubmitTikTokViews class."""
        self.video_url = video_url
        self.session = requests.Session()

    def RetrieveCookies(self) -> str:
        """Retrieve cookies from the session."""
        self.session.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "socioblend.com",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": f"{UserAgent().random}"
        }
        response = self.session.get(f"{BASE_URL}/free-tiktok-views", verify=True, allow_redirects=True)

        cookies_string = "; ".join([f"{key}={value}" for key, value in self.session.cookies.get_dict().items()])

        return cookies_string
    
    def SubmitForm(self, cookies: str) -> None:
        """Submit the form with the video URL and cookies."""
        global SUCCESS, FAILED, DELAY
        data = {
            "video_url": f"{self.video_url}",
        }
        self.session.headers.update(
            {
                "Content-Length": f"{len(json.dumps(data))}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Cookie": f"{cookies}",
                "Accept": "*/*",
                "Sec-Fetch-Dest": "empty",
                "Origin": f"{BASE_URL}",
                "Referer": f"{BASE_URL}/free-tiktok-views",
            }
        )

        response = self.session.post(f"{BASE_URL}/submit-tiktok.php", data=data, verify=True, allow_redirects=False)
        if '"status":"success"' in response.text:
            SUCCESS.append(f"{response.status_code} - {response.reason}")
            CONSOLE.print(
                Panel(f"""[bold white]Status:[bold green] Successfully sent TikTok views to your video!
[bold white]Link:[bold red] {self.video_url}
[bold white]Views:[bold yellow] +1000""", width=59, style="bold bright_black", title="[bold bright_black]> [Successfully] <")
            )
        elif '"retry_after"' in response.text:
            retry_after = re.search(r'"retry_after":(\d+)', response.text)
            if retry_after: DELAY["TIME"] = int(retry_after.group(1))
        else:
            FAILED.append(f"{response.status_code} - {response.reason}")
            println(f"[bold bright_black]   ╰─>[bold red] FAILED TO SEND TIKTOK VIEWS!             ", end="\r")
            time.sleep(5)

        return None

def Main() -> None:
    """Main function to run the script."""
    os.system("clear" if os.name == "posix" else "cls")
    Banner()
    CONSOLE.print(
        Panel(f"[bold white]Please enter your TikTok video link. Be sure to check the link before pressing enter.\nI recommend grabbing the link from your browser!", width=59, style="bold bright_black", title="[bold bright_black]> [Tiktok Link] <", subtitle="[bold bright_black]╭──────", subtitle_align="left")
    )
    video_url = CONSOLE.input("[bold bright_black]   ╰─> ").strip()
    if video_url.startswith("https://www.tiktok.com/@") or video_url.startswith("https://tiktok.com/@") or video_url.startswith("https://vt.tiktok.com/"):
        CONSOLE.print(
            Panel("[bold white]Please wait a moment..., You can use[bold red] CTRL + Z[bold white] to stop and use[bold yellow] CTRL + C[bold white] if you get stuck!", width=59, style="bold bright_black", title="[bold bright_black]> [Processing] <")
        )
        time.sleep(2)
        while True:
            try:
                if DELAY["TIME"] != 0:
                    for timer in range(DELAY["TIME"], 0, -1):
                        println(f"[bold bright_black]   ╰─>[bold white] RUNNING[bold green] {timer}[bold white]/[bold green]{DELAY['TIME']}[bold white] SUCCESS:-[bold green]{len(SUCCESS)}[bold white] FAILED:-[bold red]{len(FAILED)}     ", end="\r")
                        time.sleep(1)
                    DELAY["TIME"] = 0
                    println(f"[bold bright_black]   ╰─>[bold yellow] RE-SEND!                            ", end="\r")
                    time.sleep(5)
                    continue
                println(f"[bold bright_black]   ╰─>[bold green] SENDING TIKTOK VIEWS!               ", end="\r")
                time.sleep(2)

                submitter = SubmitTikTokViews(video_url)
                cookies = submitter.RetrieveCookies()
                submitter.SubmitForm(cookies)
            except requests.exceptions.RequestException:
                println(f"[bold bright_black]   ╰─>[bold red] YOUR CONNECTION IS HAVING A PROBLEM!     ", end="\r")
                time.sleep(10)
                continue
            except KeyboardInterrupt:
                continue
            except Exception as e:
                println(f"[bold bright_black]   ╰─>[bold red] {str(e).upper()}!", end="\r")
                time.sleep(5)
                continue
    else:
        CONSOLE.print(
            Panel("[bold red]Sorry, you entered the wrong TikTok video link, please try again with the format https://www.tiktok.com/@...", width=59, style="bold bright_black", title="[bold bright_black]> [Wrong Link] <")
        )
        sys.exit(1)

if __name__ == "__main__":
    try:
        if os.path.exists("Penyimpanan/Subscribe.json") == False:
            os.system(f"xdg-open {json.loads(requests.get('https://raw.githubusercontent.com/RozhakXD/Like4Gram/main/Penyimpanan/Youtube.json').text)['Link']}")
            with open('Penyimpanan/Subscribe.json', 'w') as w:
                w.write(json.dumps(
                    {
                        "Status": True
                    }, indent=4
                ))
            time.sleep(2.5)
        Main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        CONSOLE.print(
            Panel(f"[bold red]An error occurred: {str(e)}", width=59, style="bold bright_black", title="[bold bright_black]> [Error] <")
        )
        sys.exit(1)