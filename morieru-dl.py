import os
import time
import pathlib
import json
import schedule
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import urllib.request
import gspread
from google.oauth2.service_account import Credentials
import tweepy


ENDED_IDS = "./share/ended_ids.txt"
MORIERUS_JSON = "./morierus/json/morierus.json"


def download_morieru():
    print("downloading morieru...")
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    credentials = Credentials.from_service_account_file(os.environ.get("SECRET_CREDENTIALS_JSON_OATH"), scopes=scopes)
    gc = gspread.authorize(credentials)
    workbook = gc.open_by_key(os.environ.get("WORKBOOK_KEY"))
    worksheet = workbook.get_worksheet(0)

    # D列
    status_list = worksheet.col_values(4)

    ids = [s.replace("https://twitter.com/pirocot/status/", "") for s in status_list]

    # Twitterの認証
    auth = tweepy.OAuthHandler(os.environ.get("API_KEY"), os.environ.get("API_KEY_SECRET"))
    auth.set_access_token(os.environ.get("ACCESS_TOKEN"), os.environ.get("ACCESS_TOKEN_SECRET"))
    api = tweepy.API(auth)

    ended_ids = []
    if os.path.exists(ENDED_IDS):
        with open(ENDED_IDS, "r") as f:
            ended_ids = f.read().splitlines()

    actual = 1
    for id in ids:
        if id in ended_ids:
            print(f"{id} is already downloaded.")
            continue
        print(f"{id}:")
        s = api.get_status(id)
        if hasattr(s, "extended_entities") and "media" in s.extended_entities:
            for j, m in enumerate(s.extended_entities["media"]):
                url = m["media_url_https"]
                _, ext = os.path.splitext(url)
                save_name = f"./morierus/{jst_string(s.created_at)}_{j}{ext}"
                print(f"{id}: {url}")
                urllib.request.urlretrieve(url, save_name)
                actual += 1
        end_id(id)
        if actual % 800 == 0:
            print("Waiting API rate limit.")
            time.sleep(15 * 60)

    # ファイル一覧をJSONに出力
    morierus = os.listdir("./morierus/")
    morierus_file = [f for f in morierus if os.path.isfile(os.path.join("./morierus/", f))]

    with open(MORIERUS_JSON, "w") as f:
        json.dump(morierus_file, f, indent=4)


def main():
    load_dotenv(".env")

    schedule.every(1).days.do(download_morieru)

    schedule.run_all()

    while True:
        schedule.run_pending()
        time.sleep(60)


def end_id(id):
    with open(ENDED_IDS, "a") as f:
        f.write(f"{id}\n")


def jst_string(datetime_utc):
    datetime_jst = datetime_utc.astimezone(timezone(timedelta(hours=+9)))
    return datetime.strftime(datetime_jst, "%Y-%m-%d_%H%M%S")


if __name__ == "__main__":
    main()
