// Handle download buttons with countdown
function handleDownload(button) {
    if (button.classList.contains("counting-down")) return;
    button.classList.add("counting-down");

    const link = button.getAttribute("data-link");
    if (!link) {
        alert("Download link not available!");
        button.classList.remove("counting-down");
        return;
    }

    let countdown = 3;
    const originalHTML = button.innerHTML;
    button.disabled = true;
    button.innerHTML = `<i class="fas fa-hourglass-start"></i> Wait ${countdown}s`;

    const timer = setInterval(() => {
        countdown--;
        button.innerHTML = `<i class="fas fa-hourglass-half"></i> Wait ${countdown}s`;

        if (countdown === 0) {
            clearInterval(timer);
            button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Preparing...`;
            setTimeout(() => {
                window.location.href = link;
                button.innerHTML = originalHTML;
                button.disabled = false;
                button.classList.remove("counting-down");
            }, 1000);
        }
    }, 1000);
}

document.querySelectorAll(".download-btn").forEach(button => {
    button.addEventListener("click", () => handleDownload(button));
});

function markRecommendedButton() {
    const platform = navigator.platform.toLowerCase();
    const userAgent = navigator.userAgent.toLowerCase();

    let os = "unknown";
    if (platform.includes("win")) os = "windows";
    else if (platform.includes("linux")) os = "linux";

    document.querySelectorAll(".download-btn").forEach(button => {
        const link = button.getAttribute("data-link");
        if (!link) return;

        if (
            (os === "windows" && link.endsWith(".exe")) ||
            (os === "linux" && link.endsWith(".deb"))
        ) {
            const badge = `<span style="margin-left: 8px; background: #bf40bf; color: #fff; padding: 3px 6px; border-radius: 5px; font-size: 0.75rem;">Recommended</span>`;
            button.innerHTML += badge;
        }
    });
}

markRecommendedButton();
