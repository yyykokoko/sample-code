import random
import collections
import tkinter as tk

class Card():
    def __init__(self, suit, num):
        self.suit = suit
        self.num = num
        self.mark = None
    
    def get_suit(self):
        # スート、Joker
        if self.suit == 0:
            return 'Heart'
        elif self.suit == 1:
            return 'Spade'
        elif self.suit == 2:
            return 'Club'
        elif self.suit == 3:
            return 'Diamond'
        else:
            return 'Joker'

    def get_num(self):
        # 数字
        return self.num
    
    def get_mark(self):
        # マーク（数字とAKQJ、Jokerは0）
        if 2 <= self.num <= 10:
            self.mark = self.num
        elif self.num == 1:
            self.mark = 'A'
        elif self.num == 11:
            self.mark = 'J'
        elif self.num == 12:
            self.mark = 'Q'
        elif self.num == 13:
            self.mark = 'K'
        else:
            self.mark = 0
        return self.mark
        
    def get_sm(self):
        # 表示用。スートとマークを返す
        return self.get_suit(),self.get_mark()

class App(tk.Frame):
    # 定数
    WIDTH = 1000
    HEIGHT = 600
    FONT = 'Times New Roman'
    # 色
    COLOR_BACK = 'gray10' # 基盤となる黒地
    COLOR_BACK_FRAME = 'white' # 外側のフレーム専用white
    COLOR_WHITY = 'cornsilk' # 基盤となる白
    COLOR_TEXT_EMPHASIS = 'DarkGoldenrod3' # 強調文字色
    COLOR_CURSOR = 'green' # カーソルの色
    COLOR_CURSOR_HOLD = 'maroon3' # カーソル（HOLD）の色
    COLOR_OVER_CLEAR = '#441111' # クリア画面の色
    COLOR_CURSOR_HOLD_CON = 'gray10' # カーソル（HOLD）確定の色
    COLOR_FRAME_DENGER = 'red' # 状態：やばい借金
    COLOR_FRAME_CAUTION = 'yellow' # 状態：借金
    COLOR_FRAME_SAFETY = 'blue' # 状態：借金0
    COLOR_DIAMOND = 'blue' # ダイヤモンド
    COLOR_HEART = 'red' # ハート
    COLOR_CLUB = 'green' # クラブ
    COLOR_SPADE = 'black' # スペード
    # 各画面座標
    # 縦横の隙間
    SUKIMA_W = WIDTH * 1 / 50
    SUKIMA_H = HEIGHT * 31 / 1000
    SUKIMA_W_C = SUKIMA_W * 1 / 2
    SUKIMA_H_C = SUKIMA_H * 1 / 2
    # 全ての土台スタートゴールxy
    BACK_S_X = SUKIMA_W
    BACK_S_Y = SUKIMA_H
    BACK_G_X = WIDTH - SUKIMA_W
    BACK_G_Y = HEIGHT - SUKIMA_H
    # 土台の縦横サイズ
    BACK_WI = BACK_G_X - BACK_S_X
    BACK_HI = BACK_G_Y - BACK_S_Y
    # 役表スタートゴールxy
    ROLE_SCOPE_S_X = BACK_S_X + SUKIMA_W
    ROLE_SCOPE_S_Y = BACK_S_Y + SUKIMA_H
    ROLE_SCOPE_G_X = WIDTH * 1 / 3 - SUKIMA_W_C
    ROLE_SCOPE_G_Y = BACK_HI * 5 / 7 + ROLE_SCOPE_S_Y
    ROLE_SCOPE_POS = [ROLE_SCOPE_S_X, ROLE_SCOPE_S_Y, ROLE_SCOPE_G_X, ROLE_SCOPE_G_Y]
    # 役表縦横サイズ
    ROLE_SCOPE_WI = ROLE_SCOPE_G_X - ROLE_SCOPE_S_X
    ROLE_SCOPE_HI = ROLE_SCOPE_G_Y - ROLE_SCOPE_S_Y
    # 役の名前
    ROLE_NAME = ['ロイヤルフラッシュ','ストレートフラッシュ','フォーカード','フルハウス',
                 'フラッシュ','ストレート','スリーカード','ツーペア','J以上のワンペア','配当なし']
    ROLE_VALUE = [250, 50, 25, 9, 6, 4, 3, 2, 1, 0]

    # 役の倍率説明
    ROLE_VALUE_DEFO = ['250倍','50倍','25倍','9倍',
                       '6倍','4倍','3倍','2倍','1倍','0倍']
    # 役表個々の範囲
    ROLE_POS = []
    def cal_role_pos(self):
        self.ROLE_POS = []
        for i in range(len(self.ROLE_NAME)):
            self.ROLE_POS.append([self.ROLE_SCOPE_S_X + self.ROLE_SCOPE_WI * 1 / 20 ,
                                self.ROLE_SCOPE_S_Y + self.ROLE_SCOPE_HI * i / len(self.ROLE_NAME),
                                self.ROLE_SCOPE_S_X + self.ROLE_SCOPE_WI * 19 / 20,
                                self.ROLE_SCOPE_S_Y + self.ROLE_SCOPE_HI * (i+1) / len(self.ROLE_NAME)])
    # 右メニュー範囲スタートゴールxy
    R_MENU_SCOPE_S_X = ROLE_SCOPE_G_X + SUKIMA_W_C
    R_MENU_SCOPE_S_Y = ROLE_SCOPE_S_Y
    R_MENU_SCOPE_G_X = BACK_G_X - SUKIMA_W
    R_MENU_SCOPE_G_Y = ROLE_SCOPE_G_Y
    R_NEMU_SCOPE_POS = [R_MENU_SCOPE_S_X, R_MENU_SCOPE_S_Y, R_MENU_SCOPE_G_X, R_MENU_SCOPE_G_Y]
    # 右メニュー縦横サイズ
    R_MENU_WI = R_MENU_SCOPE_G_X - R_MENU_SCOPE_S_X
    R_MENU_HI = R_MENU_SCOPE_G_Y - R_MENU_SCOPE_S_Y
    # 右メニュー比率
    R_MENU_WI_1_2 = R_MENU_SCOPE_S_X + R_MENU_WI * 1 / 2
    R_MENU_HI_1_3 = R_MENU_SCOPE_S_Y + R_MENU_HI * 1 / 3
    R_MENU_HI_2_3 = R_MENU_SCOPE_S_Y + R_MENU_HI * 2 / 3
    # 情報表示範囲スタートゴールxy
    INFO_SCOPE_S_X = R_MENU_SCOPE_S_X + SUKIMA_W_C
    INFO_SCOPE_S_Y = R_MENU_SCOPE_S_Y + SUKIMA_H_C
    INFO_SCOPE_G_X = R_MENU_SCOPE_S_X + (R_MENU_WI * 1 / 2)
    INFO_SCOPE_G_Y = R_MENU_SCOPE_S_Y + SUKIMA_H_C + R_MENU_HI * 4 / 9
    INFO_SCOPE_POS = [INFO_SCOPE_S_X, INFO_SCOPE_S_Y, INFO_SCOPE_G_X, INFO_SCOPE_G_Y]
    # 情報表示範囲縦横サイズ
    INFO_SCOPE_WI = INFO_SCOPE_G_X - INFO_SCOPE_S_X
    INFO_SCOPE_HI = INFO_SCOPE_G_Y - INFO_SCOPE_S_Y
    # 情報表示範囲　文字スタート
    INFO_SCOPE_TEXT_S_X = INFO_SCOPE_S_X + INFO_SCOPE_WI * 0.03
    INFO_SCOPE_TEXT_S_Y = INFO_SCOPE_S_Y + INFO_SCOPE_HI * 0.03
    # クレジット表示範囲
    CREJIT_SCOPE_S_X = INFO_SCOPE_G_X + SUKIMA_W_C
    CREJIT_SCOPE_S_Y = INFO_SCOPE_S_Y
    CREJIT_SCOPE_G_X = R_MENU_SCOPE_G_X - SUKIMA_W_C
    CREJIT_SCOPE_G_Y = INFO_SCOPE_G_Y
    CREJIT_SCOPE_POS =[CREJIT_SCOPE_S_X, CREJIT_SCOPE_S_Y, CREJIT_SCOPE_G_X, CREJIT_SCOPE_G_Y]
    # クレジット表示範囲縦横サイズ
    CREJIT_SCOPE_WI = CREJIT_SCOPE_G_X - CREJIT_SCOPE_S_X
    CREJIT_SCOPE_HI = CREJIT_SCOPE_G_Y - CREJIT_SCOPE_S_Y
    # クレジット表示範囲中点xy
    CREJIT_SCOPE_C_X = CREJIT_SCOPE_S_X + CREJIT_SCOPE_WI * 1 / 2
    CREJIT_SCOPE_C_Y = CREJIT_SCOPE_S_Y + CREJIT_SCOPE_HI * 1 / 2
    # カードの範囲 描画されないからsukimaはいらない
    CARD_SCOPE_S_X = INFO_SCOPE_S_X
    CARD_SCOPE_S_Y = INFO_SCOPE_G_Y + SUKIMA_H_C
    CARD_SCOPE_G_X = CREJIT_SCOPE_G_X
    CARD_SCOPE_G_Y = R_MENU_SCOPE_G_Y - SUKIMA_H_C
    CARD_SCOPE_POS = [CARD_SCOPE_S_X, CARD_SCOPE_S_Y, CARD_SCOPE_G_X, CARD_SCOPE_G_Y]
    # カードの範囲の縦横サイズ
    CARD_SCOPE_WI = CARD_SCOPE_G_X - CARD_SCOPE_S_X
    CARD_SCOPE_HI = CARD_SCOPE_G_Y - CARD_SCOPE_S_Y
    # カードの上に表示される役名範囲
    CARD_ROLE_S_X = CARD_SCOPE_S_X
    CARD_ROLE_S_Y = CARD_SCOPE_S_Y + CARD_SCOPE_HI * 2 / 5
    CARD_ROLE_G_X = CARD_SCOPE_G_X
    CARD_ROLE_G_Y = CARD_SCOPE_S_Y + CARD_SCOPE_HI * 3 / 5
    CARD_ROLE_POS = [CARD_ROLE_S_X, CARD_ROLE_S_Y, CARD_ROLE_G_X, CARD_ROLE_G_Y]
    # カードの上に表示される役名範囲の縦横サイズ
    CARD_ROLE_WI = CARD_ROLE_G_X - CARD_ROLE_S_X
    CARD_ROLE_HI = CARD_ROLE_G_Y - CARD_ROLE_S_Y
    # カードの上に表示される役名範囲の中央座標
    CARD_ROLE_C_X = CARD_ROLE_S_X + CARD_ROLE_WI * 1 / 2
    CARD_ROLE_C_Y = CARD_ROLE_S_Y + CARD_ROLE_HI * 1 / 2
    # メッセージ範囲
    MSG_SCOPE_S_X = ROLE_SCOPE_S_X
    MSG_SCOPE_S_Y = ROLE_SCOPE_G_Y + SUKIMA_H_C
    MSG_SCOPE_G_X = R_MENU_SCOPE_G_X
    MSG_SCOPE_G_Y = BACK_G_Y - SUKIMA_H
    MSG_SCOPE_POS = [MSG_SCOPE_S_X, MSG_SCOPE_S_Y, MSG_SCOPE_G_X, MSG_SCOPE_G_Y]
    # メッセージ範囲縦横サイズ
    MSG_SCOPE_WI = MSG_SCOPE_G_X - MSG_SCOPE_S_X
    MSG_SCOPE_HI = MSG_SCOPE_G_Y - MSG_SCOPE_S_Y
    # メッセージ範囲中点xy
    MSG_SCOPE_C_X = MSG_SCOPE_S_X + MSG_SCOPE_WI * 1 / 2
    MSG_SCOPE_C_Y = MSG_SCOPE_S_Y + MSG_SCOPE_HI * 1 / 2
    # ウィンドウ範囲
    WINDOW_SCOPE_S_X = ROLE_SCOPE_S_X
    WINDOW_SCOPE_S_Y = ROLE_SCOPE_S_Y
    WINDOW_SCOPE_G_X = R_MENU_SCOPE_G_X
    WINDOW_SCOPE_G_Y = R_MENU_SCOPE_G_Y
    WINDOW_SCOPE_POS = [WINDOW_SCOPE_S_X, WINDOW_SCOPE_S_Y, WINDOW_SCOPE_G_X, WINDOW_SCOPE_G_Y]
    # ウィンドウ　縦横サイズ
    WINDOW_SCOPE_WI = WINDOW_SCOPE_G_X - WINDOW_SCOPE_S_X
    WINDOW_SCOPE_HI = WINDOW_SCOPE_G_Y - WINDOW_SCOPE_S_Y
    # ウィンドウ範囲中点xy
    WINDOW_SCOPE_C_X = WINDOW_SCOPE_S_X + WINDOW_SCOPE_WI * 1 / 2
    WINDOW_SCOPE_C_Y = WINDOW_SCOPE_S_Y + WINDOW_SCOPE_HI * 1 / 2
    # okボタン範囲
    BUTTON_OK_S_X = MSG_SCOPE_S_X + MSG_SCOPE_WI * 3 / 7
    BUTTON_OK_S_Y = MSG_SCOPE_S_Y + MSG_SCOPE_HI * 6 / 11
    BUTTON_OK_G_X = MSG_SCOPE_S_X + MSG_SCOPE_WI * 4 / 7
    BUTTON_OK_G_Y = MSG_SCOPE_S_Y + MSG_SCOPE_HI * 10 / 11
    BUTTON_OK_POS = [BUTTON_OK_S_X, BUTTON_OK_S_Y, BUTTON_OK_G_X, BUTTON_OK_G_Y]
    # okボタン縦横サイズ
    BUTTON_OK_WI = BUTTON_OK_G_X - BUTTON_OK_S_X
    BUTTON_OK_HI = BUTTON_OK_G_Y - BUTTON_OK_S_Y
    # okボタン中点xy
    BUTTON_OK_C_X = BUTTON_OK_S_X + BUTTON_OK_WI * 1 / 2
    BUTTON_OK_C_Y = BUTTON_OK_S_Y + BUTTON_OK_HI * 1 / 2
    # ABボタン
    BUTTON_A_S_X = MSG_SCOPE_S_X + MSG_SCOPE_WI * 1 / 5
    BUTTON_A_S_Y = MSG_SCOPE_C_Y + SUKIMA_H_C
    BUTTON_A_G_X = MSG_SCOPE_S_X + MSG_SCOPE_WI * 2 / 5
    BUTTON_A_G_Y = MSG_SCOPE_G_Y - SUKIMA_H_C
    BUTTON_A_POS =[BUTTON_A_S_X, BUTTON_A_S_Y, BUTTON_A_G_X, BUTTON_A_G_Y]
    BUTTON_B_S_X = MSG_SCOPE_S_X + MSG_SCOPE_WI * 3 / 5
    BUTTON_B_S_Y = MSG_SCOPE_C_Y + SUKIMA_H_C
    BUTTON_B_G_X = MSG_SCOPE_S_X + MSG_SCOPE_WI * 4 / 5
    BUTTON_B_G_Y = MSG_SCOPE_G_Y - SUKIMA_H_C
    BUTTON_B_POS = [BUTTON_B_S_X, BUTTON_B_S_Y, BUTTON_B_G_X, BUTTON_B_G_Y]
    # ABボタン縦横サイズ
    BUTTON_A_WI = BUTTON_A_G_X - BUTTON_A_S_X
    BUTTON_A_HI = BUTTON_A_G_Y - BUTTON_A_S_Y
    BUTTON_B_WI = BUTTON_B_G_X - BUTTON_B_S_X
    BUTTON_B_HI = BUTTON_B_G_Y - BUTTON_B_S_Y
    # ABボタン中点xy
    BUTTON_A_C_X = BUTTON_A_S_X + BUTTON_A_WI * 1 / 2
    BUTTON_A_C_Y = BUTTON_A_S_Y + BUTTON_A_HI * 1 / 2
    BUTTON_B_C_X = BUTTON_B_S_X + BUTTON_B_WI * 1 / 2
    BUTTON_B_C_Y = BUTTON_B_S_Y + BUTTON_B_HI * 1 / 2
    # 5ボタンの範囲
    BUTTON_5_POS = []
    def cal_five_button_pos(self):
        self.BUTTON_5_POS = []
        for i in range(len(self.BET_VALUE)):
            # 各ボックスの座標、サイズ
            box_s_x = self.MSG_SCOPE_S_X + self.MSG_SCOPE_WI * 1 / len(self.BET_VALUE) + (self.MSG_SCOPE_WI * i / 8)
            box_s_y = self.MSG_SCOPE_S_Y + self.MSG_SCOPE_HI * 4 / 7
            box_g_x = self.MSG_SCOPE_S_X + self.MSG_SCOPE_WI * 1 / len(self.BET_VALUE) + (self.MSG_SCOPE_WI * (i + 1) / 8) - self.SUKIMA_W_C
            box_g_y = self.MSG_SCOPE_S_Y + self.MSG_SCOPE_HI * 6 / 7
            box_wi = box_g_x - box_s_x
            box_hi = box_g_y - box_s_y
            box_c_x = box_s_x + box_wi * 1 / 2
            box_c_y = box_s_y + box_hi * 1 / 2
            # [0]ボタン0番 [1]ボタン1番 [2]ボタン2番 [3]ボタン3番 [4]ボタン4番
            # [0]s_x [1]s_y [2]g_x [3]g_y [4]wi [5]hi [6]c_x [7]c_y 
            self.BUTTON_5_POS.append([box_s_x, box_s_y, box_g_x, box_g_y, box_wi, box_hi, box_c_x, box_c_y])

    # 数値セット
    # タイトル画面 はじめからボタン つづきからボタン
    BUTTON_TITLE_HAJIME = [WIDTH * 1 / 7, HEIGHT * 12 / 16, WIDTH * 3 / 7, HEIGHT * 14 / 16]
    BUTTON_TITLE_TUDUKI = [WIDTH * 4 / 7, HEIGHT * 12 / 16, WIDTH * 6 / 7, HEIGHT * 14 / 16]
    # 掛け金額5種類
    BET_VALUE = [1, 5, 10, 25, 50]
    # 借金、返済選択肢
    LOAN_REPAY_VALUE = [5, 10, 25, 50, 100]
    # トロフィー価格
    TROPHY_PRICE_START = 10 # 最初の価格
    TROPHY_PRICE_RATE = 1.13 # 価格上昇レート 1.17はたるい1.12もたるい
    SKULL_APPER_LOAN = 50 # どくろが登場する借金額 100はたるい 30は低すぎ
    # ゲームオーバー、ゲームクリア基準数値
    GAME_OVER_SKULL_NUM = 20 # どくろの数がこれを超えたらゲームオーバー
    GAME_CLEAR_TROPHY_NUM = 20 # トロフィの数がこれを超えたらクリア

    # 初期値
    index = 0
    mouse_x = 0
    mouse_y = 0
    mouse_c = False
    p_hand = [] # プレイヤーハンド
    c_list = [] # トランプ
    hand_max = 5 # 配られるカードの枚数 
    hold_card =[] # ホールドしているカードのonとoff
    bet = 0 # 掛け金
    bet_info = 0 # 仮の掛け金
    flag_bet = False # ベットしたかのフラグ
    tmr_card = 0 # カードめくるときのtmr
    count_change_init = 2 # チェンジ回数初期値
    count_change = count_change_init
    hands_count_list = [0,0,0,0,0,0,0,0,0,0] # 各役の発生回数
    hold_card_list = [False, False, False, False, False]
    count_interest = 0
    count_interest_max = 5 # 借金しているとこの回数のたびに利子が入る
    INTEREST_RATE = 1.6 # 一回の利子で増加する倍率
    buyer_twice_flag = False # 訪問販売員が二回目の登場かを調べる
    tmr = 0 # どくろとトロフィーアニメーション用tmr
    credit_init = 1 # クレジット初期値 1
    credit = credit_init
    loan = 0 # 借金
    skull = 0 
    trophy = 0
    save_list_read = []
    save_list_now =[] # credit, loan, trophy, count_interest, hands_count_listの各要素　全14要素
    save_date_already_flag = False # 既存のデータがあるかのフラグ
    game_clear_flag = False # ゲームをクリアしたかのフラグ

    def __init__(self, master = None):
        super().__init__(master)
        self.master.title('借金前提ポーカー')
        self.canvas = tk.Canvas(self.master, width=self.WIDTH, height=self.HEIGHT, bg=self.COLOR_BACK)
        self.canvas.pack()
        self.yamikin_image = tk.PhotoImage(file='yamikin.png')
        self.trophy_buyer_image = tk.PhotoImage(file='trophy_buyer.png')
        self.sukll_image_l_01 = tk.PhotoImage(file='skul_l_image01.png')
        self.sukll_image_l_02 = tk.PhotoImage(file='skul_l_image02.png')
        self.sukll_image_l_03 = tk.PhotoImage(file='skul_l_image03.png')
        self.sukll_image_r_01 = tk.PhotoImage(file='skul_r_image01.png')
        self.sukll_image_r_02 = tk.PhotoImage(file='skul_r_image02.png')
        self.sukll_image_r_03 = tk.PhotoImage(file='skul_r_image03.png')
        self.trophy_image01 = tk.PhotoImage(file='trophy_image01.png')
        self.trophy_image02 = tk.PhotoImage(file='trophy_image02.png')
        self.trophy_image03 = tk.PhotoImage(file='trophy_image03.png')
        self.sukll_image_l_list = [self.sukll_image_l_01, self.sukll_image_l_02, self.sukll_image_l_03]
        self.sukll_image_r_list = [self.sukll_image_r_01, self.sukll_image_r_02, self.sukll_image_r_03]
        self.trophy_image_list = [self.trophy_image01, self.trophy_image02, self.trophy_image03]
        self.main()
        
    def mouse_move(self, e):
        # マウスの動きを感知
        self.mouse_x = e.x
        self.mouse_y = e.y

    def mouse_click(self, e):
        # マウスクリックを感知
        self.mouse_c = True

    def mouse_release(self, e):
        # マウスリリースを感知
        self.mouse_c = False

    def create_heart(self, center_x, center_y, size, **kwargs):
        # ハートを描く
        points = [
            center_x - size * 1 / 2, center_y - size * 1 / 2, # 1
            center_x, center_y,] # 2  
        self.canvas.create_oval(points, width = 0, fill = self.COLOR_HEART, tag = 'card',  **kwargs)

        points = [
            center_x, center_y - size * 1 / 2, # 1
            center_x + size * 1 / 2, center_y,] # 2  
        self.canvas.create_oval(points, width = 0, fill = self.COLOR_HEART, tag = 'card', **kwargs)

        points = [
            center_x - size * 3 / 5, center_y - size * 1 / 4, # s
            center_x - size * 2 / 16, center_y + size * 1 / 4,
            center_x, center_y + size * 1 / 2, # c
            center_x + size * 2 / 16, center_y + size * 1 / 4,
            center_x + size * 3 / 5, center_y - size * 1 / 4,
            center_x, center_y - size * 1 / 4] # G
        self.canvas.create_polygon(points, smooth = True, fill = self.COLOR_HEART, tag = 'card', **kwargs)
    
    def create_diamond(self, center_x, center_y, size, **kwargs):
        # ダイヤモンドを描く
        points = [
            center_x, center_y - size * 1 / 2, # S
            center_x - size * 1 / 50, center_y - size * 10 / 24, #SL
            center_x - size * 1 / 8, center_y - size * 1 / 8,
            center_x - size * 8 / 24, center_y - size * 1 / 50, #LS
            center_x - size * 3 / 8, center_y, # L
            center_x - size * 8 / 24, center_y + size * 1 / 50, #LC
            center_x - size * 1 / 8, center_y + size * 1 / 8,
            center_x - size * 1 / 50, center_y + size * 10 / 24, #CL
            center_x,center_y + size * 1 / 2, # C
            center_x + size * 1 / 50, center_y + size * 10 / 24, #CR
            center_x + size * 1 / 8, center_y + size * 1 / 8,
            center_x + size * 8 / 24, center_y + size * 1 / 50, #RC
            center_x + size * 3 / 8, center_y, # R
            center_x + size * 8 / 24, center_y - size * 1 / 50, #RS
            center_x + size * 1 / 8, center_y - size * 1 / 8,
            center_x + size * 1 / 50, center_y - size * 10 / 24,] #SR
        self.canvas.create_polygon(points ,width = 0 , fill = self.COLOR_DIAMOND, smooth=True, tag = 'card',**kwargs)
        
    def create_club(self, center_x, center_y, size, **kwargs):
        # クラブを描く
        points =[center_x - size * 1 / 2,
                 center_y - size * 1 / 6,
                 center_x,
                 center_y + size * 2 / 6]
        self.canvas.create_oval(points, width = 0, fill = self.COLOR_CLUB, tag = 'card', **kwargs)

        points =[center_x,
                 center_y - size * 1 / 6,
                 center_x + size * 1 / 2,
                 center_y + size * 2 / 6]
        self.canvas.create_oval(points, width = 0, fill = self.COLOR_CLUB, tag = 'card', **kwargs)

        points =[center_x - size * 1 / 4,
                 center_y - size * 1 / 2,
                 center_x + size * 1 / 4,
                 center_y]
        self.canvas.create_oval(points, width = 0, fill = self.COLOR_CLUB, tag = 'card', **kwargs)

        points =[center_x - size * 1 / 8, center_y - size * 1 / 4,
                 center_x - size * 1 / 8, center_y + size * 7 / 16,
                 center_x - size * 1 / 4, center_y + size * 7 / 16,
                 center_x - size * 1 / 4, center_y + size * 1 / 2,
                 center_x + size * 1 / 4, center_y + size * 1 / 2,
                 center_x + size * 1 / 4, center_y + size * 7 / 16,
                 center_x + size * 1 / 8, center_y + size * 7 / 16,
                 center_x + size * 1 / 8, center_y - size * 1 / 4,]
        self.canvas.create_polygon(points, width = 0, fill = self.COLOR_CLUB, tag = 'card', **kwargs)

    def create_spade(self, center_x, center_y, size, **kwargs):
        # スペードを描く
        points =[center_x - size * 5 / 12,
                 center_y,
                 center_x,
                 center_y + size * 5 / 12
        ]
        self.canvas.create_oval(points, width = 0, fill = self.COLOR_SPADE, tag = 'card', **kwargs)

        points =[center_x,
                 center_y,
                 center_x + size * 5 / 12,
                 center_y + size * 5 / 12
        ]
        self.canvas.create_oval(points, width = 0, fill = self.COLOR_SPADE, tag = 'card', **kwargs)

        points =[center_x - size * 1 / 8, center_y,
                 center_x - size * 1 / 8, center_y + size * 7 / 16,
                 center_x - size * 1 / 4, center_y + size * 7 / 16,
                 center_x - size * 1 / 4, center_y + size * 1 / 2,
                 center_x + size * 1 / 4, center_y + size * 1 / 2,
                 center_x + size * 1 / 4, center_y + size * 7 / 16,
                 center_x + size * 1 / 8, center_y + size * 7 / 16,
                 center_x + size * 1 / 8, center_y,]
        self.canvas.create_polygon(points, width = 0, fill = self.COLOR_SPADE, tag = 'card', **kwargs)

        points =[center_x, center_y - size * 1 / 2, # S
                 center_x - size * 1 / 20, center_y - size * 5 / 12, # SL
                 center_x - size * 1 / 6, center_y - size * 2 / 12,
                 center_x - size * 7 / 20,  center_y + size* 1 / 20, # LS
                 center_x - size * 8 / 20, center_y + size * 2 / 12, # L
                 center_x, center_y + size * 1 / 4, # C
                 center_x + size * 8 / 20, center_y + size * 2 / 12, # R
                 center_x + size * 7 / 20, center_y + size* 1 / 20, # RS
                 center_x + size * 1 / 6, center_y - size * 2 / 12,
                 center_x + size * 1 / 20, center_y - size * 5 / 12,] # SR
        self.canvas.create_polygon(points, smooth=True, fill = self.COLOR_SPADE, tag = 'card', **kwargs)

    def check_role_straight(self, num_list):
        # 連番かのチェック ロイヤル以外
        setsort = set(num_list)
        list2 = list(setsort)
        sort_list = sorted(list2)
        # ソートして重複を取り払う
        count = 0
        flag = False
        for i in range(1, len(sort_list)):
            if sort_list[i] == sort_list[i-1] + 1:
                count += 1
        if count >= 4:
            # count4以上　つまり連番5枚以上
            flag = True
        return flag

    def check_role_pair(self, num_list):
        # ペアのチェック
        check_num_dict = collections.Counter(num_list)
        flag_three = False
        flag_two = 0
        for val in check_num_dict.values():
            if val == 4:
                return 2 # フォーカード
            if val == 3:
                flag_three = True
            if val == 2:
                flag_two += 1

        if flag_three:
            if flag_two == 1:
                return 3 # フルハウス
            return 6 # スリーカード

        if flag_two >= 2:
            return 7 # ツーペア
        for k,v in check_num_dict.items():
            if v >= 2:
                if k in [11, 12, 13, 1]:
                    return 8 # J以上のワンペア
                else:
                    return 9 # 配当なし
        return 9 # 配当なし

    def check_role_flash(self, suit_list):
        # フラッシュ判定 5枚以上同じスートならフラッシュ判定
        flag = False
        check_dict = collections.Counter(suit_list)
        for val in check_dict.values():
            if val >= 5:
                flag = True
        return flag


    def check_role(self):
        # 役のチェック
        flag_flash = False
        flag_royal = False
        flag_straight = False
        num_list = []
        suit_list = []
        mark_list = [] # JQKA表示用
        for i in range(len(self.p_hand)):
            num_list.append(self.p_hand[i].get_num())
        for i in range(len(self.p_hand)):
            suit_list.append(self.p_hand[i].get_suit())
        for i in range(len(self.p_hand)):
            mark_list.append(self.p_hand[i].get_mark())
        sort_list = sorted(num_list)
        flag_flash = self.check_role_flash(suit_list)
        flag_straight = self.check_role_straight(num_list)
        if sort_list[0] == 1 and sort_list[1] == 10 and sort_list[2] == 11 and\
           sort_list[3] == 12 and sort_list[4] == 13:
            flag_royal = True
                
        if flag_flash and flag_royal:
            return 0 # ロイヤルフラッシュ

        if flag_flash and flag_straight:
            return 1 # ストレートフラッシュ
        if flag_flash:
            return 4 # フラッシュ
        if flag_straight:
            return 5 # ストレート
        if flag_royal:
            return 5 # ストレート(ロイヤル)
        return self.check_role_pair(num_list)

    def role_cal(self, role_num):
        # 役の最終判断
        if role_num == 0:
            role = 'ロイヤルフラッシュ'
        elif role_num == 1:
            role = 'ストレートフラッシュ'
        elif role_num== 2:
            role = 'フォーカード'
        elif role_num == 3:
            role = 'フルハウス'
        elif role_num == 4:
            role = 'フラッシュ'
        elif role_num == 5:
            role = 'ストレート'
        elif role_num == 6:
            role = 'スリーカード'
        elif role_num == 7:
            role = 'ツーペア'
        elif role_num == 8:
            role = 'J以上のワンペア'
        elif role_num == 9:
            role = '配当なし'
        return role

    def draw_title(self):
        # タイトル画面
        self.canvas.create_text(self.WIDTH * 1 / 2, self.HEIGHT * 1 / 3,
                                text= '借金前提ポーカー',
                                font=(self.FONT, int(self.WIDTH * 0.05)),
                                fill = self.COLOR_WHITY, tag= 'title')
        self.canvas.create_text(self.WIDTH * 0.38, self.HEIGHT * 0.50,
                                text= 'トロフィーを買い集めよう\n\n'\
                                      ' 借金しすぎに注意',
                                anchor='nw',
                                font=(self.FONT, int(self.WIDTH * 0.02)),
                                fill = self.COLOR_WHITY, tag= 'title')
        self.canvas.create_image(self.WIDTH * 0.35,
                                 self.HEIGHT * 0.52,
                                 image=self.trophy_image01, tag= 'title')
        self.canvas.create_image(self.WIDTH * 0.35,
                                 self.HEIGHT * 0.63,
                                 image=self.sukll_image_r_01, tag= 'title')
        # はじめからボタン
        self.canvas.create_rectangle(self.BUTTON_TITLE_HAJIME,
                                     outline=self.COLOR_TEXT_EMPHASIS,
                                     tag= 'title')
        self.canvas.create_text(self.WIDTH * 2 / 7,
                                self.HEIGHT * 13 / 16,
                                text ='はじめから',
                                fill=self.COLOR_TEXT_EMPHASIS,
                                font = (self.FONT, int((self.WIDTH * 2 / 7) * 0.12)),
                                tag= 'title')
                                
        # つづきからボタン
        if self.save_date_already_flag:
            # 既存のデータがあるなら色が黄色
            model_color = self.COLOR_TEXT_EMPHASIS
        else:
            model_color = self.COLOR_WHITY
        self.canvas.create_rectangle(self.BUTTON_TITLE_TUDUKI,
                                     outline=model_color,
                                     tag= 'title')
        self.canvas.create_text(self.WIDTH * 5 / 7,
                                self.HEIGHT * 13 / 16,
                                text ='つづきから',
                                fill=model_color,
                                font = (self.FONT, int((self.WIDTH * 2 / 7) * 0.12)),
                                tag= 'title')

    def click_button_title(self):
        # タイトルのボタンが押されたかの判定 セーブデータがないなら続きからは選べないように
        self.canvas.delete('title_curcor')
        if self.BUTTON_TITLE_HAJIME[0] < self.mouse_x < self.BUTTON_TITLE_HAJIME[2] and\
        self.BUTTON_TITLE_HAJIME[1] < self.mouse_y < self.BUTTON_TITLE_HAJIME[3]:
                # はじめからボタン
                self.canvas.create_rectangle(self.BUTTON_TITLE_HAJIME,
                                             width=6,tag ='title_curcor',
                                             outline= self.COLOR_CURSOR)
                if self.mouse_c:
                    self.mouse_c = False
                    self.canvas.delete('title')
                    self.canvas.delete('title_curcor')
                    self.init_save_list_now()
                    self.save_date_write() # 空のリストをセーブデータに上書きして記録消去
                    return True
                
        if self.save_date_already_flag:
             # 既存データがあるならつづきからボタンが選択できる
            if self.BUTTON_TITLE_TUDUKI[0] < self.mouse_x < self.BUTTON_TITLE_TUDUKI[2] and\
                self.BUTTON_TITLE_TUDUKI[1] < self.mouse_y < self.BUTTON_TITLE_TUDUKI[3] :
                self.canvas.create_rectangle(self.BUTTON_TITLE_TUDUKI,
                                                width=6,tag ='title_curcor',
                                                outline= self.COLOR_CURSOR)
                if self.mouse_c:
                        self.mouse_c = False
                        self.canvas.delete('title')
                        self.canvas.delete('title_curcor')
                        self.save_date_read()
                        return True
        # if self.mouse_c == True: 
        #     if self.BUTTON_SCOPE_TITLE[0] < self.mouse_x < self.BUTTON_SCOPE_TITLE[2]and\
        #     self.BUTTON_SCOPE_TITLE[1] < self.mouse_y < self.BUTTON_SCOPE_TITLE[3] :
        #         self.mouse_c = False
        #         self.canvas.delete('title')
                # return True
        

    def draw_state_color_frame(self):
        # 借金の具合で周りの線の色が変わる
        self.canvas.delete('frame_state')
        self.canvas.create_rectangle(self.BACK_S_X, self.BACK_S_Y, self.BACK_G_X, self.BACK_G_Y,
                                     outline=self.COLOR_BACK_FRAME,width = 5, tag= 'frame_state')
        if self.skull <= 0:
            # 借金なし
            model_color = self.COLOR_FRAME_SAFETY
        elif 0 < self.skull < self.GAME_OVER_SKULL_NUM // 2:
            # 借金している
            model_color = self.COLOR_FRAME_CAUTION
        elif self.GAME_OVER_SKULL_NUM // 2 <=self.skull:
            # どくろが上限の半分以上出るくらい借金している
            model_color = self.COLOR_FRAME_DENGER
        self.canvas.create_rectangle(self.BACK_S_X, self.BACK_S_Y, self.BACK_G_X, self.BACK_G_Y,
                                     outline = model_color,width = 2, tag= 'frame_state')
        
    def draw_menu(self):
        # ゲーム画面のベースを描く。　クレジット賭けメニュ、借金メニュ、お買い物メニュ以外
        self.canvas.delete('base')
        model_outline = {'outline':self.COLOR_WHITY, 'width':2, 'tag':'base'}
        # 役表
        self.canvas.create_rectangle(self.ROLE_SCOPE_POS, **model_outline)
        # 役表個々の範囲(目安)
        # for i in range(9):
        #     self.canvas.create_rectangle(self.ROLE_POS[i],
        #                                 outline=self.COLOR_WHITY,
        #                                 width=1,tag ='test')
        # 役名個々の文字
        for i in range(len(self.ROLE_NAME)):
            self.canvas.create_text(self.ROLE_POS[i][0],
                                    self.ROLE_POS[i][1] + (self.ROLE_POS[i][3] - self.ROLE_POS[i][1]) * 1 / 2,
                                    text=self.ROLE_NAME[i],
                                    font = (self.FONT, 14), fill = self.COLOR_WHITY,
                                    anchor='sw', tag='base')
        # 右のメニュー範囲
        self.canvas.create_rectangle(self.R_NEMU_SCOPE_POS, **model_outline)
        # 情報表示範囲
        self.canvas.create_rectangle(self.INFO_SCOPE_POS, **model_outline)
        # 賭けたクレジットの表示範囲
        self.canvas.create_rectangle(self.CREJIT_SCOPE_POS, **model_outline)
        # カードの範囲
        for i in range(self.hand_max):
            s_x = self.CARD_SCOPE_S_X + self.CARD_SCOPE_WI * i / self.hand_max + self.SUKIMA_W * 1 / 8
            s_y = self.CARD_SCOPE_S_Y + self.SUKIMA_H * 1 / 8
            g_x = (self.CARD_SCOPE_S_X + self.CARD_SCOPE_WI * (i+1) / self.hand_max) - self.SUKIMA_W * 1 / 8
            g_y =self.ROLE_SCOPE_G_Y - self.SUKIMA_H_C
            self.canvas.create_rectangle(s_x, s_y, g_x, g_y, fill = 'DarkRed', **model_outline)
            self.canvas.create_rectangle(s_x + 10, s_y + 10, g_x - 10, g_y - 10, 
                                         outline=self.COLOR_CURSOR, tag='base',
                                         width = 1)
            self.canvas.create_rectangle(s_x + 20, s_y + 20, g_x - 20, g_y - 20, 
                                         outline=self.COLOR_CURSOR, tag='base',
                                         width = 1)
            self.canvas.create_rectangle(s_x + 23, s_y + 23, g_x - 23, g_y - 23,
                                         outline=self.COLOR_CURSOR, tag='base',
                                         width = 1)
        # メッセージ範囲
        self.canvas.create_rectangle(self.MSG_SCOPE_POS, **model_outline)
        # ウィンドウ範囲(目安)
        # self.canvas.create_rectangle(self.WINDOW_SCOPE_POS, **model_outline)
        # 次のトロフィーの値段
        self.canvas.create_text(self.INFO_SCOPE_G_X - self.INFO_SCOPE_WI * 0.03,
                                self.INFO_SCOPE_G_Y,
                                text=f'目標:{self.display_credit(self.cal_trophy_val())}',
                                anchor='se',
                                tag = 'base',
                                fill=self.COLOR_WHITY,
                                font = (self.FONT, int(self.INFO_SCOPE_WI * 0.05)))
        # 現在のplay回数を表示する
        self.canvas.create_text(self.INFO_SCOPE_G_X - self.INFO_SCOPE_WI * 0.03,
                                self.INFO_SCOPE_G_Y - self.INFO_SCOPE_HI * 0.15,
                                text=f'{sum(self.hands_count_list)+1}回目',
                                anchor='se',
                                tag = 'base',
                                fill=self.COLOR_WHITY,
                                font = (self.FONT, int(self.INFO_SCOPE_WI * 0.05)))

                
        
    
    def draw_magnification(self):
        # 掛け金に応じて倍率を描写
        self.canvas.delete('mag')
        for i in range(len(self.ROLE_NAME)):
            if self.bet_info == 0:
                model_text = self.ROLE_VALUE_DEFO[i]
            elif self.bet_info > 0:
                model_text = f'+{self.ROLE_VALUE[i] * self.bet_info}億円'

            self.canvas.create_text(self.ROLE_POS[i][0],
                                    self.ROLE_POS[i][1] + 18,
                                    text=model_text,
                                    font = (self.FONT, 14), fill = self.COLOR_TEXT_EMPHASIS,
                                    anchor='nw', tag='mag')
            
    def message(self,message):
        # メッセージボックスにメッセージを表示させる
        self.canvas.delete('message')
        self.canvas.create_text(self.MSG_SCOPE_C_X,
                                self.MSG_SCOPE_S_Y + self.MSG_SCOPE_HI * 1 / 3,
                                text = f'{message}',fill=self.COLOR_WHITY,
                                font = (self.FONT, int(self.MSG_SCOPE_WI * 0.03)),
                                tag='message')
        
    def draw_role_info(self):
        # マウスオーバーで役の説明を情報表示範囲に出す
        self.canvas.delete('info_role')
        info_role_list = [f'☆ロイヤルフラッシュ\n\n全て同じマークで\n10,J,Q,K,Aが揃う役',
                          f'☆ストレートフラッシュ\n\n全て同じマークで\n全て連続した数字で揃う役',
                          f'☆フォーカード\n\n4枚同じ数字が揃う役',
                          f'☆フルハウス\n\n数字のペアが\n3枚と2枚で揃う役',
                          f'☆フラッシュ\n\n全て同じマークで揃う役',
                          f'☆ストレート\n\n全て連続した数字で揃う役',
                          f'☆スリーカード\n\n3枚同じ数字が揃う役',
                          f'☆ツーペア\n\n2枚同じ数字のペアが\n2つ揃う役',
                          f'☆J以上のワンペア\n\nJ以上で同じ数字が\n2枚揃う役',
                          f'☆配当なし\n\n10以下で同じ数字が\n2枚揃うか\nどの役にも合致しない'
                          ]
        for i in range(len(self.ROLE_POS)):
            if self.ROLE_POS[i][0] < self.mouse_x < self.ROLE_POS[i][2] and\
            self.ROLE_POS[i][1] < self.mouse_y < self.ROLE_POS[i][3]:
                self.canvas.create_rectangle(self.ROLE_POS[i],
                                             width=2,
                                             tag = 'info_role',
                                             outline=self.COLOR_CURSOR
                                             )
                self.canvas.create_text(self.INFO_SCOPE_TEXT_S_X,
                                        self.INFO_SCOPE_TEXT_S_Y,
                                        text = f'{info_role_list[i]}',
                                        anchor='nw',tag = 'info_role',
                                        fill=self.COLOR_WHITY,
                                        font = (self.FONT, int(self.INFO_SCOPE_WI * 0.05)))
                
                self.canvas.create_text(self.INFO_SCOPE_S_X + self.INFO_SCOPE_WI * 0.03,
                                        self.INFO_SCOPE_G_Y - self.INFO_SCOPE_HI * 0.15,
                                        text=f'発生 {self.hands_count_list[i]}回',
                                        anchor='sw',
                                        tag = 'info_role',
                                        fill=self.COLOR_WHITY,
                                        font = (self.FONT, int(self.INFO_SCOPE_WI * 0.05)))
        
        
    def bet_credit(self):
        # お金を賭ける
        self.canvas.delete('message')
        self.message('お金を賭けてね')
        self.flag_bet = False
        in_flag = False # マウス座標がボックスの範囲内にあるかないかのフラグ
        for i in range(len(self.BET_VALUE)):
            over_flag = False
            if self.credit >= self.BET_VALUE[i]:
                model_color = self.COLOR_TEXT_EMPHASIS
                over_flag = True
            else:
                model_color = self.COLOR_WHITY
                over_flag = False
            self.canvas.create_rectangle(self.BUTTON_5_POS[i][0], self.BUTTON_5_POS[i][1], self.BUTTON_5_POS[i][2], self.BUTTON_5_POS[i][3],
                                         outline= model_color, tag = 'bet_button')
            self.canvas.create_text(self.BUTTON_5_POS[i][6], self.BUTTON_5_POS[i][7],fill = model_color,
                                     text = f'{self.BET_VALUE[i]}億円',font = (self.FONT, int(self.BUTTON_5_POS[i][4] * 0.25)), tag = 'bet_button')

            if self.BUTTON_5_POS[i][0] < self.mouse_x < self.BUTTON_5_POS[i][2] and self.BUTTON_5_POS[i][1] < self.mouse_y < self.BUTTON_5_POS[i][3]:
                if over_flag:
                    self.canvas.create_rectangle(self.BUTTON_5_POS[i][0], self.BUTTON_5_POS[i][1], self.BUTTON_5_POS[i][2], self.BUTTON_5_POS[i][3],
                                                    outline=self.COLOR_CURSOR,width=5, tag='message')
                self.bet_info = self.BET_VALUE[i]
                self.draw_magnification() # 倍率描写
                in_flag = True
                if self.mouse_c:
                    self.mouse_c = False
                    if self.credit >= self.BET_VALUE[i]:
                        self.bet = self.BET_VALUE[i]
                        self.credit -= self.bet
                        self.flag_bet =True
        if in_flag == False:
            # マウス座標がボックス範囲外なら汎用的な倍率を表示
            self.bet_info = 0
            self.draw_magnification() # 倍率描写

    def display_credit(self,money):
        # お金の単位を表示。通常は「億円」
        if money <= 0:
            return '0円'
        if 1 <= money:
            return f'{round(money,1):,}億円'
        
    def draw_now_credit(self):
        # クレジット表示範囲の描写 所持金、借金、掛け金
        self.draw_state_color_frame() # フレームの色を更新
        self.canvas.delete('credit')
        self.canvas.create_text(self.CREJIT_SCOPE_G_X - (self.CREJIT_SCOPE_WI * 0.05),
                                self.CREJIT_SCOPE_S_Y + self.CREJIT_SCOPE_HI * 5 / 6,
                                anchor='e', tag= 'credit',
                                text = f'所持  {self.display_credit(self.credit)} ',fill = self.COLOR_WHITY,
                                font = (self.FONT, int(self.CREJIT_SCOPE_WI * 0.08)))
        if self.loan > 0:
            # 借金がある場合
            self.canvas.create_text(self.CREJIT_SCOPE_G_X - (self.CREJIT_SCOPE_WI * 0.05),
                                    self.CREJIT_SCOPE_S_Y + self.CREJIT_SCOPE_HI * 3 / 6,
                                    anchor='e', tag= 'credit',
                                    text = f'借金 {self.display_credit(self.loan)} ',fill = self.COLOR_FRAME_DENGER,
                                    font = (self.FONT, int(self.CREJIT_SCOPE_WI * 0.08)))
        if self.bet > 0:
            # お金を賭けた場合
            self.canvas.create_text(self.CREJIT_SCOPE_G_X - (self.CREJIT_SCOPE_WI * 0.05),
                        self.CREJIT_SCOPE_S_Y + self.CREJIT_SCOPE_HI * 1 / 6,
                        anchor='e', tag= 'credit',
                        text = f'掛け金 {self.display_credit(self.bet)} ',fill = self.COLOR_WHITY,
                        font = (self.FONT, int(self.CREJIT_SCOPE_WI * 0.08)))
            
    def init_card_start(self):
        # カードを生成してシャッフルしハンドも初期化
        self.c_list = []
        self.p_hand = []
        self.c_list = [Card(suit, num) for suit in range(4) for num in range(1,14)]
        # c_list.append(Card('joker',0)) # Jokerを加えるなら
        self.p_hand = [0] * self.hand_max
        random.shuffle(self.c_list)

    def dealing_card(self):
        # カードを配る
        for i in range(self.hand_max):
            if self.hold_card_list[i] == False:
                self.p_hand[i] = self.c_list.pop()

    def draw_card(self, i):
        # i番目のトランプカードを描写
        suit, mark = self.p_hand[i].get_sm()
        # i番目のトランプカードの座標
        card_s_x = self.CARD_SCOPE_S_X + self.CARD_SCOPE_WI * i / self.hand_max + self.SUKIMA_W * 1 / 8
        card_s_y = self.CARD_SCOPE_S_Y + self.SUKIMA_H * 1 / 8
        card_g_x = (self.CARD_SCOPE_S_X + self.CARD_SCOPE_WI * (i+1) / self.hand_max) - self.SUKIMA_W * 1 / 8
        card_g_y = self.ROLE_SCOPE_G_Y - self.SUKIMA_H_C
        # i番目のトランプカードのサイズ、中心点
        card_wi = card_g_x - card_s_x
        card_hi = card_g_y - card_s_y
        card_c_x = card_s_x + card_wi * 1 / 2
        card_c_y = card_s_y + card_hi * 1 / 2
        card_c_y_1_4 = card_s_y + card_hi * 1 / 4
        card_c_y_3_4 = card_s_y + card_hi * 3 / 4
        # カードの土台を白く塗る
        self.canvas.create_rectangle(card_s_x, card_s_y, card_g_x, card_g_y, 
                                     fill = self.COLOR_WHITY, tag='card')
        # スートを描写
        arg = {'center_x':card_c_x, 'center_y':card_c_y_3_4, 'size':card_wi * 0.7}
        if suit == 'Heart':
            self.create_heart(**arg)
            model_color = self.COLOR_HEART
        elif suit == 'Spade':
            self.create_spade(**arg)
            model_color = self.COLOR_SPADE
        elif suit == 'Club':
            self.create_club(**arg)
            model_color = self.COLOR_CLUB
        elif suit == 'Diamond':
            self.create_diamond(**arg)
            model_color = self.COLOR_DIAMOND
        elif suit == 'Joker':
            pass
        # マークを描写
        self.canvas.create_text(card_c_x, card_c_y_1_4,
                                text = mark ,font =(self.FONT, int(card_wi * 0.6)),
                                fill = model_color, tag='card')

    def display_now_role(self):
        # 現在の役を強調表示
        self.canvas.delete('now_role')
        now_role = self.check_role()
        if now_role != 9:
            self.canvas.create_rectangle(self.ROLE_POS[now_role],
                                        outline=self.COLOR_TEXT_EMPHASIS,
                                        width=1,tag ='now_role')

    def hold_card(self):
        # ホールドするカードを選ぶ
        self.canvas.delete('cursor_hold')
        for i in range(len(self.p_hand)):
            # ホールドされていないカードのチェックを外す
            if self.hold_card_list[i] == False:
                self.canvas.delete('cursor_hold_con')
        for i in range(len(self.p_hand)):
            # i番目のトランプカードの座標
            card_s_x = self.CARD_SCOPE_S_X + self.CARD_SCOPE_WI * i / self.hand_max + self.SUKIMA_W * 1 / 8
            card_s_y = self.CARD_SCOPE_S_Y + self.SUKIMA_H * 1 / 8
            card_g_x = (self.CARD_SCOPE_S_X + self.CARD_SCOPE_WI * (i+1) / self.hand_max) - self.SUKIMA_W * 1 / 8
            card_g_y = self.ROLE_SCOPE_G_Y - self.SUKIMA_H_C
            # i番目のトランプカードのサイズ、中心点
            card_wi = card_g_x - card_s_x
            card_hi = card_g_y - card_s_y
            card_c_x = card_s_x + card_wi * 1 / 2
            card_c_y = card_s_y + card_hi * 1 / 2
            if self.hold_card_list[i]:
                # 確定フラグの立っているカードの確定のチェックを入れる
                self.canvas.create_rectangle(card_s_x, card_s_y, card_g_x, card_g_y,
                                                outline= self.COLOR_CURSOR_HOLD_CON, 
                                                width = 10, tag='cursor_hold_con')
                self.canvas.create_rectangle(card_s_x, card_s_y + card_hi * 2 / 5, 
                                                card_g_x, card_s_y + card_hi * 3 / 5,
                                                outline= self.COLOR_CURSOR_HOLD_CON, 
                                                width = 5, tag='cursor_hold_con')
                self.canvas.create_text(card_c_x, card_c_y,
                                        text='HOLD', fill = self.COLOR_CURSOR_HOLD_CON,
                                        font=(self.FONT, int(card_wi * 0.25)),
                                        tag ='cursor_hold_con')
            if card_s_x < self.mouse_x < card_g_x and\
                    card_s_y < self.mouse_y < card_g_y:
                # 触れたi番目のカードにカーソルを出す
                self.canvas.create_rectangle(card_s_x, card_s_y, card_g_x, card_g_y,
                                             outline= self.COLOR_CURSOR_HOLD, 
                                             width = 7, tag='cursor_hold')
                self.canvas.create_rectangle(card_s_x, card_s_y + card_hi * 2 / 5, 
                                             card_g_x, card_s_y + card_hi * 3 / 5,
                                             outline= self.COLOR_CURSOR_HOLD, 
                                             width = 2, tag='cursor_hold')
                self.canvas.create_text(card_c_x, card_c_y,
                                        text='HOLD', fill = self.COLOR_CURSOR_HOLD,
                                        font=(self.FONT, int(card_wi * 0.25)),
                                        tag ='cursor_hold')
                if self.mouse_c == True:
                    # クリックしたカードに確定のフラグを立てるor下げる
                    self.mouse_c = False
                    if self.hold_card_list[i]:
                        self.hold_card_list[i] = False
                        
                    else:
                        self.hold_card_list[i] = True


    def message_role_cal_bet(self):
        # 最終的な役を表示してベット額を計算して表示
        self.canvas.create_rectangle(self.CARD_ROLE_POS,
                                     fill = 'DeepPink4',
                                     tag = 'card')
        self.canvas.create_text(self.CARD_ROLE_C_X,
                                self.CARD_ROLE_C_Y,
                                text=f'{self.role_cal(self.check_role())}',
                                fill = self.COLOR_WHITY,
                                font=(self.FONT, int(self.CARD_SCOPE_WI * 0.045)),
                                tag = 'card')
        if self.check_role() == 9:
            self.message(f'{self.role_cal(self.check_role())}   掛け金{self.display_credit(self.bet)}没収！')
            self.bet = 0
        else:
            profit = self.bet * self.ROLE_VALUE[self.check_role()]
            self.message(f'{self.role_cal(self.check_role())} {self.display_credit(profit)}GET！')
            self.credit += profit
            self.bet = 0

    def check_credit(self):
        # お金がないならTrue
        if self.credit <= 0:
            return True
        else:
            return False

    def check_loan(self):
        # 借金があれはTrue
        if self.loan > 0:
            return True
        else:
            return False
    def draw_yamikin(self):
        # 闇金の画面を作る
        self.canvas.delete('window')
        self.canvas.create_rectangle(self.WINDOW_SCOPE_POS,
                                     fill=self.COLOR_BACK,width = 2,
                                     outline=self.COLOR_WHITY,tag = 'window')
        self.canvas.create_image(self.WINDOW_SCOPE_C_X,
                                 self.WINDOW_SCOPE_C_Y,
                                 image=self.yamikin_image,tag = 'window')
        self.message('闇金業者が現れた！')


    def draw_ok_button(self):
        # okボタンを描画
        self.canvas.create_rectangle(self.BUTTON_OK_POS,
                                     outline= self.COLOR_WHITY,width= 2,
                                     tag='ok_button')
        self.canvas.create_text(self.BUTTON_OK_C_X, self.BUTTON_OK_C_Y,
                                text='OK',font=(self.FONT,int(self.BUTTON_OK_WI *0.20)),
                                fill = self.COLOR_WHITY,
                                tag='ok_button')
        
    def ckick_ok_button(self):
        # okボタンが押されたかの判定
        self.canvas.delete('ok_button_cursor')
        if self.BUTTON_OK_POS[0] < self.mouse_x < self.BUTTON_OK_POS[2]and\
        self.BUTTON_OK_POS[1] < self.mouse_y < self.BUTTON_OK_POS[3]:
            self.canvas.create_rectangle(self.BUTTON_OK_POS,
                                     outline= self.COLOR_CURSOR,width= 5,
                                     tag='ok_button_cursor')
            if self.mouse_c:
                self.mouse_c = False
                self.canvas.delete('ok_button')
                self.canvas.delete('ok_button_cursor')
                return True

    def reset_interest_add_loan(self):
        # 利子カウントリセット　借金加算
        self.count_interest = 0
        self.loan = int(self.loan * self.INTEREST_RATE)

    def draw_button_ab(self, a_text, b_text):
        # メッセージボックスの下半分にボタンAB二つ描画する
        model_outline = {'outline':self.COLOR_WHITY, 'width':2, 'tag':'ab_button'}
        model_text ={'fill' :self.COLOR_WHITY,'font':(self.FONT,int(self.BUTTON_A_WI * 0.10)), 'tag':'ab_button'}
        self.canvas.create_rectangle(self.BUTTON_A_POS, **model_outline)
        self.canvas.create_text(self.BUTTON_A_C_X, self.BUTTON_A_C_Y, text = a_text, **model_text)
        self.canvas.create_rectangle(self.BUTTON_B_POS, **model_outline)
        self.canvas.create_text(self.BUTTON_B_C_X, self.BUTTON_B_C_Y, text = b_text, **model_text)

    def do_button_ab(self):
        # ABボタンのカーソル表示。クリック判定
        self.canvas.delete('ab_button_cursor')
        model_outline = {'outline':self.COLOR_CURSOR, 'width':5, 'tag':'ab_button_cursor'}
        # Aボタン
        if self.BUTTON_A_POS[0] < self.mouse_x < self.BUTTON_A_POS[2] and\
        self.BUTTON_A_POS[1] < self.mouse_y < self.BUTTON_A_POS[3]:
            self.canvas.create_rectangle(self.BUTTON_A_POS, **model_outline)
            if self.mouse_c:
                self.mouse_c = False
                self.canvas.delete('ab_button_cursor')
                self.canvas.delete('ab_button')
                return 'A'
        # Bボタン
        if self.BUTTON_B_POS[0] < self.mouse_x < self.BUTTON_B_POS[2] and\
        self.BUTTON_B_POS[1] < self.mouse_y < self.BUTTON_B_POS[3]:
            self.canvas.create_rectangle(self.BUTTON_B_POS, **model_outline)
            if self.mouse_c:
                self.mouse_c = False
                self.canvas.delete('ab_button_cursor')
                self.canvas.delete('ab_button')
                return 'B'
            
    def draw_button_five(self, list5):
        # 5つの要素のtextリストをもらって5つのボタンを生成する
        for i in range(5):
            self.canvas.create_rectangle(self.BUTTON_5_POS[i][:4],
                                         outline=self.COLOR_WHITY,
                                         width=2, tag= 'button_five')
            self.canvas.create_text(self.BUTTON_5_POS[i][6],
                                    self.BUTTON_5_POS[i][7],
                                    text =list5[i],font = (self.FONT, int(self.BUTTON_5_POS[i][4] * 0.30)),
                                    fill = self.COLOR_WHITY, tag= 'button_five')

    def do_button_five(self):
        # 5つのボタンにマウスが入るとカーソルが出る、クリックするとボタンの種類を返す
        self.canvas.delete('button_five_cursor')
        for i in range(5):
            if self.BUTTON_5_POS[i][0] < self.mouse_x < self.BUTTON_5_POS[i][2] and\
            self.BUTTON_5_POS[i][1] < self.mouse_y < self.BUTTON_5_POS[i][3]:
                self.canvas.create_rectangle(self.BUTTON_5_POS[i][:4],
                                            outline=self.COLOR_CURSOR,
                                            width=5, tag= 'button_five_cursor')
                if self.mouse_c:
                    self.mouse_c = False
                    self.canvas.delete('button_five_cursor')
                    self.canvas.delete('button_five')
                    return i
            
    def draw_repayment_button(self):
        # 返済金額の選択肢を出す
        self.message('いくら返済する？')
        for i in range(5):
            # ボタン描画
            if self.credit >= self.LOAN_REPAY_VALUE[i] + 1:
                model_color = self.COLOR_TEXT_EMPHASIS
            else:
                model_color = self.COLOR_WHITY
            self.canvas.create_rectangle(self.BUTTON_5_POS[i][:4],
                                         outline=model_color,
                                         width=2, tag= 'button_repay')
            self.canvas.create_text(self.BUTTON_5_POS[i][6],
                                    self.BUTTON_5_POS[i][7],
                                    text =self.display_credit(self.LOAN_REPAY_VALUE[i]),
                                    font = (self.FONT, int(self.BUTTON_5_POS[i][4] * 0.20)),
                                    fill = model_color, tag= 'button_repay')
           

    def do_repayment_button(self):
        # 返済ボタンのカーソル描画クリック感知
        self.canvas.delete('button_repay_cursor')
        for i in range(5):
            if self.credit >= self.LOAN_REPAY_VALUE[i] + 1:
                cursol_flag = True
            else:
                cursol_flag = False
            if self.BUTTON_5_POS[i][0] < self.mouse_x < self.BUTTON_5_POS[i][2] and\
                self.BUTTON_5_POS[i][1] < self.mouse_y < self.BUTTON_5_POS[i][3] and cursol_flag:
                    self.canvas.create_rectangle(self.BUTTON_5_POS[i][:4],
                                                outline=self.COLOR_CURSOR,
                                                width=5, tag= 'button_repay_cursor')
                    if self.mouse_c:
                        self.mouse_c = False
                        self.canvas.delete('button_repay_cursor')
                        self.canvas.delete('button_repay')
                        if self.credit - self.LOAN_REPAY_VALUE[i] == 0:
                            # 支払うと無一文になってしまう場合
                            return False
                        # 借金返済
                        self.credit -= self.LOAN_REPAY_VALUE[i]
                        self.loan -= self.LOAN_REPAY_VALUE[i]
                        if self.loan < 0:
                            # はみ出た場合　はみ出た分を現金に戻して借金0
                            self.credit += abs(self.loan)
                            self.loan = 0
                        return True
                    
    def draw_borrow_credit(self):
        # 借金ボタンを描画
        self.message(f'いくら借りる？（一回分の利子が加算されます）')
        for i in range(5):
            # ボタン描画
            self.canvas.create_rectangle(self.BUTTON_5_POS[i][:4],
                                         outline=self.COLOR_TEXT_EMPHASIS,
                                         width=2, tag= 'button_loan')
            self.canvas.create_text(self.BUTTON_5_POS[i][6],
                                    self.BUTTON_5_POS[i][7],
                                    text =self.display_credit(self.LOAN_REPAY_VALUE[i]),
                                    font = (self.FONT, int(self.BUTTON_5_POS[i][4] * 0.20)),
                                    fill = self.COLOR_TEXT_EMPHASIS, tag= 'button_loan')

    def do_borrow_credit(self):
        # 借金を実行
        self.canvas.delete('button_loan_cursor')
        for i in range(5):
            if self.BUTTON_5_POS[i][0] < self.mouse_x < self.BUTTON_5_POS[i][2] and\
                self.BUTTON_5_POS[i][1] < self.mouse_y < self.BUTTON_5_POS[i][3]:
                    self.canvas.create_rectangle(self.BUTTON_5_POS[i][:4],
                                                outline=self.COLOR_CURSOR,
                                                width=5, tag= 'button_loan_cursor')
                    if self.mouse_c:
                        self.mouse_c = False
                        self.canvas.delete('button_loan_cursor')
                        self.canvas.delete('button_loan')
                        # 借金返済
                        self.credit += self.LOAN_REPAY_VALUE[i]
                        self.loan += int(self.LOAN_REPAY_VALUE[i] * self.INTEREST_RATE)
                        self.draw_skull()
                        self.draw_state_color_frame() # フレームの色を更新
                        return True

    def draw_trophy_buyer(self):
        # 訪問販売の描画
        self.canvas.delete('window')
        self.canvas.create_rectangle(self.WINDOW_SCOPE_POS,
                                     fill=self.COLOR_BACK,width = 2,
                                     outline=self.COLOR_WHITY,tag = 'window')
        self.canvas.create_image(self.WINDOW_SCOPE_C_X,
                                 self.WINDOW_SCOPE_C_Y,
                                 image=self.trophy_buyer_image,tag = 'window')
        if self.buyer_twice_flag:
            msg = '訪問販売員は帰らない'
        else:
            msg = '訪問販売員が現れた！'
        self.message(msg)

    def cal_trophy_val(self):
        # 現在のトロフィーの価値を計算して返す 
        return int(self.TROPHY_PRICE_RATE ** self.trophy * self.TROPHY_PRICE_START)

    def draw_trophy(self):
        # トロフィーを描画
        self.canvas.delete('trophy')
        if self.index != 778:
            image_wi = 50
            y = self.HEIGHT * 0.98
            if self.game_clear_flag:
                self.canvas.create_image(self.WIDTH * 0.48, y, 
                                         image= self.trophy_image_list[self.tmr%3],
                                         tag = 'trophy')
                self.canvas.create_text(self.WIDTH * 0.50 + 2, y+2,
                                        text = f'× {self.trophy}',
                                        anchor='w',
                                        fill = self.COLOR_BACK,
                                        font=(self.FONT, int(self.WIDTH * 0.03)),
                                        tag = 'trophy')
                self.canvas.create_text(self.WIDTH * 0.50, y,
                                        text = f'× {self.trophy}',
                                        anchor='w',
                                        fill = self.COLOR_TEXT_EMPHASIS,
                                        font=(self.FONT, int(self.WIDTH * 0.03)),
                                        tag = 'trophy')

            else:
                if self.trophy > 0:
                    for i in range(self.trophy):
                        x = 20 + ((self.WIDTH - self.trophy * image_wi) / 2) + i * image_wi
                        
                        self.canvas.create_image(x, y,
                                                image= self.trophy_image_list[self.tmr%3],
                                                tag = 'trophy')

    def draw_skull(self):
        # どくろを描写
        self.canvas.delete('sukll')
        if self.index != 669:
            self.skull = int(self.loan // self.SKULL_APPER_LOAN)
            image_wi = 50
            if self.skull >= 1:
                for i in range(self.skull):
                    x = 20 + ((self.WIDTH - self.skull * image_wi) / 2) + i * image_wi
                    y = self.HEIGHT * 0.04
                    if self.tmr%30 > 15:
                        img = self.sukll_image_l_list
                    else:
                        img = self.sukll_image_r_list
                    self.canvas.create_image(x, y,
                                            image= img[self.tmr%3],
                                            tag = 'sukll')

    def cal_last_image_list(self,num):
        # 受けた数字を一番近い整数のペアの掛け算で表示
        check_list = []
        for i in range(1, int((num**0.5)) + 1):
            if num % i == 0:
                check_list.append((i, num // i))
        return check_list[-1]

    def draw_game_clear(self):
        # ゲームクリア描写
        self.message(f'GAME CLEAR  おめでとう！{self.GAME_CLEAR_TROPHY_NUM}のトロフィーを得た！')
        self.canvas.delete('window')
        self.canvas.create_rectangle(self.WINDOW_SCOPE_POS,
                                    fill=self.COLOR_OVER_CLEAR,width = 2,
                                    outline=self.COLOR_WHITY,tag = 'window')
        last_text = self.create_record_text()
        self.canvas.create_text(self.WIDTH * 0.06,
                                self.HEIGHT * 0.08,
                                anchor = 'nw',
                                fill = self.COLOR_WHITY,
                                font = (self.FONT, int(self.WIDTH * 0.019)),
                                text =last_text,
                                tag = 'window')
        
        y, x = self.cal_last_image_list(self.GAME_CLEAR_TROPHY_NUM)
        # トロフィー敷き詰めのためのyとx
        for y_i in range(y):
            for x_i in range(x):
                self.canvas.create_image(self.WINDOW_SCOPE_C_X + self.WINDOW_SCOPE_WI*0.5 * x_i / x,
                                        (self.WINDOW_SCOPE_S_Y + self.WINDOW_SCOPE_HI * 2 / 5) + self.WINDOW_SCOPE_HI*0.5 * y_i / y,
                                        image=self.trophy_image_list[self.tmr%3],
                                        tag = 'window')
    
    def create_record_text(self):
        # クリア画面。ゲームオーバー画面で使う記録テキスト
        last_text ='記録\n'
        for i in range(len(self.ROLE_NAME)):
            last_text += f'{self.ROLE_NAME[i]} {self.hands_count_list[i]}回\n'
        last_text += f'\n合計 {str(sum(self.hands_count_list))}回'
        return last_text

    def draw_game_over(self):
        # ゲームオーバー描写
        self.message('GAME OVER  あなたはどこぞへと連れていかれました')
        self.canvas.delete('window')
        self.canvas.create_rectangle(self.WINDOW_SCOPE_POS,
                                    fill=self.COLOR_OVER_CLEAR,width = 2,
                                    outline=self.COLOR_WHITY,tag = 'window')
        last_text = self.create_record_text()
        self.canvas.create_text(self.WIDTH * 0.06,
                                self.HEIGHT * 0.08,
                                anchor = 'nw',
                                fill = self.COLOR_WHITY,
                                font = (self.FONT, int(self.WIDTH * 0.019)),
                                text =last_text,
                                tag = 'window')
        self.canvas.create_image(self.WIDTH * 0.65,
                                self.HEIGHT * 0.60,
                                image=self.sukll_image_l_list[self.tmr%3],
                                tag = 'window')
        
    def relord_save_list_now(self):
        # セーブデータ用に現在の状況をまとめているリストを更新する
        # credit, loan, trophy, count_interest, hands_count_listの各要素10個
        # 全14要素
        self.save_list_now = []
        self.save_list_now.append(self.credit)
        self.save_list_now.append(self.loan)
        self.save_list_now.append(self.trophy)
        self.save_list_now.append(self.count_interest)
        for i in self.hands_count_list:
            self.save_list_now.append(i)

    def init_save_list_now(self):
        # ゲームの中でデータを潰す用の現在データの初期化。
        self.credit = 1
        self.loan = 0
        self.trophy = 0
        self.count_interest = 0
        self.hands_count_list =[0,0,0,0,0,0,0,0,0,0]
        self.relord_save_list_now()


    def save_date_write(self):
        # save_list_nowをセーブデータに上書きする。
        with open('save_date_VIDEO_POKER.txt','w') as f:
            for i in self.save_list_now:
                    print(i, file = f)

    def save_date_read(self):
        # セーブデータの情報を読み込んで現状に移植する
        with open('save_date_VIDEO_POKER.txt','r') as f:
            self.save_list_now = [int(i) for i in f.read().split()]
        self.credit = self.save_list_now[0]
        self.loan = self.save_list_now[1]
        self.trophy = self.save_list_now[2]
        self.count_interest = self.save_list_now[3]
        index = 0
        for i in range(4,14):
            self.hands_count_list[index] = self.save_list_now[i]
            index += 1
        # self.hands_count_list[0] = self.save_list_now[4]
        # self.hands_count_list[1] = self.save_list_now[5]
        # self.hands_count_list[2] = self.save_list_now[6]
        # self.hands_count_list[3] = self.save_list_now[7]
        # self.hands_count_list[4] = self.save_list_now[8]
        # self.hands_count_list[5] = self.save_list_now[9]
        # self.hands_count_list[6] = self.save_list_now[10]
        # self.hands_count_list[7] = self.save_list_now[11]
        # self.hands_count_list[8] = self.save_list_now[12]
        # self.hands_count_list[9] = self.save_list_now[13]

    def check_already_save_date(self):
        # 既存のセーブデータがあるかチェックする
        try:
            with open('save_date_VIDEO_POKER.txt', 'r') as rfile:
                return True
        except:
            return False



    def init_game(self):
        # 一周した時用の初期化
        # self.canvas.delete('base')
        # self.canvas.delete('frame_state')
        self.canvas.delete('card')
        self.canvas.delete('mag') # 倍率
        self.canvas.delete('message')
        self.canvas.delete('bet_button')
        self.canvas.delete('credit')
        self.canvas.delete('cursor_hold')
        self.canvas.delete('cursor_hold_con')
        self.canvas.delete('two_button')
        self.canvas.delete('two_button_cursor_change')
        self.canvas.delete('two_button_cursor_end')
        self.canvas.delete('now_role')
        self.canvas.delete('ok_button')
        self.canvas.delete('ok_button_cursor')
        self.canvas.delete('ab_button')
        self.canvas.delete('window')
        self.p_hand = []
        self.count_change = self.count_change_init
        self.bet = 0
        self.hold_card_list = [False, False, False, False, False]

    def debug_text(self):
        # デバッグ用色々表示
        self.canvas.delete('debug')
        self.canvas.create_text(self.WIDTH * 0.5,self.HEIGHT * 0.98,
                                text = f'（デバッグ用）index{self.index}',
                                font=(self.FONT, 15),tag = 'debug',
                                fill = self.COLOR_WHITY)

    def main(self):
        if self.index == 0:
            # タイトル画面描画
            # セーブデータから保有クレジットと借金額を読み込む　
            self.save_date_already_flag = self.check_already_save_date() # 既存のデータがあるかチェック
            self.draw_title()
            self.relord_save_list_now()
            self.cal_role_pos() # 各役の範囲を計算
            self.cal_five_button_pos() # 5つのボタンの範囲を計算
            self.draw_state_color_frame() # フレームの色を描写　draw_creditと併用しない唯一の単体実行
            self.index = 1

        elif self.index == 1:
            # スタートボタン押し待ち
            if self.click_button_title():
                self.index = 2

        elif self.index == 2:
            # ゲーム画面描画、クレジット賭けメニューも描画
            #  一周して戻ってくる場所
            self.init_game()
            self.draw_menu()
            self.draw_now_credit() # 現在クレジットを表示
            self.draw_magnification()
            self.relord_save_list_now()
            self.save_date_write() # データセーブ
            if self.trophy >= self.GAME_CLEAR_TROPHY_NUM:
                # クリアチェック
                self.game_clear_flag = True
            self.index = 3

        elif self.index == 3:
            # クレジットを賭ける（1～5）のを待つ
            self.bet_credit()
            self.draw_role_info()
            if self.flag_bet:
                # メッセージを消して掛け金を表示
                # トランプを生成してシャッフル
                # ハンドを初期化

                self.canvas.delete('message')
                self.canvas.delete('bet_button')
                self.draw_now_credit() 
                self.canvas.delete('card') 
                self.init_card_start()
                self.index = 4    

        elif self.index == 4:
            # ホールドされていないカードを配って画面に表示
            self.canvas.delete('two_button_cursor_change')
            self.canvas.delete('two_button_cursor_end')
            self.canvas.delete('two_button')
            self.dealing_card()
            self.tmr_card = 0
            self.index = 5

        elif self.index == 5:
            # 一枚ずつカードがめくられる tmr3ずつ
            self.tmr_card += 1
            for i in range(self.hand_max):
                if self.tmr_card == i+3:
                    self.draw_card(i)
            if self.tmr_card == self.hand_max + 3:
                self.tmr_card = 0
                self.display_now_role()
                if self.count_change > 0:
                    # まだチェンジできるなら
                    self.message(f'ホールドするカードを選んでチェンジボタンを押す')
                    self.draw_button_ab(f'チェンジ{self.count_change}/{self.count_change_init}','終了')
                    self.index = 6
                else:
                    self.index = 7

        elif self.index == 6:
            # ホールドするカードを選ぶ
            # 終了か保有チェックボタンを押す
            self.hold_card()
            self.draw_role_info()
            choice = self.do_button_ab()
            if choice == 'A':
                # チェンジボタンが押された
                self.index = 4
                self.count_change -= 1
            elif choice == 'B':
                # 終了ボタンが押された
                self.index = 7
            
        elif self.index == 7:
            # ハンドの役をジャッジして役名を描写,掛け金の計算をしてクレジットに加算
            self.canvas.delete('two_button_cursor_change')
            self.canvas.delete('two_button_cursor_end')
            self.canvas.delete('two_button')
            self.hands_count_list[self.check_role()] += 1 # 発生した役の回数をカウント
            self.message_role_cal_bet() # 役と賞金を表示
            
            self.draw_now_credit() # 現在クレジットを表示
            self.draw_ok_button()
            self.index = 8

        elif self.index == 8:
            # okボタン押し待ち
            self.draw_role_info()
            if self.ckick_ok_button():
                # okボタンが押された
                if self.check_credit() or self.check_loan():
                    # お金がないor借金がある場合闇金処理へ
                    self.draw_yamikin()
                    self.draw_now_credit() 
                    self.draw_ok_button()
                    self.index = 9
                else:
                    # お金があり借金がない場合　お買い物処理へ
                    self.buyer_twice_flag = False
                    if self.cal_trophy_val()+1 < self.credit:
                        self.index = 22
                    else:
                        self.index = 2

        elif self.index == 9:
            # 闇金業者登場 ボタン押し待ち
            if self.ckick_ok_button():
                if self.check_loan():
                    # 借金ある場合 利子カウント+1　
                    self.count_interest += 1
                    self.index = 10
                else:
                    # お金がない場合　お金を借りる処理へ
                    self.index = 17

        elif self.index == 10:
            # 借金を返済する、さらに借りるボタンの描画
            if self.count_interest == self.count_interest_max:
                self.reset_interest_add_loan()
                text = f'{self.count_interest_max} 回経過して 借金が膨れ上がった！'
            else:
                text = f'借金が膨れるまであと{self.count_interest_max - self.count_interest} 回'
            self.draw_now_credit()
            self.message(text)
            self.draw_ok_button()
            self.index = 10.1
        elif self.index == 10.1:
            # okボタン押し待ち
            if self.ckick_ok_button():
                if self.skull >= self.GAME_OVER_SKULL_NUM:
                    # ゲームオーバー処理へ
                    self.message('「返すつもりないだろ」')
                    self.draw_ok_button()
                    self.index = 666
                else:
                    self.index = 10.2
        elif self.index == 10.2:
            self.message(f'「{self.display_credit(self.loan)}、いつ返すのだ？」')
            self.draw_button_ab('返済する','さらに借りる')
            self.index = 11

        elif self.index == 11:
            # ABボタンクリック待ち 返済するかさらに借りる
            choice = self.do_button_ab()
            if choice == 'A':
                # 返済するを選択
                self.index = 12
            elif choice == 'B':
                # さらに借りるを選択　借入処理へ
                if self.credit < self.LOAN_REPAY_VALUE[-1]:
                    # 所持クレジット100以下なら借金できる
                    self.message('「さすがは賭博師だ」')
                    self.draw_ok_button()
                    self.index = 19
                else:
                    self.message('「金、返せるだろ」')
                    self.draw_ok_button()
                    self.index = 11.1

        elif self.index == 11.1:
            # ok押し待ち後　戻る
            if self.ckick_ok_button():
                    # okを押して戻る
                    self.index = 10

        elif self.index == 12:
            # 返済可能か判定
            if self.credit >= self.LOAN_REPAY_VALUE[0]+1:
                self.draw_repayment_button()
                self.index = 13
            else:
                self.message(f'返済には{self.display_credit(self.LOAN_REPAY_VALUE[0] + 1)}以上必要だ')
                self.draw_ok_button()
                if self.ckick_ok_button():
                    # okを押して戻る
                    self.index = 10
        elif self.index == 13:
            # 返済処理
            if self.do_repayment_button():
                self.draw_now_credit()
                self.index = 14
        elif self.index == 14:
            # 完済したか否か
            if self.loan <= 0:
                self.message('「まいどあり」')
                self.count_interest = 0 # 利子カウントリセット
                self.draw_now_credit() # 現在クレジットを表示
                self.draw_ok_button()
                self.index = 27
            else:
                self.message('「まだ用があるか？」')
                self.draw_button_ab('返済か借金', '用はない')
                self.index = 16

        elif self.index == 16:
            # '返済か借金', '用はない' ボタン押し待ち
            choice = self.do_button_ab()
            if choice == 'A':
                #返済か借金
                self.index = 10.2
            if choice == 'B':
                # 用はない
                self.index = 2

        elif self.index == 17:
            # 金貸し処理始まり
            self.message(f'「金を貸してやろう」')
            self.draw_ok_button()
            self.index = 18

        elif self.index == 18:
            # お金を借りる処理 okボタン押し待ち
            if self.ckick_ok_button():
                self.message(f'「だが{self.count_interest_max} 回毎に借金は{self.INTEREST_RATE}倍になる」')
                self.draw_ok_button()
                self.index = 19

        elif self.index == 19:
            # okボタン押し待ち
            if self.ckick_ok_button():
                self.draw_borrow_credit()  
                self.index = 20

        elif self.index == 20:
            # 借金実行  
            if self.do_borrow_credit():
                self.draw_now_credit() # 現在クレジットを表示
                if self.skull >= self.GAME_OVER_SKULL_NUM:
                    # ゲームオーバー処理へ
                    self.message('「返すつもりないだろ？」')
                    self.draw_ok_button()
                    self.index = 666
                else:
                    self.message('「まだ用があるか？」')
                    self.draw_button_ab('さらに借金', '用はない')
                    self.index = 21

        elif self.index == 21:
            # さらに借金,用はないボタン押し待ち
            choice = self.do_button_ab()
            if choice == 'A':
                # さらに借金
                if self.credit < self.LOAN_REPAY_VALUE[-1]:
                    # 所持クレジット100以下なら借金できる
                    self.message('「さすがは賭博師だ」')
                    self.draw_ok_button()
                    self.index = 19
                else:
                    self.message('「本当に返済できるのか怪しいもんだ」')
                    self.draw_ok_button()
                    self.index = 21.1
            elif choice == 'B':
                # 用はない
                self.index = 2
        elif self.index == 21.1:
            # ok押し待ち後戻る
            if self.ckick_ok_button():
                self.index = 2

        elif self.index ==22:
            # お買い物処理　
            self.draw_trophy_buyer()
            self.draw_now_credit() # 現在クレジットを表示
            self.draw_ok_button()
            self.index = 23
            

        elif self.index ==23:
            # okボタン押し待ち
            if self.ckick_ok_button():
                if self.buyer_twice_flag:
                    self.message('「トロフィーはいくつあっても良いものです！」')
                else:
                    self.message('「儲けてますね！トロフィーを進呈します！」')
                self.draw_ok_button()
                self.index = 24

        elif self.index == 24:
            # okボタン押し待ち
            if self.ckick_ok_button():
                self.message(f'「{self.display_credit(self.cal_trophy_val())}です！」')
                self.draw_now_credit
                self.draw_button_ab('支払う','追い返す')
                self.index = 25

        elif self.index ==25:
            # 支払う、追い返す ボタン押し待ち
            choice = self.do_button_ab()
            if choice == 'A':
                # 価格判定へ
                self.index = 26
            elif choice == 'B':
                # 追い返す
                self.draw_now_credit()
                self.index = 2

        elif self.index ==26:
            # トロフィー価格判定
            if self.credit >=self.cal_trophy_val() + 1:
                # 購入して
                self.credit -= self.cal_trophy_val()
                self.trophy += 1
                self.draw_now_credit()
                self.draw_ok_button()
                if self.trophy == self.GAME_CLEAR_TROPHY_NUM:
                    # ゲームクリア判定
                    self.message('「驚くべきトロフィーの数ですね！」')
                    self.index = 777
                else:
                    self.message('「良い買い物です！」')
                    self.index = 28
            elif self.credit == self.cal_trophy_val():
                self.message('支払うと無一文になってしまう')
                self.draw_ok_button()
                self.index = 27     
            elif self.credit < self.cal_trophy_val():
                self.message('「この貧乏人！」')
                self.draw_ok_button()
                self.index = 27

        elif self.index ==27:
            # okボタン押し待ち後次の周へ
            if self.ckick_ok_button():
                self.draw_now_credit()
                self.index = 2

        elif self.index ==28:
            # okボタン押し待ち後次のトロフィー判定へ
            self.buyer_twice_flag = True
            if self.ckick_ok_button():
                self.index = 22

        elif self.index ==666:
            # ゲームオーバー処理 okボタン押し待ち
            if self.ckick_ok_button():
                self.index = 667

        elif self.index == 667:
            #ゲームオーバー処理へ
            self.message('「強制的な取り立てが必要だな」')
            self.draw_ok_button()
            self.index = 668
        elif self.index == 668:
            # okボタン押し待ち
            if self.ckick_ok_button():
                self.index = 669
        
        elif self.index == 669:
            # ゲームオーバー画面描画
            self.draw_game_over()
            self.draw_ok_button()
            if self.ckick_ok_button():
                # タイトルに戻る
                self.canvas.delete('window')
                self.canvas.delete('base')
                self.canvas.delete('frame_state')
                self.init_game()
                self.index = 0

        elif self.index == 777:
            # ゲームクリア処理　okボタン押し待ち
            if self.ckick_ok_button():
                self.index = 778

        elif self.index == 778:
            # ゲームクリア画面描写
            self.draw_game_clear()
            self.draw_button_ab('タイトルへ','さらに続ける')
            choice = self.do_button_ab()
            if choice == 'A':
                # タイトルに戻る
                self.relord_save_list_now()
                self.save_date_write() # 現状をセーブデータに上書き
                self.canvas.delete('window')
                self.canvas.delete('base')
                self.canvas.delete('frame_state')
                self.init_game()
                self.index = 0
            elif choice == 'B':
                self.game_clear_flag == True
                self.relord_save_list_now()
                self.save_date_write() # 現状をセーブデータに上書き
                self.canvas.delete('window')
                self.canvas.delete('base')
                self.canvas.delete('frame_state')
                self.init_game()
                self.index = 2

        self.tmr += 1
        if self.tmr == 30:
            self.tmr = 0
        self.canvas.bind('<Motion>', self.mouse_move)
        self.canvas.bind('<ButtonPress>', self.mouse_click)
        self.canvas.bind('<ButtonRelease>', self.mouse_release)
        # self.debug_text()
        self.draw_skull()
        self.draw_trophy()
        self.after(50, self.main)
                
        
def start():
    root = tk.Tk()
    app = App(root)
    app.mainloop()

if __name__ == '__main__':
    start()

