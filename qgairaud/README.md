*This project has been created as part of the 42 curriculum by ramaroud, qgairaud*

# DESCRIPTION

The purpose of this project is to implement a program named `push_swap`, capable of analyzing a list of unordered integers and outputting an optimized sequence of operations to sort it.

This project introduces fundamental concepts related to sorting algorithms, Big-O complexity, and highlights the importance of selecting the most appropriate strategy in order to achieve both operational efficiency and memory optimization.

The list of integers is initially stored in a first stack, named stack `a`. Using a second stack `b`, which starts empty, the program must apply a restricted set of predefined operations to swap, rotate, reverse rotate, or push values from one stack to the other, until stack `a` is fully sorted.

To ensure optimal performance, the program analyzes the input list and estimates its disorder rate before selecting the most suitable sorting algorithm.


# ALGORYTHMS

Below is a brief overview of all sorting algorithms studied during the development of this project.

<details>
<summary> Algorithm List </summary>

## Simple algorithm

Direct comparisons with progressive extraction → O(n²)

These algorithms rely on explicit comparisons between elements and progressively move values toward their final positions. They are easier to understand and implement but generate a large number of operations on large input sizes.

### Insertion sort adaptation

Builds a sorted section by inserting each element, one by one, into its correct position.

### Selection sort adaptation

At each step, searches for the smallest remaining value in the unsorted stack and places it directly into its final position.

### Bubble sort adaptation

Compares adjacent elements pairwise and swaps them when they are in the wrong order.
Several successive passes are required to sort the entire set.

### Simple min/max extraction methods

A variant of selection sort that extracts, at each iteration, both the smallest and the largest values.
Placing two elements per iteration reduces the size of the unsorted zone more quickly.


## Medium algorithm

Search space reduction by ranks → O(n√n)

These strategies reduce the number of operations by processing values in groups or ranges rather than individually. They require a preliminary partitioning step to limit unnecessary movements.

### Chunk-based sorting (divide into chunks)

Values are split into several rank ranges of equivalent sizes.
Each chunk is processed independently in order to reduce long rotations within the stack.

### Block-based partitioning methods

Stack `a` is divided into successive blocks that are pushed to stack `b`.
A small base is sorted, after which the blocks are reinserted in a controlled manner.
The final sorting phase relies on an optimized reassembly of these blocks.

### Bucket sort adaptations with buckets

Values are distributed into several groups representing rank intervals.
These groups are not fully sorted but are organized to facilitate global repositioning.
The final step consists of emptying the buckets in the appropriate order.

### Range-based sorting strategies

A sliding window of acceptable values is defined and progressively shifted.
Only the values belonging to this range are moved at each step.


## Complex algorithm

Non-comparative or global partition-based strategies → O(n log n)

These algorithms significantly reduce the number of operations by exploiting global properties of the data. They generally require a preparation phase or more advanced partitioning logic.

### Radix sort adaptation (LSD or MSD)

Values are sorted by examining successive bits or digits.
Each pass redistributes elements according to a specific binary position.
The sorting process is performed without direct value comparisons.

### Merge sort adaptation using two stacks

The stack is recursively divided into smaller subsets.
Once these subsets are sorted, they are progressively merged back in the correct order.

### Quick sort adaptation with stack partitioning

A pivot value is chosen to split elements into two groups.
Values lower and higher than the pivot are processed separately.
This process is repeated recursively until the stack is fully sorted.

### Heap sort adaptation

Relies on a heap structure guaranteeing fast access to extreme values.
Each extraction places a value at its final position before rebuilding the heap.

### Binary indexed tree approaches

Data structures allowing fast cumulative computations over indexed sets.
Used mainly for analysis purposes, such as inversion counting or disorder estimation.
</details>
<br/>

## Selected algorithms

We chose to implement four different sorting algorithms.

All of them operate on a list that has been pre-indexed using a Bubble Sort pass, which simplifies the handling of negative numbers and significantly reduces the number of operations by working on indices instead of raw values.

### Tiny sort

Designed for very small input sizes (≤ 5 elements).

- For two elements, a single swap on `a` is sufficient.

- For three elements, `b` is not required. Only five distributions are possible, all handled directly within `a`.

- For four or five elements, one or two values are pushed to `b`. `a` is sorted independently, and the elements are then reintegrated.

### Selection sort

Elements from `a` are pushed one by one to `b`, from the smallest to the largest.
They are then pushed back to `a` in reverse order to obtain a sorted stack.

### Chunk sort

Works similarly to selection sort but first organizes elements into predefined ranges (chunks).
This pre-ordering reduces the number of operations needed when reinserting values back into `a`.

### Radix sort

Processes element indices based on their binary representation.
For each bit position, all indices whose current bit is 0 are pushed to `b` and then restored to `a`.
This process is repeated for each successive bit until the entire stack is sorted.

# INSTRUCTIONS

(to be completed)

# TASK DISTRIBUTION

This project was developed by a two-person team:

ramaroud was responsible for parsing, benchmarking, and writing the bonus section.

qgairaud implemented the sorting algorithms, the Makefile, and wrote the README.

# RESOURCES

To determine which algorithms best suited our approach, we consulted several external resources.
We also studied bit manipulation techniques and their operators in C.

Below is a list of the most useful references used during the design phase:

- https://www.bigocheatsheet.com/
- https://www.geeksforgeeks.org/
- https://medium.com/
- https://www.w3schools.com/dsa/index.php