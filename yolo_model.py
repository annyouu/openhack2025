from ultralytics import YOLO

# 事前学習済みのYOLOモデルをロード
model = YOLO("yolov8n.pt")

# データセットのパスを指定してトレーニング
model.train(
    data='/Users/kakuanrou/Desktop/flask+Python+YOLO/food_dataset/food_dataset.yaml',  # データセットのyamlファイル
    epochs=60,  # エポック数
    batch=16,   # バッチサイズ
    imgsz=640,   # 画像サイズ
    patience=20, # 20エポック連続で改善しないならストップ
    fliplr=0.5,  # 左右反転の確率（50%）
    flipud=0.1,  # 上下反転の確率（10%）
    mosaic=0.8,  # モザイク（80%の確率で適用）
    mixup=0.3,   # Mixup（30%の確率で適用）
    copy_paste=0.2,  # Copy-Pasteを適用
    scale=0.6,   # 拡大縮小（無理のない範囲に調整）
    shear=0.1,   # シアー（斜め変形）
    hsv_h=0.02,  # 色相変化
    hsv_s=0.8,   # 彩度変化（強め）
    hsv_v=0.5    # 明るさ変化（適度に）
)

print("機械学習を行うことに成功！！")
