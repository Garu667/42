*This project has been created as part of the 42 curriculum by ramaroud, qgairaud*

# DESCRIPTION

The purpose of this project is to implement a program named `push_swap`, able to analyze a list of disordered integers and return an adequate set of operations to sort it.

This project introduces sorting algorithms, Big-O complexity, and highlights the importance of choosing the most appropriate strategy in order to ensure both efficiency and memory optimization.

The list of integers is initially stored in a first stack `a`. Using a second stack `b`, which starts empty, the program must apply a restricted set of predefined operations to swap, rotate, reverse rotate, or push values from one stack to the other, until stack `a` is fully sorted.

To ensure optimal efficiency, the program analyzes the input list and estimates its disorder rate before selecting the most suitable sorting algorithm.


# ALGORYTHMS LIST

Below is a brief overview of the sorting algorithms considered for building this project.

<details>
<summary> Algorithm Choices </summary>

## Simple algorithm
Allows direct comparisons with progressive extraction → O(n²)

These algorithms rely on explicit comparisons between elements and progressively move values toward their final position. They are easier to understand and implement, but generate a large number of operations on big inputs.

### Insertion sort adaptation

Builds the sorted zone by inserting, one by one, each element at its correct position.

### Selection sort adaptation

At each step, searches for the smallest remaining value in the unsorted stack and places it directly at its final position.

### Bubble sort adaptation

Compares adjacent elements pair by pair and swaps them when they are in the wrong order.  
Several successive passes are required to sort the entire set.

### Simple min/max extraction methods

A variant of selection sort that extracts, at each iteration, the smallest and the largest values.  
Both elements are placed at their final positions, reducing the unsorted zone more quickly.


## Medium algorithm
Reduction of the search space by ranks → O(n√n)

These strategies limit the number of operations by processing values by groups or ranges rather than individually. They require a preliminary partitioning step to reduce unnecessary movements.

### Chunk-based sorting (divide into chunks)

Values are split into several rank ranges of equivalent sizes.  
Each formed chunk is processed independently in order to limit long rotations within the stack.

### Block-based partitioning methods

Stack A is partitioned into successive blocks sent to stack B.  
A small base is sorted, then the blocks are reinserted in a controlled manner.  
The final sort relies on an optimized reassembly of the blocks.

### Bucket sort adaptations with buckets

Values are distributed into several groups representing rank intervals.  
These groups are not fully sorted but organized to facilitate their global repositioning.  
The final sort consists in emptying the buckets in the appropriate order.

### Range-based sorting strategies

A window of acceptable values is defined and progressively moved.  
Only the values belonging to this range are moved at each step.


## Complex algorithm
Global non-comparative or partition-based strategies → O(n log n)

These algorithms significantly reduce the number of operations by exploiting global properties of the data. They require a preparation phase or more advanced partitioning logic.

### Radix sort adaptation (LSD or MSD)

Values are first indexed, then sorted by examining successive bits or digits.  
Each pass redistributes elements according to a given binary position.  
The sorting is performed without direct value comparisons.

### Merge sort adaptation using two stacks

The stack is recursively divided into smaller and smaller subsets.  
Once these subsets are sorted, they are progressively merged back in the correct order.

### Quick sort adaptation with stack partitioning

A pivot is defined to separate values into two distinct groups.  
Elements lower and higher than the pivot are processed separately.  
The process is repeated recursively until a fully sorted set is obtained.

### Heap sort adaptation

The sort relies on a heap structure guaranteeing fast access to the extreme element.  
Each extraction places a value at its final position, then rebuilds the heap.

### Binary indexed tree approaches

A data structure allowing fast cumulative calculations over index sets.  
Used for data analysis, such as inversion counting or disorder computation.
</details>
<br/>

In this version of the project, we chose **X**, **Y**, and **Z**, each providing a different strategy to sort the list.  
By default, the program automatically selects the most appropriate algorithm based on the initial disorder rate.

# INSTRUCTIONS

# RESOURCES

To determine which algorithms best matched our approach to the project, we explored several external resources.  
Below is a list of the most useful references used during the design phase:

- https://www.bigocheatsheet.com/
- https://www.geeksforgeeks.org/
- https://medium.com/
- https://www.w3schools.com/dsa/index.php