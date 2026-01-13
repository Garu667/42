*This project has been created as part of the 42 curriculum by ramaroud, qgairaud*

# DESCRIPTION

<details>
<summary> /// VERSION EN FRANCAIS (à supprimer) ///</summary>

# Choix d'Algorythms

## Simple algorythm
Permet des comparaisons directes, avec extraction progressive → O(n²)

Ces algorithmes reposent sur des comparaisons explicites entre éléments et déplacent progressivement les valeurs vers leur position finale. Ils sont plus simples à comprendre et à implémenter, mais génèrent beaucoup d’opérations sur de grandes entrées.

### Insertion sort adaptation

Construit la zone triée en insérant, un par un, chaque élément à la bonne position.

### Selection sort adaptation

Recherche à chaque étape la plus petite valeur restante dans la pile non triée, et la place directement à sa position finale.

### Bubble sort adaptation

Compare les éléments adjacents deux par deux et les échange lorsqu’ils sont dans le mauvais ordre.
Plusieurs passages successifs sont nécessaires pour trier l'ensemble.

### Simple min/max extraction methods

Variante du tri par sélection qui extrait à chaque itération la plus petite et la plus grande valeur.
Les deux éléments sont placés à leurs positions finales, réduisant plus rapidement la zone non triée.


## Medium algorythm
Réduction de l’espace de recherche par rangs → O(n√n)

Ces stratégies limitent le nombre d’opérations en traitant les valeurs par groupes/plages et non individuellement. Elles demandent un découpage préalable pour réduire des déplacements inutiles.

### Chunk/based sorting (divide into chunks)

Les valeurs sont découpées en plusieurs plages de rangs de tailles équivalentes.
Chaque chunk formé est traité indépendamment, pour limiter les rotations longues dans la pile.

### Block/based partitioning methods

La pile A est partitionnée en blocs successifs envoyés dans la pile B.
Une petite base est triée, puis les blocs sont réinsérés de manière contrôlée.
Le tri final repose sur le réassemblage optimisé des blocs.

### Bucket sort adaptations with buckets

Les valeurs sont réparties dans plusieurs groupes représentant des intervalles de rangs.
Ces groupes ne sont pas totalement triés mais organisés pour faciliter leur repositionnement global.
Le tri final consiste à vider les buckets dans l’ordre approprié.

### Range-based sorting strategies

Une fenêtre de valeurs acceptables est définie et déplacée progressivement.
Seules les valeurs appartenant à cette plage sont déplacées à chaque étape.

## Complex Algorythm
Stratégies globales non comparatives ou par partition → O(n log n)
Ces algorithmes réduisent fortement le nombre d’opérations en exploitant des propriétés globales des données. Ils nécessitentune phase de préparation ou une logique de partition plus avancée.

### Radix sort adaptation (LSD or MSD)

Les valeurs sont d’abord indexées, puis triées en examinant leurs bits ou digits successifs.
Chaque passe redistribue les éléments selon une position binaire donnée.
Le tri s’effectue sans comparaison directe entre valeurs.

### Merge sort adaptation using two stacks

La pile est divisée récursivement en sous-ensembles de plus en plus petits.
Une fois ces sous-ensembles triés, ils sont refusionnés progressivement dans le bon ordre.

### Quick sort adaptation with stack partitioning

Un pivot est défini pour séparer les valeurs en deux groupes distincts.
Les éléments inférieurs et supérieurs au pivot sont traités séparément.
Le processus est répété récursivement jusqu’à obtenir un ensemble entièrement trié.

### Heap sort adaptation

Le tri repose sur une structure de tas garantissant l’accès rapide à l’élément extrême.
Chaque extraction place une valeur à sa position finale, puis reconstruit le tas.

### Binary indexed tree approaches

Structure de données permettant des calculs cumulés rapides sur des ensembles d’indices.
Utilisée pour analyser les données, comme le calcul d’inversions ou de disorder.
</details>

<details>
<summary>/// VERSION EN ANGLAIS (à organiser) ///</summary>

# Algorithm Choices


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
</summary>

# INSTRUCTIONS

# RESOURCES

- https://www.geeksforgeeks.org/
- https://medium.com/
- https://www.w3schools.com/dsa/index.php