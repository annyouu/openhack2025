# 必要な.pyファイル(1) app.py(Flaskのメインアプリ)

import os
from flask import Flask, request, render_template, jsonify
from ultralytics import YOLO
from database import insert_food, clear_foods_table
from nutrition_api import get_food_info
from deepl_translator import translate_text

app = Flask(__name__)

# アップロードフォルダを設定
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# YOLOモデルの読み込み
model = YOLO("runs/detect/train4/weights/best.pt")

API_KEY = "自分で取得したやつを入れてください"

@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "ファイルが見つかりません"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "ファイル名が空です"}), 400
    
    # ファイルを保存
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # YOLOで画像解析
    results = model(filepath)

    # 判別結果を取得
    objects_detected = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls.item())
            class_name = model.names[class_id]
            objects_detected.append(class_name)
    

    # "dining table"が検出された場合に表示し、その物体をリストから削除
    if "dining table" in objects_detected:
        print("dining tableが検出されましたが、データベースには追加されませんでした。")
        objects_detected = [obj for obj in objects_detected if obj != "dining table"]
    
    # foodsテーブルのデータをクリア(前回のデータを消して次回以降に影響がないように)
    clear_foods_table()

    # 検出された食品をデータベースに保存
    for object_name in objects_detected:
        object_name = object_name.replace("_", " ")
        insert_food(object_name)
    
    # 外部APIから栄養情報を取得
    nutrition_info = []
    for food_name in objects_detected:
        food_name = food_name.replace("_", " ")
        food_data = get_food_info(food_name, API_KEY)
        if food_data:
            # 栄養素情報を栄養素名ごとに追加
            food_nutrients = food_data['nutrients']
            nutrition_info.append({
                'food_name' : translate_text(food_data['food_name']),
                'calories': food_nutrients.get('calories', 'N/A'),
                'carbs': food_nutrients.get('carbs', 'N/A'),
                'protein': food_nutrients.get('protein', 'N/A'),
                'fat': food_nutrients.get('fat', 'N/A'),
                'fiber': food_nutrients.get('fiber', 'N/A'),
            })
    
    # 結果ページにリダイレクト
    return render_template("result.html", filename=file.filename, objects_detected=objects_detected, nutrition_info=nutrition_info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

