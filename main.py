import wave
from fastapi.responses import FileResponse

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from Raven"}

@app.websocket("/ws")
async def echo(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"Echo: {message}")
    except WebSocketDisconnect:
        print("Client disconnected")

PAGE = """
<!DOCTYPE html>
<html>
<body>
  <h2>Raven WebSocket test</h2>
  <input id="msg" placeholder="Type a message">
  <button onclick="send()">Send</button>
  <ul id="log"></ul>
  <script>
    const ws = new WebSocket("ws://127.0.0.1:8000/ws");
    ws.onmessage = (e) => {
      const li = document.createElement("li");
      li.textContent = e.data;
      document.getElementById("log").appendChild(li);
    };
    function send() {
      const box = document.getElementById("msg");
      ws.send(box.value);
      box.value = "";
    }
  </script>
</body>
</html>
"""

@app.get("/test")
def test_page():
    return HTMLResponse(PAGE)
@app.get("/mic")
def mic_page():
    return FileResponse("mic.html")

@app.websocket("/ws-audio")
async def audio_ws(websocket: WebSocket):
    await websocket.accept()
    chunks = []
    try:
        while True:
            data = await websocket.receive_bytes()
            chunks.append(data)
    except WebSocketDisconnect:
        pass
    pcm = b"".join(chunks)
    with wave.open("mic_test.wav", "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(pcm)
    print(f"Saved mic_test.wav ({len(pcm)} bytes)")