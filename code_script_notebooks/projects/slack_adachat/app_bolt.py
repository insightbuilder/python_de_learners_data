import os
import re
from slack_bolt import App

from slack_bolt.adapter.socket_mode import SocketModeHandler

import os
os.environ['OPENAI_API_KEY']=''
from langchain.llms import OpenAI
from langchain import OpenAI, LLMMathChain

llm = OpenAI(temperature=0)

llm_math = LLMMathChain(llm=llm,
                        verbose=True)

# Initializes your app with your bot token and socket mode handler
app = App(token="")


@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()


@app.message(
    re.compile("""(^[a-zA-Z0-9!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?\s]*$)"""))
def hello_msg(message, say):
    user_req = message['text']
    llm_reply = llm_math.run(user_req)
    say(blocks=[{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Hey there.Here is your answer!\n {llm_reply}"
        },
    }],
    )

@app.error
def global_error_handler(error, body, logger):
    logger.exception(error)
    logger.info(body)


if __name__ == "__main__":
    SocketModeHandler(app, "").start()
