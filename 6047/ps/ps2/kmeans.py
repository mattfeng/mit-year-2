import sys
from math import *
from subprocess import call
import numpy as np
from numpy import *
import copy

def assignPoints(tbl, ctrs):
    """Assign each of the points in tbl to the cluster with
        center in ctrs"""

    ptsAsgn = [[] for _ in range(len(ctrs))]

    for point in tbl:
        dists = np.array([euclideanDist(ctr, point) for ctr in ctrs])
        cluster = np.argmin(dists)
        ptsAsgn[cluster].append(point)

    return ptsAsgn


def recalculateCtrs(ctrs, ptsAsgn):
    """Update the centroids based on the points assigned to them"""

    newCtrs = [0] * len(ctrs)

    for ix, cluster in enumerate(ptsAsgn):
        centroid = np.mean(cluster, axis=0)
        newCtrs[ix] = centroid

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

    """Checks if we have the right number of command line arguments
       and reads them in"""
    if len(sys.argv) < 1:
        print("you must call program as: python ./kmeans.py <datafile>")
        sys.exit(1)
    analysis_name = sys.argv[1]

    """creates directories for storing plots and intermediate files"""
    call(["rm", "-r", "./" + analysis_name + "_plots/"])
    call(["mkdir", "-p", "./" + analysis_name + "_plots/"])
    call(["mkdir", "-p", "./" + analysis_name + "_output/"])

    """Reads in the point data from the given tissue file"""
    dataTable = []
    f = open("./" + analysis_name + "_data.txt")
    for dataLine in f:
        dataTable.append(np.array([float(str) for str in dataLine.rstrip().split("\t")]))
    f.close()

    """initializes centroids, stop criterion and step counting for clustering"""
    newCtrs = [[5,0], [5,40], [5,80]]
    clusters = assignPoints(dataTable, newCtrs)
    stopCrit = False
    stepCount = 1

    # Performs k-means clustering, plotting the
    #   clusters at each step
    while stopCrit == False:
        plotClusters(clusters, newCtrs, stepCount, analysis_name)

        oldCtrs = copy.deepcopy(newCtrs)
        newCtrs = recalculateCtrs(newCtrs, clusters)
        clusters = assignPoints(dataTable, newCtrs)

        # Stop criterion - when centroids' total movement
        #   after a step is below the threshold,
        #   stop the algorithm

        stopDist = 0
        for i in range(len(newCtrs)):
            stopDist = stopDist + euclideanDist(oldCtrs[i], newCtrs[i])
        if stopDist < 5:
            stopCrit = True

        stepCount += 1

if __name__ == "__main__":
    main()


