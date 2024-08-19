
class Board():
    def __init__(self,rows,cols):
        
        self.rows = rows
        self.cols = cols
        
        self.board = []
        self.new_board()
    
        self.bground_grid = []
        self.set_bground_grid()
        
    def set_bground_grid(self): #바둑판 모양 그리기 데이타
        for y in range(self.rows):
            col = []
            for x in range(self.cols):
                if x % 2 == y%2:
                    col.append((35,  35,  35))
                else:
                    col.append(None)
            self.bground_grid.append(col)
            
    def new_board(self):        
        self.board = []
        for y in range(self.rows):
            col = []
            for x in range(self.cols):
                col.append(None)
            self.board.append(col)
            