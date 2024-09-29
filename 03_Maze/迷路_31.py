import tkinter
import random
# 基本定数
BACK_COLOR = 'black'
CURSOR_COLOR = 'Magenta'
CURSOR_COLOR2 = 'white'
MITISUJI_COLOR = 'Maroon'
MAZE_COLOR = ['pink4', 'DarkOrchid4','Indigo']
TEXT_COLOR = 'red'
CLEAR_CLEAR_COUNT_LIST= [3,5,6]
CLEAR_CLEAR_COUNT = 0
index = 0
tmr = 0
difficulty = 0
height_scores = ['99999999999,\n', '99999999999,\n', '99999999999,\n']
# マウスの座標を得る
mouse_x = 0
mouse_y = 0
mouse_c = False
cursor_x = 0
cursor_y = 0

def mouse_click(e):
    global mouse_c
    mouse_c = True

def mouse_release(e):
    global mouse_c
    mouse_c = False

def mouse_move(e):
    global mouse_x, mouse_y
    mouse_x = e.x
    mouse_y = e.y

# 迷路の二重リスト
maze = []
clear_count = 0  # 0～6 7は難しすぎる 
MAZE_H_LIST = [9,15,19,27,31,51,81,161]
MAZE_W_LIST = [15,23,29,45,51,85,127,255]
MASUME_SIZE_LIST = [50,33,26,17,15,9,6,3]
MAZE_H = MAZE_H_LIST[clear_count]
MAZE_W = MAZE_W_LIST[clear_count]
masume_size = MASUME_SIZE_LIST[clear_count]

start_maze_x = 20
start_maze_y = 70
random_list_y = [-1, 0, 1, 0] # 二列目以降は[3]は使わない
random_list_x = [0, 1, 0, -1]

def maze_generate():
    global maze, clear_count, MAZE_H, MAZE_W, masume_size, canvas
    canvas.delete('start_button')
    MAZE_H = 0
    MAZE_W = 0
    MAZE_H = MAZE_H_LIST[clear_count]
    MAZE_W = MAZE_W_LIST[clear_count]
    masume_size = MASUME_SIZE_LIST[clear_count]
    maze = []
    for _ in range(MAZE_H): # 迷路初期化
        maze.append([0]*MAZE_W) 
    # draw_maze()
    for y in range(MAZE_H): # 迷路壁を作る
        for x in range(MAZE_W):
            maze[0][x] = 1
            maze[MAZE_H-1][x] = 1
            maze[y][0] = 1
            maze[y][MAZE_W-1] = 1

    for y in range(2, MAZE_H-2, 2): # 柱を作る
        for x in range(2, MAZE_W-2 ,2):
            maze[y][x] = 1
            if 2 < x:            # 柱から壁を生やす
                r = random.randint(0,2)
            else:
                r = random.randint(0,3)
            maze[y+random_list_y[r]][x+random_list_x[r]] = 1
    maze[0][1] = 0 # 入口の壁をとる
    maze[1][1] = 0
    maze[MAZE_H-1][MAZE_W-2] = 0 # 出口の壁をとる
    maze[MAZE_H-2][MAZE_W-2] = 0
    if clear_count % 2 == 0:
        maze[0][1] = 2
    else:
        maze[MAZE_H-1][MAZE_W-2] = 2
    draw_maze()

def draw_maze():
    canvas.delete('maze')
    for y in range(MAZE_H): # リストを元に迷路を描画
        for x in range(MAZE_W):
            if maze[y][x] == 1:
                canvas.create_rectangle(start_maze_x + x*masume_size, start_maze_y + y*masume_size,
                                        start_maze_x + x*masume_size + masume_size, start_maze_y + y*masume_size + masume_size,
                                        fill=MAZE_COLOR[difficulty], width=0, tag='maze')
            if maze[y][x] == 2:
                canvas.create_rectangle(start_maze_x + x*masume_size, start_maze_y + y*masume_size,
                                        start_maze_x + x*masume_size + masume_size, start_maze_y + y*masume_size + masume_size,
                                        fill=MITISUJI_COLOR, width=0, tag='maze')

def main():
    global mouse_x, mouse_y, mouse_c, cursor_x, cursor_y
    global clear_count, canvas, CLEAR_CLEAR_COUNT
    global start_time, stop_time, index, difficulty, tmr
    
    if index == 0: # タイトル画面生成
        tmr = 0
        try:
            with open('MAZE_save_date.txt', 'r') as file:
                lines = file.readlines()
                i = 0
                for line in lines:
                    height_scores[i] = line
                    i += 1
        except:      
            with open('MAZE_save_date.txt', 'w') as file:
                for i in range(len(height_scores)):
                    file.write(str(height_scores[i]))
        canvas.delete('game_clear')
        canvas.delete('tmr')
        canvas.create_rectangle(start_maze_x, start_maze_y,
                            start_maze_x + masume_size*MAZE_W, start_maze_y + masume_size*MAZE_H,
                            fill= MAZE_COLOR[difficulty], width =0, tag ='maze')
        canvas.create_rectangle(250,285,350,320, width=0,fill=MITISUJI_COLOR, tag ='title')
        canvas.create_rectangle(250,320,350,350, width=0,fill=BACK_COLOR, tag ='title')
        canvas.create_rectangle(250,350,350,380, width=0,fill=MITISUJI_COLOR, tag ='title')
        canvas.create_text(405, 205, text = '早解き迷路', fill=BACK_COLOR, font = ('Times New Roman', 50), tag ='title')
        canvas.create_text(400, 200, text = '早解き迷路', fill=CURSOR_COLOR, font = ('Times New Roman', 50), tag ='title')
        canvas.create_text(300, 335, text = 'ラク\n普通\n厳しい', fill=CURSOR_COLOR2, font = ('Times New Roman', 20), tag ='title')
        canvas.create_text(500, 335, text = f'{height_scores[0][:-2]}秒\n{height_scores[1][:-2]}秒\n{height_scores[2][:-2]}秒', fill=CURSOR_COLOR2, font = ('Times New Roman', 20), tag ='title')
        index = 1
        mouse_c = False
        # セーブデータを読み込む。なかったら作る

    elif index == 1: # 難易度設定の入力待ち
        CLEAR_CLEAR_COUNT = 0
        if mouse_c:
            if 250 < mouse_x and mouse_x < 350 and 285 < mouse_y and mouse_y < 320:# 普通
                difficulty = 0
                CLEAR_CLEAR_COUNT = CLEAR_CLEAR_COUNT_LIST[difficulty]
            if 250 < mouse_x and mouse_x < 350 and 320 < mouse_y and mouse_y < 350:# 厳しい
                difficulty = 1
                CLEAR_CLEAR_COUNT = CLEAR_CLEAR_COUNT_LIST[difficulty]
            if 250 < mouse_x and mouse_x < 350 and 350 < mouse_y and mouse_y < 380:# 無理
                difficulty = 2
                CLEAR_CLEAR_COUNT = CLEAR_CLEAR_COUNT_LIST[difficulty]
        if 0 < CLEAR_CLEAR_COUNT:
            index = 2
    elif index ==2: # ボタン作成、タイムスタート
        canvas.delete('title')
        canvas.create_rectangle(30,30,130,70,fill = CURSOR_COLOR2,tag='start_button')
        canvas.create_text(80,50,text='start',font=('Times New Roman',30),fill = CURSOR_COLOR,tag='start_button')
        if mouse_c:
            if 30 < mouse_x and mouse_x < 130 and 30 < mouse_y and mouse_y < 70:
                maze_generate()
                index = 3
    elif index == 3: # 迷路作成　クリア設定回数まで繰り返す
        tmr += 1
        canvas.delete('tmr')
        canvas.delete('nokori')
        count_text_size = int(250 + (tmr*0.1 +1))
        canvas.create_text(400,270,text = f'{tmr}',font=('Times New Roman',count_text_size), fill = TEXT_COLOR, tag ='tmr')
        canvas.create_text(400,50,font=('Times New Roman',25), text=f'{clear_count}/{CLEAR_CLEAR_COUNT_LIST[difficulty]}', fill='white', tag='nokori')
        if len(maze) == MAZE_H:
            if start_maze_x <= mouse_x <= start_maze_x + masume_size*MAZE_W and \
                start_maze_y <= mouse_y <= start_maze_y + masume_size*MAZE_H:
                canvas.delete('cursor')
                cursor_x = int((mouse_x - start_maze_x)/masume_size)
                cursor_y = int((mouse_y - start_maze_y)/masume_size)
                # カーソルの中心
                canvas.create_rectangle(cursor_x * masume_size + start_maze_x, cursor_y * masume_size + start_maze_y,
                                        cursor_x * masume_size + start_maze_x + masume_size,
                                        cursor_y * masume_size + start_maze_y + masume_size, fill=CURSOR_COLOR, tag='cursor')
                # カーソルの外枠
                canvas.create_line(cursor_x * masume_size + start_maze_x - masume_size,
                                cursor_y * masume_size + start_maze_y - masume_size,
                                    cursor_x * masume_size + start_maze_x - masume_size,
                                    cursor_y * masume_size + start_maze_y + masume_size*2,
                                    cursor_x * masume_size + start_maze_x + masume_size*2,
                                    cursor_y * masume_size + start_maze_y + masume_size*2,
                                    cursor_x * masume_size + start_maze_x + masume_size*2,
                                    cursor_y * masume_size + start_maze_y - masume_size,
                                    cursor_x * masume_size + start_maze_x - masume_size,
                                    cursor_y * masume_size + start_maze_y - masume_size,
                                    fill= CURSOR_COLOR2,tag='cursor')

                if 0 <= cursor_x < MAZE_W and 0 <= cursor_y < MAZE_H:
                    if maze[cursor_y][cursor_x] == 0:
                        if (cursor_y+1 < MAZE_H and maze[cursor_y+1][cursor_x] == 2) or\
                            (cursor_y-1 < MAZE_H and maze[cursor_y-1][cursor_x] == 2) or\
                            (cursor_x+1 < MAZE_W and maze[cursor_y][cursor_x+1] == 2)or\
                            (cursor_x-1 < MAZE_W and maze[cursor_y][cursor_x-1] == 2):
                            maze[cursor_y][cursor_x] = 2
                            if cursor_y+1 < MAZE_H and cursor_x+1 < MAZE_W:
                                if maze[cursor_y+1][cursor_x] != None and maze[cursor_y+1][cursor_x] != 1:
                                    maze[cursor_y+1][cursor_x] = 2
                                if maze[cursor_y-1][cursor_x] != None and maze[cursor_y-1][cursor_x] != 1:
                                    maze[cursor_y-1][cursor_x] = 2
                                if maze[cursor_y][cursor_x+1] != None and maze[cursor_y][cursor_x+1] != 1:
                                    maze[cursor_y][cursor_x+1] = 2
                                if maze[cursor_y][cursor_x-1] != None and maze[cursor_y][cursor_x-1] != 1:
                                    maze[cursor_y][cursor_x-1] = 2
                            draw_maze()
                            if (clear_count % 2 == 0 and maze[MAZE_H-1][MAZE_W-2]  == 2) or (clear_count % 2 ==1 and maze[0][1]== 2):
                                # ゴールに到達
                                clear_count += 1
                                if clear_count == len(MASUME_SIZE_LIST):
                                    clear_count = len(MASUME_SIZE_LIST)
                                if clear_count == CLEAR_CLEAR_COUNT:
                                    index = 4
                                else:
                                    index = 3
                                    maze_generate()
    elif index == 4: # クリア回数まで達するとタイムストップ。クリア画面を作る
        canvas.delete('maze')
        canvas.delete('nokori')
        # canvas.delete('txt')
        canvas.delete('cursor')
        canvas.create_text(600,425, text = f'最高：{height_scores[difficulty][:-2]}秒', font = ('Times New Roman', 20), fill = CURSOR_COLOR2, tag='game_clear')
        if tmr < int(height_scores[difficulty][:-2]) : # ハイスコアの更新
            height_scores[difficulty] = str(tmr) + ',\n'
            with open('MAZE_save_date.txt', 'w') as file:
                for i in range(len(height_scores)):
                    file.write(str(height_scores[i]))
            canvas.create_text(400,100, text = 'ハイスコア更新', font = ('Times New Roman', 50), fill = TEXT_COLOR, tag='game_clear')
        else:
            canvas.create_text(400,100, text = 'クリア', font = ('Times New Roman', 50), fill = MITISUJI_COLOR, tag='game_clear')
        index = 5
    elif index == 5: # タイトルに戻るの入力待ち
        canvas.create_rectangle(100,400,300,450, fill =MITISUJI_COLOR, tag = 'game_clear')
        canvas.create_text(200,425, text = 'タイトルに戻る', font = ('Times New Roman', 20), fill =CURSOR_COLOR2, tag = 'game_clear')
        if mouse_c == True:
            if 100 < mouse_x < 300 and 400 < mouse_y < 450:
                index = 0
                clear_count = 0
                canvas.delete('game_clear')
    root.after(50, main)

root = tkinter.Tk()
root.title('早解き迷路')
root.bind('<ButtonPress>', mouse_click)
root.bind('<Motion>', mouse_move)
root.bind('<ButtonRelease>', mouse_release)
canvas = tkinter.Canvas(root, width=800, height=600, bg = BACK_COLOR)
canvas.pack(side= tkinter.TOP)
main()
root.mainloop()