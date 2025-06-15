from dotenv import load_dotenv
import os
from src.export import excel
from src.api import retrieve_comments
import asyncio
import json

load_dotenv()
MS_TOKEN = os.getenv("MS_TOKEN")
if not MS_TOKEN:
    raise ValueError("MS_TOKEN environment variable is not set.")

with open("targets.json", "r", encoding="utf-8") as f:
    videos = json.load(f)

if len(videos) == 0:
    raise ValueError("Nothing was specified in targets.json! No Videos provided!")

async def main():
    await retrieve_comments(ms_token=MS_TOKEN, video_links=videos)


if   __name__ == "__main__":
    asyncio.run(main())