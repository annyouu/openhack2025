import requests

# DeepL APIキー
API_KEY = '77a91573-78e7-4e35-9ade-22a50150cb7d:fx'

# DeepL APIのエンドポイント
DEEPL_API_URL = 'https://api-free.deepl.com/v2/translate'

# 翻訳する処理
def translate_text(text, target_lang='JA'):
    # DeepL APIにリクエストを送信
    params = {
        'auth_key': API_KEY,
        'text': text,
        'target_lang': target_lang  # 日本語にする
    }

    response = requests.post(DEEPL_API_URL, data=params)

    if response.status_code == 200:
        data = response.json()
        if 'translations' in data and len(data['translations']) > 0:
            translated_text = data['translations'][0]['text']

            # 翻訳後に置き換えを行う
            translated_text = translated_text.replace("フライドチキン", "唐揚げ")
            translated_text = translated_text.replace("アップル", "りんご")
            
            return translated_text
        else:
            print("翻訳データが見つかりません", data)
            return "食品名不明"
    else:
        print(f"DeepL APIリクエストエラー: {response.status_code}, レスポンス: {response.text}")
        return "APIに接続できないです"

    

# food = "egg"
# translated_food = translate_text(food)
# print(f"日本語: {translated_food}")

