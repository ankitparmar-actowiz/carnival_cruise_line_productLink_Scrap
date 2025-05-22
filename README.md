# 🚢 Carnival Cruise Link Extractor – Selenium & Requests Hybrid

This repository contains two powerful scraping scripts to extract **Carnival Cruise Line** package URLs from [MyAgentGenie](https://tap5.myagentgenie.com/phillipcrane/), a dynamically rendered travel portal.

Due to the website’s reliance on JavaScript rendering and no direct API for links, a hybrid scraping approach was adopted using both **Selenium** and **Requests** (via `curl_cffi`).

---

## ✅ Approach

Scraping this site required iterative experimentation due to dynamic rendering and limited API access. Here's how the solution evolved:

1. **Initial Attempt (Full Automation)**  
   - Used `undetected_chromedriver` to simulate user behavior and manually interact with UI components (dropdowns, buttons, etc.).
   - Extracted links by clicking the share icon and pasting the copied URL using `pyperclip`.

2. **Limitations Observed**  
   - The UI was slow to respond due to JavaScript-heavy components.
   - Loading all itineraries one-by-one was inefficient for bulk extraction.

3. **Network Request Discovery**  
   - Identified a dynamic network API call made after filters were applied.
   - This endpoint returned itinerary data in JSON format – ideal for direct scraping.

4. **Final Solution (Hybrid Model)**  
   - Used `selenium-wire` to intercept network requests and extract **cookies** and **headers** (including dynamic `uniquetid`).
   - Performed high-speed data extraction using `curl_cffi.requests` by simulating the same API request with the captured headers and cookies.
   - Result: Fast and stable extraction of cruise package links using API pagination.

---

## 📁 Scripts Included

| File | Description |
|------|-------------|
| `extract_links_request.py` | Hybrid script using Selenium to get headers + cookies and `requests` for API pagination |
| `extract_links_selenium.py` | Full browser automation approach using `undetected-chromedriver` + `pyperclip` |

---

## 📦 Output Files

- `newLinks.json` – Output of API-based scraper (fast and stable)
- `links_paste.json` – Output of full Selenium-based scraping (slower and more manual)

---

## 🧰 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
