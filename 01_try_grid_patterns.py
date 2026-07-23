from life import grid, patterns

blinker = patterns.Pattern("Blinker", {(2,1), (2,2),(2,3)})
grid = grid.LifeGrid(blinker)
print(grid)

grid.evolve()
print(grid)

grid.evolve()
print(grid)
