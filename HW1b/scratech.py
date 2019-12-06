import numpy as np

#
# a = np.arange(9).reshape(3,3)
# print(a)
#
# print np.sum(a,axis=1)
#
# print np.sum(a,axis=0)
#
# print np.diagonal(a)

a = [[32, 37, 28, 30],
     [37, 25, 27, 24],
     [35, 55, 23, 31],
     [55, 21, 40, 18]]

aRavel = np.array(a).ravel()
print aRavel

mapLoc = [[0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0],
          [0, 0, 0, 0, 1],
          [0, 0, 1, 0, 0],
          [1, 0, 0, 0, 0]]

map =     [[4, 6, 2, 0, 0],
          [3, 5, 0, 1, 0],
          [1, 4, 1, 0, 0],
          [1, 4, 7, 2, 0],
          [2, 7, 5, 4, 1]]

mapLocArray = np.asarray(mapLoc)
mapArray = np.asarray(map)
print mapArray.flatten()[mapLocArray.flatten()==1]

# print sum(sum(map(mapLoc.flatten()==1)))
''' Python3 code for k largest elements in an array'''
#
# # Function to take the sum of k largest elements in 2D array
# def kLargest(array2D, k):
#      # Flatten the array
#
#      # Sort the given array arr in reverse order.
#      arr.sort(reverse=True)
#      # Print the first kth largest elements
#      for i in range(k):
#           print (arr[i], end=" ")
#
#      # Driver program
def sumkLargest(arr, k):
    # Sort the given array arr in reverse order.
    # arr.sort(reverse=True)
    arr1 = sorted(arr,reverse=True)
    sumK = 0
    # Print the first kth largest elements
    for i in range(k):
      sumK = sumK + arr1[i]
    return sumK
#
arr = [1, 23, 12, 9, 30, 2, 50]
# # n = len(arr)
k = 3
print sumkLargest(arr, k)

# This code is contributed by shreyanshi_arun.

# b = [2,4,5,3,1,7,6]
# c = [20,40,50,30,10,70,60]
#
# print np.partition(b, 3)[3]
#
# aa = np.asarray(a)
# #
# print(aa.flatten())
# print np.argsort(aa.flatten())

# print(aa.ravel())
# print np.argsort(aa.flatten())


# aa1 = np.argsort(aa.ravel()).reshape((4, 4))
# print aa1
# i=1
# j=1
# diagonal = np.diag(a, j-i)
# antidiagonal = np.diag(np.fliplr(a), 4-j-1-i)
# print np.sum(diagonal)
# print np.sum(antidiagonal)
#
# m = max(max(a))
# print m
#
# b = np.asarray(a)
#
# maxindex = b.argmax()
# print maxindex
#
# print zip(*np.where(b == m))
#
#
# print range(4)