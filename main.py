from dotenv import load_dotenv
import os
from src.export import excel

load_dotenv()
MS_TOKEN = os.getenv("MS_TOKEN")
if not MS_TOKEN:
    raise ValueError("MS_TOKEN environment variable is not set.")

videos = [
    "https://vm.tiktok.com/ZNdAx7V5k/",
    "https://vm.tiktok.com/ZNdAQ2H1g/",
    "https://vm.tiktok.com/ZNdAxK9Wo/",
    "https://vm.tiktok.com/ZNdAQdpUS/",
    "https://vm.tiktok.com/ZNdAQjJbb/",
]



def main():
    pass


if   __name__ == "__main__":
    main()