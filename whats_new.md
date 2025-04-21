# What's New in v0.0.7

Hey there, power users and automation lovers!  
Here’s the latest scoop on what’s new, improved, and upgraded in **Auto Website Visitor v0.0.7**

### Microsoft Edge Support  
You asked, we delivered!  
Now you can use **Microsoft Edge** alongside Chrome and Firefox. Pick your favorite browser and roll with it.

```bash
Choose your browser (chrome/firefox/edge): edge
```

### Smarter Auto-Scroll (Human-like)  
We’ve completely **revamped `auto_human_scroll()`** to simulate real user behavior.  
It now includes:
- Scrolling **down and up**
- Random **pauses to read**
- Targeted scrolling to elements like `<p>` tags
- More **natural behavior** that mimics actual browsing sessions  

> [!WARNING]
> **Auto-scroll now requires a minimum interval of 10 seconds**. If selected with a shorter interval, it will be automatically disabled with a warning.

---

### Dynamic Visit Timer Feedback  
Instead of silently waiting, the program now tells you exactly how long it will pause:

```bash
Waiting 7s before next visit... 💤
```

This gives you a clear, real-time indicator of the visit pacing.

---

## Improved UX & Input Handling

- **Smart input parsing** for `yes/no` answers like auto-scroll.
- **Minimum visit interval enforcement** ensures functionality works correctly.
