import sys
from math import *
from subprocess import call
import numpy as np
from numpy import *
import copy

def assignPoints(tbl, ctrs):
    """Assign each of the points in tbl to the cluster with
        center in ctrs"""

    points = []

    for point in tbl:
        probs = []
        for ctr in ctrs:
            sigma = 10
            prob = np.exp(-(np.linalg.norm(point - ctr) / sigma) ** 2)
            probs.append(prob)
        probs = np.array(probs) / sum(probs)

        points.append((point, probs))

    return points


def recalculateCtrs(ctrs, points):
    """Update the centroids based on the points assigned to them"""

    newCtrs = [0] * len(ctrs)

    for ix in range(len(ctrs)):
        weighted_sum = np.zeros(2)
        total_weight = 0
        for point, weight in points:
            weighted_sum += point * weight[ix]
            total_weight += weight[ix]
        newCtrs[ix] = weighted_sum / total_weight

    return newCtrs


def euclideanDist(x, y):
    if len(x) != len(y):
        print("x and y must be the same length")
        sys.exit(1)
    else:
        dist_val = 0
        for i in range(len(x)):
            dist_val = dist_val + math.pow((x[i] - y[i]), 2)

    return math.sqrt(dist_val)

def plotClusters(clusters, cntrs, stepCnt, anLabel):
    """generate a scatterplot of the current
       k-means cluster assignments

       filename may end in the following file extensions:
         *.ps, *.png, *.jpg
    """

    p = open("./" + anLabel + "_output/dummy_table.txt", "w")

    for ix, cluster in enumerate(clusters):
        for point in cluster:
            p.write((("{}\t" * len(point))+ "{}\n").format(*point, ix))

    for i in range(len(cntrs)):
        for j in range(len(cntrs[i])):
            p.write("{}".format(cntrs[i][j]))
            p.write("\t")
        p.write("Cluster {}".format(i))
        p.write("\n")

    p.close()

    plotCMD = "R CMD BATCH '--args ./" + anLabel + "_output/dummy_table.txt ./" + anLabel + "_plots/cluster_step%d.png" % stepCnt + "' ./kmeans_plot.R;"
    call(plotCMD, shell=True)



###############################################################################
# MAIN
###############################################################################

def main():
    # Checks if we have the right number of command line arguments
    #   and reads them in
    if len(sys.argv) < 2:
        print("you must call program as: python fuzzykmeans.py <datafile>")
        sys.exit(1)
    analysis_name = sys.argv[1]

    # Creates directories for storing plots and intermediate files
    call(["rm", "-r", "./" + analysis_name + "_plots/"])
    call(["mkdir", "-p", "./" + analysis_name + "_plots/"])
    call(["mkdir", "-p", "./" + analysis_name + "_output/"])

    # Reads in the point data from the given tissue file
    dataTable = []
    f = open("./" + analysis_name + "_data.txt")
    for dataLine in f:
        dataTable.append(np.array([float(str) for str in dataLine.rstrip().split("\t")]))
    f.close()

    K = 3

    # Initializes centroids, stop criterion and step counting for clustering
    dataMinX, dataMinY = np.min(np.array(dataTable), axis=0)
    dataMaxX, dataMaxY = np.max(np.array(dataTable), axis=0)
    newCtrs = [[np.random.randint(dataMinX, dataMaxX),
                np.random.randint(dataMinY, dataMaxY)]
                for _ in range(K)]

    points = assignPoints(dataTable, newCtrs)
    stopCrit = False
    stepCount = 1

    # Performs k-means clustering, plotting the
    #   clusters at each step
    while stopCrit == False:
        # plotClusters(clusters, newCtrs, stepCount, analysis_name)
        oldCtrs = copy.deepcopy(newCtrs)
        newCtrs = recalculateCtrs(newCtrs, points)
        points = assignPoints(dataTable, newCtrs)

        # Stop criterion - when centroids' total movement
        #   after a step is below the threshold,
        #   stop the algorithm

        stopDist = 0
        for i in range(len(newCtrs)):
            stopDist = stopDist + euclideanDist(oldCtrs[i], newCtrs[i])
        if stopDist < 5:
            stopCrit = True

        stepCount += 1
    
    print(newCtrs)

if __name__ == "__main__":
    main()


