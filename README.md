# BattleShip-Bot
A python program that uses the power of probability to play the game of battleship !

Battleship is a classic two person game, originally played with pen and paper.

On a grid (typically 10 x 10), players ’hide’ ships of mixed length; horizontally or vertically (not diagonally) without any overlaps. The exact types and number of ships varies by rule, but for this posting, I’m using ships of lengths: 5, 4, 3, 3, 2 (which results in 17 possible targets out of the total of 100 squares).

A couple of example layouts are shown below:
![Architecture Image](https://github.com/MainakRoy93/BattleShip-Bot/blob/master/Images/2020-02-02_15h57_12.png?raw=true "Optional Title")

## Game Rules
We’ll start with a description of the simplified method of play:

After each player has hidden his fleet, players alternate taking shots at each other by specifying the coordinates of the target location. After each shot, the opponent responds with either a call HIT! or MISS! indicating whether the target coordinates have hit part of a boat, or open water. An example of a game in progress is show on the left.

![Architecture Image](https://github.com/MainakRoy93/BattleShip-Bot/blob/master/Images/2020-02-02_16h07_35.png?raw=true "Optional Title")

In the diagram above, misses are depicted by grey crosses and hits by red squares with grey crosses. The first player to sink his opponent’s fleet (hitting every location covered with part of a boat) wins the game.

## Probability Density Functions
We know which ships (and even more importantly what the lengths of the ships) are still active. These facts are very valuable in determining which location we search next. The algorithm will calculate the most probably location to fire at next based on a superposition of all possible locations the enemy ships could be in. At the start of every new turn, based on the ships still left in the battle, we’ll work out all possible locations that every ship could fit (horizontally or vertically). Initially, this will be pretty much anywhere, but as more and more shots are fired, some locations become less likely, and some impossible. Every time it’s possible for a ship to be placed in over a grid location, we’ll increment a counter for that cell. The result will be a superposition of probabilities.

The program calculates discrete values for the probability of a ship being located at a given cell. These are not true probability density functions which evaluate the integral of a function. The calculated values used in the program would be better classified as a probability density matrix as they are discrete values. Below is the logical flow of the probability calculations.

![Architecture Image](https://github.com/MainakRoy93/BattleShip-Bot/blob/master/Images/2020-02-15_17h36_23.png?raw=true "Optional Title")

In Hunt Mode the probability value given to a certain cell is determined by the number of ways a single ship can be oriented to fit on a that cell. The values for each remaining ship size are then summed to produce a final value. Destroy Mode is activated when a ship is hit in Hunt Mode. In Destroy Mode the probability value given to a certain cell is determined by the number of ways a single ship can be oriented to fit on that cell and the hit simultaneously. Again, the values for each remaining ship size are summed to produce a final value.

![Architecture Image](https://github.com/MainakRoy93/BattleShip-Bot/blob/master/Images/2020-02-15_17h39_45.png?raw=true "RAW")
*The probability density for a single size 3 ship*

![Architecture Image](https://github.com/MainakRoy93/BattleShip-Bot/blob/master/Images/2020-02-15_17h43_50.png?raw=true "RAW")
*The sum of the probabilities for all ships*

![Architecture Image](https://github.com/MainakRoy93/BattleShip-Bot/blob/master/Images/2020-02-15_17h46_07.png?raw=true "RAW")
*A miss at E5 with Hunt Mode Probability*

![Architecture Image](https://github.com/MainakRoy93/BattleShip-Bot/blob/master/Images/2020-02-15_17h46_38.png?raw=true "RAW")
*A hit at F6 with Destroy Mode Probability*

Below is the flowchart of the logic of the program

![Architecture Image](https://github.com/MainakRoy93/BattleShip-Bot/blob/master/Images/2020-02-02_16h23_38.png?raw=true "Optional Title")
