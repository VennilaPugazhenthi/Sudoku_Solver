############################################################
# CMPSC442: Homework 7
############################################################

student_name = "Vennila Pugazhenthi"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import copy
import time

############################################################
# Section 1: Sudoku
############################################################

def sudoku_cells():
    l=[]
    for i in range(0,9):
        for j in range(0,9):
            l.append((i,j))
    return l


def sudoku_arcs():
    l=sudoku_cells()
    arc=[]
    for ele1 in l:
        for ele2 in l:
            if(ele1!=ele2):
                if(ele1[0]==ele2[0])or (ele1[1]==ele2[1])or(ele1[0]//3==ele2[0]//3 and ele1[1]//3==ele2[1]//3):
                    element=(ele1,ele2)
                    arc.append(element)
    return arc


def read_board(path):
    file= open(path,'r')
    row=0
    dict={}
    #possibilities=set(["1","2","3","4","5","6","7","8","9"])
    for line in file:
        possibilities = set([1,2,3,4,5,6,7,8,9])
        col=0
        for i in range(0,9):
             if(line[i]=="*"):
                dict[(row,col)]=possibilities.copy()
             else:
                 new=set([int(line[i])])
                 dict[(row,col)]=(new)
             col+=1

        row+=1
    return dict

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board=board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        num=self.board[cell2]
        #print("NUM:")
        #print(num)

        if len(num)==1:
            if next(iter(num)) in self.board[cell1]:

                self.board[cell1]-=num
                return True
        return False

    def neighbors(self,cell):
        result=set()
        for i in range(0,9):
            result.add((i,cell[1]))
            result.add((cell[0],i))
        for j in range(0,3):
            for k in range(0,3):
                result.add((cell[0]//3*3+j,cell[1]//3*3+k))
        result.remove(cell)
        return result

    def infer_ac3(self):
        q=set(self.ARCS.copy())
        while q:
            cell1, cell2 = q.pop()
            if len(self.board[cell1])==0:
                return False
            #if cell1 == (0,3):
                #print((cell1,cell2), self.board[cell1],self.board[cell2])
            res=self.remove_inconsistent_values(cell1,cell2)
            if res==True:
                for n in self.neighbors(cell1):
                    q.add((n,cell1))
        return True
    def unique_in_cell(self,cell,value):
        for j in range(0, 3):
            for k in range(0, 3):
                test = (cell[0] // 3 * 3 + j, cell[1] // 3 * 3 + k)
                if test != cell:
                    if value in self.board[test]:
                        return False
        return True
    def unique_in_rows(self,cell,value):
        for i in range(0, 9):
            test_r = (i, cell[1])
            if test_r!=cell:
                if value in self.board[test_r]:

                    return False
        return True
    def unique_in_cols(self,cell,value):
        for i in range(0, 9):
            test_c = (cell[0], i)
            if test_c != cell:
                #if test_c==(4,7):
                    #print("HERE:")
                    #print(self.board[test_c])
                if value in self.board[test_c]:
                    return False
        return True

    def unique(self,cell,value):
        return self.unique_in_cell(cell,value) or self.unique_in_rows(cell,value) or self.unique_in_cols(cell,value)
               #return True


    def infer_improved(self):
        new_assignment=True
        while new_assignment:
            new_assignment=False
            self.infer_ac3()
            #self.print()
            for cell in self.CELLS:
                if len(self.board[cell])==1:
                    continue
                for value in self.board[cell]:
                    res=self.unique(cell,value)
                    if res==True:
                        self.board[cell]=set([value])
                        new_assignment=True


    def infer_with_guessing(self):
        backtracking = copy.deepcopy(self.board)
        self.infer_improved()

        for cell in self.CELLS:
            if len(self.board[cell])==1:
                continue
            for value in self.board[cell]:
                self.board[cell]=set([value])
                self.infer_with_guessing()
                if self.is_solved():
                    return True
                else:
                    self.board=backtracking
    def is_solved(self):
        ret=True
        for i in range(0,9):
            for j in range(0,9):
                if len(self.board[(i,j)])!=1:
                    ret=False
        return ret

    def print(self):
        for i in range(0,9):
            for j in range(0,9):
                print(self.board[(i,j)],end=" ")
            print(" ")

# b=read_board("hw7-medium3.txt")
# print(Sudoku(b).get_values((0,0))) #TODO: the output doesn't match the answer
# print(sudoku_cells())
# print(((0,0),(0,8)) in sudoku_arcs())
# print(((0,0),(8,0)) in sudoku_arcs())
# print(((0,8),(0,0)) in sudoku_arcs())
# print(((0,0),(2,1)) in sudoku_arcs())
# print(((2,2),(0,0)) in sudoku_arcs())
# print(((2,3),(0,0)) in sudoku_arcs())
# sudoku=Sudoku(read_board("hw7-medium4.txt"))
#print(sudoku.get_values((0,3)))
# for col in [0,1,4]:
#     removed=sudoku.remove_inconsistent_values((0,3),(0,col))
#     print(removed,sudoku.get_values((0,3)))
#print(sudoku.ARCS)
#print("BEFORE:")
#sudoku.print()
#print(len(sudoku.ARCS))
#print("Neighbors:")
#print(sudoku.neighbors((5,5)))
# t1=time.time()
#(sudoku.infer_with_guessing())
#print(len(sudoku.ARCS))
#print(len(sudoku.CELLS))
# sudoku.infer_improved()
# print("AFTER:")
# sudoku.print()
# t2=time.time()
# print(t2-t1)
############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
It took me 15 hrs to complete this homework.
"""

feedback_question_2 = """
I found infer_improved() and infer_with_guessing() most challenging because I stumbled in understanding the
question.
"""

feedback_question_3 = """
I liked the problems 1-5 because they were easy to understand. 
I would like the complex questions to be rewritten in simpler words to help students understand it better.
"""
