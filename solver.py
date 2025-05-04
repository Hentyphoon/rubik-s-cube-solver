import json
from class_def import Cube

def reduce_to_g1(cube): #edge orientation
    allowed_moves = ['U', 'D', 'L', 'R', 'F2', 'B2']

def reduce_to_g2(cube): #corner orientation
    allowed_moves = ['U', 'D', 'L2', 'R2', 'F2', 'B2']

def reduce_to_g3(cube): #edge permutation
    allowed_moves = ['U2', 'D2', 'L2', 'R2', 'F2', 'B2']

def find_solution(cube): #final turns
    allowed_moves = ['I']

def search_solutions(cube, allowed_moves, depth=5):
    pass

def main():
    cube = json.loads()
