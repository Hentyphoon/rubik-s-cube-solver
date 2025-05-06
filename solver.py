import json
from class_def import Cube

def reduce_to_g1(cube): #edge orientation
    allowed_moves = ['U', 'D', 'L', 'R', 'F2', 'B2']
    return search_solutions(cube, allowed_moves, lambda c: c.is_g1())

def reduce_to_g2(cube): #corner orientation
    allowed_moves = ['U', 'D', 'L2', 'R2', 'F2', 'B2']
    return search_solutions(cube, allowed_moves, lambda c: c.is_g2())

def reduce_to_g3(cube): #edge permutation
    allowed_moves = ['U2', 'D2', 'L2', 'R2', 'F2', 'B2']
    return search_solutions(cube, allowed_moves, lambda c: c.is_g3())

def find_solution(cube): #final turns
    allowed_moves = ['I']
    return search_solutions(cube, allowed_moves, lambda c: c.is_solved())

def search_solutions(cube, allowed_moves, goal_check, max_depth=5):
    return dfs(cube, allowed_moves, goal_check, [], max_depth)

def dfs(cube, allowed_moves, goal_check, path, depth):
    if goal_check(cube):
        return path

    if depth == 0:
        return None

    for move in allowed_moves:
        next_cube = cube.copy()
        next_cube.apply_move(move)
        result = dfs(next_cube, allowed_moves, goal_check, path + [move], depth - 1)
        if result is not None:
            return result

    return None

  
def main():
    cube = json.loads()
    unsolved_cube = Cube(cube)
    g1_cube = reduce_to_g1(unsolved_cube)
    g2_cube = reduce_to_g2(g1_cube)
    g3_cube = reduce_to_g3(g2_cube)
    solved_cube = find_solution(g3_cube)

if __name__ == "__main__":
    main()