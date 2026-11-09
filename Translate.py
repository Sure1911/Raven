import boto3

client = boto3.client("translate", region_name="us-east-1")
result = client.translate_text(
    Text="Hello, welcome to the meeting.",
    SourceLanguageCode="fr",
    TargetLanguageCode="hi",
)
print(result["TranslatedText"])