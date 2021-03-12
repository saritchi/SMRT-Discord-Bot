import random

def roll_d6():
  roll = random.randint(1, 6)
  return roll

def roll_d20():
  roll = random.randint(1, 20)
  return roll

def flip_coin():
  result = random.randint(1,2)
  if result == 1:
    return "Heads"
  else:
    return "Tails"