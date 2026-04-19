from expectimax import MaxNode
from game_function import Grid2048


def main():
    grid = Grid2048()
    grid.add_random_tile()
    grid.add_random_tile()

    turn = 0
    depth_limit = 3

    while not grid.is_game_over() and not grid.solved():
        print(f"\nTurn {turn}")
        grid.visualize()

        root = MaxNode(grid, 0, depth_limit)
        best_move = root.get_best_move()

        print(f"Chosen move: {best_move}")
        print(f"Expected score: {root.get_score()}")

        if best_move is None:
            break

        grid = Grid2048(grid.move(best_move))
        grid.add_random_tile()
        turn += 1

    print("\nFinal grid")
    grid.visualize()

    if grid.solved():
        print("\nReached 2048.")
    elif grid.is_game_over():
        print("\nGame over.")


if __name__ == "__main__":
    main()
