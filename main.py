from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import os

from mvlubot.bot import MVLUBot
from mvlubot.message import Message
from mvlubot.cache import message_cache
#feedback router
from feedback import router as feedback_router 

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

#Feedback Router
app.include_router(feedback_router)  

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
    if message.message.lower() in message_cache:
        return Message(
            role="MVLUBOT",
            message=message_cache[message.message.lower()]
        )
    # try:
    return mvlubot.chat(message)
       
    # except:
    #     raise HTTPException(
    #         status_code=500, detail="Oops, it seems that something went wrong on our side.")

    # return result
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ["PORT"]))
