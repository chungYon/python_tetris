import random
import tetris_rotation

class Tetromino:
    block_list = tetris_rotation.MakeBlockList()

    def __init__(self, block_type):
        self.block_type = block_type
        self.current_block = Tetromino.block_list[self.block_type][self.rotation]
        self.rotation = 0
    
    def RotateClockWise(self):
        self.rotation = (self.rotation + 1) % 4
    
    def RotateCounterClockWise(self):
        self.rotation -= 1
        if self.rotation < 0:
            sel.rotation = 3
    
    def GetCurrentBlock(self):
        return current_block

    
    

# 블록 타입 상수 정의
I_BLOCK = 0
L_BLOCK = 1
J_BLOCK = 2
T_BLOCK = 3
S_BLOCK = 4
Z_BLOCK = 5
O_BLOCK = 6

def GenerateRandomBlock():
    random_block_type = random.choice([I_BLOCK, L_BLOCK, J_BLOCK, T_BLOCK, S_BLOCK, Z_BLOCK, O_BLOCK])
    return Tetromino(random_block_type)

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

def GenerateRandomBlocks():
    # 세트에 사용할 블록 타입들을 리스트로 정의
    block_type_set = [I_BLOCK, L_BLOCK, J_BLOCK, T_BLOCK, S_BLOCK, Z_BLOCK, O_BLOCK]
    selected_block_types = []

    # 한 세트에서 7개의 블록이 모두 다른 블록 타입으로 뽑힐 때까지 반복
    while block_type_set:
        random_block = GenerateRandomBlock()
        
        while(random_block.block_type not in block_type_set):
            random_block = GenerateRandomBlock()
        
        random_block_type = random_block.block_type
        
        block_type_set.remove(random_block_type)
        selected_block_types.append(random_block_type)


    return selected_block_types