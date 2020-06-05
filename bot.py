from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json

app = Flask(__name__)


@app.route("/bot", methods=['GET', 'POST'])
def bot():
    # ibm-watson auth
    authenticator = IAMAuthenticator('YOUR_API_KEY')

    assistant = AssistantV1(version='2018-07-10', authenticator=authenticator)

    # check workspace status (wait for training to complete)
    workspace_id = 'YOU_WORKSPACE_ID'
    workspace = assistant.get_workspace(workspace_id=workspace_id).get_result()

    print('The workspace status is: {0}'.format(workspace['status']))

    if workspace['status'] == 'Available':
        print('Ready to chat!')
    else:
        print('The workspace should be available shortly. Please try again in 30s.')
        print('(You can send messages, but not all functionality will be supported yet.)')

    # responde to inscoming calls with a simple text message
    # fetch the message
    msg = request.form.get('Body')

    input = {'text': msg}
    response = assistant.message(
        workspace_id=workspace_id, input=input).get_result()
    print(json.dumps(response, indent=2))

    while True:
        if response['intents']:
            print('Detected intent: #' + response['intents'][0]['intent'])

        # print the output from dialog, if any.
        if response['output']['text']:
            resp = MessagingResponse()
            resp.message(str(response['output']['text'][0]))
            return str(resp)


app.run(debug=True)
