from flask import Flask,request,Response
from botbuilder.schema import Activity
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    ConversationState, 
    MemoryStorage,
)
import asyncio


from candidate_bot import CandidateBot
from c_model import Model

app = Flask(__name__)
loop = asyncio.get_event_loop()


botadaptersettings = BotFrameworkAdapterSettings("", "")
botadapter = BotFrameworkAdapter(botadaptersettings)

memstore = MemoryStorage()
constate = ConversationState(memstore)

cbot = CandidateBot(constate)

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers['content-type']:
        jsonmessage = request.json
    else :
        return Response(status=415)
    
    activity = Activity().deserialize(jsonmessage)

    auth_header = (request.headers['Authorization'] if "Authorization" in request.headers else "")

    async def turn_call(turn_context):
        profileinfo = await cbot.welcome_user(turn_context)
        if profileinfo is not None:
            model = Model()
            model.add_profile(profileinfo)
            model.save_to_csv("candidates.csv")

    task = loop.create_task(botadapter.process_activity(activity,auth_header,turn_call))
    loop.run_until_complete(task)

    return Response(status=200)

if __name__ == '__main__':
    app.run('localhost',3978)
    