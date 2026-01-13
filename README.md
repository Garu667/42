*This project has been created as part of the 42 curriculum by ramaroud, qgairaud*

# Choix d'Algorythms


## Simple algorythm


### Insertion sort adaptation

Ajouter une à une les entrées en les plaçant selon leur valeur, < X <.

### Selection sort adaptation

Cherche l'élément le plus petit et le place à la place du premier, puis cherche le deuxième plus petit dans le reste et le place à la deuxième place, etc...

### Bubble sort adaptation

Swappe les éléments en les comparant deux par deux pour mettre le plus petit avant le plus grand. Parcoure autant de fois la liste que nécessaire.

### Simple min/max extraction method

(doute)Définir les valeurs minimale et maximale dans la liste, les placer. Recommencer avec la liste réduite de deux, etc...


## Medium algorythm

### Chunk/based sorting

Divise en plusieurs fragments la liste, les trie chacun pour réduire le nombre de manoeuvres au total.

### Block/based sorting

Envoie des blocs de liste dans B, jusqu'à garder trois éléments dans A, les trier, puis ramener proprement ceux de B dans A.

### Bucket sort adaptations

Trie l'ensemble des valeurs pour les ranger dans X containers, puis fait appel au <simple algorythme insertion sort> pour les ordonner au sein de chaque container, puis renvoie le résultat en succédant les containers du plus faible au plus grand.

### Range-based sorting strategies

Crée une plage de tri en se basant sur la valeur la plus basse et sur la valeur la plus haute de la liste. Peu d'intérêt si utilisé sur une liste contenant uniquement des valeurs distinctes.


## Complex Algorythm

### Radix sort adaptation

Trie les valeurs en les rangeant par valeur d'unité, puis par valeur de dizaine, etc... Ne fonctionne que sur des entiers non negatifs !

### Merge sort adaptation

Divise la liste en deux sous-listes de tailles le plus égales possibles, et répète l'opération jusqu'à obtenir autant de sous-listes que de valeurs initiales. Puis regroupe les sous-listes par autant d'étapes progressives en triant des bouts de liste de plus en plus grands.

### Quick sort adaptation

Définis un pivot "central" en triant tout ce qui est en dessous d'un côté, ce qui est au-dessus de l'autre côté. Répète l'opération dans chaque sous-division jusqu'à avoir tout trié'

### Heap sort

### Binary sort
