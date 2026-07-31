from google import genai

client = genai.Client()

response = client.models.generate_content(
    model='gemini-3.5-flash',
    contents='Yazılım dünyasında neden backend mühendisliği önemlidir? Tek cümleyle açıkla.'
)

print("Gemini Yanıtı:")
print(response.text)
