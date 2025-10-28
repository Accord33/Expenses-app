from google import genai
from google.genai import types
import dotenv

dotenv.load_dotenv()

with open('paypay.jpg', 'rb') as f:
    image_bytes = f.read()

image = types.Part.from_bytes(
  data=image_bytes, mime_type="image/jpeg"
)

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["""画像から金額、日付、分類を抽出してください。
以下の形式に従って出力してください。
{
  "price": "抽出した金額",
  "date": "抽出した日付(YYYYMMDD形式)",
  "category": "抽出した分類"
}
categoryは以下の選択肢から選んでください。
- 食費
- 交通費
- 娯楽
- その他

**出力はこの後Pythonで処理されるため、必ずJSON形式で出力してください。不要な文字列(`など)は絶対に含めないでください。**

デバックのため画像でpaypay店となっている場合、それは食費としてください。
""", image],
)

print(response.text)