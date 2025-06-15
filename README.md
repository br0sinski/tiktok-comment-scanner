# 🎵 TikTok Comment Scanner 🎵

A tool I wrote for my girlfriend, for her bachelor thesis.
⚠️ Keep in mind this is a tool for personal use, the codebase is not the best - it's very tailored for one specific use and that is to fetch EVERY comment of an array of TikTok Videos.

Use with caution!

## ⚠️ Known Issues

- ⏳ **MS_TOKEN Expiry:** TikTok session tokens (`MS_TOKEN`) expire quickly (often within 5–10 minutes). You must frequently update your `.env` file with a fresh token to continue scraping.
- 🚫 **Rate Limiting & Bot Detection:** TikTok aggressively rate-limits and may block scraping attempts, especially if requests are too frequent or from the same IP/MS Token.
- 🔄 **No Automatic Token Refresh:** The tool does not automatically refresh or rotate tokens. Manual intervention is required.
- 🌐 **Proxy/Network Limitations:** Using VPNs or proxies may help, but TikTok can still detect and block automated access.
- 📝 **Incomplete Comment Retrieval:** Due to rate limits and token expiry, it may take multiple runs and manual intervention to retrieve all comments from large videos.

---

## 💡 What This Tool Does

This tool allows you to **scrape comments from one or more TikTok videos** and save them into Excel files.  
For each video, it creates a separate Excel file containing the comment ID, author, text, and like count.  
It supports resuming from where it left off if interrupted or rate-limited.

---

## 🚀 How to Run

1. **Clone the Repository**
   ```sh
   git clone <this-repo-url>
   cd tiktok-comment-scanner
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set Up Your Environment**
   - Create a `.env` file in the project root:
     ```
     MS_TOKEN=your_fresh_ms_token_here
     ```
   - You must obtain a fresh `MS_TOKEN` from your browser (see TikTokApi documentation for details).

4. **Add Target Videos**
   - Edit `targets.json` and add TikTok video URLs you want to scrape, e.g.:
     ```json
     [
       "https://www.tiktok.com/@user/video/1234567890123456789",
       "https://www.tiktok.com/@user/video/9876543210987654321"
     ]
     ```

5. **Run the Tool**
   ```sh
   python main.py
   ```

6. **Check Output**
   - 📁 Scraped comments are saved in the `out/` directory as Excel files, one per video.

---

## 📝 Notes

- ⚠️ If you get rate-limited or your token expires, update your `.env` with a new `MS_TOKEN` and re-run the script. The tool will resume from where it left off.
- For best results, use a mobile hotspot or residential proxy, and avoid making requests too quickly.
- This tool is for educational and research purposes only. Use responsibly and respect TikTok's terms