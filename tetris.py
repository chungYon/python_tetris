

#-*- coding: utf-8 -*-

import curses
from curses import wrapper
import time
import keyboard
import tetromino
import windows import game, setting, start

class Tetris:

    def __init__(self):
        self.map = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            ]

        self.score = 0
        self.block_type = 0
        self.block_x = 3
        self.block_y = 0
        self.drop_speed = 1
        self.st_speed = 1
        self.das = 0.131
        self.das_flag = False
        self.arr = 0.015
        self.arr_flag = False
        self.sdf = 0.01
        self.stop = 2
        self.map_height = 20
        self.map_width = 10
        self.game_box_x = 16
        self.game_box_y = 1
        self.block_list_box_x = 41
        self.block_list_box_y = 1
        
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
        start_arrow = start.PrintStartMap(start_win) # 화살표 위치 받아오기

        if start_arrow: # setting에 화살표가 있다면
            setting.PrintSettingMap(stdscr) #세팅 화면 띄우기
        
        self.Game(stdscr) # 게임 시작
        
    def Game(self, stdscr):
        '''게임을 담당하는 메소드'''
        
        self.InitTimer() # 타이머 초기화
        stdscr.erase()

        self.block_queue = tetromino.GenerateRandomBlocks() # 블럭 7개 채우기
        self.block = self.block_queue.pop(0) # 하나 뽑기

        while True:

            self.down_end_timer = time.time() # 드랍 타이머 세기
            self.drop_speed = self.st_speed # 기본 드랍 속도

            if keyboard.is_pressed('esc'):
                break

            if keyboard.is_pressed('down'):
                self.drop_speed = self.sdf # 소프트 드랍 속도

            if keyboard.is_pressed('left'):
                self.DAS_ARR_MoveLeft() # 왼쪽 무빙 담당
            
            elif keyboard.is_pressed('right'):# 오른쪽 무빙 담당
                self.DAS_ARR_MoveRight()

            keyboard.on_release_key('left', self.InitRelease) # 키를 땔시에 작동하는 함수
            keyboard.on_release_key('right', self.InitRelease)
            
            down_elapsed_time = self.GetElapsedDownTime() # 경과시간 구하기

            # 드랍 타이머
            if down_elapsed_time > self.drop_speed: # 드랍 시간이 지났다면

                if not self.IsFloor(): # 블럭이 맨 밑바닥에 없다면

                    if not self.CheckHeightObstacle(1): # 세로로 장애물이 없다면

                        self.InitDownTimer() # 드랍 타이머 초기화
                        self.DownBlock() # 블럭 내리기

            # 바닥에서 굳히는 타이머
            if self.IsFloor() or self.CheckHeightObstacle(1):  # 세로로 장애물이 없다면
                self.stop_end_timer = time.time() # 굳히기 타이머 세기
                self.InitDownTimer() # 드랍타이머 초기화
            else:
                self.InitStopTimer()

            stop_elapsed_time = self.GetElapsedStopTime() # 굳히기 타이머 경과시간 구하기

            if stop_elapsed_time > self.stop: # 굳히기 시간이 지났다면

                self.map[self.block_y][self.block_x] = 1 # 그 자리에 1로 만들기
                self.block_x = 3 # 위치 초기화
                self.block_y = 0
                self.InitDownTimer() # 드랍타이머 초기화

            self.PrintMap(stdscr) # 맵 출력

    def DAS_ARR_MoveLeft(self): 

        if not self.IsLeftWall(): # 맵의 맨 왼쪽이 아니라면

            if not self.CheckWidthObstacle(-1): # 블럭 왼쪽에 장애물이 없다면
                
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

        if not self.IsRightWall(): # 맵의 맨 오른쪽이 아니라면

            if not self.CheckWidthObstacle(1): # 블럭 오른쪽에 장애물이 없다면

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
                line_count += 1
        
        return line_count
    
    def CheckWidthObstacle(self, dir):
        '''가로로 장애물 검사하는 메소드'''
        if self.map[self.block_y][self.block_x + dir]:
            return True
        return False
    
    def CheckHeightObstacle(self, dir):
        '''세로로 장애물 검사하는 메소드'''
        if self.map[self.block_y + dir][self.block_x]:
            return True
        return False
    
    def IsFloor(self):
        '''블럭이 밑바닥인지 검사하는 메소드'''
        if self.block_y < (self.map_height - 1):
            return False
        return True

    def IsLeftWall(self):
        '''블럭이 맨 왼쪽에 있는지 검사하는 메소드'''
        if self.block_x > 0:
            return False
        return True

    def IsRightWall(self):
        '''블럭이 맨 오른쪽에 있는지 검사하는 메소드'''
        if self.block_x < (self.map_width - 1):
            return False
        return True

    def InitRelease(self, evt):
        '''키보드 때면 초기화할 것들 정리해놓은 메소드'''
        self.das_flag = False
        self.arr_flag = False

        self.InitDASTimer()
        self.InitARRTimer()

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

    def PrintMap(self, stdscr):
        ''' 맵에 관련된 모든 것을 프린트하는 메소드'''
        begin_x = self.game_box_x
        begin_y = self.game_box_y

        stdscr.clear()
        game.PrintGameMap(stdscr)
        self.PrintBlockList(stdscr)
        self.PrintBlock(stdscr)

        for y in range(20):
            for x in range(10):
                if self.map[y][x] != 0:
                    stdscr.addstr(y + begin_y, x * 2 + begin_x, u'▣')
                
        stdscr.refresh()
    
    def PrintBlockList(self, stdscr):
        '''블럭 미리보기를 프린트하는 메소드'''
        begin_x = self.block_list_box_x
        begin_y = self.block_list_box_y

        for block_in in range(4):
            block = self.block_queue[block_in].GetCurrentBlock()
            for y in range(4):
                for x in range(4):
                    if block[y][x]:
                        stdscr.addstr(y + begin_y + block_in * 4, x * 2 + begin_x, '▣')
    
    def PrintBlock(self, stdscr):
        '''움직이는 블럭을 프린트하는 메소드'''
        begin_x = self.game_box_x
        begin_y = self.game_box_y

        block = self.block.GetCurrentBlock()
        for y in range(4):
            for x in range(4):
                if block[y][x]:
                    stdscr.addstr(y + begin_y + self.block_y, (self.block_x + x) * 2 + begin_x, '▣')
# 객체생성
t = Tetris()

# 메인메소드 실행
wrapper(t.Main)
