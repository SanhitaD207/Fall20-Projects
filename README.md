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

#### Heuristic

#### Algorithm
   
## Deliverables and other Requirements:

* Have some fun!
* In your own fork, please replace this README.md file's contents with a good introduction to your own project. 
* Targeted Algorithm Analysis:  Regardless of which option you choose, you need to _describe the important performance characteristics of your program and explain why you chose the data structures and core algorithm(s) you did_. So for example, if you chose Type #1, what's the Big-O run-time complexity of your puzzle solver? Or the puzzle generator? (I've had some students write randomized puzzle generators that could theoretically run infinitely -- we don't want that!)  If you're doing Type #2, what's the complexity of your heuristic evaluation function used for pruning?

* If your team has more than one student, take efforts to see that each makes git commits. In addition, your README documentation should include a summary of how you shared the work.
* Recorded video or live in-class presentation of your work. 

