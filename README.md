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

In the diagram above, misses are depicted by grey crosses and hits by red squares with grey crosses.

The first player to sink his opponent’s fleet (hitting every location covered with part of a boat) wins the game.
