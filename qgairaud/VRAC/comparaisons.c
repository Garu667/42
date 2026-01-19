/* Comparaisons d'efficacité entre Selection_sort et Tiny_sort


Liste de 2 éléments

                                Selection       Tiny

2 - 1                 -->     3 operations    1 operation


Listes de 3 éléments

                                Selection       Tiny

1 - 3 - 2             -->     5 operations    2 operations
2 - 3 - 1             -->     5 operations    1 operation
3 - 2 - 1             -->     6 operations    2 operations
2 - 1 - 3             -->     6 operations    1 operation
3 - 1 - 2             -->     5 operations    1 operation


Listes de 4 éléments

                                Selection       Tiny

1 - 4 - 3 - 2         -->     8 operations    4 operations
2 - 4 - 3 - 1         -->     8 operations    5 operations
3 - 4 - 2 - 1         -->     8 operations    4 operations
3 - 2 - 0 - 1         -->     9 operations    6 operations
3 - 1 - 2 - 4         -->     8 operations    5 operations


Listes de 5 éléments

                                Selection       Tiny

3 - 1 - 2 - 4 - 5     -->     10 operations    9 operations
5 - 1 - 4 - 2 - 3     -->     11 operations    10 operations
1 - 2 - 4 - 3 - 5     -->     10 operations    10 operations
2 - 4 - 1 - 5 - 3     -->     13 operations    8 operations
5 - 4 - 3 - 2 - 1     -->     12 operations    8 operations