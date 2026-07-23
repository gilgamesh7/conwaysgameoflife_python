
import collections

class LifeGrid:
    def __init__(self, pattern):
        self.pattern = pattern

    def evolve(self):
        """
            The rules of how cells evolve:
            - Alive cells die if they have fewer than two (underpopulation) or more than three living neighbors (overpopulation).
            - Alive cells stay alive if they have two or three living neighbors.
            - Dead cells with exactly three living neighbors become alive (reproduction).
        """
        # define the delta coordinates for the neighbors of the target cell
        neighbours = (
            (-1, -1) , # Above left 
            (-1,0), # Above
            (-1,1), # Above right
            (0,-1), # Left
            (0,1), # Right
            (1,-1), # Below left
            (1,0), # Below
            (1,1) # Below right
        )

        # Creates a dictionary for counting the number of living neighbors.
        # Use the defaultdict class from the collections module to build the counter 
        # with the int class as its default factory
        num_neighbours = collections.defaultdict(int)

        # Run a loop over the currently alive cells, which are stored in the .pattern object. 
        # This loop allows you to check the neighbors of each living cell 
        # so that you can determine the next generation of living cells.
        for row, col in self.pattern.alive_cells:
            # Loop over the neighbor deltas. 
            # This inner loop counts how many cells the current cell neighbors. 
            # This count allows you to know the number of living neighbors 
            # for both living and dead cells.
            for drow, dcol in neighbours:
                num_neighbours[(row + drow, col + dcol)] += 1

        # Build a set containing the cells that will stay alive. 
        # To do this, you first create a set of neighbors that have two or three alive neighbors themselves. 
        # Then, you find the cells that are common to both this set and .alive_cells.
        stay_alive = {
            cell for cell, num in num_neighbours.items() if num in {2,3}
        } & self.pattern.alive_cells

        # Create a set with the cells that will come alive. 
        # In this case, you create a set of neighbors that have exactly three living neighbors. 
        # Then, you determine the cells that come alive by removing cells that are already in .alive_cells.
        come_alive = {
            cell for cell, num in num_neighbours.items() if num == 3
        } - self.pattern.alive_cells

        # Update .alive_cells with the set that results as the union of the cells 
        # that stay alive and those that come alive.
        self.pattern.alive_cells = stay_alive | come_alive


    def as_string(self, bbox):
        pass

    # To check whether your code works as expected, 
    # Create string representation of the living cells in each generation. 
    def __str__(self):
        return (
            f"{self.pattern.name} : \n"
            f"Alive cells -> {sorted(self.pattern.alive_cells)}"
        )