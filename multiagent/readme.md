# <center>Assignment 2 - Multi-agents</center>
Matthieu Vilain  
SFSU ID: 920010985  
Number of hours spend on this assignment : between 10 and 14 hours


## Reflex Agent

For this evaluation function I simply return `-1 * distanceToTheClosestDot` if the ghost is more than 2 step away and `-infinity` if the the ghost less than 2 step away.

## Minimax, Alpha-Beta Pruning and Expectimax

For this part I just implemented the algorithms we saw in class. I noticed after implementing minimax that it was easier to create two different function for the maximization and the minimization so I implemented Alpha-Beta in this way.  
For expectimax my way to selected randomly actions with the same score is not mathematicaly uniform because I do it iteratively but I don't think it really affect the result.

## Evaluation Function

To design my evaluation function I searched for the important information that the agent need. I found that that the agent need 3 informations :
- The distance to the food
- The distance to the ghosts
- The distance to the capsule

The main idea with my evaluation function is that the agent is attract by the food and the capsule and is repulse by ghost, but if the ghost is scared then the agent is attract by the ghost.

 ```
 eval = currentScore - sum(foodCoef * foodDistance)
                     - sum(capsuleCoef * capsuleDistance)
                     + sum(ghostCoef * ghostSign * ghostDistance)

                     Where ghostSign =  1  if normal ghost
                           ghostSign = -1  if scared ghost
 ```

 Give different values ​​to the coefficients will leads to different behavior.

 Some of the different coefficient values I tried are summarized in this table :

| foodCoef | capsuleCoef | ghostCoef | Final score |   Information    |
|----------|-------------|-----------|:-----------:|------------------|
| 1        | 2           | 1         | 852.5       |                  |
| 0.1      | 2           | 1         | 1063.0      |                  |
| 0.1      | 10          | 1         | 1245.3      |                  |
| 0.1      | 10          | 0.5       | 1239.8      | Never below 1000 |
| 0.1      | 15          | 1         | 1265.7      | Never below 1100 |
| __0.1__  | __18.15__   | __1 __    | __1279.9__  | Never below 1100 |
