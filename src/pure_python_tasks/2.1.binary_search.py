def binary_search(sorted_list, n):
    left, right = 0, len(sorted_list) - 1

    while left <= right:
        mid = (left + right) // 2
        if sorted_list[mid] == n:
            return True
        elif sorted_list[mid] < n:
            left = mid + 1
        else:
            right = mid - 1

    return False


sorted_list = [1, 2, 3, 45, 356, 569, 600, 705, 923]
print(binary_search(sorted_list, 356))
print(binary_search(sorted_list, 32))
