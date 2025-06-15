import asyncio, os, json, re
from TikTokApi import TikTokApi
from TikTokApi.helpers import extract_video_id_from_url
from src.export.excel import export_comment_to_excel
from openpyxl import load_workbook

def sanitize_filename(s):
    return re.sub(r'[\\/*?:"<>|]', "_", s)

def get_existing_comment_ids(filename):
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_dir = os.path.join(root_dir, "out")
    excel_filename = os.path.join(out_dir, filename)
    if not os.path.exists(excel_filename):
        return set()
    wb = load_workbook(excel_filename)
    ws = wb.active
    return set(str(row[0].value) for row in ws.iter_rows(min_row=2) if row[0].value)

def load_state(state_file):
    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_state(state_file, state):
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f)

async def retrieve_comments(
    ms_token: str,
    video_links: list,
    target_id="",
    batch_size=50,
    wait_time=60,
    fail_wait_time=600,
    max_failures=5,
    state_file="comment_state.json"
):
    state = load_state(state_file)
    async with TikTokApi() as api:
        await api.create_sessions(headless=False, ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        
        if target_id:
            video_ids = [target_id]
            video_url_map = {target_id: video_links[0] if video_links else target_id}
        else:
            video_ids = [extract_video_id_from_url(video) for video in video_links]
            video_url_map = {extract_video_id_from_url(url): url for url in video_links}
        
        for current_id in video_ids:
            video_url = video_url_map.get(current_id, current_id)
            safe_filename = f"video_{sanitize_filename(video_url)}.xlsx"
            print(f"Starting to fetch comments for video {current_id}")
            cursor = state.get(current_id, {}).get("cursor", 0)
            fetched_comment_ids = get_existing_comment_ids(safe_filename)
            consecutive_failures = 0
            try:
                while True:
                    try:
                        comments_gen = api.video(id=current_id).comments(count=batch_size, cursor=cursor)
                        batch = []
                        async for comment in comments_gen:
                            if comment.id in fetched_comment_ids:
                                continue
                            batch.append(comment)
                            fetched_comment_ids.add(comment.id)
                        
                        if not batch:
                            print(f"No more new comments for video {current_id}.")
                            break

                        for comment in batch:
                            export_comment_to_excel(
                                comment.id,
                                comment.author.username,
                                comment.text,
                                comment.likes_count,
                                safe_filename
                            )
                            print(f"Fetched comment {comment.id} for video {current_id}")

                        cursor += batch_size

                        state[current_id] = {"cursor": cursor}
                        save_state(state_file, state)
                        print(f"Waiting {wait_time} seconds before fetching next batch for video {current_id}...")
                        await asyncio.sleep(wait_time)
                        consecutive_failures = 0 
                    except Exception as e:
                        err_msg = str(e).lower()
                        print(f"Error while fetching comments for video {current_id}: {e}")
                        if "bot" in err_msg or "fail" in err_msg or "empty response" in err_msg:
                            consecutive_failures += 1
                            print(f"Rate limited or detected as bot. Failure count: {consecutive_failures}/{max_failures}. Waiting {fail_wait_time // 60} minutes before retrying...")
                            # Save state before waiting
                            state[current_id] = {"cursor": cursor}
                            save_state(state_file, state)
                            await asyncio.sleep(fail_wait_time)
                            if consecutive_failures >= max_failures:
                                print(f"Flagged {max_failures} times in a row for video {current_id}. Saving progress and stopping for this video.")
                                state[current_id] = {"cursor": cursor}
                                save_state(state_file, state)
                                break
                        else:
                            # Save state on unknown error and break
                            state[current_id] = {"cursor": cursor}
                            save_state(state_file, state)
                            break
            except KeyboardInterrupt:
                print("Interrupted by user. Saving state and exiting...")
                state[current_id] = {"cursor": cursor}
                save_state(state_file, state)
                break