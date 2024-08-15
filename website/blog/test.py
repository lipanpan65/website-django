# -*- coding: utf-8 -*-
# @Time        : 2024/8/9
# @Author      : 李盼盼
# @Email       : 1299793997@qq.com
# @File        : test.py


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# 示例使用
array = [64, 34, 25, 12, 22, 11, 90]
sorted_array = bubble_sort(array)
print("Sorted array is:", sorted_array)


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


# 示例使用
arr = [3, 6, 8, 10, 1, 2, 1, 4, 7, 9]
sorted_arr = quicksort(arr)
print(sorted_arr)  # 输出: [1, 1, 2, 3, 4, 6, 7, 8, 9, 10]
