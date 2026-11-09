import time
import json
import urllib.request
import boto3

BUCKET = "raven-ks"
FILE = "ks.mp4"
JOB_NAME = "raven-test-" + str(int(time.time()))

s3 = boto3.client("s3", region_name="us-east-1")
transcribe = boto3.client("transcribe", region_name="us-east-1")

s3.upload_file(FILE, BUCKET, FILE)
print("Uploaded", FILE)

transcribe.start_transcription_job(
    TranscriptionJobName=JOB_NAME,
    Media={"MediaFileUri": f"s3://{BUCKET}/{FILE}"},
    MediaFormat="mp4",
    LanguageCode="en-US",
)
print("Job started...")

while True:
    job = transcribe.get_transcription_job(TranscriptionJobName=JOB_NAME)
    status = job["TranscriptionJob"]["TranscriptionJobStatus"]
    print(status)
    if status in ("COMPLETED", "FAILED"):
        break
    time.sleep(5)

if status == "COMPLETED":
    url = job["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
        text = data["results"]["transcripts"][0]["transcript"]
    print(text)
    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(text)
else:
    print(job["TranscriptionJob"].get("FailureReason"))