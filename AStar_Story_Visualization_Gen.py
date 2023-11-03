from backbone_classes import *
from events.oldEvents import *
from events.restaurantEvents import *
from events.events import *
from events.health_events import *
from events.law_events import *
from events.love_events import *
from events.generatedEvents import *

from path_finding import *
from AStar_Path_Finding import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import csv

def extract_drama_vals(path):
    # From a completed story path, pull out all the drama values in a list format.
    dramaVals = []
    for worldstate in path:
        dramaVals.append(worldstate.drama_score)
    return dramaVals

if __name__ == "__main__":

    NoRestaurantPossibleEvents = [CoffeeSpill(), DoNothing(), ThrowDrink(), Befriend(), HitOnAccepted(),
                                  HitOnRejected(), BefriendModerate(), BefriendSlight(), BefriendStrong(),
                                  IrritateStrong(), IrritateMild(), IrritateIncreasing(), BreakingPoint(),
                                  BreakingPointDuel(), MildIntentionalAnnoyance(), ModerateIntentionalAnnoyance(),
                                  SevereIntentionalAnnoyance(), MildIgnorantAnnoyance(), ModerateIgnorantAnnoyance(),
                                  SevereIgnorantAnnoyance(), FallInLove(), AskOnDate(), HitBySpaceCar(), GetMiningJob(),
                                  GetSpaceShuttleJob(), GoToSpaceJail(), SoloJailbreak(), CoffeeSpill(),
                                  HospitalVisit(), Cheat(), Steal(), Irritate(), Befriend(), LoseJob(),
                                  AssistedJailBreak(), SabotagedJailBreak(), DoNothing(), GetRejectedFromJob()]


    numStories = 10
    dramaValList = []
    for z in range(numStories):
        f = open("testStory.txt", "w")
        initWorldState, waypoints = SciFiwaypointTestEnvironment()
        start_state = initWorldState
        storyPath, VisitedStates = chained_astar_search(start_state, waypoints, get_neighbors, heuristic,
                                                        NoRestaurantPossibleEvents)
        dramaVals = extract_drama_vals(storyPath)
        f.close()

        # Ensure the list has 15 values by appending zeros
        if len(dramaVals) < 15:
            dramaVals.extend([0] * (15 - len(dramaVals)))

            # Specify the existing CSV file name
            csv_filename = "dramaValues.csv"
            # Append the list to the existing CSV file
            with open(csv_filename, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(dramaVals)


    currDramaMean = [0] * lenOfGraph
    currDramaMin = [9999] * lenOfGraph
    currDramaMax = [0] * lenOfGraph
    for x in range(numStories):
        for y in range(lenOfGraph):
            try:
                currDramaVal = dramaValList[x][0][y]
            except:
                currDramaVal = 0
            currDramaMean[y] += currDramaVal
            if currDramaMax[y] < currDramaVal:
                currDramaMax[y] = currDramaVal
            if currDramaMin[y] > currDramaVal:
                currDramaMin[y] = currDramaVal

    for index in range(lenOfGraph):
        currDramaMean[index] = currDramaMean[index] / numStories # adjust mean appropriately

    # Now generating data for box and whisker plot
    currDramaData = [[0 for i in range(numStories)] for j in range(lenOfGraph)]
    for x in range(numStories):
        for y in range(lenOfGraph):
            try:
                currDramaVal = dramaValList[x][0][y]
            except:
                currDramaVal = 0
            currDramaData[y][x] = currDramaVal

    fig = plt.figure(figsize=(12, 10))

    # Creating axes instance
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    # Creating plot
    bp = ax.boxplot(currDramaData, notch=False, vert=True, patch_artist=True)

    ax.yaxis.grid(True)

    colors = ['red']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    xVals = np.arange(start=1, stop=lenOfGraph+1)
    plt.plot(xVals, dramaVals[1], color="red", label='Target Drama Curve') #Target

    ax.set_xlabel('Plot Fragment Index')
    ax.set_ylabel('Drama Level')

    legend_elements = [Line2D([0], [0], color='red', lw=4, label='Target Drama Values'),
                       Patch(facecolor=sns.desaturate('blue', .5), edgecolor='grey', linewidth=1.5,
                             label='Produced Drama Values')]
    ax.legend(handles=legend_elements, fontsize='xx-large')

    # show plot
    plt.show()


    xVals = np.arange(start=0, stop=lenOfGraph)
    plt.title("Drama Vals")
    plt.plot(xVals, currDramaMean, color="red") #current
    plt.plot(xVals, currDramaMax, color="blue") #upper bound
    plt.plot(xVals, currDramaMin, color="blue") #Lower bound
    plt.plot(xVals, dramaVals[1], color="green") #Target