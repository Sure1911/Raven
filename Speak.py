import boto3

polly = boto3.client("polly", region_name="us-east-1")
response = polly.synthesize_speech(
    Text="Hola, bienvenidos a la reunión.",
    VoiceId="Lupe",
    OutputFormat="mp3",
    Engine="neural",
)
with open("hello.mp3", "wb") as f:
    f.write(response["AudioStream"].read())