==========================
Frequently Asked Questions
==========================

1. What is Auto Website Visitor?
--------------------------------
Auto Website Visitor is a Python-based tool that automates visits to any website using your preferred browser (Chrome, Firefox, or Edge). It supports custom intervals, auto-scrolling, proxies, and headless mode.

2. Which browsers are supported?
--------------------------------
Currently supported browsers:
- Google Chrome
- Mozilla Firefox
- Microsoft Edge

Make sure the browser is installed on your system before using the tool. See the **README** for installation steps.

3. I'm getting a "session not created" or "cannot find browser binary" error. What should I do?
-----------------------------------------------------------------------------------------------
This usually means the required browser is not installed or its binary path isn't available to Selenium.

Fix:
- Ensure the browser is installed.
- Try running it from the terminal (e.g., `google-chrome`, `firefox`, or `microsoft-edge`).
- If still facing issues, install the browser using the commands in the **README**.

4. Does this tool work on Windows & Linux?
----------------------------------------------------
Windows and Kali Linux are fully supported.

5. Can I run this in headless mode?
-----------------------------------
Yes! When prompted, choose headless mode with `y` and the browser will run in the background without a GUI.

6. What does "auto-scroll" do?
------------------------------
When enabled, the tool scrolls through the webpage to simulate human interaction. This feature requires an interval of **10 seconds or more**.

7. Can I run infinite visits?
-----------------------------
Yes! Enter `0` when asked for the number of visits to run it in infinite loop mode. You can stop it anytime using `Ctrl+C`.

8. How do I use a proxy?
------------------------
The tool will prompt you with the option. Enter `y`, and then provide your proxy in the format:

```
http://username:password@ip:port
```

9. Where is the driver downloaded?
----------------------------------
Drivers are managed automatically by `webdriver-manager` and stored in a cache directory like:

- Windows: `C:\Users\<User>\.wdm\drivers\`
- Linux: `/home/<user>/.wdm/drivers/`

10. I encountered an error. Where can I get help?
-------------------------------------------------
Feel free to reach out to the author:

- Website: https://nayandas69.github.io/link-in-bio
- Email: nayanchandradas@hotmail.com

Or, open an issue in the GitHub repository.
