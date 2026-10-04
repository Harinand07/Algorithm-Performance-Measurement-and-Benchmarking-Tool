def linear_search(arr, target):
    """Returns (index, comparison_count). Works on unsorted data."""
    comparisons = 0
    for i, value in enumerate(arr):
        comparisons += 1
        if value == target:
            return i, comparisons
    return -1, comparisons

def binary_search(arr, target):
    """Returns (index, comparison_count). Input must be sorted."""
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons

if __name__ == "__main__":
    data=[5,3,8,4,9,1,7]
    print("Linear Search:",linear_search(data,9))
    print("Binary Search:",binary_search(sorted(data),9))
