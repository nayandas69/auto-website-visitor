# Auto Website Visitor (AWV)

**Auto Website Visitor** is a fun yet powerful tool that automates repeated visits to a given website using real browser automation via Selenium.  
It supports Chrome, Firefox, and Edge with additional features like human-like scrolling, proxy support, headless mode, and interval-based automation.

![Workflow Status](https://img.shields.io/github/actions/workflow/status/nayandas69/auto-website-visitor/buildpypi.yml?style=flat-square&color=4DB6AC&logo=github)
![Python Version](https://img.shields.io/pypi/pyversions/auto-website-visitor?style=flat-square&color=42A5F5&logo=python)
![PyPI Version](https://img.shields.io/pypi/v/auto-website-visitor?style=flat-square&color=00C853&logo=pypi)
![PyPI Downloads](https://static.pepy.tech/badge/auto-website-visitor)  

Perfect for testing, load simulation, SEO boosting, and more — all with a sprinkle of style and control.

> [!WARNING]
> This tool is for **educational and personal use only**. Do not use it for any malicious or unauthorized activity.

## Supported Browsers

- [x] Google Chrome  
- [x] Mozilla Firefox  
- [x] Microsoft Edge  

## Features

- [x] **Headless mode** support (silent, no UI)  
- [x] **Proxy support** (http/https)  
- [x] **Smart auto-scroll** to simulate real user behavior  
- [x] **Randomized behavior** like scroll direction, pauses, element focus    
- [x] **Logging**: Tracks visit logs with timestamps   
- [x] **Human-readable countdown timer** between visits    

## Installation

### Clone & Run from Source

```bash
git clone https://github.com/nayandas69/auto-website-visitor.git
cd auto-website-visitor
python3 -m venv .venv            # (Recommended)
source .venv/bin/activate
pip3 install -r requirements.txt
python3 awv.py
```

### OR Install via pip

```bash
pip install auto-website-visitor
```

Then run it from anywhere:

```bash
auto-website-visitor
```

## Prebuilt EXE & Linux Binary

> [!WARNING]
> Check the **latest release assets** section to download the ready-to-use prebuilt files.

### For Windows

- Download `awv.exe` from the release
- Double click to launch
- Follow on-screen prompts

### For Linux

```bash
tar -xvzf awv-linux.tar.gz
sudo chmod +x awv
./awv
```

## Visit Our AWV Web Portal

Check it out here:  
[Click](https://nayandas69.github.io/auto-website-visitor)

> [!TIP]
> Use **headless mode** if you want background visits.
> Always keep **visit interval above 10s** when using auto-scroll.
> Add proxies for more anonymity.
> Set infinite visits with `0` for endless loops.

## How to Use (Menu Breakdown)

Once you launch AWV, you’ll see:

```
1. Start             → Start visiting a website
2. Check for Updates → Check for new releases
3. Help              → Read what it can do
4. Exit              → Close the app
```

### Start Menu Options

- Website URL  
- Number of visits (`0` = infinite)  
- Interval between visits  
- Browser of choice  
- Proxy support  
- Headless mode  
- Enable auto-scroll  

---

## Tested Platforms

- [x] Windows 11  
- [x] Kali Linux  

## Future Planned & Current Features

- [x] Human-like scrolling  
- [x] Smart pause simulation  
- [x] Proxy rotation  
- [x] Multi-browser support  
- [x] Update checker  
- [ ] GUI version with Tkinter  
- [ ] Scheduler/cron integration  
- [ ] Stats dashboard for visits  
- [ ] Customizable user-agent
- [ ] More browser support (Safari, Opera, etc.)
- [ ] More proxy types (SOCKS, etc.)

## Contribute

Got ideas or improvements?  
Pull requests, issues, or even a star ⭐ are always welcome!

## Author

- **Nayan Das**  
- [Website](https://nayandas69.github.io/link-in-bio)  
- nayanchandradas@hotmail.com  

## Disclaimer

> [!WARNING]
> This tool is strictly for **educational purposes**, testing, and personal experimentation.  
> The developer is not responsible for any misuse. Always comply with website terms and local laws.
