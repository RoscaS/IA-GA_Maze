# TP Intelligence artificielle: Labyrinthe

* 30 novembre 2019
* Sol Rosca
* INF3b


## Introduction
Ce TP nécéssite de résoudre un labyrinthe de taille variable à l'aide d'un algorithme génétique. Ce type d'algorithme fait partie de la catégorie des algorithmes d'optimisation et en tant que tel, il est capable de trouver une solution et ensuite de l'optimiser pour au final retourner une solution satisfaisante.

Je ne pense pas que ce travail a pour vocation de trouver une solution sans faille pour résoudre ce problème en particulier, il existe des methodes bien plus efficaces pour trouver le chemin le plus court entre deux points sur une grille.

Concrètement ce programme n'est pas parfait mais il a été le terrain d'expérimentations et a réussit sa mission  de renforcement des bases des algorithmes génétiques ainsi que du package DEAP.

## Encodage d'un chromosome
La solution (chromosome) est une succession de mouvement dans une des quatre directions cardinales (N, S W, E).
Ainsi, dans ce programme, un chromosome est représenté par une liste d'entiers d'une taille variable en fonction de la taille du labyrinthe. Chaque entier fait référence à une des précédentes direction.

## Initialisation de la population
L'initialisation se fait de façon complètement aléatoire et il n'existe aucune condition autre que le fait d'avoir une séquence de n entiers de 0 à 3. La population initiale (qui est fixe en taille) est composée de 1000 individus. La combinaison de ces deux points permet d'avoir une certaine diversité initiale.

## Fitness
La fonction de fitness est la somme entre:
* La distance de manhattan entre le dernier gène et la fin du labyrinthe.
* Une série de pénalités appliquées pour minimiser:
  * Les sorties de la grille
  * Le fait de repasser sur une case déja explorée
  * Traverser des obstacles

Nous somme donc dans un problème de minimisation et le score de fitness doit être le plus bas possible, idéalement à 0. Un premier problème pour atteindre ce but est le fait qu'il est interdit (par consignes) d'utiliser des algorithmes de recherche pour avoir des informations sur l'environement. En effet une analyse préliminaire via A* pourrait nous donner la taille précise que doit faire le chromosome pour la solution idéale. Sans cette information l'utilisation de pénalités n'est pas optimale (mais apporte quand même de meilleurs résultats que sans).

## Selection
La diversité de la population permet de mesurer le "niveau de convergence". Si cette dernière est faible, la probabilité de converger vers un minima local sera plus grande et ce n'est pas un effet souhaitable. Le meilleur résultats sont obtenu avec les methodes suivantes:

* Tournoi qui oppose 3 chromosomes (methode retenue)
* Roulette

Le full random ne tire pas tant proffit des subtilités intrinsèques des AG et une selection élitiste détruit la diversité rapidement.

## Crossover
Sert principalement à induire de la diversité. Intuitivement cela semble contre productif dans le présent problème comme le moindre changement dans un des gènes peut totalement détruire la qualité d'un chemin. Mais comme nous sommes face à de nombreux minima locaux le fait de garder un pool de gène varié qui peut mener à la bonne solution est déterminant.

De meilleurs résultats sont obtenu avec une valeur élevée pour la probabilité de croisement. Cette valeur est donc à 0.8.

## Mutation
Tout comme le crosover, permet d'induire de la diversité. Les valeurs sont de 0.2 pour la probabilité de muter et ensuite de 0.02 pour chaque gène qui sera changé pour une valeur aléatoire entre 0 et 3 en cas de mutation.

## Execution
Une première observation est qu'une solution stable est trouvée largement avant la fin du temps imposé. Autrement dit le programme tend à s'enfoncer dans un minima (qui peut être la solution optimale ou pas) au bout d'un certain nombre de générations (variable en fonction de la taille de la grille). Pour tenter de trouver une meilleur solution une stratégie qui consiste à répéter un certain nombre de "runs" a été mise en place. À la fin d'un nombre (variable en fonction de la taille de la grille) de générations, la meilleur solution est retournée (fitness le plus bas dans la série de runs). Cette dernière n'est pas forcément optimale où même correcte mais tend vers une "bonne" solution.

Les 4 grilles sont normalement toujours résolues sans sortir de la carte et avec peu ou pas de cases doublon dans les cases de la solution. Cela dit, dans le cas des grilles 30 et 40, un ou plusieurs obstacles peuvent être ignorés.

Dans les 4 cas, la qualité de la solution est est aléatoire mais tend vers une bonne solution.
