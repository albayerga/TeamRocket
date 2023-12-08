# myTeam.py

# ---------

# Licensing Information:  You are free to use or extend these projects for

# educational purposes provided that (1) you do not distribute or publish

# solutions, (2) you retain this notice, and (3) you provide clear

# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.

# 

# Attribution Information: The Pacman AI projects were developed at UC Berkeley.

# The core projects and autograders were primarily created by John DeNero

# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).

# Student side autograding was added by Brad Miller, Nick Hay, and

# Pieter Abbeel (pabbeel@cs.berkeley.edu).





import random

import util



from captureAgents import CaptureAgent

from game import Directions

from util import nearestPoint



#################

# Team creation #

#################

winning = False

tie = True

food = True



foodToReach = 18



def create_team(first_index, second_index, is_red,

                first='Agent1', second='Agent2', num_training=0):

    """

    This function should return a list of two agents that will form the

    team, initialized using firstIndex and secondIndex as their agent

    index numbers.  isRed is True if the red team is being created, and

    will be False if the blue team is being created.



    As a potentially helpful development aid, this function can take

    additional string-valued keyword arguments ("first" and "second" are

    such arguments in the case of this function), which will come from

    the --redOpts and --blueOpts command-line arguments to capture.py.

    For the nightly contest, however, your team will be created without

    any extra arguments, so you should make sure that the default

    behavior is what you want for the nightly contest.

    """

    

    return [eval(first)(first_index), eval(second)(second_index)]

    

    """


    if winning == True and tie == False:

        return strategy(first_index, second_index, is_red, first='DefensiveReflexAgent', second='DefensiveReflexAgent', num_training=0)

    if winning != True and tie == False:

        return strategy(first_index, second_index, is_red, first='OffensiveReflexAgent', second='OffensiveReflexAgent', num_training=0)

    if tie == True:

        return strategy(first_index, second_index, is_red, first='OffensiveReflexAgent', second='DefensiveReflexAgent', num_training=0)

    if tie == True and food == False:

        return strategy(first_index, second_index, is_red, first='OffensiveReflexAgent', second='DefensiveReflexAgent', num_training=0)

    """

    



def strategy(first_index, second_index, is_red, first, second, num_training=0):

    return [eval(first)(first_index), eval(second)(second_index)]

##########

# Agents #

##########



class MyAgent(CaptureAgent):



    def __init__(self, index, time_for_computing=.1):

        super().__init__(index, time_for_computing)

        #self.is_red = None





    def register_initial_state(self, game_state):

        self.start = game_state.get_agent_position(self.index)

        #self.is_red = game_state.is_red(self.index)

        CaptureAgent.register_initial_state(self, game_state)





    def get_successor(self, game_state, action):

        successor = game_state.generate_successor(self.index, action)

        pos = successor.get_agent_state(self.index).get_position()

        if pos != nearestPoint(pos): #verify if pos is a wall

            return successor.generate_successor(self.index, action) 

        else:

            return successor





    def get_balance(self, game_state):

        """

        Calculates the difference between our agent's current score and opponent's current score.

        Returns a positive value if our agent is winning, negative if losing, and 0 if tied.

        """

        # 1st calculate the difference in food count between the two teams

        is_red = game_state.is_red(self.start) #is_red is True if our agent is red, False if blue

        if is_red:

            our_food = game_state.get_red_food()

            opponent_food = game_state.get_blue_food()

        else:

            our_food = game_state.get_blue_food()

            opponent_food = game_state.get_red_food()



        # food is a 2d array of booleans, where True indicates the presence of food

        num_our_food = sum(row.count(True) for row in our_food)

        num_opponent_food = sum(row.count(True) for row in opponent_food)



        food_balance = num_our_food - num_opponent_food #positive if we have more food, negative if opponent has more food



        # 2nd take into account our current score (red scores positive and blue scores negative -> change it to positive for both)

        if is_red:

            positive_score = game_state.get_score()

        else:

            positive_score = -game_state.get_score()



        return food_balance

        #we can try to just return food_balance + positive_score



    

    

    def get_features(self, game_state, action):

        features = util.Counter()  

        #feature logic here

        return features



    

    def get_weights(self, game_state, action):

        #weights logic here

        #weights = {} #{'successor_score': 1.0, 'distance_to_food': -100.0, 'distance_to_capsule': -100.0, 'distance_to_ghost': 0.0, 'distance_to_teammate': 0.0, 'distance_to_border': 0.0, 'distance_to_center': 0.0, 'distance_to_opponent': 0.0, 'distance_to_wall': 0.0}

        weights = util.Counter()

        return weights

    





    def evaluate(self, game_state, action):

        features = self.get_features(game_state, action)

        weights = self.get_weights(game_state, action)

        return features * weights

    

    def getQValue(self, state, action):

        """

          Returns Q(state,action)

          Should return 0.0 if we have never seen a state

          or the Q node value otherwise

        """

        "*** YOUR CODE HERE ***"

        return self.evaluate(state, action)



    def computeValueFromQValues(self, state):

        """

          Returns max_action Q(state,action)

          where the max is over legal actions.  Note that if

          there are no legal actions, which is the case at the

          terminal state, you should return a value of 0.0.

        """

        "*** YOUR CODE HERE ***"

        if not state.get_legal_actions(self.index): #if not a real action return 0

            return 0.0

        else:

          val = util.Counter()

          for act in state.get_legal_actions(self.index):

              val[act] = self.getQValue(state, act)

          return max(val.values())

        



    def computeActionFromQValues(self, state):

        """

          Compute the best action to take in a state.  Note that if there

          are no legal actions, which is the case at the terminal state,

          you should return None.

        """

        "*** YOUR CODE HERE ***"

        if not state.get_legal_actions(self.index):

            return None

        

        qValue = self.computeValueFromQValues(state) #We get the best qValues

        actions = [] #The list of best actions to take in a state

        for action in state.get_legal_actions(self.index):

            

            if qValue == self.getQValue(state, action): 

                actions.append(action)

        return random.choice(actions)

        

    





class Agent1(MyAgent):

    def get_features(self, game_state, action):

        if self.get_score(game_state) < 5: #Attack if loosing or winning under 5

        

            features = util.Counter()

            successor = self.get_successor(game_state, action)

            food_list = self.get_food(successor).as_list()

            features['successor_score'] = -len(food_list)  # self.getScore(successor)



            # Compute distance to the nearest food



            if len(food_list) > 0:  # This should always be True,  but better safe than sorry

                my_pos = successor.get_agent_state(self.index).get_position()

                min_distance = min([self.get_maze_distance(my_pos, food) for food in food_list])

                features['distance_to_food'] = min_distance

            return features

        

        else: #Defend otherwise

        

            features = util.Counter()

            successor = self.get_successor(game_state, action)



            my_state = successor.get_agent_state(self.index)

            my_pos = my_state.get_position()



            # Computes whether we're on defense (1) or offense (0)

            features['on_defense'] = 1

            if my_state.is_pacman: features['on_defense'] = 0



            # Computes distance to invaders we can see

            enemies = [successor.get_agent_state(i) for i in self.get_opponents(successor)]

            invaders = [a for a in enemies if a.is_pacman and a.get_position() is not None]

            features['num_invaders'] = len(invaders)

            if len(invaders) > 0:

                dists = [self.get_maze_distance(my_pos, a.get_position()) for a in invaders]

                features['invader_distance'] = min(dists)



            if action == Directions.STOP: features['stop'] = 1

            rev = Directions.REVERSE[game_state.get_agent_state(self.index).configuration.direction]

            if action == rev: features['reverse'] = 1



            return features



    def get_weights(self, game_state, action):

        if self.get_score(game_state) < 5: #Attack if loosing or winning under 5

            

            return {'successor_score': 100, 'distance_to_food': -1}

        

        else:

        

            return {'num_invaders': -1000, 'on_defense': 100, 'invader_distance': -10, 'stop': -100, 'reverse': -2}

    



  

    def choose_action(self, game_state):

        if self.get_score(game_state) < 5: #Attack if loosing or winning under 5

            

            """

            Picks among the actions with the highest Q(s,a).

            """

            legalActions = game_state.get_legal_actions(self.index)

            if len(legalActions) == 0:

                return None

                

            foodLeft = len(self.get_food(game_state).as_list())

            #count = self.countDotsEated(self)

            

            my_state = game_state.get_agent_state(self.index)

            my_pos = my_state.get_position()

            

            objective = 18 - game_state.get_score()

            

            if foodLeft <= objective:

                

                bestDist = 9999

                for action in legalActions:

                    successor = self.get_successor(game_state, action)

                    pos2 = successor.get_agent_position(self.index)

                    dist = self.get_maze_distance(self.start, pos2)

                    if dist < bestDist:

                        bestAction = action

                        bestDist = dist

                return bestAction



            return self.computeActionFromQValues(game_state)

        

        else:

            

            """

            Picks among the actions with the highest Q(s,a).

            """

            actions = game_state.get_legal_actions(self.index)



            # You can profile your evaluation time by uncommenting these lines

            # start = time.time()

            values = [self.evaluate(game_state, a) for a in actions]

            # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)



            max_value = max(values)

            best_actions = [a for a, v in zip(actions, values) if v == max_value]



            food_left = len(self.get_food(game_state).as_list())



            if food_left <= 2:

                best_dist = 9999

                best_action = None

                for action in actions:

                    successor = self.get_successor(game_state, action)

                    pos2 = successor.get_agent_position(self.index)

                    dist = self.get_maze_distance(self.start, pos2)

                    if dist < best_dist:

                        best_action = action

                        best_dist = dist

                return best_action



            return self.computeActionFromQValues(game_state)

            

        

                

                

            #foodLeft = len(self.get_food(self.observationHistory[i]).as_list())



        



class Agent2(MyAgent):

    def get_features(self, game_state, action):

        features = util.Counter()

        successor = self.get_successor(game_state, action)



        my_state = successor.get_agent_state(self.index)

        my_pos = my_state.get_position()



        # Computes whether we're on defense (1) or offense (0)

        features['on_defense'] = 1

        if my_state.is_pacman: features['on_defense'] = 0



        # Computes distance to invaders we can see

        enemies = [successor.get_agent_state(i) for i in self.get_opponents(successor)]

        invaders = [a for a in enemies if a.is_pacman and a.get_position() is not None]

        features['num_invaders'] = len(invaders)

        if len(invaders) > 0:

            dists = [self.get_maze_distance(my_pos, a.get_position()) for a in invaders]

            features['invader_distance'] = min(dists)



        if action == Directions.STOP: features['stop'] = 1

        rev = Directions.REVERSE[game_state.get_agent_state(self.index).configuration.direction]

        if action == rev: features['reverse'] = 1



        return features



    def get_weights(self, game_state, action):

        return {'num_invaders': -1000, 'on_defense': 100, 'invader_distance': -10, 'stop': -100, 'reverse': -2}

    

    

    

    def choose_action(self, game_state):

        """

        Picks among the actions with the highest Q(s,a).

        """

        actions = game_state.get_legal_actions(self.index)



        # You can profile your evaluation time by uncommenting these lines

        # start = time.time()

        values = [self.evaluate(game_state, a) for a in actions]

        # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)



        max_value = max(values)

        best_actions = [a for a, v in zip(actions, values) if v == max_value]



        food_left = len(self.get_food(game_state).as_list())



        if food_left <= 2:

            best_dist = 9999

            best_action = None

            for action in actions:

                successor = self.get_successor(game_state, action)

                pos2 = successor.get_agent_position(self.index)

                dist = self.get_maze_distance(self.start, pos2)

                if dist < best_dist:

                    best_action = action

                    best_dist = dist

            return best_action



        return self.computeActionFromQValues(game_state)

