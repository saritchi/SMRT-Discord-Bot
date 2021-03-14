from discord.ext import commands
import urllib.parse
import os
import fortune
import quiz
import chance

#Used to keep bot online continuously
from keep_alive import keep_alive

bot = commands.Bot(command_prefix='$')
  
@bot.event
async def on_ready():
  print('Bot is logged in!')

@bot.command(pass_context=True)
async def ask(ctx, *, arg):
  question = urllib.parse.quote(arg)
  answer = fortune.getPrediction(question)
  await ctx.send(answer)

@bot.command(pass_context=True)
async def coin(ctx):
  result = chance.flip_coin()
  await ctx.send("{}".format(result))

@bot.command(pass_context=True)
async def d6(ctx):
  result = chance.roll_d6()
  await ctx.send("Rolled a {}".format(result))

@bot.command(pass_context=True)
async def d20(ctx):
  result = chance.roll_d20()
  await ctx.send("Rolled a {}".format(result))

@bot.command(pass_context=True)
async def trivia(ctx):
  channel = ctx.channel
  total_correct = 0

  def checkAmount(m):
    return m.content.isdigit() and int(m.content) > 4 and int(m.content) < 11 and m.channel == channel
    
  def checkCat(m):
    if m.content.isdigit() and int(m.content) in range(1, 25):
      m.content = str(int(m.content) - 1)
      return m.channel == channel

  def checkDif(m):
    trivia_dif = ['easy', 'medium', 'hard'] 
    if m.content.isdigit() and int(m.content) in range(1, 4):
      m.content = str(trivia_dif[int(m.content) - 1])
      return m.content in trivia_dif and m.channel == channel

  def checkChoice(m):
    choices = ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']
    if m.content.isupper():
      m.content = m.content.lower()
    return m.content in choices and m.channel == channel

  def convertCat(cat):
    cat = str(int(cat) + 9)
    return cat
      
  await ctx.send('Welcome to Trivia!\n**How many questions would you like?(5 - 10)**')
  amount = await bot.wait_for('message', check=checkAmount)

  cats = quiz.getCategories()
  cat_string = quiz.list_categories(cats)

  await ctx.send('**What category should the trivia be?**' + cat_string)
  category = await bot.wait_for('message', check=checkCat)
  category = convertCat(category.content)

  await ctx.send('**What difficulty would you like?**\n1. Easy\n2. Medium\n3. Hard')
  difficulty = await bot.wait_for('message', check=checkDif)

  await ctx.send('Generating Trivia...')
  trivia_data = quiz.getTrivia(amount, category, difficulty)

  total = int(amount.content)
  question_list = quiz.extractTriviaLists(trivia_data, 'question', total)
  correct_list = quiz.extractTriviaLists(trivia_data, 'correct_answer', total)
  incorrect_list = quiz.extractTriviaLists(trivia_data, 'incorrect_answers', total)

  for i in range(0, total):
    question_choices = quiz.randomize_answers(correct_list, incorrect_list, i)
    correctLetter = quiz.getAnswer(question_choices, correct_list[i])
    await ctx.send('**Question #' + str(i+1) + '**:\n' + question_list[i] + '\na) ' + question_choices[0] + '\nb) '  + question_choices[1] + '\nc) '  + question_choices[2] + '\nd) '  + question_choices[3])
    choice = await bot.wait_for('message', check=checkChoice)
    if correctLetter == choice.content:
      await ctx.send('**Correct!**\n')
      total_correct = total_correct + 1
    else:
      await ctx.send('**Incorrect!** The correct answer was: *' + correct_list[i] + '*.\n')

  await ctx.send('**Final Score**: ' + str(total_correct) + '/' + str(total))  

keep_alive()
bot.run(os.getenv('TOKEN'))
