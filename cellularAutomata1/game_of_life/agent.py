# FixedAgent: Immobile agents permanently fixed to cells
from mesa.discrete_space import FixedAgent

class Cell(FixedAgent):
    """Represents a single ALIVE or DEAD cell in the simulation."""

    DEAD = 0
    ALIVE = 1

    @property
    def x(self):
        return self.cell.coordinate[0]

    @property
    def y(self):
        return self.cell.coordinate[1]

    @property
    def is_alive(self):
        return self.state == self.ALIVE

    @property
    def neighbors(self):
        return self.cell.neighborhood.agents
    
    def __init__(self, model, cell, init_state=DEAD):
        """Create a cell, in the given state, at the given x, y position."""
        super().__init__(model)
        self.cell = cell
        self.pos = cell.coordinate
        self.state = init_state
        self._next_state = None

    def determine_state(self, row):
        """Compute if the cell will be dead or alive at the next tick.  This is
        based on the number of alive or dead neighbors.  The state is not
        changed here, but is just computed and stored in self._nextState,
        because our current state may still be necessary for our neighbors
        to calculate their next state.
        """
        # Get the neighbors and apply the rules on whether to be alive or dead
        # at the next tick.
        live_neighbors = sum(neighbor.is_alive for neighbor in self.neighbors)

        info_of_states = []
        self._next_state = self.state

        for neighbor in self.neighbors:
            info_of_states.append(neighbor.state)
        
        state = ""
        alive = ["110", "100", "011", "001"]

        state += str(info_of_states[2])
        state += str(info_of_states[4])
        state += str(info_of_states[7])

        if self.pos[1] == row:
            if state in alive:
                self._next_state = self.ALIVE
            else:
                self._next_state = self.DEAD
        elif self.pos[1] <= row:
            self._next_state = self.DEAD
        # Assume nextState is unchanged, unless changed below.

    def assume_state(self):
        """Set the state to the new computed state -- computed in step()."""
        self.state = self._next_state
