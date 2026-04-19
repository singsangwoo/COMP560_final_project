import random

class Grid2048:
    def __init__(self, grid=None):
        if grid is None:
            self.grid = [[0] * 4 for _ in range(4)]
        else:
            self.grid = grid
    
    def get_score(self):
        grid_matrix = self.get_grid()
        
        # Number of empty cells (freedom of movement)
        empty_cells = len(self.empty_cells())
        
        # Maximum tile value (closeness to 2048)
        max_tile = max(max(row) for row in grid_matrix) if any(any(cell != 0 for cell in row) for row in grid_matrix) else 0
        
        # Monotonicity (how well rows/columns are sorted)
        monotonicity = self.get_monotonicity(grid_matrix)
        
        # Smoothness (minimizing differences between adjacent tiles)
        smoothness = self.get_smoothness(grid_matrix)
        
        # Corner bonus (prefer large tiles in top-right corner)
        corner_bonus = grid_matrix[0][3] if grid_matrix[0][3] != 0 else 0
        
        # Total score calculation (weights adjustable)
        score = (
            1000 * empty_cells +
            10 * max_tile +
            1 * monotonicity +
            0.1 * smoothness +
            0.5 * corner_bonus
        )
        
        return score

    def get_monotonicity(self, grid_matrix):
        score = 0
        
        # Row-wise monotonicity
        for row in grid_matrix:
            for i in range(3):
                if row[i] >= row[i+1]:
                    score += row[i] - row[i+1]
                else:
                    score -= row[i+1] - row[i]
        
        # Column-wise monotonicity
        for j in range(4):
            for i in range(3):
                if grid_matrix[i][j] >= grid_matrix[i+1][j]:
                    score += grid_matrix[i][j] - grid_matrix[i+1][j]
                else:
                    score -= grid_matrix[i+1][j] - grid_matrix[i][j]
        
        return score

    def get_smoothness(self, grid_matrix):
        score = 0
        
        # Horizontal adjacent differences
        for i in range(4):
            for j in range(3):
                if grid_matrix[i][j] != 0 and grid_matrix[i][j+1] != 0:
                    score -= abs(grid_matrix[i][j] - grid_matrix[i][j+1])
        
        # Vertical adjacent differences
        for j in range(4):
            for i in range(3):
                if grid_matrix[i][j] != 0 and grid_matrix[i+1][j] != 0:
                    score -= abs(grid_matrix[i][j] - grid_matrix[i+1][j])
        
        return score
    
    def get_grid(self):
        return self.grid

    def empty_cells(self):
        return [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
    
    def add_random_tile(self):
        if self.empty_cells():
            i, j = random.choice(self.empty_cells())
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def grids_with_random_tile(self):
        grids = []
        chances = []
        
        if self.empty_cells():
            for i, j in self.empty_cells():
                new_grid_2 = [row[:] for row in self.grid]
                new_grid_4 = [row[:] for row in self.grid]
                new_grid_2[i][j] = 2
                new_grid_4[i][j] = 4
                grids.append(new_grid_2)
                chances.append(0.9 / len(self.empty_cells()))
                grids.append(new_grid_4)
                chances.append(0.1 / len(self.empty_cells()))
        return grids, chances

    def is_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return False
                if i < 3 and self.grid[i][j] == self.grid[i+1][j]:
                    return False
                if j < 3 and self.grid[i][j] == self.grid[i][j+1]:
                    return False
        return True
    
    def solved(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 2048:
                    return True
        return False

    def get_available_moves(self):
        moves = []
        for direction in ['up', 'down', 'left', 'right']:
            if self.can_move(direction):
                moves.append(direction)
        return moves

    def can_move(self, direction):
        if direction == "right":
            for i in range(4):
                for j in range(3):
                    if self.grid[i][j] != 0 and (self.grid[i][j] == self.grid[i][j+1] or self.grid[i][j+1] == 0):
                        return True
        elif direction == "left":
            for i in range(4):
                for j in range(1, 4):
                    if self.grid[i][j] != 0 and (self.grid[i][j] == self.grid[i][j-1] or self.grid[i][j-1] == 0):
                        return True
        elif direction == "up":
            for i in range(1, 4):
                for j in range(4):
                    if self.grid[i][j] != 0 and (self.grid[i][j] == self.grid[i-1][j] or self.grid[i-1][j] == 0):
                        return True
        elif direction == "down":
            for i in range(3):
                for j in range(4):
                    if self.grid[i][j] != 0 and (self.grid[i][j] == self.grid[i+1][j] or self.grid[i+1][j] == 0):
                        return True
        return False

    def merge_line(self, line):
        tiles = [tile for tile in line if tile != 0]
        merged = []
        i = 0

        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                merged.append(tiles[i] * 2)
                i += 2
            else:
                merged.append(tiles[i])
                i += 1

        return merged + [0] * (4 - len(merged))

    def move(self, direction):
        new_grid = [row[:] for row in self.grid]
        if direction == "right":
            for i in range(4):
                reversed_row = list(reversed(new_grid[i]))
                merged_row = self.merge_line(reversed_row)
                new_grid[i] = list(reversed(merged_row))
        elif direction == "left":
            for i in range(4):
                new_grid[i] = self.merge_line(new_grid[i])
        elif direction == "up":
            for j in range(4):
                column = [new_grid[i][j] for i in range(4)]
                merged_column = self.merge_line(column)
                for i in range(4):
                    new_grid[i][j] = merged_column[i]
        elif direction == "down":
            for j in range(4):
                reversed_column = [new_grid[i][j] for i in range(3, -1, -1)]
                merged_column = self.merge_line(reversed_column)
                for i in range(4):
                    new_grid[3 - i][j] = merged_column[i]

        return new_grid

    def visualize(self):
        for i in range(4):
            for j in range(4):
                print(f"{self.grid[i][j]:4}", end=" ")
            print()
