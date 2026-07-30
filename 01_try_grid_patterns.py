from life import grid, patterns

def print_grid(grid):
    print(grid)
    print(grid.as_string((0, 0, 5, 5)))
    for _ in range(8):
        grid.evolve()
        print(grid)
        print(grid.as_string((0, 0, 5, 5)))

# Blinker pattern
blinker = patterns.Pattern("Blinker", {(2,1), (2,2),(2,3)})
blinker_grid = grid.LifeGrid(blinker)
print_grid(blinker_grid)

# Toad pattern
toad = patterns.Pattern("Toad", {(2,2), (2,3),(2,4), (3,1), (3,2), (3,3)})
toad_grid = grid.LifeGrid(toad)
print_grid(toad_grid)

# Beacon pattern
beacon = patterns.Pattern("Beacon", {(1,1), (1,2), (2,1), (2,2), (3,3), (3,4), (4,3), (4,4)})
beacon_grid = grid.LifeGrid(beacon)
print_grid(beacon_grid)



