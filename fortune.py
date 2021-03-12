import http.client
import json

def prediction_valid(json_res):
  if json_res['magic']['type'] != 'Neutral':
    return True

def getPrediction(question):
  conn = http.client.HTTPSConnection("8ball.delegator.com")
  while True:
    conn.request('GET', '/magic/JSON/' + question)
    response = conn.getresponse()
    json_data = json.loads(response.read())
    if prediction_valid(json_data):
      answer = json_data['magic']['answer']
      return answer