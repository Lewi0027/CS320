import math
import numpy as np
import argparse

# begin PROVIDED section - do NOT modify ##################################

count = 0

def getArgs() :
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type = str, help = 'File containing terrain')
    
    parser.add_argument('h', type = float, help = 'h value')
    
    parser.add_argument('theta', type = float, help = 'Angle of elevation for Sun')
    parser.add_argument('algorithm', type = str, help = 'naive | early | fast')
    return parser.parse_args()

def compare(x,y):
    global count
    count += 1
    if abs(x-y) < .000000000001 :
        return False
    if x < y :
        return True
    else:
        return False

def print_shade(boolean_array):
    for row in boolean_array:
        for column in row:
            if column == True:
                print ('*    ', end = '')
            elif column == False:
                print ('0    ', end = '')
        print('\n')
        
def read2Dfloat(fileName) : # read CSV of floats into 2D array
    array2D = []
    # Read input file
    f = open(fileName, "r")
    data = f.read().split('\n')
    
    # Get 2-D array
    for row in data:
        float_list = list(map(float, row.split(',')[0:-1]))
        array2D.append(float_list)

    return array2D

def runTest(args, terrain = None) :

    
    # Initialize counter
    global count
    count = 0

    theta = np.deg2rad(args.theta)
    
    if terrain == None :
      terrain = read2Dfloat(args.input_file)

    N     = len(terrain)
    shade = [[False] * N for i in range(N)]

    if args.algorithm == 'naive':
        result = naive(terrain, args.h, theta, N, shade)
    elif args.algorithm == 'early':
        result = earlyexit(terrain, args.h, theta, N, shade)
    elif args.algorithm == 'fast':
        result = fast(terrain, args.h, theta, N, shade)

    #following section just for personal use. Make sure all codes creating same results.
    elif args.algorithm == 'all':
        naive_result = naive(terrain, args.h, theta, N, shade)
        print("Naive result:")
        print("Number of comparisons for Naive: " + str(count))
        print_shade(naive_result)        
        count_after_naive = count

        earlyexit_result = earlyexit(terrain, args.h, theta, N, shade)
        print("\nEarly Exit result:")
        count_early_actual = count - count_after_naive
        print("Number of comparisons for Early Exit: " + str(count_early_actual))
        print_shade(earlyexit_result)
        count_after_early = count
        
        fast_result = fast(terrain, args.h, theta, N, shade)
        print("\nFast result:")
        count_fast_actual = count - count_after_early
        print("Number of comparisons for Fast: " + str(count_fast_actual))
        return fast_result
    return result

# end PROVIDED section ##################################

# Fritz Sieker 

# Henry Lewis CODE PA1

# Go to every single element other than the first in each row, check every single element to the left of them and see if the shadow they produce shades that spot.
# Big O for this is always going to be n(n-1)(n/2) or n^3. (n-1) since we have the line if j!= 0. (n/2) since x iterates through j as j grows from 1 -> N.
def naive(image,h,angle,N,shade):
    tanx = math.tan(angle)
    for i in range(N):
        for j in range(N):
            if j!= 0:
                for x in range(j):
                    if compare(image[i][j]+(h*j*tanx), image[i][x]+(h*x*tanx)) == 1:
                        shade[i][j] = True
    return shade

# This is the same as above but each element checks to see if it is shaded in a right to left manner, checking the closest value first. If any value marks it in shade it will break.
# Big O for this is worst case n(n-1)(n/2) or n^3 if nothing is shaded and best case it could theoretically be (n-1)*n or n^2 if every value other than the left-most value is shaded by the value to its direct left.
def earlyexit(image,h,angle, N, shade):
    tanx = math.tan(angle)
    for i in range(N):
        for j in range(N):
            if j!= 0:
                for x in range(j-1,-1,-1):
                    if compare(image[i][j]+(h*j*tanx), image[i][x]+(h*x*tanx)) == 1:
                        shade[i][j] = True
                        break
    return shade

# This algorithm changes things a bit. We are going to store the height of the first value, then each time we iterate we are going to calculate the height of the shadow and compare those values.
# If the shadow height is greater we are going to mark the area as shaded and retain that max shadow height. If not we do not mark as shaded and we store the new height as the max shadow height.
# Big O for this is always going to be (n-1)n or n^2.
def fast(image,h,angle, N, shade):
    tanx = math.tan(angle)
    for i in range(N):
        maxshade = image[i][0]
        for j in range(N):
            if j!= 0:
                h_length = maxshade/tanx
                h_height = (h_length - h)/h_length
                maxshade = maxshade * h_height
                if compare(image[i][j], maxshade) == 1:
                    shade[i][j]= True
                else:
                    maxshade = image[i][j]
    return shade
    
if __name__ == '__main__':
    

    answer = runTest(getArgs())
    print_shade(answer)
    print('Number of comparisons: ' + str(count))