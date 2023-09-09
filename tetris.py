

#-*- coding: utf-8 -*-

import curses
from curses import wrapper
import time
import keyboard
import tetromino
import windows

class Tetris:

    def __init__(self):
        

        self.score = 0
        self.block = 0
        self.block_hold = False
        self.block_x = 0
        self.block_y = 0
        self.pre_block_x = 0
        self.pre_block_y = 0
        self.drop_speed = 0.7
        self.st_speed = 0.7
        self.das = 0.131
        self.das_flag = False
        self.arr = 0.015
        self.arr_flag = False
        self.hold_flag = False
        self.rotate_flag = False
        self.space_flag = False
        self.sdf = 0.02
        self.stop = 2
        self.ceiling = 4
        self.map_height = 24
        self.map_width = 10
        self.game_box_x = 17
        self.game_box_y = 1
        self.hold_box_x = 5
        self.hold_box_y = 5
        self.block_list_box_x = 42
        self.block_list_box_y = 5

        self.map = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        
        '''
        블록타입:
        I_BLOCK = 0
        L_BLOCK = 1
        J_BLOCK = 2
        T_BLOCK = 3
        S_BLOCK = 4
        Z_BLOCK = 5
        O_BLOCK = 6

        tetromino.py에 변수로 선언되어 있음
        쓰고싶으면 tetromino.I_BlOCK 로 쓰셈

        변수 설명

        self.score : 점수 저장 (나중에 콤보기능 구현할때 제대로 사용)
        self.block_type : 현재 블록의 타입 저장
        self.block_x : 현재 블록 x좌표를 저장
        self.block_y : 현재 블록 y좌표를 저장
        self.drop_speed : 블록이 몇초마다 떨어지게 할건지 저장
        self.st_speed : 기본적으로 떨어지는 시간
        self.das : 좌우이동에 관한 시간
        self.das_flag : 좌우이동에 관한 플래그
        self.arr : 좌우이동에 관한 시간
        self.arr_flag : 좌우이동에 관한 플래그
        self.sdf : 아래키 누를때 떨어지는 시간
        self.stop  : 밑바닥에서 블럭을 굳히는 시간
        self.map_height : 맵의 세로길이
        self.map_width : 맵의 가로길이
        self.game_box_x : 화면상 게임 맵의 맨 왼쪽위 좌표
        self.game_box_y  : 화면상 게임 맵의 맨 왼쪽위 좌표
        self.block_list_box_x : 화면상 블럭 미리보기 맵의 맨 왼쪽위 좌표
        self.block_list_box_y  : 화면상 블럭 미리보기 맵의 맨 왼쪽위 좌표
        self.block : 현재 블록의 tetromino객체
        self.block_queue : 랜덤으로 생성한 블록 객체들을 저장하는 리스트

        '''

    def Main(self, stdscr):
        '''시작화면, 설정화면, 게임화면을 담당하는 메소드'''
        curses.curs_set(0) # 커서 안보이게 함

        start_win = curses.newwin(30, 120, 0, 0) # 새 창 만들기
        start_arrow = windows.PrintStartMap(start_win) # 화살표 위치 받아오기

        if start_arrow: # 에 화살표가 있다면
            self.das, self.arr, self.sdf = windows.PrintSettingMap(stdscr) #세팅 화면 띄우기
        
        self.Game(stdscr) # 게임 시작
        
    def Game(self, stdscr):
        '''게임을 담당하는 메소드'''
        
        self.InitTimer() # 타이머 초기화
        stdscr.erase()

        self.block_queue = tetromino.GenerateRandomBlocks() # 블럭 7개 채우기
        self.block = self.block_queue.pop(0) # 하나 뽑기
        self.InitBlockPos()

        while True:

            if self.CheckGameOver():
                break

            if keyboard.is_pressed('esc'):
                break

            self.down_end_timer = time.time() # 드랍 타이머 세기
            self.drop_speed = self.st_speed # 기본 드랍 속도

            if keyboard.is_pressed('c'):

                if not self.hold_flag:

                    if self.block_hold:

                        self.block_hold, self.block = self.block, self.block_hold
                        
                    else:

                        self.block_hold = self.block
                        self.block = self.block_queue.pop(0)

                    self.block_hold.InitRotation()
                    self.hold_flag = True
                    self.InitBlockPos()
            
            if keyboard.is_pressed('space'):
                if not self.space_flag:

                    self.block_y = self.pre_block_y 
                    self.space_flag = True
                    self.stop_end_timer = self.stop_start_timer + self.stop + 1
                

            if keyboard.is_pressed('down'):

                self.drop_speed = self.sdf # 소프트 드랍 속도

            if keyboard.is_pressed('up'):

                if not self.rotate_flag:

                    pos = self.FindRotationPos()

                    if pos: # 회전이 가능한지 검사

                        self.block_x = pos[0]
                        self.block_y = pos[1]
                        self.block.Rotate()

                        self.rotate_flag = True

            
            if keyboard.is_pressed('z'):

                if not self.rotate_flag:

                    pos = self.FindRotationPos(False)

                    if pos: # 회전이 가능한지 검사
                        
                        self.block_x = pos[0]
                        self.block_y = pos[1]
                        self.block.Rotate(False)
                        self.rotate_flag = True
            
            if keyboard.is_pressed('right+left'):

                self.InitReleaseLR(0)
            else:

                if keyboard.is_pressed('left'):

                    self.DAS_ARR_MoveLeft() # 왼쪽 무빙 담당
                
                if keyboard.is_pressed('right'):

                    self.DAS_ARR_MoveRight() # 오른쪽 무빙 담당
            
            # 키를 땔시에 작동하는 함수들
            keyboard.on_release_key('up', self.InitRotation)
            keyboard.on_release_key('z', self.InitRotation)
            keyboard.on_release_key('space', self.InitSpace)
            keyboard.on_release_key('left', self.InitReleaseLR) 
            keyboard.on_release_key('right', self.InitReleaseLR)
            
            down_elapsed_time = self.GetElapsedDownTime() # 경과시간 구하기

            if not self.space_flag:

                if self.CheckBlockCollision(1, self.block.GetCurrentBlock(), self.block_x, self.block_y, False):  # 세로로 장애물이 있다면

                    self.stop_end_timer = time.time() # 굳히기 타이머 세기
                    self.InitDownTimer() # 드랍타이머 초기화

                else: # 세로로 장애물이 없다면

                    if down_elapsed_time > self.drop_speed:

                        self.InitDownTimer() # 드랍 타이머 초기화
                        self.DownBlock() # 블럭 내리기

                    self.InitStopTimer()

            stop_elapsed_time = self.GetElapsedStopTime() # 굳히기 타이머 경과시간 구하기

            if stop_elapsed_time > self.stop: # 굳히기 시간이 지났다면

                self.RecordBlock() # 그 자리에 1로 만들기
                self.InitDownTimer() # 드랍타이머 초기화
                self.block = self.block_queue.pop(0) # 하나 뽑기
                self.InitBlockPos()
                self.InitStopTimer()
                self.hold_flag = False

            self.score += self.CheckLines()
            self.CheckRefill()
            self.PrintMap(stdscr) # 맵 출력W

    def InitBlockPos(self):

        self.block_x, self.block_y = self.block.GetBlockSpawnPos() 

        if self.CheckBlockCollision(0, self.block.GetCurrentBlock(), self.block_x, self.block_y):
            self.block_y -= 1
        
    def InitSpace(self, evt):
        self.space_flag = False

    def DAS_ARR_MoveLeft(self): 

        if not self.CheckBlockCollision(-1, self.block.GetCurrentBlock(), self.block_x, self.block_y): # 블럭 왼쪽에 장애물이 없다면
            
            # 무빙하는거 만든거임 몇초 지나면 주르륵 움직이게 하는거 구현한거
            if not self.arr_flag: 

                if not self.das_flag:

                    self.InitDASTimer()
                    self.MoveBlock(-1)
                    self.das_flag = True
                
                elif self.das_flag:

                    self.DAS_end_timer = time.time()
                    DAS_elapsed_time = self.GetElapsedDASTime()

                    if  DAS_elapsed_time > self.das:

                        self.InitARRTimer()
                        self.MoveBlock(-1)
                        self.arr_flag = True
            else:

                self.ARR_end_timer = time.time()
                ARR_elapsed_time = self.GetElapsedARRTime()

                if  ARR_elapsed_time > self.arr:

                    self.ARR_start_timer = self.ARR_end_timer
                    self.MoveBlock(-1)

    def DAS_ARR_MoveRight(self):

        if not self.CheckBlockCollision(1, self.block.GetCurrentBlock(), self.block_x, self.block_y): # 블럭 오른쪽에 장애물이 없다면

            if not self.arr_flag:

                if not self.das_flag:

                    self.InitDASTimer()
                    self.MoveBlock(1)
                    self.das_flag = True
                
                elif self.das_flag:

                    self.DAS_end_timer = time.time()
                    DAS_elapsed_time = self.GetElapsedDASTime()

                    if  DAS_elapsed_time > self.das:

                        self.InitARRTimer()
                        self.MoveBlock(1)
                        self.arr_flag = True
            else:

                self.ARR_end_timer = time.time()
                ARR_elapsed_time = self.GetElapsedARRTime()

                if  ARR_elapsed_time > self.arr:

                    self.ARR_start_timer = self.ARR_end_timer
                    self.MoveBlock(1)

    def CheckLines(self):
        '''맵에 채워진 줄 검사하는 메소드'''
        line_count = 0
        
        for y in range(self.map_height):

            line_flag = True

            for x in range(self.map_width):

                if not self.map[y][x]:
                    line_flag = False

            if line_flag:
                del self.map[y]
                self.map.insert(0, [0 for _ in range(self.map_width)])
                y -= 1
                line_count += 1

        
        return line_count

    def FindRotationPos(self, clockwise=True):
        '''회전이 가능한지 확인하는 메소드'''
        block_next = self.block.RotatePeek(clockwise)
        end_offset_list = self.block.MakeEndOffset(clockwise)

        for eol in end_offset_list:

            offset_x = self.block_x + eol[0]
            offset_y = self.block_y + eol[1]

            if not self.CheckBlockCollision(0, block_next, offset_x, offset_y):

                return (offset_x, offset_y)

        return False

    
    def CheckBlockCollision(self, dir_, block, block_x, block_y, width=True):
        '''블럭간의 충돌과 맵을 총괄하는 메소드'''

        block_height = len(block)
        block_width = len(block[0])

        new_block_x = block_x
        new_block_y = block_y

        if width:
            new_block_x += dir_
        else:
            new_block_y += dir_

        for y in range(block_height):
            for x in range(block_width):
                if block[y][x]:
                    if new_block_x + x > self.map_width - 1:
                        return True
                    if new_block_y + y > self.map_height - 1:
                        return True
                    if new_block_y + y < 0:
                        return True
                    if new_block_x + x < 0:
                        return True
                    if self.map[new_block_y + y][new_block_x + x]:
                        return True
        return False

    def InitReleaseLR(self, evt):
        '''좌우 키보드 때면 초기화할 것들 정리해놓은 메소드'''
        self.das_flag = False
        self.arr_flag = False

        self.InitDASTimer()
        self.InitARRTimer()

    def InitRotation(self, evt):
        '''좌우 키보드 때면 초기화할 것들 정리해놓은 메소드'''
        self.rotate_flag = False

    def InitTimer(self):
        '''모든 타이머를 초기화하는 메소드'''
        self.InitDownTimer()
        self.InitDASTimer()
        self.InitARRTimer()
        self.InitStopTimer()

    def InitDownTimer(self):
        self.down_start_timer = time.time()
        self.down_end_timer = time.time()

    def InitStopTimer(self):
        self.stop_start_timer = time.time()
        self.stop_end_timer = time.time()

    def InitDASTimer(self):
        self.DAS_start_timer = time.time()
        self.DAS_end_timer = time.time()

    def InitARRTimer(self):
        self.ARR_start_timer = time.time()
        self.ARR_end_timer = time.time()

    # 경과시간 구하는 메소드 경과시간 : (끝 - 시작)
    def GetElapsedDownTime(self):
        return self.down_end_timer - self.down_start_timer
    
    def GetElapsedStopTime(self):
        return self.stop_end_timer - self.stop_start_timer

    def GetElapsedDASTime(self):
        return self.DAS_end_timer - self.DAS_start_timer

    def GetElapsedARRTime(self):
        return self.ARR_end_timer - self.ARR_start_timer

    def DownBlock(self):
        self.block_y += 1

    def MoveBlock(self, dir):
        self.block_x += dir

    def CheckRefill(self):
        '''블록 세트를 리필하는 메소드'''
        if len(self.block_queue) < 4:
            self.block_queue.extend(tetromino.GenerateRandomBlocks())  #여기 사실 잘 모르겠어...

    def CheckGameOver(self):

        for y in range(self.ceiling):

            for x in range(self.map_width):

                if self.map[y][x]:

                    return True

        return False 

    def PrintMap(self, stdscr):
        ''' 맵에 관련된 모든 것을 프린트하는 메소드'''
        begin_x = self.game_box_x
        begin_y = self.game_box_y

        stdscr.clear()
        windows.PrintGameMap(stdscr)
        self.PrintBlockList(stdscr)
        self.PrintHold(stdscr)
        self.PrintPreviewBlock(stdscr)
        self.PrintBlock(stdscr)

        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.map[y][x] != 0 and y + begin_y >= self.ceiling:
                    stdscr.addstr(y + begin_y, x * 2 + begin_x, u'▣')

        stdscr.addstr(begin_y + self.map_height + 1, begin_x, "score : {}".format(self.score))
                
        stdscr.refresh()
    
    def PrintBlockList(self, stdscr):
        '''블럭 미리보기를 프린트하는 메소드'''
        begin_x = self.block_list_box_x
        begin_y = self.block_list_box_y
        
            
        for block_in in range(4):
            block = self.block_queue[block_in].GetCurrentBlock()
            block_type = self.block_queue[block_in].GetBlockType()

            if block_type == tetromino.I_BLOCK:
                for y in range(1, 5):
                    for x in range(1, 5):
                        if block[y][x]:
                            stdscr.addstr((y - 1) + begin_y + block_in * 4, (x - 1) * 2 + begin_x, '▣')
            else:
                for y in range(4):
                    for x in range(4):
                        if block[y][x]:
                            stdscr.addstr(y + begin_y + block_in * 4, x * 2 + begin_x, '▣')
            
    
    def PrintBlock(self, stdscr):
        '''움직이는 블럭을 프린트하는 메소드'''
        begin_x = self.game_box_x
        begin_y = self.game_box_y
        
        block = self.block.GetCurrentBlock()

        block_x = self.block_x
        block_y = self.block_y

        block_height = len(block)
        block_width = len(block[0])

        for y in range(block_height):
            for x in range(block_width):
                if block[y][x] and y + block_y >= self.ceiling:
                    stdscr.addstr(y + begin_y + block_y, (block_x + x) * 2 + begin_x, '▣')
    
    def PrintPreviewBlock(self, stdscr):
        '''움직이는 블럭을 프린트하는 메소드'''
        begin_x = self.game_box_x
        begin_y = self.game_box_y
        
        pre_block = self.block.GetCurrentBlock()

        self.pre_block_x = self.block_x
        self.pre_block_y = self.block_y

        block_height = len(pre_block)
        block_width = len(pre_block[0])

        while not self.CheckBlockCollision(1, pre_block, self.pre_block_x, self.pre_block_y, False):
            self.pre_block_y += 1

        for y in range(block_height):
            for x in range(block_width):
                if pre_block[y][x]:
                    stdscr.addstr(y + begin_y + self.pre_block_y, (self.pre_block_x + x) * 2 + begin_x, '▧')

    def PrintHold(self, stdscr):
        '''움직이는 블럭을 프린트하는 메소드'''

        if self.block_hold:

            begin_x = self.hold_box_x
            begin_y = self.hold_box_y
            
            block = self.block_hold.GetCurrentBlock()
            block_type = self.block_hold.GetBlockType()

            block_height = len(block)
            block_width = len(block[0])

            if block_type == tetromino.I_BLOCK:
                for y in range(1, 5):
                    for x in range(1, 5):
                        if block[y][x]:
                            stdscr.addstr((y - 1) + begin_y, (x - 1) * 2 + begin_x, '▣')
            else:
                for y in range(4):
                    for x in range(4):
                        if block[y][x]:
                            stdscr.addstr(y + begin_y, x * 2 + begin_x, '▣')

    
    def RecordBlock(self):
        '''움직이는 블럭을 프린트하는 메소드'''
        begin_x = self.block_x
        begin_y = self.block_y

        block = self.block.GetCurrentBlock()

        block_height = len(block)
        block_width = len(block[0])

        for y in range(block_height):
            for x in range(block_width):
                if block[y][x]:
                    self.map[begin_y + y][begin_x + x] = block[y][x]
        

# 객체생성
t = Tetris()

# 메인메소드 실행
wrapper(t.Main)
