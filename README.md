# StrongholdNet

Generate the dataset from the stronghold file:

```
python dataset.py 100k_strongholds.txt > 100k_dataset.csv
```

The resulting dataset should look like this:

```
depth prev_room prev_exit room exit_0 exit_1 exit_2 exit_3 exit_4 exit_portal
0 Start 0 FiveWayCrossing Corridor LeftTurn None Corridor Stairs 0
0 Start 0 FiveWayCrossing Corridor RightTurn None Corridor RightTurn 0
2 RightTurn 0 Corridor SquareRoom None Corridor None None 0
0 Start 0 FiveWayCrossing Stairs None None None Corridor 4
1 FiveWayCrossing 4 Corridor Corridor SpiralStaircase Stairs None None 0
…
5 LeftTurn 0 Corridor SquareRoom None Corridor None None 0
6 Corridor 0 SquareRoom Corridor RightTurn Corridor None None 2
7 SquareRoom 2 Corridor Corridor LeftTurn SmallCorridor None None 0
0 Start 0 FiveWayCrossing LeftTurn Corridor None RightTurn None 0
4 LeftTurn 0 FiveWayCrossing LeftTurn None SpiralStaircase Corridor None 0
```
