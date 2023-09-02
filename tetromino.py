import random
import tetris_rotation

# 블록 타입 상수 정의
I_BLOCK = 0
L_BLOCK = 1
J_BLOCK = 2
T_BLOCK = 3
S_BLOCK = 4
Z_BLOCK = 5
O_BLOCK = 6

ROTATION_NUM = 4

# 블록 타입과 색상 매핑
block_color_mapping = {
    I_BLOCK: "cyan",
    L_BLOCK: "orange",
    J_BLOCK: "blue",
    T_BLOCK: "purple",
    S_BLOCK: "green",
    Z_BLOCK: "red",
    O_BLOCK: "yellow",
}

class Tetromino:
    block_list = tetris_rotation.MakeBlockList()

    block_offset_LJZST = [
        [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],   # 0 state
        [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],  # R state
        [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],   # 2 state
        [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],  # L state
        ]

    block_offset_I = [
        [(0, 0), (-1, 0), (2, 0), (-1, 0), (2, 0)],
        [(-1, 0), (0, 0), (0, 0), (0, -1), (0, 2)],
        [(-1, -1), (1, -1), (-2, -1), (1, 0), (-2, 0)],
        [(0, -1), (0, -1), (0, -1), (0, 1), (0, -2)],
        ]

    block_offset_O = [
        [(0, 0)],
        [(0, 1)],
        [(-1, 1)],
        [(-1, 0)],
        ]

    block_spawn_x = [2, 3, 3, 3, 3, 3, 3]

    def __init__(self, block_type):

        self.block_type = block_type
        self.rotation = 0
    
    def Rotate(self, clockwise=True):

        self.rotation = (self.rotation + 1) % ROTATION_NUM
    
    def RotatePeek(self, clockwise=True):

        rotation_next = 0

        if clockwise:

            rotation_next = (self.rotation + 1) % ROTATION_NUM

        else:

            rotation_next = self.rotation - 1

            if rotation_next < 0:

                rotation_next = ROTATION_NUM - 1

        return Tetromino.block_list[self.block_type][rotation_next]  

    def MakeEndOffset(self, clockwise=True):

        rotation_next = 0

        if clockwise:

            rotation_next = (self.rotation + 1) % ROTATION_NUM

        else:

            rotation_next = self.rotation - 1

            if rotation_next < 0:

                rotation_next = ROTATION_NUM - 1

        end_offset_list = []

        pos_list_initial = 0
        pos_list_final = 0

        if self.block_type == I_BLOCK:

            pos_list_initial = Tetromino.block_offset_I[self.rotation]
            pos_list_final = Tetromino.block_offset_I[rotation_next]
        
        elif self.block_type == O_BLOCK:

            pos_list_initial = Tetromino.block_offset_O[self.rotation]
            pos_list_final = Tetromino.block_offset_O[rotation_next]
        
        else:

            pos_list_initial = Tetromino.block_offset_LJZST[self.rotation]
            pos_list_final = Tetromino.block_offset_LJZST[rotation_next]

        for i in range(len(pos_list_initial)):

            end_offset = SubtractPos(pos_list_initial[i], pos_list_final[i])
            end_offset_list.append(end_offset)
        
        return end_offset_list
    
    def GetCurrentBlock(self):

        return Tetromino.block_list[self.block_type][self.rotation]   
    
    def GetBlockSpawnX(self):

        return Tetromino.block_spawn_x[self.block_type]

    def GetBlockType(self):

        return self.block_type

    def GetRotationState(self):

        return self.rotation

def SubtractPos(pos1, pos2):
    return (pos1[0] - pos2[0], pos1[1] - pos2[1],)

def GenerateRandomBlock():

    random_block_type = random.choice([I_BLOCK, L_BLOCK, J_BLOCK, T_BLOCK, S_BLOCK, Z_BLOCK, O_BLOCK])
    
    return Tetromino(random_block_type)

def GenerateRandomBlocks():
    # 세트에 사용할 블록 타입들을 리스트로 정의
    block_type_set = [I_BLOCK, L_BLOCK, J_BLOCK, T_BLOCK, S_BLOCK, Z_BLOCK, O_BLOCK]
    selected_block = []

    # 한 세트에서 7개의 블록이 모두 다른 블록 타입으로 뽑힐 때까지 반복
    while block_type_set:

        random_block = GenerateRandomBlock()
        
        while(random_block.block_type not in block_type_set):

            random_block = GenerateRandomBlock()
        
        random_block_type = random_block.block_type
        
        block_type_set.remove(random_block_type)
        selected_block.append(random_block)

    return selected_block