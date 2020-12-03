# Fall20-Projects

### Fox, Geese and Elephants
This project contains scripts for an AI game player for the game - Fox, Geese and Elephant. The game player uses a Minimax algorithm with a heuristic scoring function. 

The board layout is as follows:
* 1 Foxes
* 13 Geese

![Sample Board](https://github.com/SanhitaD207/Fall20-Projects/blob/main/images/sample-board.png?raw=true)


The fox tries to capture the geese by jumping over them and landing on the empty intersection behind the latter (like checkers). The geese try to surround the fox such that the fox is unable to move. The basic movement of all animals are similar, which is moving one step front or back or left or right.

### Variation
A couple of variations are to be added:
* First variation is the introduction of elephants. In this variation, 3 geese will be replaced by elephants and the total number of foxes is 2. The elephants will have the movement like that of the rest of the pieces on the board and will assist the geese in capturing the foxes. However, the fox will not be able to jump over an elephant (because the elephant is large). The only way to capture an elephant is by having the two foxes in its periphery.
* Second variation is marking certain regions on the board invalid when there are fewer pieces on board. This will ensure convergence of the game.

### Data Structures
**__Classes__**:
* BoardCell
* Board
* Player (base class)
    * FoxPlayer
    * GeeseElephantPlayer

**__Structure__**:
* BoardCell:
    * _cell_value_ - contains the animal value when filled (E/F/G)
    * _is_valid_cell_ - contains a boolean value signifying where the cell is in a valid region or not

* Board:
    * _nrows_: Number of rows
    * _ncols_: Number of columns
    * _board_: 2d array of elements (each 1 BoardCell)
    * _board_regions_: List of lists containing the row range and column range of elements in the upper/lower/left/right outer regions. This list will be used to block a region during game play when there are few pieces on board, so that the game converges.

* Player:
    * FoxPlayer:
        * _fox_collection_ : A dictionary containing key value pairs signifying fox positions on the board. For example - `{'fox_1': (3, 2), 'fox_2': (3, 4)}`
    * GeeseElephantPlayer:
        * _geese_collection_: A dictionary containing key value pairs signifying geese positions on the board. For example - `{'ge_1': (4, 1), 'ge_2': (4, 2) ...}`
        * _elephant_collection_: A dictionary containing key value pairs signifying elephant positions on the board. For example - `{'ele_1': (4, 0), 'ele_2': (4, 3), 'ele_3': (4, 6)}`
 

### Minimax
We have implemented a minimax algorithm to fetch the best move to be made by a player. The source code has been adapted from the implementation in this [heuristic](https://github.com/lfpelison/ine5430-gomoku/blob/master/src/heuristic.py) and [minimax](https://github.com/lfpelison/ine5430-gomoku/blob/master/src/minimax.py) scripts in the Gomoku game player.

#### Heuristic
We have defined a heuristic to reward the fox with capturing a goose/elephant as well as arriving at a location from where it can capture a goose/elephant in the next move. 
Similarly we have reward the GeeseElephantPlayer for capturing a fox or arriving at a position from where it can either partially block a fox or if an elephant can capture a fox.
All neutral moves are given the same points - 50.

This heuristic is used for the scoring part of the minimax algorithm.

```
{
    'f': {
        'captured_e': 500,
        'captured_g': 250,
        'can_capture_e': 300,
        'can_capture_g': 200
    },
    'g_e': {
        'captured_f': 500,
        'partial_blocked_f': 250,
        'e_can_capture_f': 250
    }
}
```

#### Algorithm
We have assumed the fox-player to start the game. The algorithm for minimax is as follows:
* Fetch available moves for the player:
* Iterate over the moves to fetch scores using the heuristic:
    * A move is played and the `min_play()` function is called
    * The available moves for the other player are fetched and are iterated for calculating the scores:
        * A move is played and the `max_play()` function is called.
        * We have restricted the depth for minimax to 2, so the heuristic calculation function is called in `max_play()`
        * Score is compared with a `min_node_value`
        * At the end of iteration, `min_node_value` is returned
    * Score is compared with a `node_value`
        * If a better score is achieved, the board_piece and move are appended to the `next_board_piece` and `next_move` lists
* An index number is generated randomly (between 0 and length of the next_move list), and the board_piece and move at that index is returned to the `play_game()` function

### Game Snapshots
![Game Snapshot](https://github.com/SanhitaD207/Fall20-Projects/blob/main/images/snapshots.png?raw=true)

### Distribution of work

Sanhita -  Created board and board cell data structure, set up initial board state, game play logic and its methods (like move board piece, remove captured animal)

Adarsh - Created player data structure and its methods (like get available moves), helper functions (get single step move, get hop move),minimax algorithm

Equally split - Heuristic function optimization, documentation (README, presentation), docstrings

