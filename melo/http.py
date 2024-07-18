import uvicorn
import io

from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, Response

from melo.api import TTS


class Speaker(str, Enum):
    EN_US = "EN-US"
    EN_BR = "EN-BR"
    EN_INDIA = "EN_INDIA"
    EN_AU = "EN-AU"
    EN_DEFAULT = "EN-Default"


app = FastAPI()


class SpeechRequest(BaseModel):
    text: str
    voice: Speaker = Speaker.EN_DEFAULT


model = TTS(language="EN", device="cuda")
spk2id = model.hps.data.spk2id


@app.get("/audio/speakers")
def get_audio_speakers():
    # {"speakers":["EN-US","EN-BR","EN_INDIA","EN-AU","EN-Default"]}
    return {"speakers": list(spk2id.keys())}


@app.post("/audio/speech")
def create_audio_speech(request: SpeechRequest):
    speaker_id = spk2id[request.voice]

    bio = io.BytesIO()
    model.tts_to_file(request.text, speaker_id, bio, format="wav")
    return Response(content=bio.getvalue(), media_type="audio/wav")


def start():
    uvicorn.run("melo.http:app", host="0.0.0.0", port=9000, reload=True)
