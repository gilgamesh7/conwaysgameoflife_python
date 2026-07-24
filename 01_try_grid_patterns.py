from life import grid, patterns

blinker = patterns.Pattern("Blinker", {(2,1), (2,2),(2,3)})
grid = grid.LifeGrid(blinker)

print(grid)
print(grid.as_string((0, 0, 5, 5)))

for _ in range(8):
    grid.evolve()
    print(grid)
    print(grid.as_string((0, 0, 5, 5)))

    grid.evolve()
    print(grid)
    print(grid.as_string((0, 0, 5, 5)))