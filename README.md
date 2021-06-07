# StrongholdNet

Generate the dataset from the stronghold file:

```
python dataset.py 100k_strongholds.txt > 100k_dataset.csv
```

The resulting dataset should look like this:

```
depth prev_room prev_exit room exit_1 exit_2 exit_3 exit_4 exit_5 exit_portal
0 Start 1 FiveWayCrossing Corridor LeftTurn None Corridor Stairs 1
0 Start 1 FiveWayCrossing Corridor RightTurn None Corridor RightTurn 1
2 RightTurn 1 Corridor SquareRoom None Corridor None None 1
0 Start 1 FiveWayCrossing Stairs None None None Corridor 5
1 FiveWayCrossing 5 Corridor Corridor SpiralStaircase Stairs None None 1
…
5 LeftTurn 1 Corridor SquareRoom None Corridor None None 1
6 Corridor 1 SquareRoom Corridor RightTurn Corridor None None 3
7 SquareRoom 3 Corridor Corridor LeftTurn SmallCorridor None None 1
0 Start 1 FiveWayCrossing LeftTurn Corridor None RightTurn None 1
4 LeftTurn 1 FiveWayCrossing LeftTurn None SpiralStaircase Corridor None 1
```
