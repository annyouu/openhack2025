# nutrition_api.py(外部栄養素データ取得)
import requests
from deepl_translator import translate_text
def get_food_info(food_name, api_key):
    # FoodData Central APIのURL
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&api_key={api_key}"

    # APIリクエストを送信
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['foods']:
            food_data = data['foods'][0]
            food_name = food_data.get('description', 'N/A').lower()
            foodtranslated_name = translate_text(food_name)

            # 五大栄養素を取得するためのリスト
            target_nutrients = {
                'Energy': 'カロリー',
                'Protein': 'たんぱく質',
                'Total lipid (fat)': '脂質',
                'Carbohydrate, by difference': '炭水化物',
                'Fiber, total dietary': '食物繊維',
                'Sugars, total': '糖質',  
                'Vitamin A': 'ビタミンA',  
                'Vitamin C': 'ビタミンC',  
                'Calcium, Ca': 'カルシウム',  
                'Iron, Fe': '鉄分'  
            }

            # 栄養素データを格納するための辞書を作成
            nutrients = {
                'calories': {'value': 'N/A', 'unit': 'N/A'},
                'protein': {'value': 'N/A', 'unit': 'N/A'},
                'fat': {'value': 'N/A', 'unit': 'N/A'},
                'carbs': {'value': 'N/A', 'unit': 'N/A'},
                'fiber': {'value': 'N/A', 'unit': ''}
            }

            for nutrient in food_data.get('foodNutrients', []):
                nutrient_name = nutrient.get('nutrientName')
                value = nutrient.get('value', 'N/A')
                unit = nutrient.get('unitName', '').lower()

                # 5大栄養素だけを抽出
                if nutrient_name == 'Energy':
                    nutrients['calories'] = {'value': value, 'unit': unit}
                elif nutrient_name == 'Protein':
                    nutrients['protein'] = {'value': value, 'unit': unit}
                elif nutrient_name == 'Total lipid (fat)':
                    nutrients['fat'] = {'value': value, 'unit': unit}
                elif nutrient_name == 'Carbohydrate, by difference':
                    nutrients['carbs'] = {'value': value, 'unit': unit}
                elif nutrient_name == 'Fiber, total dietary':
                    nutrients['fiber'] = {'value': value, 'unit': unit}

            return {'food_name': foodtranslated_name, 'nutrients': nutrients}
        
        else:
            print(f"食品が見つかりませんでした: {food_name}")
            return None
    
    else:
        print(f"APIリクエストエラー: {response.status_code}")
        return None



