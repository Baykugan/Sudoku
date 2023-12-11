import random
from tqdm.auto import tqdm

class Board():
    def __init__(self):
        self.index = [[Tile(0, [i, j]) for j in range(9)] for i in range(9)]
        self.checkIndex = [[Tile(0, [i, j]) for j in range(9)] for i in range(9)]
        self.solvedIndex = [[Tile(0, [i, j]) for j in range(9)] for i in range(9)]


    def __repr__(self):
        ret = ''
        ret += f'    ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗\n'
        ret += '    '
        for i in range(9):
            if (i) % 3 == 0:
                ret += f'║'
            else:
                ret += f'│'
            ret += f' \033[36;1m{i + 1}\033[0m '
        ret += '║\n'
        for i in range(9):
            if i == 0: 
                ret += f'╔═══╬═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣\n'
            elif (i) % 3 == 0:
                ret += f'╠═══╬═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣\n'
            else:
                ret += f'╟───╫───┼───┼───╫───┼───┼───╫───┼───┼───╢\n'

            ret += f'║ \033[36;1m{i + 1}\033[0m '
            ret
            for j in range(9):
                if (j) % 3 == 0:
                    ret += f'║'
                else:
                    ret += f'│'
                if self.index[i][j].isLocked:
                    ret += f' \033[36m{self.index[i][j]}\033[0m '
                elif self.index[i][j].num == 0:
                    ret += '   '
                else:
                    ret += f' {self.index[i][j]} '
            ret += f'║\n'
        ret += f'╚═══╩═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝'

        return ret


    def load(self, save):
        arr = ''
        lockArr = ''
        try:
            load = open(f'sudokuSaves/{save}.txt', 'r')
            arr, lockArr = load

            arr = [int(i) for i in arr if i.isdigit()]
            lockArr = [int(i) for i in lockArr if i.isdigit()]

            if len(arr) == 81 and len(lockArr) == 81:
                for i in range(81):
                    tile = self.index[i // 9][i % 9]
                    tile.num = arr[i]
                    tile.isLocked = False
                    if lockArr[i] == 1:
                        tile.isLocked = True
                print(self)
            else:
                print(f'{save}.txt have been corrupted, and can no longer be opened, Please choose another save: ')
        except:
            print(f'That save does not exist, a new game will be made.')
            load = open(f'sudokuSaves/newGame.txt', 'r')
       

    def save(self, save):
        save = open(f'sudokuSaves/{save}.txt', 'w')
        for row in range(9):
            for col in range(9):
                save.write(f'{self.index[row][col].num}')
        save.write(f'\n')

        for i, row in enumerate(self.index):
            for j, cell in enumerate(row):
                if cell.isLocked:
                    save.write(f'1')
                else:
                    save.write(f'0')
        


    def isSolved(self):
        for i in range(9):
            for j in range(9):
                if self.index[i][j].num == 0:
                    return False
        return True
    

    def doMove(self, iterations):
        count = 0
        for i in range(iterations):
            didMove = self.solve(self.index, 1)

            if didMove:
                count += 1
            else:
                print(f'There is no tile with only one possibility left.')
                break
            
        print(f'Did {count} moves.')
        print(board)
        return count

    def makeBoard(self):
        
        base  = 3
        side  = base * base

        # pattern for a baseline valid solution
        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        # randomize rows, columns and numbers (of valid base pattern)
        def shuffle(s): 
            return random.sample(s, len(s)) 

        rBase = range(base) 
        rows  = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)] 
        cols  = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums  = shuffle(range(1, base * base + 1))

        # produce board using randomized baseline pattern
        newBoard = [[nums[pattern(r, c)] for c in cols] for r in rows]

        self.index = [[Tile(0, [i, j]) for j in range(9)] for i in range(9)]

        for row in range(9):
            for col in range(9):
                self.index[row][col].num = newBoard[row][col]
        

    def newGame(self, iterations):
        self.makeBoard()
        removed = 0
        failed = 0
        tryList = [(i, j) for i in range(9) for j in range(9)]


        
        for i in tqdm(range(iterations)):
            ind = random.randint(0, len(tryList)-1)
            row, col = tryList[ind]
            tryList.pop(ind)

            
            for i in range(9):
                for j in range(9):
                    self.checkIndex[i][j].num = self.index[i][j].num
            self.checkIndex[row][col].num = 0
            
            if self.isSolvable():
                self.index[row][col].num = 0
                removed += 1
            else:
                failed += 1
            

        for i in range(81):
            if self.index[i // 9][i % 9].num != 0:
                self.index[i // 9][i % 9].isLocked = True
                

        print(f'{removed} nummbers were removed')
        print(f'The function made an unsolvable sudoku {failed} times')
        print(self)

    
    def isSolvable(self):
        self.solve(self.checkIndex, 81)
        
        for i in range(9):
            for j in range(9):
                if self.checkIndex[i][j].num == 0:
                    return False
        return True

    
    def solve(self, boardVersion, iterations):
        for i in range(iterations):
            doneMove = False
            for row in boardVersion:
                for pos in row:
                    if pos.num == 0:
                        pos.getPossible(boardVersion)

            for row in boardVersion:
                for pos in row:
                    if pos.num == 0:
                        pos.haveToBe(boardVersion)

            for i in range(81):
                tile = boardVersion[i // 9][i % 9]
                if not tile.isLocked and tile.num == 0:

                    if len(tile.possMoves) == 1:
                        tile.num = tile.possMoves[0]
                        doneMove = True

                    elif len(tile.haveTo) == 1:
                        tile.num = tile.haveTo[0] 
                        doneMove = True
                if doneMove == True:
                    break
            if doneMove == False:
                return False
        return True


class Tile():
    def __init__(self, num, index):
        self.num = num
        self.index = index
        self.isLocked = False
        self.possMoves = []
        self.haveTo = []


    def __repr__(self):
        return f'{self.num}'
    

    def isLegal (self, num):
        legal = True
        checkRow, checkCol, checkSqr = self.getIllegal(board.index)
        
        if num in checkRow:
            print(f'That number already exists in this row.')
            legal = False

        if num in checkCol:
            print(f'That number already exists in this column.')
            legal = False

        if num in checkSqr:
            print(f'That number already exists in this square.')
            legal = False

        if legal == False:
            return False
        return self.index, num
    

    def switchNum(self, num):
        if not self.isLocked:
            self.num = num
        else:
            print(f'That position is locked.')


    def getIllegal(self, boardVersion):
        row, col = self.index
        checkRow = []
        checkCol = []
        checkSqr = []
        
        for i in range(9):
            if self != boardVersion[row][i]:
                checkRow.append(boardVersion[row][i].num)
            if self != boardVersion[i][col]:
                checkCol.append(boardVersion[i][col].num)

        for subRow in range(1 , 8 , 3):
            for subCol in range(1 , 8 , 3):
                subSqr = [[subRow + i, subCol + j] for j in range(-1, 2) for i in range(-1, 2)]
                if not self.index in subSqr:
                    continue

                for i in range(9):
                    if self != boardVersion[subSqr[i][0]][subSqr[i][1]]:
                        checkSqr.append(boardVersion[subSqr[i][0]][subSqr[i][1]].num)
        return checkRow, checkCol, checkSqr
    

    def getPossible(self, boardVersion):
        self.possMoves = []
        allNums = []
        checkList = []
        checkRow, checkCol, checkSqr = self.getIllegal(boardVersion)
        allNums = [int(num) for ind in (checkRow, checkCol, checkSqr) for num in ind]
        [checkList.append(num) for num in allNums if num not in checkList]

        for i in range(1,10):
            if i not in checkList:
                self.possMoves.append(i)

        return self.possMoves
    

    def haveToBe(self, boardVersion):
        self.haveTo = []
        checkRow = []
        checkCol = []
        checkSqr = []
        row, col = self.index

        for i in range(9):
            if boardVersion[row][i].num == 0:
                checkRow.append(boardVersion[row][i].possMoves)
            if boardVersion[i][col].num == 0:
                checkCol.append(boardVersion[i][col].possMoves)

        for subRow in range(1 , 8 , 3):
            for subCol in range(1 , 8 , 3):
                subSqr = []
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        subSqr.append([subRow + i, subCol + j])
                    
                if self.index in subSqr:
                    for i in range(9):
                        if boardVersion[subSqr[i][0]][subSqr[i][1]].num == 0:
                            checkSqr.append(boardVersion[subSqr[i][0]][subSqr[i][1]].possMoves)

        try:
            row = [num for ind in checkRow for num in ind]
            col = [num for ind in checkCol for num in ind]
            sqr = [num for ind in checkSqr for num in ind]
            check = [row, col, sqr]

            for ind in check:
                for i in set(ind):
                    count = ind.count(i)

                    if count == 1 and i in self.possMoves:
                        self.haveTo.append(i)
        except:
            pass


def isLegal(nextMove):
    if len(nextMove) >= 3 and nextMove[:3].isdigit():
        row = int(nextMove[0]) - 1
        col = int(nextMove[1]) - 1
        num = int(nextMove[2])
        if num == 0:
            return [row, col], num
        elif board.index[row][col].isLegal(num):
            return [row, col], num
        else:
            return False
    else:
        return False
    
def clearBoard():
    for i in range(9):
        for j in range(9):
            if not board.index[i][j].isLocked:
                board.index[i][j].num = 0
    print(f'The board have been cleared.')
    print(board)


def checkSolvablility():
    for i in range(9):
        for j in range(9):
            board.checkIndex[i][j].num = board.index[i][j].num
    if board.isSolvable():
        print(f'The board is solvable.')
        return
    else:
        print(f'The board is unsaolvable.')




def main():
    global board
    board = Board()
    board.newGame(81)
    exit = False
    usedHints = 0

    while not board.isSolved():
        nextMove = input(('What move do you want to do? Write this like abc,\n'
                          'where a is the row, b is the column and c is the number.\n'
                          'Alternatively, write load or save: '))

        while isLegal(nextMove) == False:
            legalInput = False
            if nextMove != '':

                if nextMove[0] == 's':
                    try:
                        save = nextMove.split(' ', 1)[1]
                    except:
                        save = input(f'What would you like to save the game as? ')
                        if save == '':
                            save = 'tempSave'
                    board.save(save)
                    print(f'The board have been saved as \'{save}.txt\'.')
                    legalInput = True


                elif nextMove[0] == 'l':
                    try:
                        save = nextMove.split(' ', 1)[1]
                    except:
                        save = input(f'Which save would you like to load? ')
                    if save != '':
                        board.load(save)
                        print(f'The file \'{save}.txt\' have been loaded.')
                        legalInput = True


                elif nextMove[0] == 'h':
                    try:
                        hints = nextMove.split(' ', 1)[1]
                        hints = int(hints)
                        if hints <= 0:
                            hints = 1

                    except:
                        hints = 1

                    usedHints += board.doMove(hints)

                    if board.isSolved():
                        exit = True
                    legalInput = True
                    

                elif nextMove[0] == 'b':
                    exit = True
                

                elif nextMove[0] == 'c':
                    clearBoard()
                    legalInput = True


                elif nextMove[0] == 'f':
                    checkSolvablility()
                    legalInput = True


                elif nextMove[0] == 'n':
                    try:
                        iterations = nextMove.split(' ', 1)[1]
                        iterations = int(iterations)
                        if iterations > 81:
                            iterations = 81
                        elif iterations < 20:
                            iterations = 20
                    except:
                        iterations = 81

                    board.newGame(iterations)
                    usedHints = 0
                    legalInput = True

                if exit:
                    break

            if legalInput:
                nextMove = input(f'What do you want to do? ')
            else:
                nextMove = input(f'Please write a legal input: ')

        if exit:
            break

        index, num = isLegal(nextMove)
        

        board.index[index[0]][index[1]].switchNum(num)
        print(board)

    if board.isSolved():
        print(f'Congratulations on beating the sudoku.')
        if usedHints >= 1:
            filledTiles = 0

            for i in range(81):
                if not board.index[i // 9][i % 9].isLocked:
                    filledTiles += 1
                    selfSolved = filledTiles - usedHints
            print(f'You used {usedHints} hints.')
            print(f'You filled {selfSolved} tiles yourself')
    else:
        print(f'You have exited the game.')


main()