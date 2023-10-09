import sys
import math

# BEGIN DO NOT MODIFY

db = False
swap_count = 0
heapify_call_count = 0


def reset_counts():
    global swap_count
    swap_count = 0
    global heapify_call_count
    heapify_call_count = 0

    
def swap(A, i, j):
    global swap_count
    swap_count += 1
    A[i], A[j] = A[j], A[i]

    
def count_heapify():
    global heapify_call_count
    heapify_call_count += 1

    
def current_counts():
    return {'swap_count': swap_count, 'heapify_call_count': heapify_call_count}


def readNums(filename):
    """Reads a text file containing whitespace separated numbers.
    Returns a list of those numbers."""
    with open(filename) as f:
        lst = [int(x) for line in f for x in line.strip().split() if x]
        if db:
            print("List read from file {}: {}".format(filename, lst))
        return lst

    
# heaps here are complete binary trees allocated in arrays (0 based)
def parent(i):
    return (i - 1) // 2


def left(i):
    return 2 * i + 1


def right(i):
    return left(i) + 1

# END DO NOT MODIFY

def heapify(A, i, n=None):
    """Ensure that the tree rooted at element i in the list A is a min-heap,
    assuming that the trees rooted at elements left(i) and right(i) are already
    min-heaps. Obviously, if left(i) or right(i) are >= len(A), then element i simply does
    not have those out-of-bounds children. In order to implement an in-place heap sort,
    we will sometimes need to consider the tail part of A as out-of-bounds, even though
    elements do exist there. So instead of comparing with len(A), use the parameter n to
    determine if the child "exists" or not. If n is not provided, it defaults to None,
    which we check for and then set n to len(A).

    Since the (up to) two child trees are already min-heaps, we just need to find the right
    place for the element at i. If it is smaller than both its children, then nothing
    more needs to be done, it's already a min heap. Otherwise you should swap the root
    with the smallest child and recursively heapify that tree.

    If you determine that the element at i should swap with one of its children nodes,
    MAKE SURE you do this by calling the swap function defined above.
    """

    count_heapify() # This MUST be the first line of the heapify function, don't change it.
    if n is None:
        n = len(A)
    if not(i < n):
        # if asked to heapify an element not below n (the conceptual size of the heap), just return
        # because no work is required
        return
    # Your code here
    if (left(i) > n-1):
        return
    if (right(i) > n-1):
        truemin = min(A[i], A[left(i)])
    else:
        truemin = min(A[i], A[left(i)], A[right(i)])
    if A[i] != truemin:
        if (A[left(i)] == truemin):
            swap(A, i, left(i))
            return 1
        else:
            swap(A, i, right(i))
            return 2
    


def buildHeap(A):
    """Turn the list A (whose elements could be in any order) into a
    heap. Call heapify on all the internal nodes, starting with
    the last internal node, and working backwards to the root."""
    n = len(A)
    parent_n = parent(n-1)
    for i in range(parent_n, -1, -1):
        old_root = A[i]
        changing_value_identifier = heapify(A, i, n)
        
        root_has_changed = old_root != A[i]
        is_parent_of_parent = i <= parent(parent_n)

        next_index = i
        first_flag = True

        while root_has_changed and is_parent_of_parent:
            if changing_value_identifier:
                if first_flag:
                    next_index = next_index * 2 + changing_value_identifier
                    first_flag = False
                changing_value_identifier = heapify(A, next_index, n)
                if changing_value_identifier:
                    next_index = next_index * 2 + changing_value_identifier 
            else:
                break


def heapExtractMin(A):
    """Extract the min element from the heap A. Make sure that A
    is a valid heap afterwards. Return the extracted element.
    This operation should perform approximately log_2(len(A))
    comparisons and swaps (heapify calls and swap calls).
    Your implementation should not perform O(n) (linear) work."""
    newmin = A[0]

    if len(A) == 1:
        A.remove(A[0])
        return newmin

    swap(A, 0, len(A)-1)
    A.remove(A[len(A)-1])
    
    jump_to_index = 0

    jump_to_is_valid = jump_to_index <= parent(len(A)-1)

    while jump_to_is_valid:
        if right(jump_to_index) >= len(A):
            trumin = min(A[jump_to_index], A[left(jump_to_index)])
        else:
            trumin = min(A[jump_to_index], A[left(jump_to_index)], A[right(jump_to_index)])
        if trumin != A[jump_to_index]:
            if trumin == A[left(jump_to_index)]:
                heapify(A, jump_to_index)
                jump_to_index = left(jump_to_index)
                jump_to_is_valid = jump_to_index <= parent(len(A)-1)
            else:
                heapify(A, jump_to_index)
                jump_to_index = right(jump_to_index)
                jump_to_is_valid = jump_to_index <= parent(len(A)-1)
        else:
            return newmin



def heapInsert(A, v):
    """Insert the element v into the heap A. Make sure that A
    is a valid heap afterwards.
    This operation should perform approximately log_2(len(A))
    comparisons and swaps (swap calls).
    Your implementation should not perform O(n) (linear) work.
    MAKE SURE you swap elements by calling the swap function defined above."""
    if v != None:
        x = int(v)
    else:
        return
    A.append(x)
    current_index = len(A)-1

    while current_index > 0:
        parent_index = parent(current_index)
        if A[current_index] < A[parent_index]:
            swap(A, parent_index, current_index)
            current_index = parent_index
        else:
            break


def printCompleteTree(A):
    """ A handy function provided to you, so you can see a
    complete tree in its proper shape."""
    
    height = int(math.log(len(A), 2))
    width = len(str(max(A)))
    for i in range(height + 1):
        print(width * (2 ** (height - i) - 1) * " ", end="")
        for j in range(2 ** i):
            idx = 2 ** i - 1 + j
            if idx >= len(A):
                print()
                break
            if j == 2 ** i - 1:
                print("{:^{width}}".format(A[idx], width=width))
            else:
                print("{:^{width}}".format(A[idx], width=width),
                      width * (2 ** (height - i + 1) - 1) * " ", sep='', end='')
    print()


def shuffled_list(length, seed):
    A = list(range(10, length + 10))
    import random
    r = random.Random(seed) # pseudo random, so it is repeatable
    r.shuffle(A)
    return A


def report_counts_on_basic_ops(A, loop_extracts=1, loop_inserts=1):
    original_len = len(A)
    print("\nREPORT on list of len: {}".format(original_len))
    reset_counts()
    buildHeap(A)
    print("buildHeap(A):           \t", current_counts())

    reset_counts()
    m = heapExtractMin(A)
    print("heapExtractMin(A) => {}:\t".format(m), current_counts())

    reset_counts()
    heapInsert(A, m)
    print("heapInsert(A, {}):       \t".format(m), current_counts())

    for i in range(loop_extracts):
        reset_counts()
        m = heapExtractMin(A)
        print("heapExtractMin(A) => {}:\t".format(m), current_counts())

    import random
    r = random.Random(0)
    for i in range(loop_inserts):
        reset_counts()
        new_number = r.randrange(0, original_len // 8)
        heapInsert(A, new_number)
        print("heapInsert(A, {}):       \t".format(new_number), current_counts())


def main():
    global db
    if len(sys.argv) > 2:
        db = True
    
    A = [5, 1, 3, 2, 4]
    printCompleteTree(A)
    heapify(A, 0)
    printCompleteTree(A)

    A = shuffled_list(20, 0)
    print("Complete Tree size 20:")
    printCompleteTree(A)
    buildHeap(A)
    print("Heap size 20:")
    printCompleteTree(A)
    heapExtractMin(A)
    printCompleteTree(A)
    B = heapInsert(A, 8)
    printCompleteTree(B)

    A = shuffled_list(30, 0)
    report_counts_on_basic_ops(A)
    
    A = shuffled_list(400, 0)
    report_counts_on_basic_ops(A)
    
    A = shuffled_list(10000, 0)
    report_counts_on_basic_ops(A)

    A = shuffled_list(100000, 0)
    report_counts_on_basic_ops(A, 3, 3)

if __name__ == "__main__":
    main()
