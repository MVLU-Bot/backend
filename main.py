from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import os


from mvlubot.bot import MVLUBot
from mvlubot.message import Message
from mvlubot.cache import message_cache

load_dotenv()

app = FastAPI()
mvlubot = MVLUBot()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    """
    Basic root resolver
    """
    return {"message": "Welcome to MVLU Bot"}


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.post("/chat")
async def chat(message: Message):
    result = Message(role="MVLUBOT")

    if message.message.lower() in message_cache:
        result.message = message_cache[message.message.lower()]
        return result

    try:
        output = mvlubot.chat(message.message)
        result.message = output

    except:
        raise HTTPException(
            status_code=500, detail="Oops, it seems that something went wrong on our side.")

    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ["PORT"]))
