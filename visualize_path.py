from expectimax import MaxNode
from game_function import Grid2048


def print_initial_step(step_index, grid: Grid2048, score):
    print(f"\nStep {step_index}: initial")
    print(f"Score at the initial max node: {score}")
    grid.visualize()


def print_max_step(step_index, move, moved_grid: Grid2048, score):
    print(f"\nStep {step_index}: max")
    print(f"Chosen move: {move}")
    print(f"Expected score after choosing this move: {score}")
    moved_grid.visualize()


def print_chance_step(step_index, probability, spawned_grid: Grid2048, expected_score, child_score):
    print(f"\nStep {step_index}: chance")
    print(f"Representative spawn probability for visualization: {probability}")
    print(f"Expected score at this chance node: {expected_score}")
    print(f"Score of the representative spawned child: {child_score}")
    spawned_grid.visualize()


def visualize_best_path(root: MaxNode):
    print("Representative expectimax path")
    print("Chance-node score is still the weighted expected value.")
    print("Chance-node visualization follows one representative spawned child.")

    step_index = 0
    print_initial_step(step_index, root.grid, root.get_score())
    step_index += 1

    current_max = root
    while current_max.best_child is not None:
        chance_node = current_max.best_child

        print_max_step(
            step_index,
            current_max.get_best_move(),
            chance_node.grid,
            current_max.get_score(),
        )
        step_index += 1

        if chance_node.representative_child is None:
            break

        print_chance_step(
            step_index,
            chance_node.representative_probability,
            chance_node.representative_child.grid,
            chance_node.get_score(),
            chance_node.representative_child.get_score(),
        )
        step_index += 1

        current_max = chance_node.representative_child


def main():
    initial_grid = Grid2048([
        [2, 4, 2, 0],
        [4, 8, 0, 0],
        [2, 16, 32, 0],
        [0, 0, 0, 0],
    ])

    root = MaxNode(initial_grid, 0, 3)
    visualize_best_path(root)


if __name__ == "__main__":
    main()
