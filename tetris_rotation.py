def MakeBlockList():
    '''
    블록 회전리스트 저장 설명
    4차원 리스트로 제작되었음

    ex)block[i][j][l][k]
    i: 블록타입, j : 회전모양, l : 회전모양의 y좌표, k 회전모양의 x좌표
    '''
    
    data = '''

00000000000000000100
00000001000000000100
01111001001111000100
00000001000000000100
00000001000000000000

0010010000001100
1110010011100100
0000011010000100
0000000000000000

1000011000000100
1110010011100100
0000010000101100
0000000000000000

0100010000000100
1110011011101100
0000010001000100
0000000000000000

0110010000001000
1100011001101100
0000001011000100
0000000000000000

1100001000000100
0110011011001100
0000010001101000
0000000000000000

0110000000001100
0110011011001100
0000011011000000
0000000000000000

'''


    block_list = []
    matrix_rows = data.strip().split('\n\n')
    matrix_list = []

    for matrix_data in matrix_rows:
        matrix = []
        lines = matrix_data.strip().split('\n')
        
        for line in lines:
            if line:
                row = [int(cell) for cell in line]
                matrix.append(row)
        
        matrix_list.append(matrix)

    block_list.append([])
    for j in range(5):
        block_list[0].append([])
        for l in range(5):
            block_list[0][j].append([])
            block_list[0][j][l].extend(matrix_list[0][l][j * 5 : (j + 1) * 5])

    for i in range(1, 7):
        block_list.append([])
        for j in range(4):
            block_list[i].append([])
            for l in range(4):
                block_list[i][j].append([])
                block_list[i][j][l].extend(matrix_list[i][l][j * 4 : (j + 1) * 4])

    return block_list