import tkinter
import random

class App(tkinter.Frame):
    # 定数
    WIDTH = 1000
    HEIGHT = 600
    FONT = 'Times New Roman'

    # 色
    COLOR_BACK = 'gray10'
    COLOR_WHITY = 'gray80'
    COLOR_BALL ='white' # ボールの色
    COLOR_CURSOR = 'green' # カーソルの色
    COLOR_BLOCK_SCOPE = 'chartreuse3' # ブロック設置可能範囲
    COLOR_ZABUTON = 'dark khaki' # 座布団
    COLOR_MENU_SCOPE = 'gray20' # メニュー範囲
    COLOR_MENU_TEXT = COLOR_WHITY
    COLOR_POWER_UP = 'red'
    COLOR_POWER_DOWN = COLOR_WHITY
    COLOR_HEART_BLANK = 'MidnightBlue' # ハートの器の色
    COLOR_HEART = 'red' # ハートの色
    COLOR_SCORE = 'green1'

    # 初期値
    index = 0
    mouse_x = 0
    mouse_y = 0
    mouse_c = False
    cursor_x = 0 # マウスの座標がどのマスに相当するか
    cursor_y = 0
    block_x = 0 # ボールの座標がどのマスに相当するか
    block_y = 0
    score = 0
    hi_score = 0
    life_max = 3 # 最大ライフ
    life = life_max
    block_hold_max_init = 30
    block_hold_max = block_hold_max_init
    block_hold = block_hold_max # 保有ブロック数
    mistake_flag = False # ボールが外に出たかどうかの論理値
    hi_scores = [0, 0, 0, 0, 0] # ハイスコアは5個まで保持 大きい順
    read_save_list = []
    maki_flag = False
    ten_flag = False
    # ブロック関連
    BLOCK_H = 25 #25*25
    BLOCK_W = 35
    b_list = []
    for _ in range(BLOCK_H):
        b_list.append([0] * BLOCK_W)

    # tmr
    tmr_miss = 0 # ミス演出用変数
    tmr_wait = 0 # 待つ時のtmr
    maki_tmr = 0
    ten_tmr = 0

    # 描画定数
    # 画面全体に対する比率
    wi_1_2 = WIDTH * 1 / 2
    wi_1_3 = WIDTH * 1 / 3
    wi_2_3 = WIDTH * 2 / 3
    wi_2_5 = WIDTH * 2 / 5
    wi_3_5 = WIDTH * 3 / 5
    wi_1_100 = WIDTH * 1 / 100
    wi_3_100 = WIDTH * 3 / 100
    wi_2_100 = WIDTH * 2 / 100
    wi_99_100 = WIDTH * 99 / 100
    hi_1_2 = HEIGHT * 1 / 2
    hi_1_3 = HEIGHT * 1 / 3
    hi_2_3 = HEIGHT * 2 / 3
    hi_11_16 =  HEIGHT * 11 / 16
    hi_3_6 = HEIGHT * 3 / 6
    hi_4_6 = HEIGHT * 4 / 6
    hi_5_6 = HEIGHT * 5 / 6
    hi_5_8 = HEIGHT * 5 / 8
    hi_6_8 = HEIGHT * 6 / 8
    hi_2_100 = HEIGHT * 2 / 100
    hi_3_100 = HEIGHT * 3 / 100
    hi_4_100 = HEIGHT * 4 / 100
    hi_80_100 = HEIGHT * 80 / 100
    hi_97_100 = HEIGHT * 97 / 100
    # 座布団関連
    # 画面と座布団の隙間
    sukima_wi = wi_2_100
    sukkima_hi = hi_2_100
    # 座布団スタートx且つ左右の空白、スタートy
    back_s_x = sukima_wi
    back_s_y = sukkima_hi
    # 座布団ゴールx,ゴールy
    back_g_x = WIDTH - sukima_wi ##############################後で治す
    back_g_y = hi_80_100
    # 座布団サイズ
    back_wi = back_g_x - back_s_x
    back_hi = back_g_y - back_s_y
    # ブロック範囲関連
    # 座布団からブロック範囲までの隙間左上xy
    bz_sukima_wi = wi_3_100
    bz_suima_hi = hi_4_100
    # ブロック範囲スタートx且つ左右の空白、スタートy
    bz_s_x = back_s_x + bz_sukima_wi
    bz_s_y = back_s_y + bz_suima_hi
    # 各ブロックの隙間
    b_sukima_wi = 1
    b_sukima_hi = 1
    # ブロック範囲ゴール
    bz_g_x = back_g_x - bz_sukima_wi
    bz_g_y = back_g_y - bz_suima_hi
    # ブロック範囲の縦横サイズ
    bz_wi = bz_g_x - bz_s_x
    bz_hi = bz_g_y - bz_s_y
    # 1ブロックのサイズ縦
    b_hi = bz_hi * 1 / BLOCK_H
    # 1ブロックのサイズ横
    b_wi = bz_wi * 1 / BLOCK_W
    # ブロック範囲比率
    bz_wi_1_3 = bz_s_x + bz_wi * 1 / 3
    bz_wi_2_3 = bz_s_x + bz_wi * 2 / 3
    bz_wi_1_2 = bz_s_x + bz_wi * 1 / 2
    bz_hi_1_2 = bz_s_y + bz_hi * 1 / 2
    bz_hi_1_3 = bz_s_y + bz_hi * 1 / 3
    bz_hi_2_3 = bz_s_y + bz_hi * 2 / 3
    # メニュー範囲関連
    # メニュー範囲スタート左上xy
    menu_s_x = back_s_x
    menu_s_y = back_g_y + bz_suima_hi
    # メニュー範囲ゴール右下xy
    menu_g_x = back_g_x
    menu_g_y = HEIGHT - bz_suima_hi
    # メニュー縦横サイズ
    menu_wi = menu_g_x - menu_s_x
    menu_hi = menu_g_y - menu_s_y   
    # メニュー比率
    menu_wi_1_3 = menu_s_x + menu_wi * 1 / 3
    menu_wi_2_3 = menu_s_x + menu_wi * 2 / 3
    menu_wi_1_2 = menu_s_x + menu_wi * 1 / 2
    menu_hi_1_2 = menu_s_y + menu_hi * 1 / 2
    # ボール関連
    # ボール座標x,y 初期値
    ball_x_init = wi_1_2
    ball_x = ball_x_init
    ball_y_init = bz_g_y - bz_hi* 1/ 2
    ball_y = ball_y_init
    # ボールの1fの移動量
    ball_xp_init = 2
    ball_yp_init = 2
    ball_xp = ball_xp_init
    ball_yp = ball_yp_init
    # ボールサイズ 1ブロックの高さ依存
    ball_size = b_hi * 1 / 2
    # ボールサイズの半分
    ball_size_c = ball_size * 1 / 2

    # ポジションタプル
    # タイトル画面のスタートボタン
    title_button_pos = [wi_2_5, hi_3_6, wi_3_5, hi_4_6]
    gameover_button_pos = [wi_1_3, hi_5_8, wi_2_3, hi_6_8]

    def __init__(self, master = None):
        super().__init__(master)
        self.master.title('羊脱走阻止ゲーム')
        self.canvas = tkinter.Canvas(self.master, width=self.WIDTH, height=self.HEIGHT, bg=self.COLOR_BACK)
        self.canvas.pack()
        self.hituji_r = tkinter.PhotoImage(file = 'hituji_r.png')
        self.hituji_l = tkinter.PhotoImage(file = 'hituji_l.png')
        self.saku = tkinter.PhotoImage(file = 'saku.png')
        self.maki = tkinter.PhotoImage(file = 'maki.png')
        self.main()

    def mouse_move(self, e):
        #マウスの動き検出
        self.mouse_x = e.x
        self.mouse_y = e.y

    def mouse_click(self, e):
        # マウスクリック検出
        self.mouse_c = True

    def mouse_release(self, e):
        # マウスリリース検出
        self.mouse_c = False

    def draw_title(self):
        self.canvas.create_rectangle(self.wi_1_100, self.hi_3_100,
                                     self.wi_99_100, self.hi_97_100,
                                     fill = self.COLOR_BLOCK_SCOPE, outline=self.COLOR_WHITY,
                                     width=1, tag = 'title')
        self.canvas.create_text(self.wi_1_2, self.hi_1_3,
                                text = '羊脱走阻止ゲーム',
                                font =(self.FONT, 50), fill = self.COLOR_BACK, tag = 'title')
        self.canvas.create_image(self.wi_1_3, self.hi_4_6,image= self.hituji_r, tag = 'title')
        self.canvas.create_image(self.wi_2_3, self.hi_4_6,image= self.saku, tag = 'title')
        self.canvas.create_rectangle(self.title_button_pos,
                                     outline=self.COLOR_BACK, tag = 'title')
        self.canvas.create_text(self.title_button_pos[0] + (self.title_button_pos[2] - self.title_button_pos[0]) * 1 / 2,
                                self.title_button_pos[1] + (self.title_button_pos[3] - self.title_button_pos[1]) * 1 / 2,
                                text = 'スタート',
                                font =(self.FONT, 25), fill = self.COLOR_BACK, tag = 'title')
        for i in range(len(self.read_save_list)):
            self.canvas.create_text(self.title_button_pos[0] + (self.title_button_pos[2] - self.title_button_pos[0]) * 1 / 2,
                                (self.title_button_pos[3] + (self.hi_97_100 - self.title_button_pos[3]) * 1 / 3)+ i * 22,
                                text = f'{i+1} 位　{self.read_save_list[i]}点',
                                font =(self.FONT, 15), fill = self.COLOR_BACK, tag = 'title')

    def click_title_button(self):
        # タイトルボタンを押したかの判定
        if self.mouse_c:
            if  self.title_button_pos[0] < self.mouse_x < self.title_button_pos[2]\
            and self.title_button_pos[1] < self.mouse_y < self.title_button_pos[3]:
                self.canvas.delete('title')
                return True

    def draw_back(self):
        # ブロックとボールの可動範囲の座布団を描画
        self.canvas.create_rectangle(self.back_s_x, self.back_s_y,
                                     self.back_g_x, self.back_g_y,
                                     outline = self.COLOR_WHITY, width=2,
                                     tag = 'base')
        # ブロック設置範囲の描画
        self.canvas.create_rectangle(self.bz_s_x, self.bz_s_y,
                                     self.bz_g_x, self.bz_g_y,
                                     fill = self.COLOR_BLOCK_SCOPE, width=0, tag ='base')
         # メニューの範囲を描画 
        self.canvas.create_rectangle(self.menu_s_x, self.menu_s_y,
                                     self.menu_g_x, self.menu_g_y,
                                     fill = self.COLOR_MENU_SCOPE, width=0,
                                     tag= 'base')
        # 残りの羊を描写
        if self.life > 1:
            for i in range(self.life - 1):
                self.canvas.create_image(self.wi_1_2 + i * 50, self.hi_1_3,
                                         image= self.hituji_r, tag= 'base')
    def draw_start_button(self):
        # スタートボタンを描画
        self.canvas.create_rectangle(self.bz_wi_1_3, self.bz_hi_1_3,
                                     self.bz_wi_2_3, self.bz_hi_2_3,
                                     fill = self.COLOR_WHITY,width=10, tag = 'start_button')
        self.canvas.create_text(self.bz_wi_1_2, self.bz_hi_1_2,
                                text = 'START', fill = self.COLOR_BACK, tag = 'start_button',
                                font = (self.FONT, int(self.bz_wi_1_3 *0.19 )))

    def push_start_button(self):
        # スタートボタンが押されたらTrueを返す
        if self.mouse_c == True and self.bz_wi_1_3 < self.mouse_x <self.bz_wi_2_3\
        and self.bz_hi_1_3 < self.mouse_y < self.bz_hi_2_3:
            self.canvas.delete('start_button')
            self.mouse_c = False
            return True
        
    def draw_state(self):
        #ステータスを描く
        self.canvas.delete('state')
        if self.block_hold <= 0:
            model_color = self.COLOR_POWER_UP
        else:
            model_color = self.COLOR_MENU_TEXT
        self.canvas.create_text(self.menu_wi_1_3, self.menu_hi_1_2,
                                text = f'柵ストック{self.block_hold}/{self.block_hold_max}',
                                font = (self.FONT, int(self.WIDTH*0.03)),
                                fill = model_color, tag='state')
        self.canvas.create_text(self.menu_wi_2_3, self.menu_hi_1_2,
                                text = f'　{self.score}点',
                                font = (self.FONT, int(self.WIDTH*0.03)),
                                fill = self.COLOR_MENU_TEXT, tag='state')


    def draw_ball(self):
        # ボールを描画
        self.canvas.delete('ball')
        if self.ball_xp > 0:
            model_img = self.hituji_r
        else:
            model_img = self.hituji_l
        self.canvas.create_image(self.ball_x, self.ball_y, image = model_img,
                                tag = 'ball')
        # self.canvas.create_oval(self.ball_x - (self.ball_size * 1 / 2),
        #                         self.ball_y - (self.ball_size * 1 / 2),
        #                         self.ball_x + (self.ball_size * 1 / 2),
        #                         self.ball_y + (self.ball_size * 1 / 2),
        #                         fill=self.COLOR_BALL, tag = 'ball')
    def move_ball(self):
        # ボールが動く
        self.ball_x += self.ball_xp
        self.ball_y += self.ball_yp
        if  not (self.back_s_x < self.ball_x < self.back_g_x and self.back_s_y < self.ball_y < self.back_g_y):
            # ボールが画面外ならミス判定
            self.mistake_flag = True
        if self.bz_s_x < self.ball_x < self.bz_g_x and self.bz_s_y < self.ball_y < self.bz_g_y:       
            # ボールがブロック範囲内にあるならば
            # ボールの座標がb_listのどこに相当するかの計算
            self.block_x = int((self.ball_x - self.bz_s_x) / self.b_wi)
            self.block_y = int((self.ball_y - self.bz_s_y) / self.b_hi)
            if self.b_list[self.block_y][self.block_x] == 1:
                # 外側のブロックに当たったら内側に反射する
                if not(int(self.BLOCK_H * 1/4) < self. block_y < int(self.BLOCK_H * 3 / 4)):
                    self.ball_yp = -self.ball_yp
                if not(int(self.BLOCK_W * 1/4) < self. block_x < int(self.BLOCK_W * 3 / 4)):
                    self.ball_xp = -self.ball_xp
                # 内側のブロックに当たったら上下に反射する
                if (int(self.BLOCK_H * 1/4) < self. block_y < int(self.BLOCK_H * 3 / 4))and\
                (int(self.BLOCK_W * 1/4) < self. block_x < int(self.BLOCK_W * 3 / 4)):
                    self.ball_yp = -self.ball_yp
                # if self.ball_xp < 0: #速度が増えていく
                #     self.ball_xp = -(abs(self.ball_xp) + 1)
                # else:
                #     self.ball_xp = (abs(self.ball_xp) + 1)
                # if abs(self.ball_xp) >= 8: # 速度が上限(8)を超えたら2にリセット
                #     if self.ball_xp < 0: 
                #         self.ball_xp = -2
                #     else:
                #         self.ball_xp = 2
                self.b_list[self.block_y][self.block_x] -=1
                if self.b_list[self.block_y][self.block_x] == 0:
                    r = random.randint(0,100)
                    if r > 30: # 7割で普通に壊れる
                        self.b_list[self.block_y][self.block_x] = 0
                    elif 15 < r <= 30: # 1.5割で薪アイテム
                        self.b_list[self.block_y][self.block_x] = 2
                    # elif 10 <= r <= 20: # 1割で呪アイテム
                    #     self.b_list[self.block_y][self.block_x] = 3
                    elif 0<= r <= 15: # 1.5割で点アイテム
                        if self.score >= 11: # 11点以上なら出現 以下なら薪
                            self.b_list[self.block_y][self.block_x] = 4
                        else:
                            self.b_list[self.block_y][self.block_x] = 2
                    self.score += 1
                    self.block_hold += 1
        else:
            # 範囲を出たらミス
            self.mistake_flag = True
        
    def draw_cursor(self):
        # カーソルを描画
        if self.bz_s_x < self.mouse_x < self.bz_g_x and\
        self.bz_s_y < self.mouse_y < self.bz_g_y:
            self.cursor_x = int((self.mouse_x - self.bz_s_x) / self.b_wi)
            self.cursor_y = int((self.mouse_y - self.bz_s_y) / self.b_hi)
            self.canvas.delete('cursor')
            cursor_s_x = self.bz_s_x + self.b_wi * self.cursor_x + self.b_sukima_wi
            cursor_s_y = self.bz_s_y + self.b_hi * self.cursor_y + self.b_sukima_hi
            cursor_g_x = self.bz_s_x + self.b_wi * self.cursor_x + self.b_wi
            cursor_g_y =self.bz_s_y + self.b_hi * self.cursor_y + self.b_hi
            self.canvas.create_rectangle(cursor_s_x,
                                         cursor_s_y,
                                         cursor_g_x,
                                         cursor_g_y,
                                         outline = self.COLOR_CURSOR, width=2, tag='cursor')
            self.canvas.create_rectangle(cursor_s_x +4,
                                         cursor_s_y +4,
                                         cursor_g_x -4,
                                         cursor_g_y -4,
                                         outline = self.COLOR_CURSOR, width=1, tag='cursor')
    
    def click_block(self):
        # クリックしてブロックを追加かアイテムを得る
        if self.mouse_c and self.bz_s_x < self.mouse_x < self.bz_g_x and\
        self.bz_s_y < self.mouse_y < self.bz_g_y:
            # self.mouse_c = False
            if self.b_list[self.cursor_y][self.cursor_x] ==0:
                if self.block_hold > 0:
                    self.b_list[self.cursor_y][self.cursor_x] = 1 # 柵設置
                    self.block_hold -= 1
            elif self.b_list[self.cursor_y][self.cursor_x] == 2: # 薪ゲット
                self.mouse_c = False
                self.maki_flag = True
                self.b_list[self.cursor_y][self.cursor_x] = 0
                self.block_hold_max += 1
            elif self.b_list[self.cursor_y][self.cursor_x] == 3: # 呪いアイテム　不使用
                self.mouse_c = False
                self.b_list[self.cursor_y][self.cursor_x] = 0
                self.block_hold_max -= 1
            elif self.b_list[self.cursor_y][self.cursor_x] == 4: # 点アイテム
                self.mouse_c = False
                self.ten_flag = True
                self.b_list[self.cursor_y][self.cursor_x] = 0
                self.score = self.score + int(self.score * 1 / 10)

    def draw_maki_get(self):
        # 柵+の表示
        self.maki_flag =False
        self.canvas.create_text(self.menu_wi_1_2, self.menu_hi_1_2 - 20,
                                font = (self.FONT, int(self.WIDTH*0.03)),
                                fill = self.COLOR_SCORE,
                                text='柵+1',tag ='maki_get')
    
    def draw_ten_get(self):
        # 点+の表示
        self.ten_flag = False
        self.canvas.create_text(self.menu_wi_2_3+50, self.menu_hi_1_2 - 20,
                                font = (self.FONT, int(self.WIDTH*0.03)),
                                fill = self.COLOR_SCORE,
                                text='+10％',tag ='ten_get')

    def draw_blocks(self):
        # ブロックを描く
        self.canvas.delete('block')
        for y in range(self.BLOCK_H):
            for x in range(self.BLOCK_W):
                b_s_x = self.bz_s_x + (self.bz_wi * x / self.BLOCK_W) + self.b_sukima_wi
                b_s_y = self.bz_s_y + (self.bz_hi * y / self.BLOCK_H) + self.b_sukima_hi
                b_g_x = self.bz_s_x + (self.bz_wi * x /self.BLOCK_W) + self.b_wi
                b_g_y = self.bz_s_y + (self.bz_hi * y / self.BLOCK_H) + self.b_hi
                if self.b_list[y][x] == 1:
                    self.canvas.create_image(b_s_x+(b_g_x -b_s_x)*1/2,
                                             b_s_y+(b_g_y -b_s_y)*1/2,image=self.saku,tag ='block')
                    # self.canvas.create_rectangle(b_s_x, b_s_y, b_g_x, b_g_y,
                    #                              fill=self.COLOR_WHITY, width=0,tag ='block')
                if self.b_list[y][x] == 2:
                    self.canvas.create_rectangle(b_s_x, b_s_y, b_g_x, b_g_y,
                                                 outline=self.COLOR_POWER_UP, width = 2, tag = 'block')
                    self.canvas.create_image(b_s_x + self.b_wi * 1 / 2, b_s_y + self.b_hi * 1 / 2,
                                             image=self.maki, tag = 'block')
                    # self.canvas.create_text(b_s_x + self.b_wi * 1 / 2, b_s_y + self.b_hi * 1 / 2,
                    #                         font = (self.FONT, int(self.b_wi * 1 / 3)),
                    #                         text = '祝',fill = self.COLOR_POWER_UP,
                    #                         width=0,tag ='block')
                if self.b_list[y][x] == 3:
                    self.canvas.create_rectangle(b_s_x, b_s_y, b_g_x, b_g_y,
                                                 outline=self.COLOR_POWER_DOWN, width = 2, tag = 'block')
                    self.canvas.create_text(b_s_x + self.b_wi * 1 / 2, b_s_y + self.b_hi * 1 / 2,
                                            font = (self.FONT, int(self.b_wi * 1 / 3)),
                                            text = '呪',fill = self.COLOR_POWER_DOWN,
                                            width=0,tag ='block')
                if self.b_list[y][x] == 4:
                    self.canvas.create_rectangle(b_s_x, b_s_y, b_g_x, b_g_y,
                                                 outline=self.COLOR_POWER_DOWN, width = 2, tag = 'block')
                    self.canvas.create_text(b_s_x + self.b_wi * 1 / 2, b_s_y + self.b_hi * 1 / 2,
                                            font = (self.FONT, int(self.b_wi * 1 / 3)),
                                            text = '点',fill = self.COLOR_POWER_UP,
                                            width=0,tag ='block')
                    
    def create_heart(self, canvas, center_x, center_y, size, **kwargs):
        # ハートを描く
        points = [
            center_x - size * 1 / 2, center_y - size * 1 / 2, # 1
            center_x, center_y, # 2  
        ]
        canvas.create_oval(points, width = 0,  **kwargs)

        points = [
            center_x, center_y - size * 1 / 2, # 1
            center_x + size * 1 / 2, center_y, # 2  
        ]
        canvas.create_oval(points, width = 0, **kwargs)

        points = [
            center_x - size * 3 / 5, center_y - size * 1 / 4, # s
            center_x - size * 2 / 16, center_y + size * 1 / 4,
            center_x, center_y + size * 1 / 2, # c
            center_x + size * 2 / 16, center_y + size * 1 / 4,
            center_x + size * 3 / 5, center_y - size * 1 / 4,
            center_x, center_y - size * 1 / 4 # G
        ]
        canvas.create_polygon(points, smooth = True, **kwargs)

    def draw_heart_rest(self, blink_flag):
        # ミスった時の演出
        # ハートの器を描く
        self.canvas.delete('heart')
        for i in range(self.life_max):
            heart_x = i / self.life_max * self.back_wi + self.back_s_x + (self.back_wi / self.life_max * 0.5)
            heart_y = self.back_hi * 1 / 2 + self.back_s_y
            heart_size = self.back_wi * 1 / self.life_max * 0.5
            self.create_heart(self.canvas, center_x = heart_x, center_y = heart_y,
                              size = heart_size, fill = self.COLOR_HEART_BLANK,
                              tag= 'heart')
        if blink_flag:
            # 現在のハート
            model_mun = self.life
        else:
            # 現在のハート-1
            model_mun = self.life - 1
            
        for i in range(model_mun):
            heart_x = i / self.life_max * self.back_wi + self.back_s_x + (self.back_wi / self.life_max * 0.5)
            heart_y = self.back_hi * 1 / 2 + self.back_s_y
            heart_size = self.back_wi * 1 / self.life_max * 0.5
            self.create_heart(self.canvas, center_x = heart_x, center_y = heart_y,
                            size = heart_size * 0.9, fill = self.COLOR_HEART,
                            tag= 'heart')

    def draw_game_over(self):
        # ゲームオーバー処理
        self.canvas.create_text(self.wi_1_2, self.hi_1_3,
                                text = 'GAME OVER',
                                font = (self.FONT, int(self.WIDTH * 0.05)),
                                tag = 'gameover',
                                fill =self.COLOR_POWER_DOWN)
        self.canvas.create_text(self.wi_1_2, self.hi_1_2,
                        text = f'{self.score}点',
                        font = (self.FONT, int(self.WIDTH * 0.05)),
                        tag = 'gameover',
                        fill =self.COLOR_SCORE)
        self.canvas.create_text(self.wi_1_2, self.hi_11_16,
                        text = f'タイトルへ',
                        font = (self.FONT, int(self.WIDTH * 0.03)),
                        tag = 'gameover',
                        fill =self.COLOR_POWER_DOWN)
        self.canvas.create_rectangle(self.gameover_button_pos,
                                    outline= self.COLOR_POWER_DOWN,
                                    tag = 'gameover',)
        # if self.mouse_c and self.mouse_x and self.mouse_y

    def check_back_title(self):
        # タイトルに戻るボタンを押したかの判定
        if self.mouse_c and\
        self.gameover_button_pos[0] < self.mouse_x < self.gameover_button_pos[2] and\
        self.gameover_button_pos[1] < self.mouse_y < self.gameover_button_pos[3]:
            self.mouse_c = False
            return True

    def message_escape(self):
        # 脱走の文字を出す
        self.canvas.create_text(self.WIDTH * 1 / 2, self.bz_hi_1_2,
                                text = '脱走', font = (self.FONT , int(self.WIDTH * 0.40)),
                                tag='escape')

    def init_clear(self):
        # 仕切り直し用初期化
        self.canvas.delete('block')
        self.canvas.delete('ball')
        self.canvas.delete('cursor')
        self.canvas.delete('heart')
        self.canvas.delete('base')
        self.canvas.delete('state')
        self.canvas.delete('up')
        self.canvas.delete('down')
        self.canvas.delete('escape')
        self.canvas.delete('maki_get')
        self.canvas.delete('ten_get')
        self.ball_x = self.ball_x_init
        self.ball_y = self.ball_y_init
        self.mistake_flag = False # 外に出たフラグを元に戻す
        self.b_list = [] # b_listを元に戻す
        for _ in range(self.BLOCK_H):
            self.b_list.append([0] * self.BLOCK_W)
        self.block_hold = self.block_hold_max # ブロック保有数をmaxに戻す
        self.ball_xp = self.ball_xp_init   # ボールの速度リセット
        self.ball_yp = self.ball_yp_init
        

    def init_clear_back_title(self):
        # ゲームオーバーからの復帰用初期化
        self.canvas.delete('gameover')
        self.score = 0
        self.life = self.life_max
        self.block_hold_max = self.block_hold_max_init
        self.block_hold = self.block_hold_max

    def save_date_read(self):
        # セーブデータを読みこむ。なかったら生成する
        try:
            with open('save_date_HITSUJI.txt', 'r') as rfile:
                self.read_save_list = [int(i) for i in rfile.read().split()]
                self.hi_scores = self.read_save_list
        except:      
            with open('save_date_HITSUJI.txt', 'w') as wfile:
                for i in self.hi_scores:
                    print(i, file = wfile)
                self.read_save_list = self.hi_scores

    def save_date_write(self):
        # ハイスコア更新チェックとセーブデータ更新
        # チェック
        update_flag = False
        print(f'（デバッグ用）{self.hi_scores=}')
        for i in self.hi_scores:
            if self.score > i:
                update_flag = True
                break
        # ハイスコアリスト更新
        if update_flag:
            self.hi_scores.pop()
            self.hi_scores.append(self.score)
            self.hi_scores.sort(reverse=True)
        with open('save_date_HITSUJI.txt', 'w') as wfile:
            for i in self.hi_scores:
                    print(i, file = wfile)


    def debug_mouse_move(self):
        # デバッグ用色々表示
        self.canvas.delete('debug_mouse')
        self.canvas.create_text(int(self.WIDTH * 1 / 2),
                                int(self.HEIGHT * 0.05),
                                text = f'(デバッグ用)mx={self.mouse_x} my={self.mouse_y} mc={self.mouse_c} '
                                        f'Cx={self.cursor_x} Cy={self.cursor_y} '
                                        f'Bx={self.block_x} By={self.block_y} '
                                        f'スコア={self.score} life={self.life} index={self.index} '
                                        f'残りブロック={self.block_hold} '
                                        F'♡{self.life}/{self.life_max}',
                                fill= self.COLOR_WHITY, font = (self.FONT, int(self.WIDTH * 1 / 100)),
                                tag='debug_mouse')

    def main(self):
        if self.index == 0:
            # タイトル描画
            # セーブデータの処理もやる？　
            
            self.save_date_read()
            print(f'（デバッグ用）{self.hi_scores =} {self.read_save_list=}')
            self.draw_title()
            
            self.index = 1
        elif self.index == 1:
            # スタートボタン押し待ち
            self.click_title_button()
            if self.click_title_button():
                self.mouse_c = False
                self.index = 2
        elif self.index == 2:
            # 基礎を描画
            self.draw_back()
            self.draw_start_button()
            self.draw_state()
            self.index = 3
        elif self.index == 3:
            # スタート押し待ち
            if self.push_start_button():
                self.index = 4
        elif self.index == 4:
            # プレイヤーがブロック配置
            # ボールが画面外に出るまで
            self.draw_blocks()
            self.move_ball()
            self.draw_ball()
            self.draw_cursor()
            self.click_block()
            self.draw_state()
            if self.ten_flag: # 点ゲット判定
                self.draw_ten_get()
                self.ten_tmr = 0
            if self.maki_flag: # 薪ゲット判定
                self.draw_maki_get()
                self.maki_tmr =0
            self.maki_tmr += 1
            self.ten_tmr += 1
            if self.maki_tmr ==10:
                self.canvas.delete('maki_get')
            if self.ten_tmr ==10:
                self.canvas.delete('ten_get')
            if self.mistake_flag:
                self.canvas.delete('maki_get')
                self.canvas.delete('ten_get')
                self.message_escape()
                self.index =5
                self.tmr_miss = 0
        elif self.index == 5 :
                self.tmr_miss += 1
                if self.tmr_miss ==60:
                    self.tmr_miss = 0
                    self.index =6
        # elif self.index == 5:
        #     # 奈落に落ちた時の処理。
        #     # ハートの器と現在のハートを描画
        #     self.tmr_miss += 1
        #     if self.tmr_miss % 6 > 3:
        #         self.draw_heart_rest(True)
        #     else:
        #         self.draw_heart_rest(False)
        #     if self.tmr_miss == 30:
        #         self.tmr_miss = 0
        #         self.tmr_wait = 0
                
        #         self.index = 6

        elif self.index == 6:
            # ライフが一つ減ってゲームオーバー判定
            self.life -= 1 # ここでライフが1減る

            if self.life <= 0:
                self.index = 100
            else:
                self.index = 7
        elif self.index == 7:
            # 仕切り直しの処理
            
            self.init_clear()
            self.index = 2

        elif self.index == 100:
            # ハイスコア更新、ゲームオーバー
            self.save_date_write()
            self.init_clear()
            self.draw_game_over()
            self.index = 101

        elif self.index == 101:
            # クリック待ち
            if self.check_back_title():
                self.init_clear_back_title()
                self.index = 0

        self.canvas.bind('<Motion>', self.mouse_move)
        self.canvas.bind('<ButtonPress>', self.mouse_click)
        self.canvas.bind('<ButtonRelease>', self.mouse_release)
        # self.debug_mouse_move() # デバッグ用
        self.after(20, self.main)

def start():
    root = tkinter.Tk()
    app = App(root)
    app.mainloop()

if __name__ == '__main__':
    start()