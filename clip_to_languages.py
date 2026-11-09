import boto3

translate = boto3.client("translate", region_name="us-east-1")
polly = boto3.client("polly", region_name="us-east-1")

VOICES = {"es": "Lupe", "fr": "Lea", "hi": "Kajal"}

def translate_text(text, lang):
    r = translate.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=lang)
    return r["TranslatedText"]

def speak(text, lang):
    r = polly.synthesize_speech(
        Text=text, VoiceId=VOICES[lang],
        OutputFormat="mp3", Engine="neural")
    return r["AudioStream"].read()

with open("transcript.txt", encoding="utf-8") as f:
    sentence = f.read()

print("English:", sentence)
for lang in ["es", "fr", "hi"]:
    translated = translate_text(sentence, lang)
    print(lang, translated)
    with open(f"clip_{lang}.mp3", "wb") as f:
        f.write(speak(translated, lang))