import http.client
import json
import random
import html
from replit import db

def getSession(conn, restype):
  url = ""
  if "quizkey" in db.keys() and restype == 4:
    print("Resetting key")
    key = db["quizkey"]
    url += '/api_token.php?command=reset&token=' + key
  else:
    print("Getting new key")
    url += '/api_token.php?command=request' 
  conn.request('GET', url)
  response = conn.getresponse()
  json_data = json.loads(response.read())
  newkey = json_data['token']
  db["quizkey"] = newkey
  return newkey

def getTrivia(amount, category, difficulty):
  conn = http.client.HTTPSConnection("opentdb.com")
  if "quizkey" not in db.keys():
    key = getSession(conn, 3)
  key = db["quizkey"]
  while True:
    conn.request('GET', '/api.php?amount=' + amount.content + '&category=' + category + '&difficulty=' + difficulty.content + '&type=multiple&token=' + key)
    response = conn.getresponse()
    json_data = json.loads(response.read())
    if json_data['response_code'] == 0:
      return json_data
    else:
      print("Getting a new session key...\n")
      key = getSession(conn, json_data['response_code'])


def getCategories():
  conn = http.client.HTTPSConnection("opentdb.com")
  conn.request('GET', '/api_category.php')
  response = conn.getresponse()
  json_data = json.loads(response.read())
  categories = []
  for i in range(0, 24):
    categories.append(json_data['trivia_categories'][i]['name'])
  return categories

def list_categories(category_list):
  cat_list = "\n"
  tot = len(category_list)
  for i in range(0, tot):
    cat_list += str(i+1) + ". " + category_list[i] + "\n" 
  return cat_list

def fix_regex(string):
  if type(string) == str:
    string = html.unescape(string)
  else:
    for i in range(0, 3):
      string[i] = html.unescape(string[i])
  return string

def extractTriviaLists(triviaData, listType, tot_index):
  required_data = []
  for i in range(0, tot_index):
    temp = triviaData['results'][i][listType]
    data = fix_regex(temp)
    required_data.append(data)
  return required_data

def randomize_answers(correct, incorrect, index):
  all_answers = [incorrect[index][0], incorrect[index][1], incorrect[index][2], correct[index]]
  random.shuffle(all_answers)
  return all_answers

def getAnswer(options, correct_option):
  if options[0] == correct_option:
    return 'a'
  elif options[1] == correct_option:
    return 'b'
  elif options[2] == correct_option:
    return 'c'
  else:
    return 'd'