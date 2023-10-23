import RandomPopHeapQ
from backbone_classes import *
from events.oldEvents import *
from events.restaurantEvents import *
from events.events import *
from events.health_events import *
from events.law_events import *
from events.love_events import *
from events.generatedEvents import *

from path_finding import *
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from run import SciFiwaypointTestEnvironmentAlt


class Node:
    def __init__(self, state, parent=None, cost=0, heuristic=0):
        self.state = state  # The current state of the node
        self.parent = parent  # The parent node
        self.cost = cost  # Cost to reach this node from the start node
        self.heuristic = heuristic  # Estimated cost to reach the goal from this node

    def total_cost(self):
        return self.cost + self.heuristic

    def __lt__(self, other):
        return (self.total_cost() < other.total_cost())

    def __gt__(self, other):
        return (self.total_cost() > other.total_cost(other))

def print_story(path):
    storyLength = len(path)
    startState = path[0]
    for i in range(storyLength-1):
        PriorState = path[i]
        CurrentState = path[i+1]
        EventTuple = CurrentState.event_history[i]
        EventType = EventTuple[0]
        eventCharacters = EventTuple[3]
        eventEnvironments = EventTuple[4]
        eventInstance = EventType()
        eventInstance.doEvent(worldstate=PriorState, characters=eventCharacters, environment=eventEnvironments)

def astar_search(start_state, goal_state, get_neighbors, heuristic, events, depthLimit = 15):
    open_set = []  # Priority queue for nodes to be evaluated
    closed_set = set()  # Set to keep track of visited nodes

    # Create the initial node
    start_node = Node(state=start_state, cost=0, heuristic=heuristic(start_state, goal_state))
    RandomPopHeapQ.heappush(open_set, (start_node.total_cost(), start_node))

    while open_set:
        if random.random() < .5:
            _, current_node = RandomPopHeapQ.heappop(open_set)
        else:
            _, current_node = RandomPopHeapQ.heaprandpop(open_set)

        distanceToTarget = heuristic(current_node.state, goal_state)
        print(distanceToTarget)
        if distanceToTarget < 100:
            print(distanceToTarget)
        if distanceToTarget < 75:
            # Found the goal, reconstruct the path
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent


            # Completed story should be formed. Now we wish to print it.
            path = list(path)
            path.reverse()
            #print_story(path)
            return path

        closed_set.add(current_node.state)

        for neighbor_state in get_neighbors(current_node.state, events, depthLimit):
            if neighbor_state in closed_set:
                continue

            # Calculate the cost to reach the neighbor node
            new_cost = current_node.cost + 5

            # Check if the neighbor is already in the open set
            neighbor_node = next((node for _, node in open_set if node.state == neighbor_state), None)

            if not neighbor_node or new_cost < neighbor_node.cost:
                if neighbor_node:
                    open_set.remove((neighbor_node.total_cost(), neighbor_node))

                neighbor_node = Node(
                    state=neighbor_state,
                    parent=current_node,
                    cost=new_cost,
                    heuristic=heuristic(neighbor_state, goal_state)
                )
                RandomPopHeapQ.heappush(open_set, (neighbor_node.total_cost(), neighbor_node))

    # If no path is found, return an empty list
    return []

def get_neighbors(state, possible_events, depthLimit):
    return getReachableWorldstates(state, possible_events, depthLimit)

def heuristic(state, goal_state):
    return distanceBetweenWorldstates(state, goal_state)

def chained_astar_search(start_state, waypoints, get_neighbors, heuristic, events, depthLimit = 15):
    InitialState = start_state

    waypoint = waypoints[0]
    pathChunk = astar_search(InitialState, waypoint, get_neighbors, heuristic, events, depthLimit)
    FinalPath = pathChunk
    SecondState = pathChunk[len(pathChunk) - 1]
    depthLimit -= len(pathChunk)
    waypoint = waypoints[1]
    pathChunk2 = astar_search(SecondState, waypoint, get_neighbors, heuristic, events, depthLimit)
    skip = True
    for i in pathChunk2:
        if skip:
            skip = False
        else:
            FinalPath.append(i)
    print(len(FinalPath))
    print(len(pathChunk2))
    print(len(pathChunk))
    InitialState = pathChunk[len(pathChunk) - 1]
    depthLimit -= len(pathChunk)





    #import pdb; pdb.set_trace()
    print_story(FinalPath)




NoRestaurantPossibleEvents = [CoffeeSpill(), DoNothing(), ThrowDrink(), Befriend(), HitOnAccepted(), HitOnRejected(), BefriendModerate(), BefriendSlight(), BefriendStrong(), IrritateStrong(), IrritateMild(), IrritateIncreasing(), BreakingPoint(), BreakingPointDuel(), MildIntentionalAnnoyance(), ModerateIntentionalAnnoyance(), SevereIntentionalAnnoyance(), MildIgnorantAnnoyance(), ModerateIgnorantAnnoyance(), SevereIgnorantAnnoyance(), FallInLove(), AskOnDate(), HitBySpaceCar(), GetMiningJob(),
                      GetSpaceShuttleJob(), GoToSpaceJail(), SoloJailbreak(), CoffeeSpill(),
                      HospitalVisit(), Cheat(), Steal(), Irritate(), Befriend(), LoseJob(),
                      AssistedJailBreak(), SabotagedJailBreak(), DoNothing(), GetRejectedFromJob()]

initWorldState, waypoints = SciFiwaypointTestEnvironment()
start_state = initWorldState
goal_state = waypoints[0]
#path = astar_search(start_state, goal_state, get_neighbors, heuristic, NoRestaurantPossibleEvents)
path2 = chained_astar_search(start_state, waypoints, get_neighbors, heuristic, NoRestaurantPossibleEvents)
# TODO: Implement waypoint chaining
print(path2)
