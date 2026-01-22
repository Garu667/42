*This project has been created as part of the 42 curriculum by ramaroud, qgairaud.*


# DESCRIPTION

The purpose of this project is to implement a program named `push_swap`, capable of analyzing a list of unordered integers and outputting an optimized sequence of operations to sort it.

This project introduces fundamental concepts related to sorting algorithms, `Big-O` complexity, and highlights the importance of selecting the most appropriate strategy in order to achieve both operational efficiency and memory optimization.

The list of integers is initially stored in a first stack, named stack `a`. Using a second stack `b`, which starts empty, the program must apply a restricted set of predefined operations to **swap**, **rotate**, **reverse rotate**, or **push** values from one stack to the other, until stack `a` is fully sorted.

The program does not output the sorted list itself, but only the sequence of operations used to sort it.

To ensure optimal performance, the program first validates the input, then analyzes the level of disorder of the list in order to select the most suitable sorting algorithm.


# ALGORITHMS

Below is a brief overview of the sorting algorithms studied during the development of this project.

<details>
<summary> Studied sorting strategies </summary>

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

## Selected algorithms

We chose to implement **four different sorting algorithms**.

All of them operate on a list that is first **pre-indexed** using a _Bubble Sort_ pass, which simplifies the handling of negative numbers and significantly reduces the number of operations by working on indices instead of raw values.

<details>
<summary> Algorithm List </summary>


### Tiny sort

Designed for very small input sizes (**≤ 5 elements**).

- For two elements, a single swap on stack `a` is sufficient.

- For three elements, stack `b` is not required. Only five unsorted configurations are possible, all handled directly within stack `a`.

- For four to five elements, one or two values are first pushed to stack `b`. Stack `a` is sorted independently, then the extracted elements are reintegrated.

### Selection sort

Elements from stack `a` are pushed one by one to stack `b`, from the smallest value to the largest.
They are then pushed back to stack `a` in reverse order to obtain a sorted stack.

### Chunk sort

Works similarly to selection sort but organizes elements into predefined index ranges (**chunks**) before pushing them.
This pre-ordering reduces the number of operations needed when reinserting elements back into stack `a`.

### Radix sort

Processes element index based on their binary representation.
For each bit position, all indices whose current bit is 0 are pushed to stack `b` and then restored to stack `a`.
This process is repeated for each successive bit until the entire stack is sorted.
</details>

# INSTRUCTIONS

A Makefile is provided.

<details>
<summary> Mandatory part </summary>

#### Compilation

Compile the program using:

    make

This will generate the `push_swap` executable.

#### Usage

Run the program as follows:

    ./push_swap [flags] [arguments]

Only valid integers separated by spaces are accepted.
Floating-point numbers or invalid characters will result in an error.

#### Flag parsing policy

For clarity and robustness, flags are only parsed if they appear **before any numeric argument**.
Any flag appearing after the first integer will be considered invalid and will trigger an error.
This design choice was made intentionally to secure argument parsing and avoid ambiguous command-line interpretations.

#### Flags

Four algorithms are available:

    --simple
    --medium
    --complex

They explicitly select, respectively:
- `selection_sort`
- `chunk_sort`
- `radix_sort`

If no algorithm flag is specified, or if `--adaptive` is used, the program automatically selects the most appropriate algorithm based on the computed disorder rate of the input.

Small lightly disordered lists will use the `tiny_sort` algorithm.

#### Benchmark mode

A benchmark system is included to analyze:
- disorder rate
- chosen algorythm
- operation distribution

To display benchmark information, add the `--bench` flag **before the numeric arguments**.
</details>

<details>
<summary> Bonus part</summary>
<br/>
The bonus part adds an additional program named checker, designed to verify whether a sequence of operations correctly sorts a given list.

#### Compilation

Compile the program using:

    make bonus

This will generate the `checker` executable.

#### Usage

Run the program as follows:

    ./checker [arguments]

The program will then wait for instructions on **standard input**.
Each instruction must be entered on a new line.

These instructions correspond to the predefined operations allowed in the `push_swap` project.

#### Available operations

- `sa` ~ swap the first two elements of stack `a`
- `sb` ~ swap the first two elements of stack `b`
- `ss` ~ swap both stacks simultaneously
- `ra` ~ rotate stack `a`
- `rb` ~ rotate stack `b`
- `rr` ~ rotate both stacks simultaneously
- `rra` ~ reverse rotate stack `a`
- `rrb` ~ reverse rotate stack `b`
- `rrr` ~ reverse rotate both stacks simultaneously

#### Validation

Once all instructions have been entered, end the input with **Ctrl + D** (EOF).

- If stack `a` is sorted and stack `b` is empty, the program prints:

    `OK`

- In any other case, it prints:

    `KO`

#### Error handling

The program will display `Error` if:

- one or more arguments are not valid integers
- values exceed the integer range
- duplicate values are detected
- an instruction does not exist or is incorrectly formatted
</details>

<details>
<summary> Confrontation </summary>
<br/>
To verify the efficiency and correctness of the `push_swap` program, both executables can be used together.

    make
    make bonus

Then run:

    ./push_swap [flags] [arguments] | ./checker [arguments]

The output of `push_swap` is piped directly into `checker`, allowing automatic verification of the generated instruction sequence.

</details>

# TASK DISTRIBUTION

This project was developed by a two-person team:

- **ramaroud** handled parsing, benchmarking, and the bonus checker implementation _(based on a previous GNL project)_.

- **qgairaud** implemented sorting algorithms, Makefile, and wrote the README.


# RESOURCES

To determine which algorithms best suited our approach, we consulted several external resources and studied bit manipulation techniques in C.

Some of the most useful references include:

- https://www.bigocheatsheet.com/
- https://www.geeksforgeeks.org/
- https://medium.com/
- https://www.w3schools.com/dsa/index.php

_Finally, IA (ChatGPT) was used as a language support tool to improve clarity and refine this documentation._