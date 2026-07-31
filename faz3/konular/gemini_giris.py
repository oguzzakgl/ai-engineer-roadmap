from google import genai

# Client, çevresel değişkenlerdeki GEMINI_API_KEY'i otomatik arar.
client = genai.Client()

response = client.models.generate_content(
    model='gemini-1.5-flash',
    contents='Yazılım dünyasında neden backend mühendisliği önemlidir? Tek cümleyle açıkla.'
)

print("Gemini Yanıtı:")
print(response.text)
