import random
def bubbleSort(arr):
    # 冒泡排序
    for i in range(1, len(arr)):
        for j in range(0, len(arr)-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
def quickSort ( arr, start, end ):
    # 快速排序
    if start >= end:
        return
    tmp = arr[start]
    # l必须等于start，不能等于start+1，否则会报错
    l = start
    r = end
    while l < r:
        while l < r and arr[r] > tmp:
            r -= 1
        while l < r and arr[l] <= tmp:
            l += 1
        arr[l], arr[r] = arr[r], arr[l]
    arr[start], arr[l] = arr[l], arr[start]
    quickSort(arr, start, l - 1)
    quickSort(arr, l + 1, end)

def main():
    arr=[]
    for i in range(100):
        arr.append(random.randint(0,100))
    print("list before sort is:", arr)
    quickSort(arr, 0, len(arr)-1)
    print("list after sort is:", arr)
main()
