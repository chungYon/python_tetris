import curses
import keyboard
from curses import wrapper

def PrintGameMap(stdscr):
    
    # 맨 왼쪽 사각형 12 x 6 가로 하나당 2로 계산
    # 시작점 : (1, 4)
    stdscr.addstr(0, 3, '┏━━━━━━━━┓') 
    stdscr.addstr(1,3,'┃        ┃')
    stdscr.addstr(2,3,'┃        ┃')
    stdscr.addstr(3,3,'┃        ┃')
    stdscr.addstr(4,3,'┃        ┃')
    stdscr.addstr(5,3,'┗━━━━━━━━┛')     


    # 24x 22 가로x세로
    # 시작점 : (1, 16)
    stdscr.addstr(0,15,'┏━━━━━━━━━━━━━━━━━━━━┓') 
    stdscr.addstr(1,15,'┃                    ┃')
    stdscr.addstr(2,15,'┃                    ┃')
    stdscr.addstr(3,15,'┃                    ┃')
    stdscr.addstr(4,15,'┃                    ┃')
    stdscr.addstr(5,15,'┃                    ┃')
    stdscr.addstr(6,15,'┃                    ┃')
    stdscr.addstr(7,15,'┃                    ┃')
    stdscr.addstr(8,15,'┃                    ┃')
    stdscr.addstr(9,15,'┃                    ┃')
    stdscr.addstr(10,15,'┃                    ┃')
    stdscr.addstr(11,15,'┃                    ┃')
    stdscr.addstr(12,15,'┃                    ┃')
    stdscr.addstr(13,15,'┃                    ┃')
    stdscr.addstr(14,15,'┃                    ┃')
    stdscr.addstr(15,15,'┃                    ┃')
    stdscr.addstr(16,15,'┃                    ┃')
    stdscr.addstr(17,15,'┃                    ┃')
    stdscr.addstr(18,15,'┃                    ┃')
    stdscr.addstr(19,15,'┃                    ┃')
    stdscr.addstr(20,15,'┃                    ┃')
    stdscr.addstr(21,15,'┗━━━━━━━━━━━━━━━━━━━━┛')    



    #  12x18
    # 시작점 : (1, 41)
    stdscr.addstr(0,40,'┏━━━━━━━━┓') 
    stdscr.addstr(1,40,'┃        ┃')
    stdscr.addstr(2,40,'┃        ┃')
    stdscr.addstr(3,40,'┃        ┃')
    stdscr.addstr(4,40,'┃        ┃') 
    stdscr.addstr(5,40,'┃        ┃')              
    stdscr.addstr(6,40,'┃        ┃') 
    stdscr.addstr(7,40,'┃        ┃') 
    stdscr.addstr(8,40,'┃        ┃') 
    stdscr.addstr(9,40,'┃        ┃') 
    stdscr.addstr(10,40,'┃        ┃') 
    stdscr.addstr(11,40,'┃        ┃')
    stdscr.addstr(12,40,'┃        ┃')
    stdscr.addstr(13,40,'┃        ┃')
    stdscr.addstr(14,40,'┃        ┃')
    stdscr.addstr(15,40,'┃        ┃')
    stdscr.addstr(16,40,'┃        ┃')
    stdscr.addstr(17,40,'┗━━━━━━━━┛')

def PrintSettingMap(stdscr):
    global arrow_flag
    arrow_flag= False

    def InitArrowFlag(evt):
        global arrow_flag
        arrow_flag = False
    
    def PrintMap():
        stdscr.clear()
        stdscr.addstr(arrow_y , 13, "➤ ",RED_AND_WHITE)
        stdscr.addstr(0, 15, "DAS",RED_AND_WHITE) 
        stdscr.addstr(1, 15,"ARR",RED_AND_WHITE)
        stdscr.addstr(2, 15,"SDF",RED_AND_WHITE)
        stdscr.addstr(3,15,'EXIT',RED_AND_WHITE)
        stdscr.refresh()

    
    curses.init_pair(1, curses.COLOR_WHITE,curses.COLOR_RED)
    RED_AND_WHITE= curses.color_pair(1)
    arrow_y = 0
    PrintMap()
    while True:
        
            if keyboard.is_pressed('esc'):
                break

            if keyboard.is_pressed('up'):
                if not arrow_flag:
                    arrow_y -= 1
                    if arrow_y < 0:
                        arrow_y = 3
                    PrintMap()
                    arrow_flag = True

            if keyboard.is_pressed('down'):
                if not arrow_flag:
                    arrow_y = (arrow_y + 1) % 4
                    PrintMap()
                    arrow_flag = True

            if keyboard.is_pressed('enter'):
                if arrow_y == 0:
                    pass
                elif arrow_y == 1:   
                    pass
                elif arrow_y == 2:
                    pass
                else:
                    break

            keyboard.on_release_key('down', InitArrowFlag)
            keyboard.on_release_key('up', InitArrowFlag)
            

def PrintStartMap(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE,curses.COLOR_RED)
    RED_AND_WHITE= curses.color_pair(1)

    global arrow_flag
    arrow_flag= False

    def InitArrowFlag(evt):
        global arrow_flag
        arrow_flag = False
    
    def PrintMap():
        stdscr.erase()
        stdscr.addstr(arrow_y + 1, 0, "➤ ",RED_AND_WHITE)
        
        stdscr.addstr(0, 15, "TETRIS",RED_AND_WHITE) 
        stdscr.addstr(1, 15,"START",RED_AND_WHITE)
        stdscr.addstr(2, 15,"SETTING",RED_AND_WHITE)
        stdscr.refresh()

    arrow_y = 0

    PrintMap()
    while True:
        
        if keyboard.is_pressed('esc'):
            break

        if keyboard.is_pressed('up'):
            if not arrow_flag:
                arrow_y -= 1
                if arrow_y < 0:
                    arrow_y = 1
                
                PrintMap()

                arrow_flag = True

        if keyboard.is_pressed('down'):
            if not arrow_flag:
                arrow_y = (arrow_y + 1) % 2

                PrintMap()
                arrow_flag = True

        keyboard.on_release_key('down', InitArrowFlag)
        keyboard.on_release_key('up', InitArrowFlag)
        
        if keyboard.is_pressed('enter'):
            return (arrow_y) % 2
                  

