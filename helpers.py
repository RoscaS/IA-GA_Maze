from collections import namedtuple
from typing import List, Tuple

from Maze import Maze

Gene = namedtuple("Gene", ["apply", "str"])
Direction = namedtuple("Direction", ["callback", "str"])

GENE_LENGTH = 1

directions = {
    0: Direction(lambda pos: (pos[0], pos[1] - 1), "N"),
    1: Direction(lambda pos: (pos[0], pos[1] + 1), "S"),
    2: Direction(lambda pos: (pos[0] - 1, pos[1]), "W"),
    3: Direction(lambda pos: (pos[0] + 1, pos[1]), "E")
}

def _parse_gene(gene: int) -> Gene:
    """Convert bit string to Code namedtuple"""
    return Gene(directions[gene].callback, directions[gene].str)

def _parse_chromosome(chromosome: List[int]) -> List[Gene]:
    """Parse chromosome's genes"""
    return list(map(_parse_gene, chromosome))

def maze_repr(chromosome: List[int], maze: Maze) -> str:
    """String containing a view of the state of the maze"""
    path = extract_path(chromosome, maze)
    maze.reset()
    maze.apply_solution(path)
    penalities = compute_penalities(path, maze)
    out = f"\nOut: {penalities[0]}"
    itself = f"\nItself: {penalities[1]}"
    walls = f"\nwalls: {int(penalities[2] / 2)}"
    return maze.__str__() + out + itself + walls

def extract_path(chromosome: List[int], maze: Maze) -> List[Tuple]:
    """Turn a chromosome to a list of coordinates"""
    genes = _parse_chromosome(chromosome)
    path = [maze.start]
    for gene in genes:
        path.append(gene.apply(path[-1]))
    return path

def compute_manhattan_distance(a: Tuple, b: Tuple) -> int:
    """Compute manhattan distance between a and b"""
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def compute_fitness(chromosome: List[int], maze: Maze) -> int:
    """Fitness is the sum of manhattan distance (between the last
    gene of the chromosome and the end of the maze) and
    penalities. """
    path = extract_path(chromosome, maze)
    penalties = compute_penalities(path, maze)
    manhattan = compute_manhattan_distance(path[-1], maze.end)
    return manhattan + sum(penalties)

def compute_penalities(path: List[Tuple], maze: Maze) -> Tuple:
    """Used to give some direction to the evolution of the
    chromosome."""
    uniques = set(path)
    x = lambda coord: coord < 0 or coord > maze.width - 1
    y = lambda coord: coord < 0 or coord > maze.height - 1
    out = sum([1 for coord in path if x(coord[0]) or y(coord[1])])
    itself = len(path) - len(uniques)
    walls = len(uniques.intersection(set(maze.obstacles))) * 2
    return out, itself, walls
