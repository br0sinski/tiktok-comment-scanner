import asyncio, os
from TikTokApi import TikTokApi
from TikTokApi.helpers import extract_video_id_from_url
from src.export.excel import export_comment_to_excel

async def retrieve_comments(ms_token: str, video_links: list, target_id=""):
    async with TikTokApi() as api:
        await api.create_sessions(headless=False, ms_tokens=[ms_token], num_sessions=10, sleep_after=3)
        
        if target_id:
            video_ids = [target_id]
        else:
            video_ids = [extract_video_id_from_url(video) for video in video_links]
        
        for current_id in video_ids:
            comments = api.video(id=current_id).comments(count=50)
            async for comment in comments:
                print(current_id)
                id = comment.id
                author = comment.author.username
                text = comment.text
                likes = comment.likes_count
                export_comment_to_excel(id, author, text, likes, current_id)


