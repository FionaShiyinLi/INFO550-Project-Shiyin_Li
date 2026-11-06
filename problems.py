'''
This file will contain your the code for your problems. 
'''
import numpy as np
import cv2
from algorithms import RandomAgent

class Game:
    def __init__(self, problem,player,verbose=True):
      self.problem = problem      
      self.player = player
      self.verbose = verbose   
      if self.verbose:
         self.problem.showState()
    def playGame(self):
      while self.problem.isTerminal()==False:           
         move = self.player.getMove(self.problem)
         self.problem.doMove(move)
         if self.verbose:
            self.problem.showState()
            print(f"Move {self.problem.ticks}:")
            print(self.problem.state)

      print(f"Game Over! Food eaten: {self.problem.score}")
      if self.verbose:
         self.problem.showState(1500)
      return self.problem.score
              
class Snake:
   def __init__(self):
      self.state = ((0, 0), (1, 1), (1, 0))
      self.ticks = 0
      self.score = 0
      self.stepsWithoutFood = 0

   def getLegalMoves(self, state=None):
      if state is None:
         state = self.state
      food, head = state[0], state[1]
      moves = []
      for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
         newHead = (head[0] + dr, head[1] + dc)

         if not (0 <= newHead[0] < 3 and 0 <= newHead[1] < 3):
            continue

         if len(state) > 2 and newHead == state[2]:
            continue

         body = state[2:] if newHead == food else state[2:-1]
         if newHead not in body:
            moves.append((dr, dc))
      return moves

   def getSuccessor(self, move, state):
      food, head = state[0], state[1]
      newHead = (head[0] + move[0], head[1] + move[1])

      if newHead == food:
         snake = (newHead,) + state[1:]
         empty = [(r, c) for r in range(3) for c in range(3)
                  if (r, c) not in snake]
         newFood = empty[np.random.randint(len(empty))] if empty else None
      else:
         snake = (newHead,) + state[1:-1]
         newFood = food
      return (newFood,) + snake

   def doMove(self,move):
      oldFood = self.state[0]
      self.state = self.getSuccessor(move, self.state)
      self.ticks += 1

      if self.state[1] == oldFood:
         self.score += 1
         self.stepsWithoutFood = 0
      else:
         self.stepsWithoutFood += 1

   def isTerminal(self, state=None):
      if state is None:
         state = self.state

      return (state[0] is None or
              self.stepsWithoutFood >= 18 or
              len(self.getLegalMoves(state)) == 0)

   def showState(self, ms = 1000,state=None):
      if state is None:
         state = self.state

      screen = np.zeros((150, 150, 3), dtype=np.uint8)

      # Snake: red
      for r, c in state[1:]:
         cv2.rectangle(screen, (c * 50 + 1, r * 50 + 1),
                       (c * 50 + 48, r * 50 + 48), (0, 0, 255), -1)

      # Food: yellow
      if state[0] is not None:
         r, c = state[0]
         cv2.rectangle(screen, (c * 50 + 1, r * 50 + 1),
                       (c * 50 + 48, r * 50 + 48), (0, 255, 255), -1)

      cv2.imshow('Snake', screen)
      cv2.waitKey(ms)


game = Game(Snake(), RandomAgent())
game.playGame()
