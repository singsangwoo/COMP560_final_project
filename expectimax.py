from game_function import Grid2048


class MaxNode:
    def __init__(self, grid: Grid2048, depth: int, depth_limit: int):
        self.grid = grid
        self.depth = depth
        self.depth_limit = depth_limit
        self.best_move = None
        self.best_child = None

        if self.grid.solved():
            self.score = float("inf")
        elif self.grid.is_game_over():
            self.score = 0
        elif self.depth >= self.depth_limit:
            self.score = self.grid.get_score()
        else:
            available_moves = self.grid.get_available_moves()
            if not available_moves:
                self.score = 0
            else:
                best_score = float("-inf")
                for available_move in available_moves:
                    moved_grid = Grid2048(self.grid.move(available_move))
                    child_node = ChanceNode(moved_grid, self.depth, self.depth_limit)
                    if child_node.score > best_score:
                        best_score = child_node.score
                        self.best_move = available_move
                        self.best_child = child_node
                self.score = best_score

    def get_score(self):
        return self.score

    def get_best_move(self):
        return self.best_move

    def get_best_path(self):
        path = [("max", self.grid, self.best_move, self.score)]
        if self.best_child is not None:
            path.extend(self.best_child.get_best_path())
        return path


class ChanceNode:
    def __init__(self, grid: Grid2048, depth: int, depth_limit: int):
        self.grid = grid
        self.depth = depth
        self.depth_limit = depth_limit
        self.representative_probability = None
        self.representative_child = None

        if self.grid.solved():
            self.score = float("inf")
        elif self.grid.is_game_over():
            self.score = 0
        elif self.depth >= self.depth_limit:
            self.score = self.grid.get_score()
        else:
            grids, probs = self.grid.grids_with_random_tile()
            if not probs:
                self.score = 0
            else:
                weighted_score = 0
                best_child_score = float("-inf")
                for possible_grid, prob in zip(grids, probs):
                    child_node = MaxNode(Grid2048(possible_grid), self.depth + 1, self.depth_limit)
                    contribution = child_node.score * prob
                    weighted_score += contribution

                    # This does not affect expectimax scoring; it only picks a
                    # representative spawn branch for visualization.
                    if child_node.score > best_child_score:
                        best_child_score = child_node.score
                        self.representative_probability = prob
                        self.representative_child = child_node

                self.score = weighted_score

    def get_score(self):
        return self.score

    def get_best_path(self):
        path = [("chance", self.grid, self.representative_probability, self.score)]
        if self.representative_child is not None:
            path.append(
                (
                    "tile_spawn",
                    self.representative_child.grid,
                    self.representative_probability,
                    self.representative_child.score,
                )
            )
            path.extend(self.representative_child.get_best_path())
        return path
