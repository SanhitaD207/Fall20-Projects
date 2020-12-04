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

### Time Complexity Analysis

The following calculations are performed for the minimax algorithm of depth = 2.

In the worst case scenario each board piece has 4 moves available. Therefore, from the total combinations tested for best move = 13 * 4 * 2 * 4 = 416 where total geese/elephant pieces are 13 and fox pieces are 2.
However, in most cases all the board pieces cannot move in all four directions and the board pieces also get eliminated. 
So on an average we can assume that 7 of the geese/elephant player has board pieces that have 2 possible moves each, and that the fox player has 3 available moves for each fox.
This way for an average case combinations tried are - 7 * 2 * 2 * 3 = 84

Most of the calculations in the heuristic function involve constant time but the part where the code tries to identify the captured animal requires O(n) time. Thus the heuristic function has time complexity of O(n) where n is number of animals in the animal collection. 

Therefore the time complexities are as follows: 
* _Average_ - O(3m * 2n * m) or O(2n * 3m * n) 
    * m is the number of fox-pieces and n is the number of geese/elephant pieces, fox having 3 moves each and geese/elephant having 2 moves each
    * a fox or geese/elephant being captured in each move is the reason for the additional m or n factor
* _Worst_ - O(4m * 4n * m) or O(4n * 4m * n)
    * m is the number of fox-pieces and n is the number of geese/elephant pieces, fox having 4 moves each and geese/elephant having 4 moves each
    * a fox or geese/elephant being captured in each move is the reason for the additional m or n factor
    
    
### Game Snapshots
![Game Snapshot](https://github.com/SanhitaD207/Fall20-Projects/blob/main/images/snapshots.png?raw=true)

### Distribution of work by Contributors

* _Sanhita Dhamdhere (sanhita2)_ -  Created board and board cell data structure, set up initial board state, game play logic and its methods (like move board piece, remove captured animal)

* _Adarsh Agarwal (adarsha2)_ - Created player data structure and its methods (like get available moves), helper functions (get single step move, get hop move),minimax algorithm

* _Equally split_ - Heuristic function optimization, documentation (README, presentation), docstrings

### References

- https://github.com/lfpelison/ine5430-gomoku/blob/master/src/minimax.py
- https://bonaludo.com/2015/09/05/halatafl-or-fox-and-geese/
- Game play – TicTacToe (Assignment 4) game play logic

