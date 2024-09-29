import tkinter
import random

class App(tkinter.Frame):
    # 定数
    WIDTH = 1000 # 画面の横 1000*620
    HEIGHT = 620 # 画面の縦
    SUKIMA_W = WIDTH * 1 / 50 # 横の隙間
    SUKIMA_H = HEIGHT * 31 / 1000 # 縦の隙間
    FONT = 'Times New Roman' # フォント
    # 色
    BACK_COLOR = 'gray16'
    GRID_COLOR_BACK = 'black' # 座布団の色＝格子の色
    MOUSE_COLOR_KARI = 'red' # マウスの軌跡仮
    SHADOW_COLOR = 'gray10' # 影の色
    WHITEY_COLOR ='seashell2' # 黒バック専用文字色
    CURSOR_DOT_COLOR = 'brown4' # アップグレード画面の実装済みカーソルのドットの色
    CURSOR_GRID_COLOR = 'GreenYellow' # アップグレード画面のカーソルのグリッドの色
    MAX_VALUE = 'brown1' # 上限に達してそれ以上アップグレードできないときの'MAX'の色
    MONEY_COLOR_FALSE = 'dark gray' # 払えないお金の色
    MONEY_COLOR_TRUE = 'gold' # 払えるお金の色
    OK_CURSOR_COLOR = 'BlueViolet' # アップデート可能のマスにオンマウスで出る枠の色
    COLOR_DIC = {}
    # 初期値
    index = 0
    mouse_c = False
    mouse_x = 0
    mouse_y = 0
    cursor_x = 0 # カーソルの中心マスx
    cursor_y = 0 # カーソルの中心マスy
    block_position_list =[]
    tmr_max = 100 # マウス描画の制限時間
    tmr = tmr_max
    money = 0
    max_money_value = 1 # ブロック一個の消滅が最大いくらのmoneyを生み出すか
    max_mouse_block_strength = 101 # マウスブロックのmax強度 101～最大値(199)
    max_enemy_block_strength = 201 # 敵ブロックのmax強度 201～上限なし
    pass_count = 0 # クリアカウント　敵ブロックのmax強度に影響
    grow_count = 0 # 地面のせり上がりアニメーションに使う変数
    gameover_tmr = 0 # gameoverの時にアニメーションで使う変数
    before_money = 0 # 今回ウェーブの習得金を表示するのに使う変数
    fix_money = 0 # 今回ウェーブの習得金を固定するための変数
    # グリッド関連
    GRID_H = 65 # H65*W50 SIZE9
    GRID_W = 52
    g_list = [] # 敵ブロック・マウスブロック・爆発ブロック・空白。すべてのマスの情報
    G_START_X = 20
    G_START_Y = 20
    G_SIZE = 9
    G_SUKIMA = 1
    MASUME_GROW = 0.1 #　高さ*MASUME_GROW 地面がせり上がる 標準0.1
    # カーソル関連
    cursor_shape_list = []
    cursor_max = 3 # 必ず奇数　cursor_max*cursor_maxの正方形がMAX範囲になる
                   # (cursor_max // 2 )がカーソルの中心座標になる
    for _ in range(cursor_max):
        cursor_shape_list.append([0] * cursor_max) 
    cursor_shape_list[cursor_max // 2][cursor_max // 2] = 1
    # # ↓デバッグ用のカーソル
    # cursor_shape_list = [[1, 0, 0, 0, 1], 
    #                      [0, 1, 0, 1, 0], 
    #                      [0, 0, 1, 0, 0], 
    #                      [0, 1, 0, 1, 0], 
    #                      [1, 0, 0, 0, 1]]
    # cursor_shape_list = [[1, 1, 1],
    #                      [1, 1, 1],
    #                      [1, 1, 1]]
    # # ↑デバッグ用のカーソル

    # ファイル関連
    read_save_list =[]
    # 防衛回数[0]　＄倍率[1]　マウス強度[2]　一辺[3]　カーソル形リスト[4:]　
    height_scores =[pass_count, max_money_value, max_mouse_block_strength, len(cursor_shape_list)]
    for i in range(len(cursor_shape_list)):
        for j in (cursor_shape_list[i]):
            height_scores.append(j) 

    # アップグレード関連
    count_mouse_strength = 0 # マウスブロック強化の回数
    count_cursor_dot = 0 # カーソルドットを増やした回数
    count_cursor_max = 0 # カーソル範囲を増やした回数
    count_value_money = 0 # 獲得金を増やした回数
    # 難易度関連
    enemy_mag = 3.20 # 敵ブロックの成長倍率（最低1.00）ちょいむず4.20
    BUKKA = 100 # 全てのアップグレード資金の基数
    BUKKA_DOT = 3.00 # ドット追加の資金
    BUKKA_VALUE = 1.50 # 獲得金の資金
    BUKKA_STR = 2.00 # 強化の資金 
    BUKKA_DOTMAX = 70.00 # カーソル範囲拡大の資金

    # 描画用変数
    # 土台メニュー左上xy
    m_x_s = G_START_X + G_SIZE * GRID_W + SUKIMA_W
    m_y_s = G_START_Y
    # 土台メニュー右下xy
    m_x_g = WIDTH - SUKIMA_W
    m_y_g = G_START_Y + G_SIZE * GRID_H
    # 土台メニュー横と縦のサイズ
    m_wi = m_x_g - m_x_s
    m_hi = m_y_g - m_y_s
    # 土台メニュー横の比率
    m_wi_1_2 = m_x_s + m_wi * 1 / 2
    m_wi_1_6 = m_x_s + m_wi * 1 / 6
    m_wi_5_6 = m_x_s + m_wi * 5 / 6
    m_wi_1_50 = m_x_s + m_wi * 1 / 50
    m_wi_16_50 = m_x_s + m_wi * 16 / 50
    m_wi_17_50 = m_x_s + m_wi * 17 / 50
    m_wi_33_50 = m_x_s + m_wi * 33 / 50
    m_wi_34_50 = m_x_s + m_wi * 34 / 50
    m_wi_49_50 = m_x_s + m_wi * 49 / 50
    # 土台メニュー縦の比率
    m_hi_3_100 = m_y_s + m_hi * 3 / 100
    m_hi_29_50 = m_y_s + m_hi * 29 / 50
    m_hi_31_50 = m_y_s + m_hi * 31 / 50
    m_hi_34_50 = m_y_s + m_hi * 34 / 50
    m_hi_37_50 = m_y_s + m_hi * 37 / 50
    m_hi_40_50 = m_y_s + m_hi * 40 / 50
    m_hi_42_50 = m_y_s + m_hi * 42 / 50
    m_hi_43_50 = m_y_s + m_hi * 43 / 50
    m_hi_45_50 = m_y_s + m_hi * 45 / 50
    m_hi_47_50 = m_y_s + m_hi * 47 / 50
    m_hi_48_50 = m_y_s + m_hi * 48 / 50

    # カーソル形メニュー
    # カーソル形メニュー左上xy
    bm_x_s = m_x_s + m_wi * 1 / 6
    bm_y_s = m_y_s + m_hi * 3 / 50
    # カーソル形メニュー右下xy
    bm_x_g = m_x_s + m_wi * 5 / 6
    bm_y_g = m_y_s + m_hi * 27 / 50
    # カーソル形メニュー横の長さ縦の長さ
    bm_wi = bm_x_g - bm_x_s
    bm_hi = bm_y_g - bm_y_s
    # カーソル形メニュー1マスの横と縦の長さ
    bm_one_wi = bm_wi / len(cursor_shape_list)
    bm_one_hi = bm_hi / len(cursor_shape_list)
    # カーソル形メニューの比率
    bm_wi_1_2 = bm_x_s + bm_wi * 1 / 2
    bm_hi_3_4 = bm_y_s + bm_hi * 3 / 4
    # WIDTHとHEIGHTの比率
    wi_1_2 = WIDTH * 1 / 2
    wi_1_3 = WIDTH * 1 / 3
    wi_2_3 = WIDTH * 2 / 3
    wi_1_5 = WIDTH * 1 / 5
    wi_2_5 = WIDTH * 2 / 5
    wi_3_5 = WIDTH * 3 / 5
    wi_4_5 = WIDTH * 4 / 5
    wi_1_6 = WIDTH * 1 / 6
    wi_5_6 = WIDTH * 5 / 6
    hi_1_2 = HEIGHT * 1 / 2
    hi_1_4 = HEIGHT * 1 / 4
    hi_1_5 = HEIGHT * 1 / 5
    hi_2_5 = HEIGHT * 2 / 5
    hi_4_5 = HEIGHT * 4 / 5
    hi_30_100 = HEIGHT * 30 / 100
    hi_35_100 = HEIGHT * 35 / 100
    hi_45_100 = HEIGHT * 45 / 100
    hi_55_100 = HEIGHT * 55 / 100
    hi_51_100 = HEIGHT * 51 / 100
    hi_58_100 = HEIGHT * 58 / 100
    hi_63_100 = HEIGHT * 63 / 100
    hi_60_100 = HEIGHT * 60 / 100
    hi_70_100 = HEIGHT * 70 / 100

    def __init__(self, master = None):
        super().__init__(master)
        self.master.title('ペイント落ちゲー')
        self.canvas = tkinter.Canvas(self.master, width=self.WIDTH, height=self.HEIGHT, bg=self.BACK_COLOR)
        self.canvas.pack()
        self.main()

    def draw_title_screen(self):
        # タイトル画面の描画 WIDTHとHEIGHTの比率で位置を決定したい
        # 座布団
        zabuton_color = self.COLOR_DIC[0]
        self.canvas.create_text(987,610,text='click!',
                                font=(self.FONT, 7), fill='gray5', tag='not_delete')
        self.canvas.create_rectangle(self.SUKIMA_W, self.SUKIMA_H, 
                                     self.WIDTH - self.SUKIMA_W, self.HEIGHT - self.SUKIMA_H, 
                                     fill=zabuton_color, width=0, tag='title')
        # 文字：ドロー落ちゲー
        self.canvas.create_text(self.wi_1_2 + 2, self.hi_1_4 + 2,
                                 text = 'ペイント落ちゲー', font=(self.FONT, 70), fill=self.SHADOW_COLOR, tag='title')
        self.canvas.create_text(self.wi_1_2 , self.hi_1_4,
                                 text = 'ペイント落ちゲー', font=(self.FONT, 70), fill=self.COLOR_DIC[1], tag='title')
        # タイトル画面のスタートボタン枠
        self.canvas.create_rectangle(self.wi_2_5, self.hi_35_100,
                                     self.wi_3_5, self.hi_45_100,
                                     outline=self.COLOR_DIC[2], width=4, tag='title')
        self.canvas.create_rectangle(self.wi_2_5 +5, self.hi_35_100 +5,
                                     self.wi_3_5 -5, self.hi_45_100 -5,
                                     outline=self.COLOR_DIC[2], tag='title')
        # スタートの文字　
        self.canvas.create_text(self.wi_1_2 + 1 ,self.hi_2_5 + 1,
                                text='スタート', font=(self.FONT, 30), fill=self.SHADOW_COLOR, tag='title')
        self.canvas.create_text(self.wi_1_2 ,self.hi_2_5,
                                text='スタート', font=(self.FONT, 30), fill=self.COLOR_DIC[3], tag='title')
        # ハイスコア
        self.canvas.create_text(self.wi_1_2 + 1 ,self.hi_51_100 + 1,
                                text=f'最高防衛{self.read_save_list[0]}回'.center(14,'*'),
                                  font=(self.FONT, 30), fill=self.SHADOW_COLOR, tag='title')
        self.canvas.create_text(self.wi_1_2 ,self.hi_51_100,
                                text=f'最高防衛{self.read_save_list[0]}回'.center(14,'*'),
                                  font=(self.FONT, 30), fill=self.COLOR_DIC[4], tag='title')
        self.canvas.create_text(self.wi_1_2 + 1,self.hi_58_100 + 1,
                                text=f'最高防衛時の max強度: {self.read_save_list[2] - 100}　'
                                     f'max$: {self.read_save_list[1]}'.center(14,'*'),
                                  font=(self.FONT, 20), fill=self.SHADOW_COLOR, tag='title')
        self.canvas.create_text(self.wi_1_2 ,self.hi_58_100,
                                text=f'最高防衛時の max強度: {self.read_save_list[2] - 100}　'
                                     f'max$: {self.read_save_list[1]}'.center(14,'*'),
                                  font=(self.FONT, 20), fill=self.COLOR_DIC[4], tag='title')
        
        # ハイスコアカーソル
        # self.read_save_list[4:]がカーソル形のデータ
        # self.read_save_list[3]が一辺の長さ　を参照してハイスコアカーソルの格子 座布団と同じ色
        # len(self.read_save_list[4:]) の平方根がself.read_save_list[3]で一辺の長さ　だけど出し方はわからないから[3]使う
        for i in range(self.read_save_list[3]):
            for j in range(self.read_save_list[3]):
                if self.read_save_list[self.read_save_list[3] * i + j + 4] != 0:
                    model_color = self.COLOR_DIC[5] # 背景と違う色
                else:
                    model_color = zabuton_color # 背景と同じ色　self.COLOR_DIC[0]
                self.canvas.create_rectangle(self.wi_2_5 + self.wi_1_5 / self.read_save_list[3] * j,
                                            self.hi_63_100 + self.hi_30_100 / self.read_save_list[3] * i,
                                            self.wi_2_5 + self.wi_1_5 / self.read_save_list[3] * (j + 1),
                                            self.hi_63_100 + self.hi_30_100 / self.read_save_list[3] * (i +1 ),
                                            outline= self.SHADOW_COLOR, fill =model_color ,tag= 'title')

    def draw_start_button(self):
        # 準備OKボタン描画
        self.canvas.create_rectangle((self.G_START_X + self.GRID_W * self.G_SIZE * 0.5) - self.GRID_W* self.G_SIZE* 0.3,
                                     self.G_START_Y + self.GRID_H * self.G_SIZE *0.2,
                                     (self.G_START_X + self.GRID_W * self.G_SIZE * 0.5) + self.GRID_W* self.G_SIZE* 0.3,
                                     self.G_START_Y + self.GRID_H * self.G_SIZE *0.4,
                                     fill='DarkSeaGreen3', tag='start_button')
        self.canvas.create_text(self.G_START_X + (self.GRID_W * self.G_SIZE / 2),
                                self.G_START_Y + (self.GRID_H * self.G_SIZE *0.3),
                                text= '準備OK',font= (self.FONT, int(self.GRID_W* self.G_SIZE * 0.05)),
                                fill=self.GRID_COLOR_BACK, tag='start_button')

    def click_start_button(self):
        # 準備OKボタンが押されたかの判定
        if self.mouse_c:
            if (self.G_START_X + self.GRID_W * self.G_SIZE * 0.5) - self.GRID_W* self.G_SIZE* 0.3 < self.mouse_x\
                < (self.G_START_X + self.GRID_W * self.G_SIZE * 0.5) + self.GRID_W* self.G_SIZE* 0.3 and\
                self.G_START_Y + self.GRID_H * self.G_SIZE *0.2 < self.mouse_y\
                < self.G_START_Y + self.GRID_H * self.G_SIZE *0.4:
                self.canvas.delete('start_button')
                return True
        else:
            return False
    
    def first_mountain_generate(self):
        # 最初の山を作る 高さに対して一割
        # 山の高さをランダム生成してrlistに格納
        rlist = [random.randint(1, int(self.GRID_H * 0.5)) for _ in range(self.GRID_W)]
        # rlistを元に山を生成。敵ブロックの強度は上限を参照してランダム
        self.g_list = [[0 if y < self.GRID_H - rlist[x] else random.randint(201,self.max_enemy_block_strength)\
                         for x in range(self.GRID_W)] for y in range(self.GRID_H)]
        for y in range(self.GRID_H):
            for x in range(self.GRID_W):
                if self.g_list[y][x] != 0:
                    self.block_position_list.append((y, x))
                    # block_position_listには空以外の座標をタプルで保管。内容不問

    def define_cursor_shape_tuple_list(self): 
        # カーソルのドット位置を格納したタプルのリストを生成
        # 中心点からみたらそれぞれのドットがどの位置にあるかの相対パスで集める
        cursor_shape_tuple_list =[]
        center = len(self.cursor_shape_list) // 2
        for y in range(len(self.cursor_shape_list)):
            for x in  range(len(self.cursor_shape_list)):
                if self.cursor_shape_list[y][x] != 0:
                    cursor_shape_tuple_list.append((y-center, x-center))
        return cursor_shape_tuple_list

    def cursor_pos_defin(self, cursor_shape_tuple_list):
        # マウスが範囲内にあるならばカーソルの中心が確定,
        # カーソルの座標も確定
        # カーソルでなぞったところがMOUSE_COLOR_KARI色に塗られる
        # g_list_append_cursor()と同時進行　
        if self.G_START_X < self.mouse_x < self.G_START_X + self.G_SIZE * self.GRID_W\
        and self.G_START_Y + self.G_SUKIMA < self.mouse_y < self.G_START_Y + self.G_SIZE * self.GRID_H:
            self.cursor_x = int((self.mouse_x-self.G_START_X)/self.G_SIZE) # g_listにおけるカーソル中心x
            self.cursor_y = int((self.mouse_y-self.G_START_Y)/self.G_SIZE) # g_listにおけるカーソル中心y
            for y, x in cursor_shape_tuple_list:
                if 0 <= x + self.cursor_x < self.GRID_W and 0 <= y + self.cursor_y < self.GRID_H:
                    self.canvas.create_rectangle((x + self.cursor_x) * self.G_SIZE + self.G_START_X + self.G_SUKIMA,
                                                (y + self.cursor_y) * self.G_SIZE + self.G_START_Y + self.G_SUKIMA,
                                                (x + self.cursor_x) * self.G_SIZE + self.G_START_X + self.G_SIZE,
                                                (y + self.cursor_y) * self.G_SIZE + self.G_START_Y + self.G_SIZE,
                                                fill=self.MOUSE_COLOR_KARI, width=0, tag='cursor_track')
                    
    def g_list_append_cursor(self, cursor_shape_tuple_list):
        # g_listにカーソル形リストが触れた部分のg_listを書き換える。マウスブロックの出現
        # block_position_listにブロック位置を格納 
        # cursor_pos_defin()と同時進行　
        for y, x in cursor_shape_tuple_list:
                if 0 <= x + self.cursor_x < self.GRID_W and 0 <= y + self.cursor_y < self.GRID_H\
                    and self.g_list[y + self.cursor_y][x + self.cursor_x] == 0:
                    r = random.randint(101, self.max_mouse_block_strength)
                    self.g_list[self.cursor_y + y][self.cursor_x + x] = r
                    self.block_position_list.append((self.cursor_y + y, self.cursor_x + x))

    def masume_drop(self):
        # 升目の落下処理・対消滅の処理・お金の加算
        new_block_position_list = []
        for y, x in self.block_position_list:
            if y + 1 <self.GRID_H and self.g_list[y+1][x] == 0:
                # 落下処理　落下するのはマウスブロックのみ
                self.g_list[y+1][x] = self.g_list[y][x]
                self.g_list[y][x] = 0
                new_block_position_list.append((y+1, x))
            else:
                new_block_position_list.append((y,x))
            # 落下した後の処理
            if  y + 1 <self.GRID_H and 101 <= self.g_list[y][x] <= self.max_mouse_block_strength:
                # マウスブロックを補足
                # 下のブロックの強度を下げる。対消滅、爆発処理・money加算
                if 200 <= self.g_list[y+1][x] <= self.max_enemy_block_strength:
                    self.g_list[y][x] -= 1 
                    if self.g_list[y][x] <= 100:
                        # マウスブロックの強度が下がり100以下になったら100番にする→爆発
                        self.g_list[y][x] = 100
                    self.g_list[y+1][x] -= 1
                    if self.g_list[y+1][x] <= 200:
                        # 敵ブロックの耐久が200以下になったら100番にする→爆発
                        self.g_list[y+1][x] = 100
                        new_block_position_list.append((y+1, x))
            if self.g_list[y][x] == 100:
                # 爆発四散処理　お金の加算
                self.g_list[y][x] = 0
                self.money += random.randint(1, self.max_money_value)
                new_block_position_list.remove((y, x))
        self.block_position_list = new_block_position_list

    def masume_back_draw(self):
        # 升目の座布団（結果的には格子）を描画
        self.canvas.create_rectangle(self.G_START_X + self.G_SUKIMA,
                                    self.G_START_Y + self.G_SUKIMA,
                                    self.G_START_X + self.G_SIZE * self.GRID_W,
                                    self.G_START_Y + self.G_SIZE * self.GRID_H,
                                    fill=self.GRID_COLOR_BACK, width=0, tag='grid_base')
        
    def random_color_generate(self):
        # ランダムな色を生成
        red = random.randint(0,255)
        green = random.randint(0,255)
        blue = random.randint(0,255)
        return f'#{red:02x}{green:02x}{blue:02x}'
    
    def color_dic_generation(self):
        # ランダム色100種類の辞書を生成
        for i in range(100):
            r = self.random_color_generate()
            self.COLOR_DIC[i] = r

    def masume_draw(self):
        # 升目を描写。爆発エフェクトも描写
        self.canvas.delete('masume')
        self.canvas.delete('explosion')
        for y, x in self.block_position_list:
            if 101 <= self.g_list[y][x] <= self.max_mouse_block_strength: # マウスブロック描画
                # color = None
                mouse_color = self.g_list[y][x] 
                mouse_color += 55 # 敵ブロックと色を一致させないように色番号をずらす
                for i in range(100,1000,100): # 下二桁だけにして色辞書に合わせる
                    if i <= mouse_color <= i + 99:
                        mouse_color = mouse_color - i
                        break
                self.canvas.create_rectangle(self.G_START_X + self.G_SIZE * x + self.G_SUKIMA,
                                            self.G_START_Y + self.G_SIZE * y + self.G_SUKIMA,
                                            self.G_START_X + self.G_SIZE * x + self.G_SIZE,
                                            self.G_START_Y + self.G_SIZE * y + self.G_SIZE,
                                            fill=self.COLOR_DIC[mouse_color],
                                            width=0, tag ='masume')
            elif 201 <= self.g_list[y][x] <= self.max_enemy_block_strength: # 敵ブロック
                color = None
                for i in range(100,1000,100): # 下二桁だけにして色辞書に合わせる
                    if i <= self.g_list[y][x] <= i + 99:
                        color = self.g_list[y][x] - i
                        break
                self.canvas.create_rectangle(self.G_START_X + self.G_SIZE * x + self.G_SUKIMA,
                                            self.G_START_Y + self.G_SIZE * y + self.G_SUKIMA,
                                            self.G_START_X + self.G_SIZE * x + self.G_SIZE,
                                            self.G_START_Y + self.G_SIZE * y + self.G_SIZE,
                                            fill=self.COLOR_DIC[color],
                                            width=0, tag ='masume')
            elif self.g_list[y][x] == 100: # 爆発
                ex_size = random.randint(1,5)
                self.canvas.create_oval(self.G_START_X + self.G_SIZE * x - self.G_SIZE * ex_size,
                                        self.G_START_Y + self.G_SIZE * y - self.G_SIZE * ex_size,
                                        self.G_START_X + self.G_SIZE * x + self.G_SIZE * ex_size,
                                        self.G_START_Y + self.G_SIZE * y + self.G_SIZE * ex_size,
                                        outline=self.random_color_generate(), width=8, tag='explosion')
    def g_list_mouse_change(self):
        # マウスブロックを強度1の敵ブロックにする
        # g_listにマウスブロック（101番～強化値）があるか検索
        flag_mouse_block = False
        for y in range(self.GRID_H):
            for x in range(self.GRID_W):
                if 101 <= self.g_list[y][x] <= self.max_mouse_block_strength:
                    flag_mouse_block = True
                    break
        # マウスブロック（101番以上）があるなら強度1の敵ブロックに置き換え
        if flag_mouse_block:
            for y, x in self.block_position_list:
                if 101 <= self.g_list[y][x] <= self.max_mouse_block_strength:
                    self.g_list[y][x] = 201
        
    def masume_grow(self):
        # 地面がせり上がる
        # 削除、追加、表示をadd_row回繰り返す

        self.g_list.pop(0)
        add_int = random.randint(201, self.max_enemy_block_strength)
        self.g_list.append([add_int] * self.GRID_W)
        self.position_list_update()


    def position_list_update(self):
        # g_listの内容をposition_listに更新
        new_block_position_list = []
        for y in range(self.GRID_H):
            for x in range(self.GRID_W):
                if self.g_list[y][x] != 0:
                    new_block_position_list.append((y, x))
        self.block_position_list = list(new_block_position_list)

    def pass_count_add(self):
        # 面クリア回数と敵ブロックの耐久加算
        self.pass_count += 1
        # max_enemy_block_strength初期値201 pass_count初期値0
        # それぞれ上限なし
        # 6k0.5 ぬるい 6k0.9壁
        step = int((self.pass_count / 6) + 1)
        self.max_enemy_block_strength = int((self.pass_count * self.enemy_mag) *  (step*0.6) + 201)
        
    def gameover_judge(self):
        # ゲームオーバー判定
        if 0 < sum(self.g_list[0]):
            return True
        else:
            return False

    def menu_draw(self):
        # メニューのベースを描画　グリッドの大きさで指定したい
        self.canvas.delete('pass_count')
        self.canvas.delete('money')
        self.canvas.delete('menu') # パスカウントとマネー以外はmenuで統一してよいのでは？ 
        # 枠　メニュー黒座布団
        self.canvas.create_rectangle(self.m_x_s, self.m_y_s, self.m_x_g , self.m_y_g,
                                    fill=self.GRID_COLOR_BACK, width=0,tag ='menu' )
        # 文字　+＄
        if self.index == 11:
            self.canvas.create_text(self.m_wi_1_2, self.m_hi_48_50,
                                    text = f'+${self.fix_money:,}',fill=self.WHITEY_COLOR,
                                    font=(self.FONT, int(self.m_wi * 0.04)), tag='wave_money')
        else:
            self.canvas.create_text(self.m_wi_1_2, self.m_hi_48_50,
                                    text = f'+${(self.money - self.before_money):,}',fill=self.WHITEY_COLOR,
                                    font=(self.FONT, int(self.m_wi * 0.04)), tag='wave_money')
        # 文字　＄
        self.canvas.create_text(self.m_wi_1_2, self.m_hi_45_50,
                                text = f'${self.money:,}',fill=self.WHITEY_COLOR,
                                font=(self.FONT, int(self.m_wi * 0.08)), tag='money')

        # 文字　防衛回数
        self.canvas.create_text(self.m_wi_1_2, self.m_hi_42_50,
                                text = f'防衛：{self.pass_count}回',fill=self.WHITEY_COLOR,
                                font=(self.FONT, int(self.m_wi * 0.04)), tag='pass_count')

        # 枠　外枠現在のカーソル
        self.canvas.create_rectangle(self.bm_x_s, self.bm_y_s, self.bm_x_g, self.bm_y_g, 
                                     outline='green', width=5, tag ='menu' )
        # 枠・文字資金　カーソルドット
        if self.cal_cost_cursor_dot() <= self.money:
            model_money_color = self.MONEY_COLOR_TRUE
        else:
            model_money_color = self.MONEY_COLOR_FALSE
        for i in range(len(self.cursor_shape_list)):
            for j in range(len(self.cursor_shape_list)):
                if self.cursor_shape_list[i][j] != 0:
                    model_color = self.CURSOR_DOT_COLOR
                    model_text = ''
                else:
                    model_color = self.GRID_COLOR_BACK
                    model_text = f'${self.cal_cost_cursor_dot()}'
                self.canvas.create_rectangle(self.bm_x_s + self.bm_wi / len(self.cursor_shape_list) * j,
                                             self.bm_y_s + self.bm_hi / len(self.cursor_shape_list) * i,
                                             self.bm_x_s + self.bm_wi / len(self.cursor_shape_list) * (j+1),
                                             self.bm_y_s + self.bm_hi / len(self.cursor_shape_list) * (i+1),
                                             outline=self.CURSOR_GRID_COLOR, fill =model_color ,tag= 'menu')
                if  len(self.cursor_shape_list) <= 3:
                    self.canvas.create_text(self.bm_x_s + self.bm_wi * (j+0.5) / len(self.cursor_shape_list),
                                            self.bm_y_s + self.bm_hi * (i+0.5) / len(self.cursor_shape_list) ,
                                            text=model_text,font=(self.FONT, int(self.bm_one_wi * 0.2)),anchor='c',
                                            fill=model_money_color, tag= 'menu')
                else:
                    self.canvas.create_text(self.bm_wi_1_2, self.m_hi_29_50,
                                            text=model_text,font=(self.FONT, int(self.bm_wi * 0.10)),anchor='c',
                                            fill=model_money_color, tag= 'menu')

        # 文字　ハイスコア
        self.canvas.create_text(self.m_wi_1_2, self.m_hi_3_100,
                                text=f'最高防衛{self.read_save_list[0]}回', 
                                font=(self.FONT, int(self.m_wi * 0.03)),
                                fill=self.WHITEY_COLOR, tag='menu')
        # 枠　maxカーソル範囲
        self.canvas.create_rectangle(self.m_wi_1_50, self.m_hi_31_50, self.m_wi_16_50, self.m_hi_40_50,
                                     outline=self.WHITEY_COLOR, width=1, tag='menu')
        # 文字　maxカーソル範囲
        self.canvas.create_text(self.m_wi_1_6, self.m_hi_34_50,
                                text=f'{self.cursor_max}×{self.cursor_max}',fill=self.WHITEY_COLOR,
                                font=(self.FONT, int(self.m_wi * 0.05)), tag ='menu')
        # 文字資金　maxカーソル範囲
        if self.cal_cost_cursor_max() <= self.money:
            model_money_color = self.MONEY_COLOR_TRUE
            model_money_size = int(self.m_wi * 0.04)
        else:
            model_money_color = self.MONEY_COLOR_FALSE
            model_money_size = int(self.m_wi * 0.03)
        self.canvas.create_text(self.m_wi_1_6,
                                self.m_hi_37_50,
                                text=f'${self.cal_cost_cursor_max()}',fill=model_money_color,
                                font=(self.FONT, model_money_size), tag ='menu')
        # 枠　max強度
        self.canvas.create_rectangle(self.m_wi_17_50, self.m_hi_31_50, self.m_wi_33_50, self.m_hi_40_50,
                                     outline=self.WHITEY_COLOR, width=1, tag='menu')
        # 文字　max強度
        self.canvas.create_text(self.m_wi_1_2, self.m_hi_34_50,
                                text=f'強度{self.max_mouse_block_strength - 100}',fill=self.WHITEY_COLOR,
                                font=(self.FONT, int(self.m_wi * 0.05)), tag='menu')
        # 文字資金　max強度
        if self.cal_cost_mouse_strength() <= self.money:
            model_money_color = self.MONEY_COLOR_TRUE
            model_money_size = int(self.m_wi * 0.04)
        else:
            model_money_color = self.MONEY_COLOR_FALSE
            model_money_size = int(self.m_wi * 0.03)
        if 199 <= self.max_mouse_block_strength:
            model_money_color = self.MAX_VALUE
            model_money_size = int(self.m_wi * 0.03)
            model_text = 'MAX'
        else:
            model_text = f'${self.cal_cost_mouse_strength()}'
        self.canvas.create_text(self.m_wi_1_2,
                                self.m_hi_37_50,
                                text = model_text,fill=model_money_color,
                                font=(self.FONT, model_money_size), tag='menu')
        # 枠　max獲得金
        self.canvas.create_rectangle(self.m_wi_34_50, self.m_hi_31_50, self.m_wi_49_50, self.m_hi_40_50,
                                     outline=self.WHITEY_COLOR, width=1, tag='menu')
        # 文字　max獲得金
        self.canvas.create_text(self.m_wi_5_6, self.m_hi_34_50,
                                text=f'max${self.max_money_value}',fill=self.WHITEY_COLOR,
                                font=(self.FONT, int(self.m_wi * 0.05)), tag='menu')
        # 文字資金　max獲得金
        if self.cal_cost_value_money() <= self.money:
            model_money_color = self.MONEY_COLOR_TRUE
            model_money_size = int(self.m_wi * 0.04)
        else:
            model_money_color = self.MONEY_COLOR_FALSE
            model_money_size = int(self.m_wi * 0.03)
        self.canvas.create_text(self.m_wi_5_6, self.m_hi_37_50,
                                text=f'${self.cal_cost_value_money()}',fill=model_money_color,
                                font=(self.FONT, model_money_size), tag='menu')
        
    def upgrade_click(self):
        #アップグレード処理。
        self.canvas.delete('ok_cursor')
        # カーソルドット
        cursor_dot_click_scope_list = []
        # アップグレード可能なドットの範囲を(スタートx,ゴールx,スタートy,ゴールy)のタプルのリストを作成
        if self.cal_cost_cursor_dot() <= self.money:
            for i in range(len(self.cursor_shape_list)):
                for j in range(len(self.cursor_shape_list)):
                    if self.cursor_shape_list[i][j] != 1:
                        cursor_dot_click_scope_list.append((self.bm_x_s + self.bm_wi / len(self.cursor_shape_list) * j,
                                                        self.bm_x_s + self.bm_wi / len(self.cursor_shape_list) * (j+1),
                                                        self.bm_y_s + self.bm_hi / len(self.cursor_shape_list) * i,
                                                        self.bm_y_s + self.bm_hi / len(self.cursor_shape_list) * (i+1)))
        # タプルのリストからxの範囲とyの範囲を取り出してクリック判定の範囲を条件式に渡す
        for xy in cursor_dot_click_scope_list:
            if xy[0] < self.mouse_x < xy[1] and xy[2] < self.mouse_y < xy[3]:
                self.canvas.create_rectangle(xy[0], xy[2], xy[1], xy[3],
                                outline=self.OK_CURSOR_COLOR, width=5, tag ='ok_cursor')
                self.canvas.create_rectangle(xy[0]+7, xy[2]+7, xy[1]-7, xy[3]-7,
                                outline=self.OK_CURSOR_COLOR, width=1, tag ='ok_cursor')
                if self.mouse_c:
                    # クリックされた座標からカーソル形リストのどのドットを指しているのかを判定
                    # カーソルメニューの縦横をカーソルリストのlen数で割った数字と一致したスタートx、スタートyが指定したドット
                    rrr = None
                    ccc = None
                    
                    for i in range(len(self.cursor_shape_list)):
                       if int(xy[0]) == int(self.bm_x_s + (self.bm_wi * i / len(self.cursor_shape_list))):
                           ccc = i
                           break
                    for i in range(len(self.cursor_shape_list)):
                       if int(xy[2]) == int(self.bm_y_s + (self.bm_hi * i / len(self.cursor_shape_list))):
                           rrr = i
                           break
                    self.mouse_c =False
                    self.money -= self.cal_cost_cursor_dot()
                    self.count_cursor_dot += 1
                    self.cursor_shape_list[rrr][ccc] = 1
                    self.menu_draw()
        # maxカーソル範囲
        if self.m_wi_1_50 < self.mouse_x < self.m_wi_16_50 and\
                self.m_hi_31_50 < self.mouse_y < self.m_hi_40_50 and\
                self.cal_cost_cursor_max() <= self.money:
            self.canvas.create_rectangle(self.m_wi_1_50, self.m_hi_31_50,
                                         self.m_wi_16_50, self.m_hi_40_50,
                                         outline=self.OK_CURSOR_COLOR, width=5, tag ='ok_cursor')
            self.canvas.create_rectangle(self.m_wi_1_50 + 7, self.m_hi_31_50 + 7,
                                         self.m_wi_16_50 - 7, self.m_hi_40_50 - 7,
                                         outline=self.OK_CURSOR_COLOR, width=1, tag ='ok_cursor')
            if self.mouse_c:
                self.mouse_c = False
                self.money -= self.cal_cost_cursor_max()
                self.count_cursor_max += 1
                self.cursor_max += 2
                self.cursor_scope_up()
                self.menu_draw()
        # max強度
        if self.m_wi_17_50 < self.mouse_x < self.m_wi_33_50 and\
                self.m_hi_31_50 < self.mouse_y < self.m_hi_40_50 and\
                self.cal_cost_mouse_strength() <= self.money and\
                self.max_mouse_block_strength < 199:
            self.canvas.create_rectangle(self.m_wi_17_50, self.m_hi_31_50,
                                self.m_wi_33_50, self.m_hi_40_50,
                                outline=self.OK_CURSOR_COLOR, width=5, tag ='ok_cursor')
            self.canvas.create_rectangle(self.m_wi_17_50 + 7, self.m_hi_31_50 + 7,
                                self.m_wi_33_50 - 7, self.m_hi_40_50 - 7,
                                outline=self.OK_CURSOR_COLOR, width=1, tag ='ok_cursor')
            if self.mouse_c:
                self.mouse_c = False
                self.money -= self.cal_cost_mouse_strength()
                self.count_mouse_strength += 1
                self.max_mouse_block_strength += 1
                self.menu_draw()
        # max獲得金
        if self.m_wi_34_50 < self.mouse_x < self.m_wi_49_50 and\
                self.m_hi_31_50 < self.mouse_y < self.m_hi_40_50 and\
                self.cal_cost_value_money() <= self.money:
            self.canvas.create_rectangle(self.m_wi_34_50, self.m_hi_31_50,
                                self.m_wi_49_50, self.m_hi_40_50,
                                outline=self.OK_CURSOR_COLOR, width=5, tag ='ok_cursor')
            self.canvas.create_rectangle(self.m_wi_34_50 + 7, self.m_hi_31_50 + 7,
                                self.m_wi_49_50 - 7, self.m_hi_40_50 - 7,
                                outline=self.OK_CURSOR_COLOR, width=1, tag ='ok_cursor')
            if self.mouse_c:
                self.mouse_c = False
                self.money -= self.cal_cost_value_money()
                self.count_value_money += 1
                self.max_money_value += self.cal_max_money_value_up()
                self.menu_draw()

    def cal_max_money_value_up(self):
        # 獲得金の上り幅
        # 10刻みぬるい
        # step = int(self.count_value_money / 20) + 1
        # return int(self.count_value_money * step * 1.05) 
        return int(self.count_value_money / 20) + 1

    def cursor_scope_up(self):
        #カーソルを拡張する self.cursor_max
        new_list = []
        new_list.append([0] * (len(self.cursor_shape_list)+2))
        for row in self.cursor_shape_list:
            new_list.append([0]+row+[0])
        new_list.append([0] * (len(self.cursor_shape_list)+2))
        self.cursor_shape_list = list(new_list)

    def update_pass_count(self):
        # 更新した防衛回数を描画
        self.canvas.create_text(self.m_wi_1_2, self.m_hi_42_50,
                                text = f'防衛：{self.pass_count}回',fill=self.WHITEY_COLOR,
                                font=(self.FONT, int(self.m_wi * 0.04)), tag='pass_count')
    def update_wave_money(self):
        # 今回のwaveで稼いだお金
        self.canvas.delete('wave_money')
        # 文字　+＄
        self.canvas.create_text(self.m_wi_1_2, self.m_hi_48_50,
                                text = f'+${(self.money - self.before_money):,}',fill=self.WHITEY_COLOR,
                                font=(self.FONT, int(self.m_wi * 0.04)), tag='wave_money')
    def update_money(self):
        # 現在のお金をメニューに表示
        self.canvas.delete('money')
        # 文字　＄
        self.canvas.create_text(self.m_wi_1_2, self.m_hi_45_50,
                                text = f'${self.money:,}',fill=self.WHITEY_COLOR,
                                font=(self.FONT, int(self.m_wi * 0.08)), tag='money')
        
    def gameover_do(self):
        # ゲームオーバーの演出。ハイスコア更新ならハイスコア演出
        self.gameover_tmr += 1
        if self.gameover_tmr % 2 ==0:
            self.color_dic_generation()
            self.masume_draw()
        if 30 < self.gameover_tmr:
            self.canvas.create_rectangle(self.wi_1_6, self.hi_1_5,
                                         self.wi_5_6, self.hi_4_5,
                                         fill=self.SHADOW_COLOR, width=0, tag='gameover')
            self.canvas.create_rectangle(self.wi_1_6+7, self.hi_1_5+5,
                                         self.wi_5_6-7, self.hi_4_5-5,
                                         outline=self.WHITEY_COLOR, width=5, tag='gameover')
            self.canvas.create_rectangle(self.wi_1_6+9, self.hi_1_5+9,
                                         self.wi_5_6-9, self.hi_4_5-9,
                                         fill=self.GRID_COLOR_BACK, width=0, tag='gameover')
            if self.read_save_list[0] < self.pass_count:
                # 記録更新の場合ハイスコアの文字を出す
                self.canvas.create_text(self.wi_1_2, self.hi_45_100,
                                    text='ハイスコア更新',fill = 'red', font=(self.FONT, int(self.WIDTH * 0.065)),
                                    tag='gameover')
            else:
                # 更新しなかった場合ゲームオーバーの文字を出す
                self.canvas.create_text(self.wi_1_2, self.hi_45_100,
                                    text='GAME OVER',fill = 'red', font=(self.FONT, int(self.WIDTH * 0.07)),
                                    tag='gameover')
        if 50 < self.gameover_tmr:
            self.canvas.create_rectangle(self.wi_1_3, self.hi_60_100,
                                         self.wi_2_3, self.hi_70_100,
                                         fill='gray', width=0, tag='gameover')
            self.canvas.create_text(self.wi_1_2, self.HEIGHT * 0.65,
                                    text='タイトルに戻る',fill = 'black', font=(self.FONT, int(self.WIDTH * 0.03)),
                                    tag='gameover')
            self.gameover_tmr = 0
            return True
        
    def gameover_button(self):
        # タイトルに戻るボタンが押されたら表示を全て消して
        # 変数を初期化　
        if self.mouse_c and self.wi_1_3 < self.mouse_x < self.wi_2_3\
            and self.hi_60_100 < self.mouse_y < self.hi_70_100:
            self.save_date_write() # 記録更新しているか判定して記録更新ならデータファイルを更新
            self.init_value()
            return True
        
    def init_value(self):
            # 表示を全部消す
            self.canvas.delete('gameover')
            self.canvas.delete('start_button')
            self.canvas.delete('cursor_track')
            self.canvas.delete('masume')
            self.canvas.delete('money')
            self.canvas.delete('pass_count')
            self.canvas.delete('grid_base')
            self.canvas.delete('menu')
            self.canvas.delete('wave_money')
            # 変数を全部初期化
            self.money = 0
            self.max_money_value = 1
            self.max_mouse_block_strength = 101
            self.max_enemy_block_strength = 201
            self.pass_count = 0
            self.g_list = []
            self.block_position_list = []
            self.cursor_shape_list = []
            self.cursor_max = 3 # 必ず奇数　cursor_max*cursor_maxの正方形がMAX範囲になる
                        # (cursor_max // 2 )がカーソルの中心座標になる
            for _ in range(self.cursor_max):
                self.cursor_shape_list.append([0] * self.cursor_max) 
            self.cursor_shape_list[self.cursor_max // 2][self.cursor_max // 2] = 1
            self.count_mouse_strength = 0
            self.count_cursor_dot = 0
            self.count_cursor_max = 0
            self.count_value_money = 0

    def save_date_read(self):
        # セーブデータを読みこむ。なかったら生成する
        try:
            with open('save_date_DRAW.txt', 'r') as rfile:
                self.read_save_list = [int(i) for i in rfile.read().split()]
        except:      
            with open('save_date_DRAW.txt', 'w') as wfile:
                for i in self.height_scores:
                    print(i, file = wfile)
                self.read_save_list = self.height_scores

    def save_date_write(self):
        # 今回の防衛回数と記録にある防衛回数を比較して今回の方が高ければ記録を上書きする
        if self.read_save_list[0] < self.pass_count:
            self.height_scores =[] # 防衛回数[0]　＄倍率[1]　マウス強度[2]　一辺[3]　カーソル形リスト[4:]
            self.height_scores.append(self.pass_count)
            self.height_scores.append(self.max_money_value)
            self.height_scores.append(self.max_mouse_block_strength)
            self.height_scores.append(len(self.cursor_shape_list))
            for i in range(len(self.cursor_shape_list)):
                for j in (self.cursor_shape_list[i]):
                    self.height_scores.append(j) # 保存用データのリスト作成完了
            with open('save_date_DRAW.txt', 'w') as wfile:
                for i in self.height_scores:
                    print(i, file = wfile)
        else:
            pass

    # 資金計算式　sikin = 1.15 **(count) * BUKKA_AAA （参考：クッキークリッカー）
    def cal_cost_mouse_strength(self):
        # 強度アップグレードに必要な資金を計算する。 価格[0]
        sikin = 1.15 **(self.count_mouse_strength) * self.BUKKA * self.BUKKA_STR
        return int(sikin)

    def cal_cost_cursor_dot(self):
        # カーソルドットアップグレードに必要な資金を計算する。 価格[1]
        sikin = 1.15 **(self.count_cursor_dot) * self.BUKKA * self.BUKKA_DOT
        return int(sikin)

    def cal_cost_cursor_max(self):
        # カーソル範囲アップグレードに必要な資金を計算する。 価格[2]
        sikin = 1.15 **(self.count_cursor_max) * self.BUKKA * self.BUKKA_DOTMAX
        return int(sikin)

    def cal_cost_value_money(self):
        # 獲得金アップグレードに必要な資金を計算する。 価格[3]
        sikin = 1.15 **(self.count_value_money) * self.BUKKA * self.BUKKA_VALUE
        return int(sikin)

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

    def debug_draw_mouse_xyc(self):
        # デバッグ用　色々表示
        self.canvas.delete('debug_text')
        self.canvas.create_text(self.wi_1_2 ,10,
                                text = f'（デバッグ用）x:{self.mouse_x} y:{self.mouse_y} c:{self.mouse_c} '
                                        f'tmr:{self.tmr} Cx:{self.cursor_x} Cy{self.cursor_y} index:{self.index} '
                                        f'value:{self.max_money_value} mony:{self.money} ',
                                        fill = self.WHITEY_COLOR, tag='debug_text')
        self.canvas.create_text(self.wi_1_2 ,self.HEIGHT * 0.99,
                                text = f'（デバッグ用）敵ブロックmax強度{self.max_enemy_block_strength - 200}',
                                        fill = self.WHITEY_COLOR, tag='debug_text')
        
    def debug_draw_rectangle(self):
        # デバッグ用クリック領域の描画
        self.canvas.create_rectangle(0, 0, self.SUKIMA_W, self.SUKIMA_H, 
                                     fill = self.SHADOW_COLOR, tag='debug')
        self.canvas.create_rectangle(self.SUKIMA_W + self.G_SUKIMA, 0, 
                                     self.SUKIMA_W * 2 + self.G_SUKIMA, self.SUKIMA_H, 
                                     fill = self.SHADOW_COLOR, tag='debug')
    def debug_change_color(self):
        # デバッグ用　色辞書の再定義　再描画
        if self.mouse_c and 980 <= self.mouse_x <= 1000 and\
              600 <= self.mouse_y <= 620 and self.index != 101:
            self.mouse_c = False
            self.color_dic_generation()
            self.masume_draw()
            if self.index == 1:
                self.index = 0

    def debug_money_up(self):
        # デバッグ用金策ボタン
        if self.mouse_c and self.SUKIMA_W + self.G_SUKIMA <= self.mouse_x <= self.SUKIMA_W * 2 + self.G_SUKIMA and\
              0 <= self.mouse_y <= self.SUKIMA_H:
            self.money += 10000
            self.menu_draw()

    def main(self):
        if self.index == 0:
            # タイトル画面の描写
            self.save_date_read() #セーブデータ読み込み、なかったら生成
            self.color_dic_generation() # ランダム色辞書を作っておく
            # self.debug_draw_rectangle() ######## デバッグ用クリック領域の描画
            self.draw_title_screen()
            self.index =1
        elif self.index == 1:
            # プレイヤーのスタート入力待ち。クリックされるとタイトル画面を消す。
            # メニュー画面ベースを作る 最初のgリストを生成。
            if self.mouse_c == True and \
                self.wi_2_5 < self.mouse_x < self.wi_3_5 and\
                self.hi_35_100 < self.mouse_y < self.hi_45_100:
                    self.canvas.delete('title')
                    self.menu_draw()
                    self.masume_back_draw()
                    self.first_mountain_generate()
                    self.index = 2

        elif self.index == 2:
            # リストを元に升目を描画、準備完了ボタンを描画
            self.masume_draw()
            self.draw_start_button()
            self.index= 3

        elif self.index == 3:
            # プレイヤーの準備完了ボタンクリック待ち
            if self.click_start_button():
                self.before_money = self.money
                self.update_wave_money()
                self.index = 4

        elif self.index == 4:
            # カーソルの位置にカーソルの形に応じて線をひく。
            # tmrが0になるまで
            self.tmr -= 1
            self.cursor_shape_tuple_list =self.define_cursor_shape_tuple_list()
            self.cursor_pos_defin(self.cursor_shape_tuple_list)
            self.g_list_append_cursor(self.cursor_shape_tuple_list)
            if self.tmr == 0:
                self.canvas.delete('cursor_track')
                self.tmr = 3
                self.index = 5

        elif self.index == 5:
            # マウスの軌跡がマウスブロックに再描画
            self.masume_draw()
            self.tmr -= 1
            if self.tmr == 0:
                self.tmr = 100
                self.index = 6

        elif self.index == 6:
            # 軌跡が落ちてブロックと対消滅、消滅したブロックに応じてお金加算、メニューに表示
            # 全てのブロックが落下したのを判定して次のindexへ（現状tmr100で次のindexへ）　
            check_position = list(self.block_position_list)
            self.masume_drop()
            self.masume_draw()
            self.update_money()
            self.update_wave_money()
            if check_position ==self.block_position_list:
                # block_position_listに変化がない＝落下し終わった
                self.index = 7

        elif self.index == 7:
            # 残ったマウスブロックが強度1のブロックに代わる。g_list書き換え。再描画。
            self.g_list_mouse_change()
            self.masume_draw()
            self.grow_count = 0
            self.index = 8
        elif self.index ==8:
            # すでにある敵ブロックの強度そのままで地面がせり上がる
            add_row = int(self.GRID_H * self.MASUME_GROW)
            self.grow_count += 1
            self.masume_grow()   
            self.masume_draw()
            if self.grow_count == add_row:
                # せり上がりのアニメーション
                self.index = 9
        elif self.index == 9:
            # ブロックが最上段に達しているか判定
            if self.gameover_judge():
                # 　y\データを更新してgameoverのindexへ
                self.index = 100
            else:
                # pass_countと敵ブロックの耐久加算
                # 防衛回数を再描画してn\次のindexへ
                self.pass_count_add()
                self.update_pass_count()
                self.index = 10

        elif self.index == 10:
            # メニューを描画しなおす
            self.menu_draw() 
            self.draw_start_button()
            self.fix_money = self.money - self.before_money # 今回取得金用の変数
            self.index = 11
        elif self.index == 11:
            #次のフェーズへ行くかアップグレードする
            self.debug_money_up() # ←デバッグ用お金増やし関数#####################################################最後に消す
            self.upgrade_click()
            if self.click_start_button():
                self.before_money = self.money
                self.update_wave_money()
                self.index = 4

        elif self.index == 100:
            # ゲームオーバー演出とタイトルに戻るボタンを出す
            if self.gameover_do():
                self.index = 101
        elif self.index == 101:
            # ボタン押し待ち
            # 押されたらデータファイルを更新して
            # 表示を全て消し変数を初期化してタイトルへ
            if self.gameover_button():
                self.index = 0

        self.canvas.bind('<Motion>', self.mouse_move)
        self.canvas.bind('<ButtonPress>', self.mouse_click)
        self.canvas.bind('<ButtonRelease>', self.mouse_release)
        #self.debug_draw_mouse_xyc() #########デバッグ用表示
        self.debug_change_color()
        self.after(30, self.main)

def start():
    root = tkinter.Tk()
    app = App(root)
    app.mainloop()

if __name__ == '__main__':
    start()
