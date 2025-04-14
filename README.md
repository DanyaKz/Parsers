# 🔎 Social Media Keyword Comment Scraper

A unified Python-based scraper to collect comments from **Facebook**, **Telegram**, and **Instagram** posts that contain specified **keywords**. Useful for social research, public opinion monitoring, vaccine-related studies, or sentiment analysis.

---

## 📌 Features

- ✅ **Keyword filtering** in multiple languages (Kazakh, Russian, English)
- ✅ Extracts **comments, usernames, timestamps, likes, and post URLs**
- ✅ Supports:
  - 📘 Facebook groups/pages via `facebook_page_scraper`
  - 📷 Instagram via `instagrapi`
  - 📢 Telegram via `telethon`
- ✅ Saves all data in a clean `JSON` format
- ✅ Smart **resuming** and **state tracking** for long-running jobs

---

## 📂 Project Structure

project 
├── requierments.txt # Packages requirements
├── telegram.py # Collects keyword-based Telegram comments 
├── inst.py # Collects keyword-based Instagram posts 
├── instComments.py # Collects Instagram comments 
└── facebook.py # Collects keyword-based Facebook comments 

