from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import paho.mqtt.client as mqtt

mqtt_client = None
app = FastAPI()

class EMQX(BaseModel):
    username: str
    password: str

class PublishMessage(BaseModel):
    topic: str
    message: str

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/connect/")
def EMQX_connection(credentials: EMQX):
    global mqtt_client
    try:
        mqtt_client = mqtt.Client()
        mqtt_client.username_pw_set(credentials.username, credentials.password)
        mqtt_client.connect("emqx", 1883, 60)
        mqtt_client.loop_start()
        return {"status": "Connected to EMQX broker"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/publish/")
def EMQX_publish_message(data: PublishMessage):
    if mqtt_client is None:
        raise HTTPException(status_code=400, detail="Not connected to EMQX broker")
    try:
        mqtt_client.publish(data.topic, data.message)
        return {"status": "Message published", "topic": data.topic, "message": data.message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)