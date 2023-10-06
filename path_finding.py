from backbone_classes import *
from events.oldEvents import *
import random

from run import *


def selectEventIndex(eventList, desiredWorldState):
    if len(eventList) == 0: # TODO: Handle this before calling it, rather than after.
        print("No events left in this tree!")
        return 0, float('inf')

    currEventMinDistance = float('inf')
    equallyValubleIndexes = []
    for x in range (len(eventList)):
        reachable_worldstate = eventList[x][0].getNewWorldState(eventList[x][1], eventList[x][2], eventList[x][3])
        currEventValue = distanceBetweenWorldstates(reachable_worldstate, desiredWorldState)

        if (currEventValue < currEventMinDistance):
            equallyValubleIndexes = []
            currEventMinDistance = currEventValue
        if (currEventValue == currEventMinDistance):
            equallyValubleIndexes.append(x)


    if len(equallyValubleIndexes) >= 1:
        return random.choice(equallyValubleIndexes), currEventMinDistance # Return the index of the event with the lowest distance to the desiredWorldState
    else:
        return 0, float('inf')

def getBestIndexLookingAhead(depth, eventList, desiredWorldState, possible_events):
    if depth == 1:
        return selectEventIndex(eventList, desiredWorldState)

    if depth >= 2:
        currEventMinDistance = float('inf')
        equallyValubleIndexes = []

        for x in range (len(eventList)):
            reachable_worldstate = eventList[x][0].getNewWorldState(eventList[x][1], eventList[x][2], eventList[x][3])
            runable_events = getRunableEvents(reachable_worldstate, possible_events)
            currWorldStateValue = getBestIndexLookingAhead(depth-1, runable_events, desiredWorldState, possible_events)

            if (currWorldStateValue[1] < currEventMinDistance):
                equallyValubleIndexes = []
                currEventMinDistance = currWorldStateValue[1]
                equallyValubleIndexes.append(x)

            if (currWorldStateValue[1] == currEventMinDistance):
                equallyValubleIndexes.append(x)

        return random.choice(equallyValubleIndexes), currEventMinDistance


def distanceBetweenWorldstates(currWorldState, newWorldState):
    distance = 0
    #drama_weight = 0
    drama_weight = 1
    causalityWeight = 3
    #causalityWeight = 0

    if currWorldState.characters:
        for character in currWorldState.characters:
            for future_character in newWorldState.characters:
                if future_character.name == character.name:
                    distanceBetweenVersions = character.getDistanceToFutureState(future_character.getAttributes())
                    distance += distanceBetweenVersions

    if len(currWorldState.characters) != len(newWorldState.characters):
        deadCharacterPenalty = abs(len(currWorldState.characters)-len(newWorldState.characters)) * 150 # Change this value to change weight of undesired deaths.
        distance += deadCharacterPenalty

    causalityScore = determineCausalityScore(currWorldState)
    if causalityScore != 0:
        distance -= causalityScore * causalityWeight

    # Drama scores using drama curve methodology
    if newWorldState.getDramaCurve() != None:
        #print("DramaCurveTargetFound")
        plotSteps = len(currWorldState.event_history)
        #print(plotSteps)
        dramaTarget = newWorldState.getDramaCurve().getDramaTargets()[plotSteps]
        drama_distance = abs(currWorldState.drama_score - dramaTarget) * drama_weight
        distance += drama_distance
        #print(drama_distance)
        return distance

    # Drama scoring using arbitrary assigned target for a waypoint
    if newWorldState.drama_score != None:
        #drama_distance = abs(currWorldState.drama_score - newWorldState.drama_score) * 5/2
        drama_distance = abs(currWorldState.drama_score - newWorldState.drama_score) * drama_weight
        distance += drama_distance
        #print(drama_distance)
    return distance

def determineCausalityScore(currWorldState):
    # Look back along the path of worldstate. If along the event history, there are events that are causal
    # (ie happen immediately after they become possible), we reduce the distance heuristic from that worldstate
    # to the target worldstate for the pourposes of pathfinding selection, but not for hitting waypoints.
    # We use each worldstate's stored event history for this, in this manner:
    if len(currWorldState.event_history) == 0:
        return 0

    lastEvent = currWorldState.event_history[-1 * 1:][0]
    eventStr = str(lastEvent[0])
    charsStr = lastEvent[1]
    envStr = lastEvent[2]
    lastEventString = eventStr + charsStr + envStr

    oldPossibleEvents = None
    if currWorldState.prior_worldstate != None:
        prior = currWorldState.prior_worldstate
        if prior.prior_worldstate != None:
            oldPossibleEvents = prior.prior_worldstate.runnable_events

    if oldPossibleEvents:
        if lastEventString in oldPossibleEvents:
            #print("non-casual event.")
            return 0
        else:
            #print("causal event.")
            return 1
    return 0

def getRunableEvents(current_worldstate, possible_events):
    runableEvents = []
    for event in possible_events: # Check to see if an instance of an event is runnable
        preconditions_met, characters, environments = event.checkPreconditions(current_worldstate)
        if preconditions_met: # If so, add all possible instances to the list of runnable events
            for x in range(len(characters)):
                runableEvents.append([event, current_worldstate, characters[x], environments[x]])
    return runableEvents

def getReachableWorldstates(current_worldstate, possible_events):
    NeighborWorldstates = []
    runableEvents = getRunableEvents(current_worldstate, possible_events)
    for x in range (len(runableEvents)):
        reachable_worldstate = runableEvents[x][0].getNewWorldState(runableEvents[x][1], runableEvents[x][2], runableEvents[x][3])
        NeighborWorldstates.append(reachable_worldstate)
    return NeighborWorldstates
