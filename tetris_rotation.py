def MakeBlockList():
    '''
    블록 회전리스트 저장 설명
    4차원 리스트로 제작되었음

    ex)block[i][j][l][k]
    i: 블록타입, j : 회전모양, l : 회전모양의 y좌표, k 회전모양의 x좌표
    '''


    data = '''
0000001000000100
1111001000000100
0000001011110100
0000001000000100

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

0110010001101000
1100011011001100
0000001000000100
0000000000000000

1100001011001000
0110011001101100
0000010000000100
0000000000000000

0110011001100110
0110011001100110
0000000000000000
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

    for i in range(7):
        block_list.append([])
        for j in range(4):
            block_list[i].append([])
            for l in range(4):
                block_list[i][j].append([])
                block_list[i][j][l].extend(matrix_list[i][l][j * 4 : (j + 1) * 4])

    return block_list