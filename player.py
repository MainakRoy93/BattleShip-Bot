from ship import Ship
from board import Board
from position import Position
import numpy as np

class Player:

    def __init__(self, name):
        self.sunkArray = []
        self.shotcount = 0
        self.hit_to_sunk = 0
        self.hit_miss_sunk = 0
        self.sunk_count = 0
        self.seek = True
        self.__name = name
        self.shotList = []
        self.__results = []
        self.shipLengthArray = [5, 4, 3, 3, 2]
        self.hitMiss = np.ones((10,10), dtype=np.int32)
        for row in range(65,75):
            for col in range(1,11):
                self.shotList.append([row,col])
        self.calcProb()
        self.targetModeProbabilities = np.zeros((10,10), dtype=np.int32)
        print(probabilityMatrix)
               
    def get_name(self):
        return self.__name

    def __str__(self):
        return self.get_name()
    
    def get_board(self):
        ships_list = [Ship('Carrier', Position('B', 3), 5, False),
                      Ship('battleship', Position('J', 5), 4, False),
                      Ship('submarine', Position('G', 2), 3, True),
                      Ship('crusier', Position('D', 9), 3, True),
                      Ship('destroyer', Position('H', 10), 2, True)]
        return Board(ships_list)
    
    def next_shot(self):
       self.shotcount += 1
       row, col, maximumProb = self.getMaxProb(self.seek)   
       row  = chr(row + 65)
       col += 1
       return Position(row, col)

   
    def updateBoard(self, posObject):
        row = posObject[0].get_row_idx()
        col = posObject[0].get_col_idx()
        if posObject[1]:
            self.hitMiss[row, col] = 2
        elif posObject[1] is False:
            self.hitMiss[row, col] = 0
            
    def getMaxProb(self, mode):
        if mode:
            return np.where(self.probabilityMatrix == np.amax(self.probabilityMatrix))[0][0],\
    np.where(self.probabilityMatrix == np.amax(self.probabilityMatrix))[1][0], np.amax(self.probabilityMatrix)
        else:
            return np.where(self.targetModeProbabilities == np.amax(self.targetModeProbabilities))[0][0],\
    np.where(self.targetModeProbabilities == np.amax(self.targetModeProbabilities))[1][0], np.amax(self.targetModeProbabilities)
   
    def calcProb(self):
        self.probabilityMatrix = np.zeros((10,10), dtype=np.int32)
        for shipLength in self.shipLengthArray:
            for i in range(10):
                for j in range(10):
                    if self.hitMiss[i, j] != 1:
                        self.probabilityMatrix[i,j] = 0
                    else:
                        self.probabilityMatrix[i,j] += self.__checkRight(i,j,shipLength) \
                        + self.__checkLeft(i,j,shipLength) \
                        + self.__checkUp(i,j,shipLength) + self.__checkDown(i,j,shipLength) \
                        + self.__check_mid_horizontal(i,j,shipLength, False) \
                        + self.__check_mid_vertical(i,j,shipLength, False)

    def post_shot_result(self, result):
        self.__results.append(result)
        self.updateBoard(result)
        self.calcProb()
        
        if result[1]:          
            self.targetModeProbability()
            self.sunkArray.append((result[0].get_row_idx(), result[0].get_col_idx()))
            self.hit_to_sunk += 1
            self.seek = False
            if result[2]:
                length_of_ship_sunk = self.hit_to_sunk
                self.shipLengthArray.remove(length_of_ship_sunk)
                for i in range(len(self.sunkArray)):
                    self.hitMiss[self.sunkArray[i][0],self.sunkArray[i][1]] = 3
                self.sunkArray.clear()
                self.hit_miss_sunk = 0
                self.hit_to_sunk = 0
                self.seek = True
                
        if result[1] is False and self.seek is False:
            self.targetModeProbability()
            
        
    def targetModeProbability(self):
        self.targetModeProbabilities = np.zeros((10,10), dtype=np.int32)
        hitTargets = np.where(self.hitMiss==2)
        for i in range(hitTargets[0].size):
            row = hitTargets[0][i]
            col = hitTargets[1][i]
            self.targetModeProbabilities[row, col] = 0
            for shipLength in self.shipLengthArray:
                if self.__checkRight(row, col, shipLength) == 1:
                    for column in range(col+1, col + shipLength):
                        if self.hitMiss[row, column] not in (0,2,3):
                            self.targetModeProbabilities[row, column] += 1
                if self.__checkLeft(row, col, shipLength) == 1:
                    for column in range(col - shipLength + 1, col):
                         if self.hitMiss[row, column] not in (0,2,3):
                             self.targetModeProbabilities[row, column] += 1
                if self.__checkUp(row, col, shipLength) == 1:
                    for rows in range(row - shipLength + 1, row):
                         if self.hitMiss[rows, col] not in (0,2,3):
                             self.targetModeProbabilities[rows, col] += 1
                if self.__checkDown(row, col, shipLength) == 1:
                    for rows in range(row + 1, row + shipLength):
                        if self.hitMiss[rows, col] not in (0,2,3):
                            self.targetModeProbabilities[rows, col] += 1
                self.__check_mid_horizontal(row, col, shipLength, True)
                self.__check_mid_vertical(row, col, shipLength, True)

    def __checkRight(self, start_row_index, start_col_index,ship_length):
        if start_col_index == 9 or start_col_index + ship_length - 1 > 9:
            return 0
        sliced_row = self.hitMiss[start_row_index, start_col_index + 1:start_col_index + ship_length]
        zeroArray  = np.where(sliced_row==0)[0].size
        threeArray  = np.where(sliced_row==3)[0].size
        if zeroArray == 0 and threeArray == 0:
            return 1
        else:
            return 0
    def __checkLeft(self, start_row_index, start_col_index,ship_length):
        if start_col_index == 0 or start_col_index - ship_length + 1 < 0:
            return 0
        sliced_row = self.hitMiss[start_row_index,start_col_index - ship_length + 1 :start_col_index]
        zeroArray  = np.where(sliced_row==0)[0].size
        threeArray  = np.where(sliced_row==3)[0].size
        if zeroArray == 0 and threeArray == 0:
            return 1
        else:
            return 0
    def __checkUp(self, start_row_index, start_col_index,ship_length):
        if start_row_index == 0 or start_row_index - ship_length + 1 < 0:
            return 0
        sliced_row = self.hitMiss[start_row_index - ship_length + 1 :start_row_index,start_col_index]
        zeroArray  = np.where(sliced_row==0)[0].size
        threeArray  = np.where(sliced_row==3)[0].size
        if zeroArray == 0 and threeArray == 0:
            return 1
        else:
            return 0
    def __checkDown(self, start_row_index, start_col_index,ship_length):
        if start_row_index == 9 or start_row_index + ship_length - 1 > 9:
            return 0
        sliced_row = self.hitMiss[start_row_index + 1:start_row_index + ship_length:,start_col_index]
        zeroArray  = np.where(sliced_row==0)[0].size
        threeArray  = np.where(sliced_row==3)[0].size
        if zeroArray == 0 and threeArray == 0:
            return 1
        else:
            return 0
        
    def __check_mid_horizontal(self,row,col,ship_length,mode_flag):
        count = 0
        if ship_length == 3:
            if col+1<self.hitMiss.shape[1] and col-1>=0:
                if self.hitMiss[row, col+1] not in (0,3) and self.hitMiss[row,col-1] not in (0,3):
                    count+=1
                    if mode_flag == True:
                        if self.hitMiss[row, col+1] == 1:
                            self.targetModeProbabilities[row, col+1]+=1
                        if self.hitMiss[row, col-1] == 1:
                            self.targetModeProbabilities[row, col-1]+=1
        elif ship_length == 4:
            if col+2<self.hitMiss.shape[1] and col-1>=0:
                if self.hitMiss[row, col+1] not in (0,3) and self.hitMiss[row, col+2] not in (0,3) and self.hitMiss[row,col-1] not in (0,3):
                    count+=1
                    if mode_flag == True:
                        if self.hitMiss[row, col+1] == 1:
                            self.targetModeProbabilities[row, col+1]+=1
                        if self.hitMiss[row, col+2] == 1:
                            self.targetModeProbabilities[row, col+2]+=1
                        if self.hitMiss[row, col-1] == 1:
                            self.targetModeProbabilities[row, col-1]+=1
            if col+1<self.hitMiss.shape[1] and col-2>=0:
                if self.hitMiss[row, col+1] not in (0,3) and self.hitMiss[row, col-2] not in (0,3) and self.hitMiss[row,col-1] not in (0,3):
                    count+=1
                    if mode_flag == True:
                        if self.hitMiss[row, col+1] == 1:
                            self.targetModeProbabilities[row, col+1]+=1
                        if self.hitMiss[row, col-2] == 1:
                            self.targetModeProbabilities[row, col-2]+=1
                        if self.hitMiss[row, col-1] == 1:
                            self.targetModeProbabilities[row, col-1]+=1
        elif ship_length == 5:
            if col+3<self.hitMiss.shape[1] and col-1>=0:
                if self.hitMiss[row,col+1] not in (0,3) and self.hitMiss[row,col+2] not in (0,3) and self.hitMiss[row,col+3] not in (0,3) and self.hitMiss[row,col-1] not in (0,3):
                    count+=1
                    if mode_flag == True:
                        if self.hitMiss[row, col+1] == 1:
                            self.targetModeProbabilities[row, col+1]+=1
                        if self.hitMiss[row, col+2] == 1:
                            self.targetModeProbabilities[row, col+2]+=1
                        if self.hitMiss[row, col+3] == 1:
                            self.targetModeProbabilities[row, col+3]+=1
                        if self.hitMiss[row, col-1] == 1:
                            self.targetModeProbabilities[row, col-1]+=1
            if col+1<self.hitMiss.shape[1] and col-3>=0:
                if self.hitMiss[row,col+1] not in (0,3) and self.hitMiss[row,col-1] not in (0,3) and self.hitMiss[row,col-2] not in (0,3) and self.hitMiss[row,col-3] not in (0,3):
                    count+=1
                    if mode_flag == True:
                        if self.hitMiss[row, col+1] == 1:
                            self.targetModeProbabilities[row, col+1]+=1
                        if self.hitMiss[row, col-2] == 1:
                            self.targetModeProbabilities[row, col-2]+=1
                        if self.hitMiss[row, col-3] == 1:
                            self.targetModeProbabilities[row, col-3]+=1
                        if self.hitMiss[row, col-1] == 1:
                            self.targetModeProbabilities[row, col-1]+=1
            if col+2<self.hitMiss.shape[1] and col-2>=0:
                if self.hitMiss[row,col+1] not in (0,3) and self.hitMiss[row,col+2] not in (0,3) and self.hitMiss[row,col-1] not in (0,3) and self.hitMiss[row,col-2] not in (0,3):
                    count+=1
                    if mode_flag == True:
                        if self.hitMiss[row, col+1] == 1:
                            self.targetModeProbabilities[row, col+1]+=1
                        if self.hitMiss[row, col+2] == 1:
                            self.targetModeProbabilities[row, col+2]+=1
                        if self.hitMiss[row, col-1] == 1:
                            self.targetModeProbabilities[row, col-1]+=1
                        if self.hitMiss[row, col-2] == 1:
                            self.targetModeProbabilities[row, col-2]+=1
        return count
    def __check_mid_vertical(self,row,col,ship_length, mode_flag):
        count = 0
        if ship_length == 3:
            if row+1<self.hitMiss.shape[0] and row-1>=0:
                if self.hitMiss[row+1, col] not in (0,3) and self.hitMiss[row-1,col] not in (0,3):
                    count+=1
                    if mode_flag == True:
                        if self.hitMiss[row+1, col] == 1:
                            self.targetModeProbabilities[row+1, col]+=1
                        if self.hitMiss[row-1, col] == 1:
                            self.targetModeProbabilities[row-1, col]+=1
        elif ship_length == 4:
            if row+2<self.hitMiss.shape[0] and row-1>=0:
                if self.hitMiss[row+1, col] not in (0,3) and self.hitMiss[row+2, col] not in (0,3) and self.hitMiss[row-1,col] not in (0,3):
                    count+=1
                    if mode_flag == True:
                         if self.hitMiss[row+1, col] == 1:
                             self.targetModeProbabilities[row+1, col]+=1
                         if self.hitMiss[row+2, col] == 1:
                             self.targetModeProbabilities[row+2, col]+=1
                         if self.hitMiss[row-1, col] == 1:
                             self.targetModeProbabilities[row-1, col]+=1
            if row+1<self.hitMiss.shape[0] and row-2>=0:
                if self.hitMiss[row+1, col] not in (0,3) and self.hitMiss[row-1, col] not in (0,3) and self.hitMiss[row-2,col] not in (0,3):
                    count+=1
                    if mode_flag == True:
                        if self.hitMiss[row+1, col] == 1:
                            self.targetModeProbabilities[row+1, col]+=1
                        if self.hitMiss[row-2, col] == 1:
                            self.targetModeProbabilities[row-2, col]+=1
                        if self.hitMiss[row-1, col] == 1:
                            self.targetModeProbabilities[row-1, col]+=1
        elif ship_length == 5:
            if row+3<self.hitMiss.shape[0] and row-1>=0:
                if self.hitMiss[row+1,col] not in (0,3) and self.hitMiss[row+2,col] not in (0,3) and self.hitMiss[row+3,col] not in (0,3) and self.hitMiss[row-1,col] not in (0,3):
                    count+=1
                    if mode_flag == True:
                        if self.hitMiss[row+1, col] == 1:
                            self.targetModeProbabilities[row+1, col]+=1
                        if self.hitMiss[row+2, col] == 1:
                            self.targetModeProbabilities[row+2, col]+=1
                        if self.hitMiss[row+3, col] == 1:
                            self.targetModeProbabilities[row+3, col]+=1
                        if self.hitMiss[row-1, col] == 1:
                            self.targetModeProbabilities[row-1, col]+=1
            if row+1<self.hitMiss.shape[0] and row-3>=0:
                if self.hitMiss[row+1,col] not in (0,3) and self.hitMiss[row-1,col] not in (0,3) and self.hitMiss[row-2,col] not in (0,3) and self.hitMiss[row-3,col] not in (0,3):
                    count+=1
                    if mode_flag == True:
                        if self.hitMiss[row+1, col] == 1:
                            self.targetModeProbabilities[row+1, col]+=1
                        if self.hitMiss[row-2, col] == 1:
                            self.targetModeProbabilities[row-2, col]+=1
                        if self.hitMiss[row-3, col] == 1:
                            self.targetModeProbabilities[row-3, col]+=1
                        if self.hitMiss[row-1, col] == 1:
                            self.targetModeProbabilities[row-1, col]+=1
            if row+2<self.hitMiss.shape[0] and row-2>=0:
                if self.hitMiss[row+1,col] not in (0,3) and self.hitMiss[row+2,col] not in (0,3) and self.hitMiss[row-1,col] not in (0,3) and self.hitMiss[row-2,col] not in (0,3):
                    count+=1
                    if mode_flag == True:
                        if self.hitMiss[row+1, col] == 1:
                            self.targetModeProbabilities[row+1, col]+=1
                        if self.hitMiss[row+2, col] == 1:
                            self.targetModeProbabilities[row+2, col]+=1
                        if self.hitMiss[row-1, col] == 1:
                            self.targetModeProbabilities[row-1, col]+=1
                        if self.hitMiss[row-2, col] == 1:
                            self.targetModeProbabilities[row-2, col]+=1

        return count
