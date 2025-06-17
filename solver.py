from class_def import Cube

def reduce_to_g1(cube):
    allowed_moves = [(f, t) for f in ['U', 'D', 'L', 'R', 'F', 'B'] for t in [1, 2, 3]]
    return search_solutions(cube, allowed_moves, lambda c: c.is_g1())

def reduce_to_g2(cube):
    allowed_moves = [(f, t) for f in ['U', 'D', 'L', 'R', 'F', 'B'] for t in [1, 2, 3]]
    return search_solutions(cube, allowed_moves, lambda c: c.is_g2())

def reduce_to_g3(cube):
    allowed_moves = [(f, t) for f in ['U', 'D', 'L', 'R', 'F', 'B'] for t in [1, 2, 3]]
    return search_solutions(cube, allowed_moves, lambda c: c.is_g3())

def find_solution(cube):
    allowed_moves = [(f, t) for f in ['U', 'D', 'L', 'R', 'F', 'B'] for t in [1, 2, 3]]
    return search_solutions(cube, allowed_moves, lambda c: c.is_solved())

def search_solutions(cube, allowed_moves, goal_check, max_depth=7):
    return dfs(cube, allowed_moves, goal_check, [], max_depth)

def dfs(cube, allowed_moves, goal_check, path, depth):
    if goal_check(cube):
        return path

    if depth == 0:
        return None

    for move in allowed_moves:
        next_cube = cube.copy()
        next_cube.move(move)
        result = dfs(next_cube, allowed_moves, goal_check, path + [move], depth - 1)
        if result is not None:
            return result

    return None

def apply_solution(cube, moves):
    new_cube = cube.copy()
    for move in moves:
        new_cube.move(move)
    return new_cube

def main():
    import json
    with open("cube_input.json") as f:
        cube_data = json.load(f)

    unsolved_cube = Cube(cube_data)
    g1_solution = reduce_to_g1(unsolved_cube)
    g1_cube = apply_solution(unsolved_cube, g1_solution)

    g2_solution = reduce_to_g2(g1_cube)
    g2_cube = apply_solution(g1_cube, g2_solution)

    g3_solution = reduce_to_g3(g2_cube)
    g3_cube = apply_solution(g2_cube, g3_solution)

    final_solution = find_solution(g3_cube)

    total_solution = g1_solution + g2_solution + g3_solution + final_solution
    print("Total moves:", total_solution)

if __name__ == "__main__":
    main()
