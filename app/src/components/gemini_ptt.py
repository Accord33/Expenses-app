"""Gemini APIを使用した画像解析機能"""
import json
from pathlib import Path
from google import genai
from google.genai import types


def analyze_receipt_image(image_path: Path) -> dict:
    """
    画像から金額、日付、分類を抽出する
    
    Args:
        image_path: 解析する画像ファイルのパス
        
    Returns:
        dict: 抽出されたデータ {"price": str, "date": str, "category": str}
              エラー時は {"error": str} を返す
    """
    try:
        # 画像ファイルを読み込み
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        # MIMEタイプの判定
        suffix = image_path.suffix.lower()
        mime_type_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_type_map.get(suffix, 'image/jpeg')
        
        # Gemini API用の画像オブジェクトを作成
        image = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )
        
        # Gemini APIクライアントを初期化
        client = genai.Client()
        
        # プロンプトを作成
        prompt = """画像から金額、日付、分類を抽出してください。
以下の形式に従って出力してください。
{
  "price": "抽出した金額",
  "date": "抽出した日付(YYYYMMDD形式)",
  "category": "抽出した分類"
}
categoryは以下の選択肢から選んでください。
- 食費
- 交通費
- 娯楽費
- 日用品

**出力はこの後Pythonで処理されるため、必ずJSON形式で出力してください。不要な文字列(```json などのマークダウン記法)は絶対に含めないでください。**

デバッグのため画像でpaypay店となっている場合、それは食費としてください。
"""
        
        # Gemini APIにリクエストを送信
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image],
        )
        
        # レスポンステキストを取得
        response_text = response.text.strip()
        print(f"Gemini APIレスポンス: {response_text}")
        
        # JSONとしてパース
        # マークダウンのコードブロックが含まれている場合は除去
        if response_text.startswith('```'):
            # ```json と ``` を除去
            lines = response_text.split('\n')
            response_text = '\n'.join(lines[1:-1])
        
        result = json.loads(response_text)
        
        # 必要なキーが含まれているか確認
        required_keys = ['price', 'date', 'category']
        if not all(key in result for key in required_keys):
            return {"error": "必要なデータが抽出できませんでした"}
        
        return result
        
    except FileNotFoundError:
        return {"error": f"画像ファイルが見つかりません: {image_path}"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON解析エラー: {str(e)}"}
    except Exception as e:
        return {"error": f"画像解析エラー: {str(e)}"}