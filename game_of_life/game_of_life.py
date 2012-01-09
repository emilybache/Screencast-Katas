
def game_of_life_generator(seed):	
    game = GameOfLife(seed)
    while True:
        yield game.tick()

class GameOfLife(object):
    def __init__(self, seed):
        self.alive_cells = seed
    
    def tick(self):
        self.alive_cells = set.union(self.survivors(), self.births())
        return self.alive_cells
            
    def survivors(self):
        survivors = [cell 
                     for cell in self.alive_cells 
                     if len(self.live_neighbours(cell)) in [2, 3]]
        return set(survivors)

    def live_neighbours(self, cell):
        live_neighbours = [neighbour 
                            for neighbour in neighbours(cell) 
                            if neighbour in self.alive_cells]
        return set(live_neighbours)

    def births(self):
        births = [candidate
                  for candidate in self.birth_candidates() 
                  if len(self.live_neighbours(candidate)) == 3]
        return set(births)
        
    def birth_candidates(self):
        dead_with_one_live_neighbour = [self.dead_neighbours(cell) 
                                        for cell in self.alive_cells]
        if not dead_with_one_live_neighbour:
            return set()
        return set.union(*dead_with_one_live_neighbour)
        
    def dead_neighbours(self, cell):
        dead_neighbours = [neighbour 
                            for neighbour in neighbours(cell) 
                            if neighbour not in self.alive_cells]
        return set(dead_neighbours)

def neighbours(cell):
    deltas = [(-1, -1), (0, -1), (1, -1),
              (-1,  0),          (1,  0),
              (-1,  1), (0,  1), (1,  1)]
    x, y = cell
    return [(x+dx, y+dy) for (dx, dy) in deltas]


def test_GameOfLife_tick():
    seed = set()
    game = GameOfLife(seed)
    next_generation = game.tick()
    assert next_generation == set()
    
def test_GameOfLife_tick_with_one_death():
    seed = set([(0, 0)])
    game = GameOfLife(seed)
    game.tick()
    assert game.alive_cells == set()

def test_GameOfLife_tick_with_a_survival():
    """
    stable foursome
    .**.
    .**.
    """
    seed = set([(1, 0), (2, 0), (1, 1), (2, 1)])
    game = GameOfLife(seed)
    assert game.tick() == seed

def test_GameOfLife_live_neighbours_with_no_live_neighbours():
    """
    .*.
    """
    live_neighbours = GameOfLife(set([(1, 0)])).live_neighbours((1, 0))
    assert live_neighbours == set()

def test_GameOfLife_live_neighbours_with_one_live_neighbour():
    """
    .**.
    """
    live_neighbours = GameOfLife(set([(1, 0), (2, 0)])).live_neighbours((1, 0))
    assert live_neighbours == set([(2, 0)])
    
def test_GameOfLife_births():
    """
    .*
    **
    """
    seed = set([(1, 0), (0, 1), (1, 1)])
    game = GameOfLife(seed)
    assert game.births() == set([(0, 0)])

def test_GameOfLife_birth_candidates():
    """
    *.
    """
    seed = set([(0, 0)])
    game = GameOfLife(seed)
    candidates = game.birth_candidates()
    assert len(candidates) == 8
    assert candidates == set(neighbours((0, 0)))
    
def test_neighbours_at_origin():
    my_neighbours = neighbours((0, 0))
    assert len(my_neighbours) == 8
    assert (0, 0) not in my_neighbours
    
def test_neighbours():
    my_neighbours = neighbours((1, 0))
    assert len(my_neighbours) == 8
    assert (1, 0) not in my_neighbours
    assert (0, 0) in my_neighbours
    assert (0, 1) in my_neighbours
    assert (-1, 0) not in my_neighbours
        

def test_blinker_several_generations():
    """
    blinker:
    
    .....
    .***.
    .....
    
    ->
    
    ..*..
    ..*..
    ..*..
    """
    seed = set([(1, 1), (2, 1), (3, 1)])
    game = game_of_life_generator(seed)
    assert game.next() == set([(2, 0), (2, 1), (2, 2)])
    assert game.next() == set([(1, 1), (2, 1), (3, 1)])

def test_generations():	
    seed = set()
    game = game_of_life_generator(seed)
    assert game.next() == set()
