import pygame
import sys
import random
import json
import time

# 定数
WIDTH = 1400
HEIGHT = 600
MAX_REACH = WIDTH * 0.8 # 最大到達点、およびグラフの描画限界
CHARA_SIZE = 60 # 自機のサイズはすべてこのサイズに固定 60
LAG = 80 # 壁の出る間隔
LAG_TAIL = -2 # 煙の出る間隔
GRAZE_MAG = 0.001 # 1フレームかすることで増えるポイントの倍率
DIFFICULTY_LIST = [
    [ 6, 10, (CHARA_SIZE * 2, CHARA_SIZE * 5)],#10,17,22,30
    [ 8, 17, (CHARA_SIZE * 2, CHARA_SIZE * 4)],
    [10, 23, (CHARA_SIZE * 2, CHARA_SIZE * 3)],
    [12, 30, (CHARA_SIZE * 1, CHARA_SIZE * 2)]
] # [朝,昼,夕,夜][0.move_xp, 1.passed, 2.sukima]
# それぞれの番号対応辞書
SELECT_DICT_CHARA= {0:['chara_00ufo','smog'], 1:['chara_01bird','stamp_big'], 2:['chara_02redman', 'bubble'], 
                    3:['chara_03carpet','scatter'], 4:['chara_04girl','footprints'], 5:['chara_05nu','footprints']} # chara_num:['名前','tailタイプ']
SELECT_DICT_WALL = {0:'wall_00building', 1:'wall_01giraffe', 2:'wall_02pipe', 3:'wall_03palm', 4:'wall_04eye', 5:'wall_05aaa'}
SELECT_DICT_BACK = {0:'back_00town', 1:'back_01mountain', 2:'back_02underwater', 3:'back_03desert', 4:'back_04people', 5:'back_05moji'}
MISS_TMR = 60 # ミスしたときに画面が止まるフレーム数
KOMA = 5 # アニメーション。何コマ撮りか
RENBAN = 3 # アニメーションは何枚のループか。
CHARA_X = WIDTH * 1 / 6 # 自機のx座標は固定
MISS_ANIM = 2 # ミス演出用のスローモーション
BACK_DELAY = 80 # 背景の切り替わりに要する時間
MUSIC= ['furerarenaiomoi.mp3', # しっとりした音楽
        'Scrambled_Egg.mp3', # 元気な音楽
        'nohohontori.mp3', # のほほんとした音楽
        'letsgo.mp3', # マリオっぽい音楽
        'taiyounojuutan.mp3', # アラビアっぽい音楽
        'kurayaminootomodati.mp3', # ホラーっぽい音楽
        'gyaaaaa.mp3', # せわしない音楽
        ]
SE_NAME =[
    '.\sound\se_pass_big.mp3',    # 通過したときのSE
    '.\sound\se_miss.mp3',    # ミスしたときのSE
    '.\sound\se_button.mp3',  # ボタンクリックのときのSE
    '.\sound\se_graze.mp3',# グレイズしたときのSE
]
PRICE_CHARA = 100 # 新自機械の値段
PRICE_WALL = 100 # 新壁の値段
PRICE_BACK = 1000 # 新背景の値段

# 色
COLOR_SCREEN = (20, 20, 20)
COLOR_SCREEN_SHOPPING = (50,50,50)
COLOR_WHITY = (200, 200, 150)
COLOR_BLACKY = (10,10,10)
COLOR_BAR = (180,180,0)
COLOR_BAR_NOW = (150,0,150)
COLOR_BAR_FRAME = (100,255,100) # グラフの外枠
COLOR_OUTLINE = (0,255,0) # マスクの境界線

class WallSet(pygame.sprite.Sprite):
    '''壁の色変えをセットする'''
    def __init__(self,wall_num, wall_color):
        super().__init__()
        model_file = SELECT_DICT_WALL[wall_num]
        self.image = pygame.image.load(f'./img/{model_file}.png').convert_alpha()
        self.rect = self.image.get_rect()
        # wall_colorに応じて壁の色変え
        self.color_changer_back = ColorChanger(wall_color)
        self.color_changer_back.change_color(self.image, *self.color_changer_back.color_set)

class CrashSet(pygame.sprite.Sprite):
    '''クラッシュの色変えをセットする'''
    def __init__(self, model_file_crush, chara_color):
        # chara_colorに応じてクラッシュ画像を色変え
        self.image = pygame.image.load(f'./img/{model_file_crush}_crash.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.color_changer_crash = ColorChanger(chara_color)
        self.color_changer_crash.change_color(self.image, *self.color_changer_crash.color_set)

class Wall(pygame.sprite.Sprite):
    '''壁クラス'''
    def __init__(self, wall_set, crash_set, miss_count, stage, pass_count):
        super().__init__()
        self.image_lower = wall_set.image
        self.image_upper = pygame.transform.flip(wall_set.image, False, True,)
        self.mask_lower = pygame.mask.from_surface(self.image_lower)
        self.mask_upper = pygame.mask.from_surface(self.image_upper)
        self.rect_lower = self.image_lower.get_rect()
        self.rect_upper = self.image_lower.get_rect()
        self.crash_image = crash_set.image
        # self.crash_rect = self.crash_image.get_rect()

        # 高さをランダム生成
        hi = random.randint(CHARA_SIZE * 3 , HEIGHT - CHARA_SIZE)
        if pass_count >= MAX_REACH:
            # グラフ横軸1120(=WITH*0.8)より上のグラフは表示限界で書けなくなるので1120番目の壁で絶対死ぬようにする。　
            hi = 0
        self.rect_lower.top = hi
        space = random.randint(*(DIFFICULTY_LIST[stage % len(DIFFICULTY_LIST)][2]))
        self.rect_upper.bottom = hi - space
        # 壁のx座標の初期値
        self.rect_lower.left = WIDTH
        self.rect_upper.left = WIDTH

        # 通り抜けたかのフラグ
        self.flag_pass = False

        if miss_count == -1:
            txt = 'BEST'
            self.flag_crash = True
        elif miss_count == 0:
            txt = ''
            self.flag_crash = False
        elif miss_count > 0:
            txt = 'x'+ str(miss_count)
            self.flag_crash = True
                
        font = pygame.font.Font(None, 50)
        self.text = font.render(txt,True, (200,0,0))
        
    def update(self, screen, stage):
        '''動き制御'''
        self.rect_lower.centerx -= DIFFICULTY_LIST[stage % len(DIFFICULTY_LIST)][0]
        self.rect_upper.centerx -= DIFFICULTY_LIST[stage % len(DIFFICULTY_LIST)][0]
        if self.rect_lower.right < 0 and self.rect_upper.right < 0:
            # 画面外に出たら消滅
            self.kill()
        screen.blit(self.image_lower, self.rect_lower)
        screen.blit(self.image_upper, self.rect_upper)

        if self.flag_crash:
            screen.blit(self.text, (self.rect_lower.centerx, HEIGHT*0.90))
            screen.blit(self.crash_image,(self.rect_lower.centerx - CHARA_SIZE*1.5, HEIGHT*0.85))
        screen.blit(self.text, (self.rect_lower.centerx, HEIGHT*0.90))
        if self.rect_lower.right < CHARA_X and self.flag_pass == False:
            # charaを超えたら加点フラグ
            self.flag_pass = True
            return True

    def update_miss(self, screen):
        '''壁ミス演出用の動き'''
        self.rect_lower.centerx -= MISS_ANIM
        self.rect_upper.centerx -= MISS_ANIM
        if self.rect_lower.right < 0 and self.rect_upper.right < 0:
            self.kill()
        screen.blit(self.image_lower, self.rect_lower)    
        screen.blit(self.image_upper, self.rect_upper)  
        if self.flag_crash:
            screen.blit(self.text, (self.rect_lower.centerx, HEIGHT*0.90))
            screen.blit(self.crash_image,(self.rect_lower.centerx - CHARA_SIZE*1.5, HEIGHT*0.85))    
        screen.blit(self.text, (self.rect_lower.centerx, HEIGHT*0.90))


class Chara(pygame.sprite.Sprite):
    '''自機クラス'''
    yp = 1
    Y_UP = 0.4
    Y_DOWN = 0.2
    def __init__(self, chara_num, chara_color):
        super().__init__()
        # numに応じて使う画像を切り替える
        model = SELECT_DICT_CHARA[chara_num][0]
        self.model_file = model
        self.model_file_crush = f'./img/{model}_crash.png'

        # 透過情報を持った連番のリストを作る
        self.image_list = []
        for i in range(RENBAN):
            self.image_list.append(pygame.image.load(f'./img/{model}_{str(i)}.png').convert_alpha())
        # 画像サイズの縦横長い方を既定の大きさに合わせて比率を変えずにリサイズする
        wi, hi = self.image_list[0].get_size()
        if wi > hi:
            scale = CHARA_SIZE / wi
        else:
            scale = CHARA_SIZE / hi
        self.scale = scale # その画像の拡大縮小率。crashの画像にも使用するのでselfにする
        new_wi, new_hi = int(scale * wi) , int(scale * hi)
        for i in range(len(self.image_list)):
            self.image_list[i] = pygame.transform.scale(self.image_list[i], (new_wi, new_hi))

        # chara_colorに応じて色を変える
        self.color_changer = ColorChanger(chara_color)
        for image in self.image_list:
            self.color_changer.change_color(image, *self.color_changer.color_set)


        # rectオブジェクトを作って座標を設定
        self.rect = self.image_list[0].get_rect()
        self.rect.center = CHARA_X, HEIGHT * 0.5

        # 衝突判定用のマスク生成 中心1ドットのみ
        self.mask = pygame.mask.from_surface(self.image_list[0])
        self.mask.clear() # 一度作ったmaskをリセットしてからset_atで範囲を指定
        self.mask.set_at((self.rect.width // 2, self.rect.height // 2), 1)

        # 得点表示用
        self.display_point_counter = 0
        self.display_point = 0


    def update(self, mouse_c01, screen, tmr):
        '''CHARAのy方向の挙動を決める'''
        self.rect.centery += self.yp
        if mouse_c01:
            # マウスボタンを押し続けることで上昇
            self.yp -= self.Y_UP
        else:
            self.yp += self.Y_DOWN

        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            # 画面の上端下端に到達したらそこで止まる
            self.yp = 0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

        # KOMAコマ撮り
        index = (tmr // KOMA) % RENBAN
        screen.blit(self.image_list[index], self.rect)

        # 得点表示の更新

        if self.display_point_counter > 0:
            font = pygame.font.Font(None, 50)
            get_point_txt = font.render(f'+${self.display_point}', True, COLOR_WHITY)
            rect_xy = pygame.Rect(self.rect.left, self.rect.centery - CHARA_SIZE, 100, 50)
            screen.blit(get_point_txt, rect_xy)
            self.display_point_counter -= 1


    def update_miss(self, screen, miss_tmr):
        '''ミス演出用CHARAの挙動を決める'''
        self.rect.centerx -= MISS_ANIM

        if miss_tmr >= int(MISS_TMR * 1 / 10):
            old_center = self.rect.center
            self.image = pygame.image.load(self.model_file_crush).convert_alpha()
            self.color_changer.change_color(self.image, *self.color_changer.color_set)
            new_wi, new_hi = int(self.scale * self.image.get_width()), int(self.scale * self.image.get_height())
            self.image = pygame.transform.scale(self.image, (new_wi, new_hi))
            
            self.rect = self.image.get_rect(center = old_center)
            screen.blit(self.image, self.rect)
        else:
            index = (miss_tmr // KOMA*10) % RENBAN
            screen.blit(self.image_list[index], self.rect)

class Tail(pygame.sprite.Sprite):
    '''自機の後ろに残る残像のクラス'''
    def __init__(self, chara_num, chara_rect):
        super().__init__()
        # 画像の読み込み
        model_file = SELECT_DICT_CHARA[chara_num][0]
        self.image = pygame.image.load(f'./img/{model_file}_tail.png').convert_alpha()
        # 挙動タイプを取得
        self.tail_type = SELECT_DICT_CHARA[chara_num][1]
        # rectを作る
        self.rect = self.image.get_rect()

        # 画像の発生座標
        if self.tail_type in ['smog']:
            self.rect.right = chara_rect.centerx
            self.rect.bottom = chara_rect.bottom
        if self.tail_type in ['stamp_big']:
            self.rect.right = chara_rect.left - CHARA_SIZE * 0.3
            self.rect.centery = chara_rect.centery
        if self.tail_type in ['bubble']:
            self.rect.centerx = chara_rect.centerx
            self.rect.centery = chara_rect.centery
        if self.tail_type in ['scatter']:
            if random.choice([True, False]):
                self.rect.right = chara_rect.centerx
            else:
                 self.rect.left = chara_rect.centerx
            self.rect.bottom = chara_rect.bottom
        if self.tail_type in ['footprints']:
            self.rect.center = chara_rect.midbottom[0] - CHARA_SIZE*0.5, chara_rect.midbottom[1]
            

        # 画像のリサイズ
        # インスタンスごとに大きさが違う
        wi, hi = self.image.get_size()
        if self.tail_type in ['smog']:
            # 自機より大きくなることもある
            x = random.uniform(0.5, 1.5)
        if self.tail_type in ['bubble']:
            # とても小さめ
            x = random.uniform(0.2, 0.6)
        if self.tail_type in ['scatter', 'footprints']:
            # 自機より小さめで固定
            x = 0.8
        if self.tail_type in ['stamp_big']:
            # 自機より大きめで固定
            x = random.uniform(0.2, 1.8)
        if wi > hi:
            scale = CHARA_SIZE * x / wi
        else:
            scale = CHARA_SIZE * x / hi
        self.scale = scale # その画像の拡大縮小率。crashの画像にも使用するのでselfにする
        new_wi, new_hi = int(scale * wi) , int(scale * hi)
        self.image = pygame.transform.scale(self.image, (new_wi, new_hi))
        
        # 画像の透明度
        if self.tail_type in ['smog']:
            # 100～200で半透明
            self.image.set_alpha(random.randint(100, 200))
        if self.tail_type in ['bubble', 'scatter']:
            # 1/3の確率で存在
            x = random.choice([0,0,1])
            self.image.set_alpha(150 * x)
        if self.tail_type in ['stamp_big', 'footprints']:
            # 常に存在
            self.image.set_alpha(255 * x)

        # 画像の回転
        if self.tail_type in ['scatter', 'stamp_big']:
            r = random.randint(0, 360)
            self.image = pygame.transform.rotate(self.image, r)


    def update(self, screen, stage):
        '''tailの挙動'''
        self.rect.centerx -= DIFFICULTY_LIST[stage % len(DIFFICULTY_LIST)][0]
        if self.tail_type in ['bubble']:
            self.rect.centery -= 2
        if self.tail_type in ['scatter']:
            self.rect.centery += 7
        if self.rect.right < 0:
            self.kill() 
        screen.blit(self.image, self.rect)
        
class ColorChanger:
    '''色変えメソッドだけを持つクラス'''
    # color_numを渡せば色変えセットをセッティングする
    # メソッドを呼び出せば色を変えてくれる　
    def __init__(self, color_num):
        if color_num == 0:
            # (   0,   0,   0) # 未所持
            self.color_set = (   0,   0,  -1)
        elif color_num == 1:
            # (   0,   0,   0) # 1カラー(デフォルト）
            self.color_set = (   0,   0,   0)
        elif color_num == 2:
            # (+50%,   0,   0) # 2カラー（色違いa）
            self.color_set = ( 90,   0,   0)
        elif color_num == 3:
            # (-50%,   0,   0) # 3カラー（色違いb）
            self.color_set = (180,   0,   0)
        elif color_num == 4:
            # (+50%,+50%,   0) # 4カラー（サイケデリック色違いa）
            self.color_set = ( 90,  0.5,  0)
        elif color_num == 5:
            # (-50%,+50%,   0) # 5カラー（サイケデリック色違いb）
            self.color_set = (180,  0.5,  0)
        elif color_num == 6:
            # (   0,+50%,-50%) # 6カラー（サイケデリックダーク）
            self.color_set = (   0, 0.5,-0.5)
        elif color_num == 7:
            # (   0,+50%,+50%) # 7カラー（サイケデリックブライト）
            self.color_set = (   0, 0.5, 0.5)


    def rgb_to_hsv(self, r, g, b):
        '''RGBから色彩(H)彩度(S)明度(V)に変換'''
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx, mn = max(r, g, b), min(r, g, b)
        df = mx - mn
        h, s, v = 0, 0, mx

        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360

        if mx != 0:
            s = df / mx

        return h, s, v

    def hsv_to_rgb(self, h, s, v):
        '''色彩(H)彩度(S)明度(V)からRGBに変換'''
        h = float(h)
        s = float(s)
        v = float(v)
        hi = int(h / 60.0) % 6
        f = (h / 60.0) - hi
        p = v * (1.0 - s)
        q = v * (1.0 - f * s)
        t = v * (1.0 - (1.0 - f) * s)

        if hi == 0:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q

        return int(r * 255), int(g * 255), int(b * 255)

    def change_color(self,surface, h_change, s_change, v_change):
        '''色変え'''
        # h(色相)は0～360 s(彩度)は0～1 v(明度)は0～1
        wi, hi = surface.get_size()
        for x in range(wi):
            for y in range(hi):
                r, b, g, a = surface.get_at((x, y))
                if a != 0: # 透明部分を除外して計算
                    h, s, v = self.rgb_to_hsv(r, g, b)
                    h = (h + h_change) % 360
                    s = max(0, min(1, s + s_change))
                    v = max(0, min(1, v + v_change))
                    r, b, g = self.hsv_to_rgb(h, s, v)
                    surface.set_at((x, y), (r, g, b, a))
        return surface


class App():
    '''ゲームクラス'''
    # 初期値
    index = 0
    mouse_x, mouse_y = 0, 0
    mouse_c01, mouse_c02, mouse_c03 = False, False, False
    tmr = 0
    point_total = 0 # 現在所有ポイント
    point_getted = 0 # 今回得たポイント
    graze_frame = 0 # 今回得たかすりフレーム
    wall_group = pygame.sprite.Group()
    tail_group = pygame.sprite.Group()
    stage = 0 # 現在ステージ
    stage_clear_count = 0 # 上限に達するとステージが上がってリセット
    pass_count = 0 # いくつ壁を通ったかのカウント
    collection_miss = {} # ミスした個所と回数の辞書　最高到達点・チャレンジ回数・これまで稼いだpointもわかる
    collection_looks = {'_point_total': 0, '_hiscore_higraze_hipass':[0,0,0],
                        'back_00town': 1, 'back_01mountain': 0, 'back_02underwater':0, 'back_03desert': 0, 'back_04people':0, 'back_05moji':0,
                        'chara_00ufo':1, 'chara_01bird':0, 'chara_02redman':0, 'chara_03carpet':0, 'chara_04girl':0, 'chara_05nu':0,
                        'wall_00building':1,'wall_01giraffe':0, 'wall_02pipe':0, 'wall_03palm':0, 'wall_04eye':0, 'wall_05aaa':0,
                        }
                    # 所持得点、当たり判定境界線フラグ、集めた外見。外見は0なら未取得、1以上で色違いの取得
    best_wall_flag = False # 最高点の壁を作ったか否か
    wall_count = 0 # 生成する壁の番号（1からスタート）
    flag_mask = False # 当たり判定を表示するか否か
    check_stage_temp = 0 # ステージが上がったかどうかのチェック用変数
    tmr_delay = 0 # ステージが上がった時の背景の切り替えに使うtmr
    scroll_x = 0 # スクロール初期位置
    click_delay = 0.3
    last_click_time = 0
    scrool_delay = 0.1
    last_scrool_time = 0
     

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init(channels=2, buffer=1024) # frequency=44100
        pygame.display.set_caption('ふらふらUFO')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 80)
        self.SE = [pygame.mixer.Sound(txt) for txt in SE_NAME]
        # 色チェンジ用のリスト
        self.color_changer_list = [ColorChanger(i) for i in range(8)]

    def create_tail(self, chara_num ,center):
        '''自機の後ろのものを生成'''
        self.tail = Tail(chara_num ,center)
        self.tail_group.add(self.tail)

    def create_wall(self, wall_set, crash_set):
        '''壁を生成'''
        if self.wall_count in self.collection_miss:
            if self.wall_count == max(self.collection_miss):
                miss_count = -1
            else:
                miss_count = self.collection_miss[self.wall_count]
        else:
            miss_count = 0
        self.wall = Wall(wall_set, crash_set, miss_count, self.stage, self.pass_count)
        self.wall_group.add(self.wall)
        self.wall_count += 1

    def draw_mask_outline(self, mask, offset, size, color = COLOR_OUTLINE):
        '''マスクの境界線を描く'''
        outline = mask.outline()
        # mask.outline()メソッドはマスクの境界をタプルをリストで返す
        for point in outline:
            # offsetの値が元のsurfaceの左上xy。
            # なのでoutlineの座標を足し算することで現在の座標が求まる
            # 線を描きたいのでwidthもheightも共に1
            pygame.draw.rect(self.screen,color,(point[0] + offset[0], point[1] + offset[1], size, size))

    def draw_mask_chara_and_wall(self):
        '''自機と壁の当たり判定を描画'''
        if self.flag_mask:
            # 自機の当たり判定描画
            offset = (self.chara.rect.left, self.chara.rect.top)
            outline_size_chara = 7
            self.draw_mask_outline(self.chara.mask, offset, outline_size_chara)
            
            #壁の当たり判定描画
            outline_size_wall = 2
            for wall in self.wall_group:
                offset_lower = (wall.rect_lower.left, wall.rect_lower.top)
                offset_upper = (wall.rect_upper.left, wall.rect_upper.top)
                self.draw_mask_outline(wall.mask_lower, offset_lower, outline_size_wall)
                self.draw_mask_outline(wall.mask_upper, offset_upper, outline_size_wall)

    def judgement_hit(self):
        '''当たり判定、キャラと壁が当たったらTrueを返す'''
        for wall in self.wall_group:
            # rect同士が衝突しているか確認
            if self.chara.rect.colliderect(wall.rect_lower) or self.chara.rect.colliderect(wall.rect_upper):
                # 差を計算 offsetはタプルで
                offset_lower = (wall.rect_lower.left - self.chara.rect.left, wall.rect_lower.top - self.chara.rect.top)
                offset_upper = (wall.rect_upper.left - self.chara.rect.left, wall.rect_upper.top - self.chara.rect.top)
                # かすり判定、graze数増加
                self.graze_frame += 1
                self.SE[3].set_volume(0.5)
                self.SE[3].play() # グレイズ音
                # self.channel2.play(self.SE[3])
                # マスク同士の衝突判定
                if self.chara.mask.overlap(wall.mask_lower, offset_lower):
                    return True
                if self.chara.mask.overlap(wall.mask_upper, offset_upper):
                    return True
        return False
    
    def init_respawn(self):
        '''ミスからの復帰用初期化'''
        self.wall_group.empty()
        self.tail_group.empty()
        self.stage = 0
        self.stage_clear_count = 0
        self.pass_count = 0
        self.wall_count = 0
        self.best_wall_flag = False
        self.tmr = 0
        self.check_stage_temp = 0 # ステージが上がったかどうかのチェック用変数
        self.tmr_delay = 0
        self.point_getted = 0
        self.graze_frame = 0
        self.flag_best_reach = False

    def sort_dict(self):
        '''二つの辞書をソートする（グラフを作るときに必須）'''
        self.collection_miss = {i:self.collection_miss[i] for i in sorted(self.collection_miss)} # dictの並び替えを一行で
        self.collection_looks = {i:self.collection_looks[i] for i in sorted(self.collection_looks)} # dictの並び替えを一行で

    def is_button_clicked(self, rect, event, offset_x=0, offset_y=0):
        '''ボタンがクリックされたらTrue'''
        current_time = time.time()
        if current_time - self.last_click_time < self.click_delay:
            return False
        if hasattr(event, 'pos'):
            x, y = event.pos
            if rect.collidepoint(x + offset_x, y - offset_y):
                # if event.type == pygame.MOUSEMOTION:
                #     pygame.draw.rect(self.screen, COLOR_OUTLINE, rect, 3)
                # 謎にずれるカーソル
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.SE[2].set_volume(0.5)
                    self.SE[2].play() # ボタン押し音
                    self.last_click_time = current_time
                    return True
        return False

    def cal_point(self,num):
        '''通過したときの獲得ポイントの計算'''
        current_value = 1
        count = 0

        while True:
            for item in DIFFICULTY_LIST:
                for _ in range(item[1]):
                    if count == num:
                        return current_value
                    count += 1
                current_value += 1

    def point_get(self):
        '''ポイント加算処理'''
        self.pass_count += 1
        self.point_getted += self.cal_point(self.pass_count)
        

    def point_cal_getted_graze(self):
        '''獲得ポイントとグレイズポイントを計算する'''
        return int(self.point_getted * (1 + (self.graze_frame * GRAZE_MAG)))

    def stage_cal(self):
        '''passした時点での現在のステージを計算する'''
        self.stage_clear_count += 1
        if self.stage_clear_count >= DIFFICULTY_LIST[self.stage % len(DIFFICULTY_LIST)][1]:
            self.stage += 1
            self.stage_clear_count = 0

    def display_get_point(self):
        '''得点したときに自機の頭上に表示する'''
        self.chara.display_point_counter = 30
        self.chara.display_point = self.cal_point(self.pass_count)

    def load_title_image(self):
        '''タイトルに使う画像を読み込む'''
        self.title_image_list = []
        self.title_ufo_list = []
        # タイトルロゴ
        for i in range(5):
            self.title_image_list.append(pygame.image.load(f'./img/title_{i}.png').convert_alpha())
        for i in range(3):
            self.title_ufo_list.append(pygame.image.load(f'./img/chara_00ufo_{i}.png').convert_alpha())
        # 各種ボタン画像
        self.image_turn = pygame.image.load('./img/button_image_turn.png').convert()
        self.image_start = pygame.image.load('./img/button_image_start.png').convert()
        self.image_record = pygame.image.load('./img/button_image_record.png').convert()
        self.image_explain = pygame.image.load('./img/button_image_explain.png').convert()
        self.image_shopping = pygame.image.load('./img/button_image_shopping.png').convert()
        self.image_rect_turn = self.image_turn.get_rect()
        self.image_rect_start = self.image_start.get_rect()
        self.image_rect_record = self.image_record.get_rect()
        self.image_rect_explain = self.image_explain.get_rect()
        self.image_rect_shopping = self.image_shopping.get_rect()

    def draw_title(self):
        '''タイトルを描画する'''
        # ロゴ
        rogo_rect = pygame.Rect(WIDTH * 0.5, HEIGHT * 0.3, 600, 350)
        rogo_rect.center = WIDTH * 0.5, HEIGHT * 0.3
        self.screen.blit(self.title_image_list[(self.tmr // 10) % len(self.title_image_list)], rogo_rect)
        # UFO
        ufo_rect = pygame.Rect(WIDTH * 0.5, HEIGHT * 0.7, 60, 60)
        ufo_rect.center = WIDTH * 0.5, HEIGHT * 0.65
        self.screen.blit(self.title_ufo_list[(self.tmr // 5) % len(self.title_ufo_list)], ufo_rect)

        # 始めるボタン
        self.image_rect_start.center = WIDTH * 3 / 10, HEIGHT * 7 / 10
        self.screen.blit(self.image_start ,self.image_rect_start)
        # 説明ボタン
        self.image_rect_explain.center = WIDTH * 3 / 10, HEIGHT * 9 / 10
        self.screen.blit(self.image_explain, self.image_rect_explain)
        # 記録ボタン
        if self.collection_miss:
            self.image_rect_record.center = WIDTH * 7 / 10, HEIGHT * 7 / 10
            self.screen.blit(self.image_record, self.image_rect_record)
        # お買い物ボタン
        self.image_rect_shopping.center = WIDTH * 7 / 10, HEIGHT * 9 / 10
        self.screen.blit(self.image_shopping, self.image_rect_shopping)


    def draw_record(self, bar_hi_one, wi):
        '''記録画面を描画'''
        GRAPH_BOTTOM = HEIGHT*0.75
        GRAPH_TOP = HEIGHT*0.25
        GRAPH_RIGHT = WIDTH*0.9
        GRAPH_LEFT = WIDTH*0.1
        topleft = [GRAPH_LEFT, GRAPH_TOP]
        bottomleft = [GRAPH_LEFT, GRAPH_BOTTOM]
        bottomright = [GRAPH_RIGHT, GRAPH_BOTTOM]
        topright = [GRAPH_RIGHT, GRAPH_TOP]

        # 一周セット範囲の描写 self.pass_count_set
        for i in range((max(self.collection_miss) // self.pass_count_set)+1):
            if i % 2==0:
                model_color = (20,0,20)
            else:
                model_color = (0,20,20)
            set_x = GRAPH_LEFT + self.pass_count_set * wi * i
            set_y =int(GRAPH_TOP)
            set_hi = max(self.collection_miss.values()) * bar_hi_one

            if wi * self.pass_count_set + set_x <= GRAPH_RIGHT:
                set_wi = int(wi * self.pass_count_set)
            else:
                set_wi = wi * self.pass_count_set - ((wi * self.pass_count_set + set_x) - GRAPH_RIGHT) +1
            set_rect = (set_x, set_y, set_wi, set_hi) 
            pygame.draw.rect(self.screen , model_color, set_rect)

        # 棒グラフの範囲
        pygame.draw.lines(self.screen, COLOR_BAR_FRAME,False,[[GRAPH_LEFT-1, GRAPH_TOP],
                                                        [GRAPH_LEFT-1, GRAPH_BOTTOM],
                                                        [GRAPH_RIGHT+1, GRAPH_BOTTOM],
                                                        [GRAPH_RIGHT+1, GRAPH_TOP]]) # 左右1ピクセル外側を描画
        
        # 棒グラフの数値
        # 原点0
        font = pygame.font.Font(None, 30)
        text_graph_0 = font.render('0', True, COLOR_WHITY)
        text_graph_0_rect = pygame.Rect(0,0,20,10)
        text_graph_0_rect.topright = bottomleft
        self.screen.blit(text_graph_0, text_graph_0_rect)
        # 縦軸max
        font = pygame.font.Font(None, 30)
        text_graph_0 = font.render(f'{max(self.collection_miss.values())}', True, COLOR_WHITY)
        text_graph_0_rect = pygame.Rect(0,0,20,50)
        text_graph_0_rect.midright = topleft
        self.screen.blit(text_graph_0, text_graph_0_rect)
        # 横軸max
        font = pygame.font.Font(None, 30)
        text_graph_0 = font.render(f'{max(self.collection_miss)}', True, COLOR_WHITY)
        text_graph_0_rect = pygame.Rect(0,0,50,20)
        text_graph_0_rect.topleft = bottomright
        self.screen.blit(text_graph_0, text_graph_0_rect)
        # 文字画像を入れる
        # ←ミス回数→
        text0_rect = self.text_image_list[0].get_rect()
        text0_rect.midright = topleft[0],bottomleft[1] - topleft[1]
        self.screen.blit(self.text_image_list[0], text0_rect)
        # ←到達深度→
        text1_rect = self.text_image_list[1].get_rect()
        text1_rect.midtop = WIDTH*0.5,bottomleft[1]
        self.screen.blit(self.text_image_list[1], text1_rect)
        # 挑戦回数　画像
        text2_rect = self.text_image_list[2].get_rect()
        text2_rect.midright = WIDTH * 0.50, HEIGHT * 0.05
        self.screen.blit(self.text_image_list[2], text2_rect)
        # 挑戦回数　数値
        font2 = pygame.font.Font(None, 50) 
        record_text = font2.render(f'{self.challenge_num}',True, COLOR_WHITY)
        record_rect = record_text.get_rect()
        record_rect.midleft = WIDTH * 0.50 + 5, HEIGHT * 0.05
        self.screen.blit(record_text, record_rect) 
        # 最高得点
        text3_rect = self.text_image_list[3].get_rect()
        text3_rect.midright = WIDTH * 0.50, HEIGHT * 0.15
        self.screen.blit(self.text_image_list[3], text3_rect)
        # 最高得点　数値
        font3 = pygame.font.Font(None, 50) 
        record_text = font3.render(f'${self.collection_looks['_hiscore_higraze_hipass'][0]}(x{self.collection_looks['_hiscore_higraze_hipass'][1]})',
                                True, COLOR_WHITY)
        record_rect = record_text.get_rect()
        record_rect.midleft = WIDTH * 0.50 + 5, HEIGHT * 0.15
        self.screen.blit(record_text, record_rect) 

        # 棒グラフ描写
        
        for key, val in self.collection_miss.items():
            model_color = COLOR_BAR
            if key == self.pass_count: #  and self.pass_count !=0
                model_color = COLOR_BAR_NOW
            rect = pygame.Rect(topleft[0] + key * wi+1, val * bar_hi_one, wi, val * bar_hi_one)
            rect.bottom = GRAPH_BOTTOM
            pygame.draw.rect(self.screen, model_color, rect)
            

        # 戻るボタン
        self.image_rect_turn.center = WIDTH * 5 / 10, HEIGHT * 9 / 10
        self.screen.blit(self.image_turn, self.image_rect_turn)

    def create_back_image(self, back_num):
        '''背景画像を読み込む'''
        self.image_back_list = []
        model =SELECT_DICT_BACK[back_num]

        for i in range(len(DIFFICULTY_LIST)):
            surface = pygame.image.load(f'./img/{model}_{i}.png').convert()
            rect = surface.get_rect()
            self.image_back_list.append((surface, rect))
        
            
    def check_stage_index(self):
        '''ステージが一段階上がったらTrue'''
        index = self.stage % len(DIFFICULTY_LIST)
        if self.check_stage_temp == index:
            pass
        else:
            self.check_stage_temp = index
            return True

    def draw_back(self):
        '''背景を描写'''
        index = self.stage % len(DIFFICULTY_LIST)
        image_back_wi = self.image_back_list[0][1].width
        if self.check_stage_index():
            self.tmr_delay = BACK_DELAY
        # 背景の種類が変わるタイミングで前後の画像をディレイさせる
        for i in range((WIDTH // image_back_wi) + 2): # 11
            self.image_back_list[index][0].set_alpha(255)
            self.screen.blit(self.image_back_list[index][0], 
                             (image_back_wi * i - (self.tmr % image_back_wi), 0))
        
        if self.tmr_delay > 0:
            # ひとつ前の画像がだんだん透明になっていく
            suf = self.image_back_list[index-1 if index - 1 != -1 else len(DIFFICULTY_LIST) - 1][0]
            x = (self.tmr_delay / BACK_DELAY )
            suf.set_alpha(int(x * 255))
            
            for i in range(11):
                self.screen.blit(suf, (image_back_wi * i - (self.tmr % image_back_wi), 0))
            self.tmr_delay -= 1

        
    def display_text(self, text, x, y, size = 50, color = COLOR_WHITY, text_font = None):
        '''文字を表示'''
        font = pygame.font.Font(text_font, size)
        lines = text.split('\n')
        lines_hi = font.get_linesize()

        for line in lines:
            model_text = font.render(line, True, color)
            rect = model_text.get_rect()
            rect.center = x, y
            self.screen.blit(model_text, rect)
            y += lines_hi

    def save_date_read(self):
        '''セーブデータを読み込む。なかったら作る'''
        # ミス辞書
        try:
            with open('save_data_UFO_miss.json', 'r') as file:
                x = json.load(file)
                self.collection_miss = {}
                self.collection_miss = {int(key):val for key, val in x.items()}
        except:
            with open('save_data_UFO_miss.json', 'w') as file:
                self.collection_miss = {}
                json.dump(self.collection_miss, file)
        
        # 所持得点、境界線フラグ、含むルックス辞書
        try:
            with open('save_data_UFO_looks.json', 'r') as file:
            # 新しいテンプレートを受け入れつつデータを保持する
                x = json.load(file)
                for key, val in self.collection_looks.items():
                    if key not in x:
                        x[key] = val
                self.collection_looks = x

        except:
            with open('save_data_UFO_looks.json', 'w') as file:
                json.dump(self.collection_looks, file)
        # セーブデータの所持ポイントをゲーム内の所持ポイントに反映させる
        self.point_total = self.collection_looks['_point_total']

    def save_data_write(self):
        '''セーブデータをjsonに書き込む'''
        with open('save_data_UFO_miss.json', 'w') as file:
            json.dump(self.collection_miss, file)

        with open('save_data_UFO_looks.json', 'w') as file:
            json.dump(self.collection_looks, file)

    def sensing_click(self):
        '''マウスクリックを感知'''
        self.mouse_c01 = pygame.mouse.get_pressed()[0]

    def play_music(self, miss = False):
        '''numに応じた音楽を再生する'''
        if miss == False:
            if  self.chara_num ==1 and self.wall_num ==1 and self.back_num==1:
                num = 2 # のほほんとした音楽
            elif  self.chara_num ==2 and self.wall_num ==2 and self.back_num==2:
                num = 3 # マリオっぽい音楽
            elif self.chara_num ==3 and self.wall_num ==3 and self.back_num==3:
                num = 4 # アラビアっぽい音楽
            elif self.chara_num ==4 and self.wall_num ==4 and self.back_num==4:
                num = 5 # ホラーっぽい音楽
            elif self.chara_num ==5 and self.wall_num ==5 and self.back_num==5:
                num = 6 # せわしない音楽
            else:
                num = 1 # 元気な音楽
        else:
            num = 0 # しっとりした音楽
        txt = f'.\sound\{MUSIC[num]}'
        pygame.mixer.music.load(txt) # 音楽を読み込み
        pygame.mixer.music.set_volume(1)  # 音量を設定
        pygame.mixer.music.play(-1)  # 音楽を再生

    def display_info_text(self):
        '''ゲーム中の情報表示'''
        font = pygame.font.Font(None, 50)
        debug_text = font.render(f'${self.point_getted} x ({round(1+(GRAZE_MAG * self.graze_frame),3)})',
                                True, COLOR_WHITY)#  yp={int(self.chara.yp)}
        rect = pygame.Rect(0, 0, 100, 50)
        rect.topleft = CHARA_X, HEIGHT * 0.01
        self.screen.blit(debug_text, rect)

    def prepare_shopping_surface(self):
        '''お買い物画面の画像準備 画像変換もあるため重い、ゲーム起動時にやっておく'''
        self.sort_dict()
        # 画像を一枚ずつ用意する
        self.chara_list = []
        self.wall_list = []
        self.back_list = []
        self.chara_list_shadow = []
        self.wall_list_shadow = []
        self.back_list_shadow = []
        self.chara_list_rect = []
        self.wall_list_rect = []
        self.back_list_rect = []
        temp_num_chara = 0
        temp_num_wall = 0
        # 画像を読み込む
        for key in self.collection_looks.keys():
            if 'chara_' in key:
                self.chara_list.append([pygame.image.load(f'./img/{key}_0.png').convert_alpha() for _ in range(len(self.color_changer_list))])
                for i in range(len(self.color_changer_list)-1, -1, -1):
                    self.color_changer_list[i].change_color(self.chara_list[temp_num_chara][i], *self.color_changer_list[i].color_set)
                temp_num_chara += 1
            if 'wall_' in key:
                self.wall_list.append([pygame.image.load(f'./img/{key}.png').convert_alpha() for _ in range(len(self.color_changer_list))])
                for i in range(len(self.color_changer_list)-1, -1, -1):
                    self.color_changer_list[i].change_color(self.wall_list[temp_num_wall][i], *self.color_changer_list[i].color_set)
                temp_num_wall += 1
            if 'back_' in key:
                self.back_list.append(pygame.image.load(f'./img/{key}_0.png').convert())

        # 壁を小さくする
        for i in range(len(self.wall_list)):
            for j in range(len(self.wall_list[i])):
                self.wall_list[i][j] = pygame.transform.scale(self.wall_list[i][j], (CHARA_SIZE,CHARA_SIZE))
        
        # 背景を小さくする
        for i in range(len(self.back_list)):
            self.back_list[i] = pygame.transform.scale(self.back_list[i], (CHARA_SIZE,CHARA_SIZE))
        
        # rectを作る、塗りつぶしfill（surfaceになる）も作る
        for i in range(len(self.chara_list)):
            temp_list = []
            temp_list_fill = []
            for j in range(len(self.chara_list[i])):
                silhouette_surface = self.chara_list[i][j].copy()
                silhouette_surface.fill([0,0,0], special_flags=pygame.BLEND_RGBA_MIN)
                temp_list.append(self.chara_list[i][j].get_rect())
                temp_list_fill.append(silhouette_surface)
            self.chara_list_rect.append(temp_list)
            self.chara_list_shadow.append(temp_list_fill)
        for i in range(len(self.wall_list)):
            temp_list = []
            temp_list_fill = []
            for j in range(len(self.wall_list[i])):
                silhouette_surface = self.wall_list[i][j].copy()
                silhouette_surface.fill([0,0,0], special_flags=pygame.BLEND_RGBA_MIN)
                temp_list.append(self.wall_list[i][j].get_rect())
                temp_list_fill.append(silhouette_surface)
            self.wall_list_rect.append(temp_list)
            self.wall_list_shadow.append(temp_list_fill)
        for i in self.back_list:
            silhouette_surface = i.copy()
            silhouette_surface.fill([0,0,0])
            self.back_list_rect.append(i.get_rect())
            self.back_list_shadow.append(silhouette_surface)
        # 隙間定数
        self.SUKIMA_HI_SHOPPING = 10 #45

        # charaのrectを設定する
        for i in range(len(self.chara_list)): # charaの種類
            for j in range(1, len(self.chara_list[i])): # 色変えの種類
                i_x = i * CHARA_SIZE * 4 + CHARA_SIZE
                if j == 1:
                    model_x = i_x + CHARA_SIZE
                    model_y = self.SUKIMA_HI_SHOPPING 
                elif j == 2:
                    model_x = i_x + 0
                    model_y = self.SUKIMA_HI_SHOPPING + CHARA_SIZE
                elif j == 3:
                    model_x = i_x + CHARA_SIZE
                    model_y = self.SUKIMA_HI_SHOPPING + CHARA_SIZE
                elif j == 4:
                    model_x = i_x + CHARA_SIZE * 2
                    model_y = self.SUKIMA_HI_SHOPPING + CHARA_SIZE
                elif j == 5:
                    model_x = i_x + 0
                    model_y = self.SUKIMA_HI_SHOPPING + CHARA_SIZE * 2
                elif j == 6:
                    model_x = i_x + CHARA_SIZE
                    model_y = self.SUKIMA_HI_SHOPPING + CHARA_SIZE * 2
                elif j == 7:
                    model_x = i_x + CHARA_SIZE * 2
                    model_y = self.SUKIMA_HI_SHOPPING + CHARA_SIZE * 2
                self.chara_list_rect[i][j].topleft = model_x, self.SUKIMA_HI_SHOPPING + model_y 
        # wallのrectを設定する
        for i in range(len(self.wall_list)): # wallの種類
            for j in range(1, len(self.wall_list[i])): # 色変えの種類
                i_x = i * CHARA_SIZE * 4 + CHARA_SIZE
                wall_y = CHARA_SIZE * 3 + self.SUKIMA_HI_SHOPPING
                if j == 1:
                    model_x = i_x + CHARA_SIZE
                    model_y = self.SUKIMA_HI_SHOPPING 
                elif j == 2:
                    model_x = i_x + 0
                    model_y = self.SUKIMA_HI_SHOPPING + CHARA_SIZE
                elif j == 3:
                    model_x = i_x + CHARA_SIZE
                    model_y = self.SUKIMA_HI_SHOPPING + CHARA_SIZE
                elif j == 4:
                    model_x = i_x + CHARA_SIZE * 2
                    model_y = self.SUKIMA_HI_SHOPPING + CHARA_SIZE
                elif j == 5:
                    model_x = i_x + 0
                    model_y = self.SUKIMA_HI_SHOPPING + CHARA_SIZE * 2
                elif j == 6:
                    model_x = i_x + CHARA_SIZE
                    model_y = self.SUKIMA_HI_SHOPPING + CHARA_SIZE * 2
                elif j == 7:
                    model_x = i_x + CHARA_SIZE * 2
                    model_y = self.SUKIMA_HI_SHOPPING + CHARA_SIZE * 2
                self.wall_list_rect[i][j].topleft = model_x, wall_y + model_y 
        # backのrectを設定する
        for i in range(len(self.back_list)):
            i_x = i * CHARA_SIZE * 4 + CHARA_SIZE * 2
            back_y = CHARA_SIZE * 7 + self.SUKIMA_HI_SHOPPING
            self.back_list_rect[i].topleft = i_x, back_y
        
        # ボタン画像を読み込む
        self.button_surface_shopping = [pygame.image.load(f'./img/button_new_{i}.png').convert_alpha() for i in range(3)]
        # rectを取得して位置を指定
        self.button_rect_shopping = [i.get_rect() for i in self.button_surface_shopping]
        for i in range(len(self.button_rect_shopping)):
            self.button_rect_shopping[i].midbottom = WIDTH * (i + 2) / 6, HEIGHT

        # カーソル画像を読み込む
        self.cursor_surface = pygame.image.load('./img/cursor.png').convert_alpha()
        self.cursor_rect_chara = self.cursor_surface.get_rect()
        self.cursor_rect_wall = self.cursor_surface.get_rect()
        self.cursor_rect_back = self.cursor_surface.get_rect()


    def draw_shopping_surface(self, event):
        '''お買い物画面のsurfaceを描画する。スクロール前提'''
        # キャラ・壁・背景が乗るmain surface
        self.frame_shopping_main_WI = CHARA_SIZE * 4 * len(SELECT_DICT_CHARA) + CHARA_SIZE
        self.frame_shopping_main_surface = pygame.Surface((self.frame_shopping_main_WI, HEIGHT * 5 / 6))
        self.frame_shopping_main_surface.fill(COLOR_SCREEN_SHOPPING) 
        self.frame_shopping_main_rect = self.frame_shopping_main_surface.get_rect()
        self.frame_shopping_main_rect.topleft = 0, 0

        # スクロールで見える範囲のsurface
        self.frame_scroll_rect = pygame.Rect(*self.frame_shopping_main_rect.topleft, WIDTH, HEIGHT * 5 / 6)
        self.frame_scroll_surface = pygame.Surface(self.frame_scroll_rect.size)

        # charaをmainにblit
        for i in range(len(self.chara_list)):
            model_txt = SELECT_DICT_CHARA[i][0]
            val = self.collection_looks[model_txt]
            for j in range(1, len(self.chara_list[i])):
                    if j <= val:
                        self.frame_shopping_main_surface.blit(self.chara_list[i][j], self.chara_list_rect[i][j])
                    else:
                        self.frame_shopping_main_surface.blit(self.chara_list_shadow[i][j], self.chara_list_rect[i][j])          
                
        # wallをmainにblit
        for i in range(len(self.wall_list)):
            model_txt = SELECT_DICT_WALL[i]
            val = self.collection_looks[model_txt]
            for j in range(1, len(self.wall_list[i])):
                if j <= val:
                    self.frame_shopping_main_surface.blit(self.wall_list[i][j], self.wall_list_rect[i][j])
                else:
                    self.frame_shopping_main_surface.blit(self.wall_list_shadow[i][j], self.wall_list_rect[i][j])  

        # backをmainにblit
        for i in range(len(self.back_list)):
            model_txt = SELECT_DICT_BACK[i]
            val = self.collection_looks[model_txt]
            if val == 0:
                self.frame_shopping_main_surface.blit(self.back_list_shadow[i], self.back_list_rect[i])
            elif val == 1:
                self.frame_shopping_main_surface.blit(self.back_list[i], self.back_list_rect[i])

        # 選択中の物にカーソルをmainにblit
        self.cursor_rect_chara = self.chara_list_rect[self.chara_num][self.chara_color].topleft
        self.cursor_rect_wall = self.wall_list_rect[self.wall_num][self.wall_color].topleft
        self.cursor_rect_back = self.back_list_rect[self.back_num].topleft
        self.frame_shopping_main_surface.blit(self.cursor_surface, self.cursor_rect_chara)
        self.frame_shopping_main_surface.blit(self.cursor_surface, self.cursor_rect_wall)
        self.frame_shopping_main_surface.blit(self.cursor_surface, self.cursor_rect_back)

        # 画面のスクロール
        if event.type == pygame.MOUSEWHEEL:
            current_time = time.time()
            if current_time - self.last_click_time > self.scrool_delay:
                self.scroll_x -= event.y * CHARA_SIZE  # 横方向のスクロール速度調整
                self.scroll_x = max(0, min(self.scroll_x, self.frame_shopping_main_WI - self.frame_scroll_rect.width))  # スクロール範囲を制限
                self.last_click_time = current_time

        # 所持金をscreenにblit
        font = pygame.font.Font(None, 50)
        total_point = font.render(f'${self.point_total}', True, COLOR_WHITY)
        text_wi, text_hi = total_point.get_size()
        font_rect = pygame.Rect(0, 0, text_wi, text_hi)
        font_rect.bottom = HEIGHT
        font_rect.left = CHARA_SIZE
        self.screen.blit(total_point, font_rect)

        # お買い物ボタンをscreenにblit
        for i in range(3):
            self.screen.blit(self.button_surface_shopping[i], self.button_rect_shopping[i])
            
        # 自機の金額をscreenにblit
        font = pygame.font.Font(None, 40)
        chara_price = font.render(f'${self.price_chara()}', True, COLOR_BLACKY)
        chara_price_rect = chara_price.get_rect()
        chara_price_rect.centerx = self.button_rect_shopping[0].centerx
        chara_price_rect.centery = self.button_rect_shopping[0].centery + chara_price_rect.height*0.5
        self.screen.blit(chara_price, chara_price_rect)
        
        # 壁の金額をscreenにblit
        font = pygame.font.Font(None, 40)
        wall_price = font.render(f'${self.price_wall()}', True, COLOR_BLACKY)
        wall_price_rect = wall_price.get_rect()
        wall_price_rect.centerx = self.button_rect_shopping[1].centerx
        wall_price_rect.centery = self.button_rect_shopping[1].centery + wall_price_rect.height*0.5
        self.screen.blit(wall_price, wall_price_rect)
        # 背景の金額をscreenにblit
        font = pygame.font.Font(None, 40)
        back_price = font.render(f'${self.price_back()}', True, COLOR_BLACKY)
        back_price_rect = back_price.get_rect()
        back_price_rect.centerx = self.button_rect_shopping[2].centerx
        back_price_rect.centery = self.button_rect_shopping[2].centery + back_price_rect.height*0.5
        self.screen.blit(back_price, back_price_rect)
        
        # 戻るボタンをscreenにblit
        self.image_rect_turn.bottom = HEIGHT
        self.image_rect_turn.centerx = WIDTH * 5 / 6
        self.screen.blit(self.image_turn, self.image_rect_turn)

        # mainをscrollにblit
        self.frame_scroll_surface.blit(self.frame_shopping_main_surface, (-self.scroll_x, 0))
        # scrollをscreenにblit
        self.screen.blit(self.frame_scroll_surface, self.frame_scroll_rect)


    def price_chara(self):
        '''次の新スキンの価格を決める'''
        val_list = []
        model = 0
        for i in range(len(SELECT_DICT_CHARA)):
            val_list.append(self.collection_looks[SELECT_DICT_CHARA[i][0]])
        for i in range(len(val_list)):
            if val_list[i] == 0:
                model =val_list[i-1]
                break
        if model < 7:
            # まだカンストしていないcharaがここで確定
            return PRICE_CHARA
        elif model ==7:
            return PRICE_CHARA * 10
        
    def price_wall(self):
        '''次の新壁の価格を決める'''
        val_list = []
        model = 0
        for i in range(len(SELECT_DICT_WALL)):
            val_list.append(self.collection_looks[SELECT_DICT_WALL[i]])
        for i in range(len(val_list)):
            if val_list[i] == 0:
                model =val_list[i-1]
                break
        if model < 7:
            # まだカンストしていないwallがここで確定
            return PRICE_WALL
        elif model ==7:
            return PRICE_WALL * 10
            
    def price_back(self):
        '''次の新背景の価格を決める'''
        return PRICE_BACK


    def generate_debug_text(self):
        '''デバッグ用表示'''
        if 20 <= self.index:
            font = pygame.font.Font(None, 50)
            debug_text = font.render(f'point_getted ={self.point_getted} pass={self.pass_count} graze={self.graze_frame} {self.stage_clear_count}/{DIFFICULTY_LIST[self.stage % len(DIFFICULTY_LIST)][1]}',
                                    True, COLOR_WHITY)#  yp={int(self.chara.yp)}
            rect = pygame.Rect(WIDTH * 0.01, HEIGHT * 0.85, 100, 50)
            self.screen.blit(debug_text, rect.center)

    def main(self):
        '''ゲーム本体'''
        running = True
        while running:
            self.tmr += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    running = False
            self.screen.fill(COLOR_SCREEN)
            if self.index == 0:
                # タイトル画面の準備
                self.save_date_read()
                self.load_title_image()
                # 自機・壁・背景の初期値
                self.chara_num = 0 # 自機をセット　
                self.chara_color = 1 # 自機の色をセット
                self.wall_num = 0 # 壁をセット
                self.wall_color = 1 # 壁の色をセット
                self.back_num = 0 # 背景をセット

                # 1周分のpass数を算出(現状80)
                self.pass_count_set = 0
                for i in range(len(DIFFICULTY_LIST)):
                    self.pass_count_set += DIFFICULTY_LIST[i][1]
                self.prepare_shopping_surface() # お買い物画面用の画像読み込み+画像変換
                self.play_music(miss = True) # 音楽再生 しっとりBGM
                self.index = 1

            elif self.index == 1:
                # タイトル画面。
                self.draw_title()
                if self.is_button_clicked(self.image_rect_start, event):
                    # 「始める」ボタン
                    self.index = 10
                if self.is_button_clicked(self.image_rect_explain, event):
                    # 「説明」ボタン
                    self.index = 50
                if self.collection_miss:
                    if self.is_button_clicked(self.image_rect_record, event):
                        # 「記録」ボタン
                        self.index = 2
                if self.is_button_clicked(self.image_rect_shopping, event):
                    # 「お買い物」ボタン
                    self.index = 40
            
            elif self.index == 2:
                # 「記録」画面準備
                # 挑戦回数を算出
                self.challenge_num = 0
                for val in self.collection_miss.values():
                    self.challenge_num += val
                # 最高到達点を算出
                self.max_reach = max(self.collection_miss)
                # 最も多いミス数を算出
                bar_hi_max = 0
                for val in self.collection_miss.values():
                    if bar_hi_max < val:
                        bar_hi_max = val
                # ミス一回分の棒の高さ
                bar_hi_one = HEIGHT * 0.50 / bar_hi_max
                # 一つの棒にかかる横幅
                if max(self.collection_miss) != 0:
                    wi = MAX_REACH / (max(self.collection_miss)+1)
                    if wi <= 1:
                        wi = 1
                else:
                    wi = MAX_REACH
                # グラフの文字画像読み込み
                self.text_image_list =[pygame.image.load(f'./img/txt_image_graph0{i}.png').convert_alpha() for i in range(4)]

                self.index = 3
            elif self.index ==3:
                # 「記録」画面描写
                self.draw_record(bar_hi_one, wi)
                if self.is_button_clicked(self.image_rect_turn, event): 
                    self.index = 1 

            elif self.index == 10:
                # ゲームの始まり、ゲームの初期化
                self.init_respawn()
                model_file_crush = SELECT_DICT_CHARA[self.chara_num][0]
                self.wall_set = WallSet(self.wall_num, self.wall_color)
                self.crash_set = CrashSet(model_file_crush,self.chara_color)
                # 「更新中」画像読み込み
                self.best_reach_image_list = [pygame.image.load(f'./img/text_best_reach{i}.png').convert_alpha() for i in range(4)]
                self.best_reach_image_list_rect = [self.best_reach_image_list[i].get_rect() for i in range(4)]
                for i in self.best_reach_image_list_rect:
                    i.midbottom = WIDTH * 0.5, HEIGHT
                # 「更新中」壊れ画像読み込み
                self.best_reach_crash_image_list = [pygame.image.load(f'./img/text_best_reach_crash{i}.png').convert_alpha() for i in range(10)]
                self.best_reach_crash_image_list_rect = [self.best_reach_image_list[i].get_rect() for i in range(4)]
                for i in self.best_reach_crash_image_list_rect:
                    i.midbottom = WIDTH * 0.5, HEIGHT
                self.index = 11
            
            elif self.index == 11:
                # 自機が生成される
                self.chara = Chara(self.chara_num, self.chara_color)
                self.create_back_image(self.back_num)
                self.play_music() # 音楽再生 ゲームメインBGM
                self.index = 20
                
            elif self.index == 20:
                # フラッピーバードメイン
                self.draw_back()
                if self.tmr % LAG ==0:
                    # LAG秒後に壁を生成
                    self.create_wall(self.wall_set, self.crash_set)
                for wall in self.wall_group:
                    if wall.update(self.screen, self.stage):
                        # 壁を通り抜けた時の処理
                        self.point_get()
                        self.stage_cal()
                        self.display_get_point()
                        self.SE[0].set_volume(5.0)
                        self.SE[0].play() # pass音
                        # self.channel1.play(self.SE[0])

                self.chara.update(self.mouse_c01, self.screen, self.tmr)
                for tail in self.tail_group:
                    # tailの描画
                    tail.update(self.screen, self.stage)

                if self.tmr % (LAG_TAIL + DIFFICULTY_LIST[self.stage % len(DIFFICULTY_LIST)][0]) == 0:
                    # xy = self.chara.rect.centerx, self.chara.rect.centery
                    self.create_tail(self.chara_num, self.chara.rect)

                # フラグ立ってるなら当たり判定描写
                self.draw_mask_chara_and_wall() 
                # 情報表示
                self.display_info_text()
                # 最高記録更新中表示
                if self.pass_count > self.collection_looks['_hiscore_higraze_hipass'][2] and self.stage >= len(DIFFICULTY_LIST):
                    # 記録更新中且つ一周以上しているときだけ「更新中」表示
                    self.screen.blit(self.best_reach_image_list[(self.tmr//4) % 4], self.best_reach_image_list_rect[(self.tmr//4) % 4])
                    self.flag_best_reach = True

                # クリック感知
                self.sensing_click()
                if self.judgement_hit():
                    # ミスしたとき
                    pygame.mixer.music.stop()
                    # ミス箇所を記述
                    if self.pass_count  in self.collection_miss:
                        
                        self.collection_miss[self.pass_count ] += 1
                    else:
                        self.collection_miss[self.pass_count] = 1
                    miss_tmr = 0
                    self.index = 21
                
            elif self.index == 21:
                # ミス演出用スローモーション
                self.SE[1].set_volume(5.0)
                self.SE[1].play() # 衝突音
                #self.channel1.play(self.SE[1])
                
                self.draw_back()

                for wall in self.wall_group:
                    wall.update_miss(self.screen) 
                for tail in self.tail_group:
                    # tailの描画
                    tail.update(self.screen, self.stage)
                self.chara.update_miss(self.screen, miss_tmr)
                
                # フラグ立ってるなら当たり判定描写
                self.draw_mask_chara_and_wall()
                # 記録更新中だったら更新中の文字が崩れる
                if self.flag_best_reach:
                    koma = (MISS_TMR // len(self.best_reach_crash_image_list))
                    self.screen.blit(self.best_reach_crash_image_list[(miss_tmr // koma ) % len(self.best_reach_crash_image_list)], self.best_reach_crash_image_list_rect[0])
                # 情報表示
                self.display_info_text() 
                miss_tmr += 1
                if miss_tmr == MISS_TMR:
                    miss_tmr = 0
                    self.index = 22
            elif self.index == 22:
                '''データ書き込み'''
                self.point_total += self.point_cal_getted_graze()
                self.collection_looks['_point_total'] = self.point_total
                # ハイスコアを更新
                model_text = 'MISS!'
                if self.collection_looks['_hiscore_higraze_hipass'][0] < self.point_getted:
                    self.collection_looks['_hiscore_higraze_hipass'][0] = self.point_getted
                    self.collection_looks['_hiscore_higraze_hipass'][1] = round(1+(GRAZE_MAG * self.graze_frame),3)
                    self.collection_looks['_hiscore_higraze_hipass'][2] = self.pass_count
                    model_text = 'NEW RECORD!'

                self.sort_dict()
                self.save_data_write()
                self.play_music(miss = True) # 音楽再生 しっとりBGM
                self.index = 30
            
            elif self.index == 30:
                # ミス後の画面
                self.display_text(f'{model_text}\n\n${self.point_getted} x ({round(1+(GRAZE_MAG * self.graze_frame),3)})'
                                  f' = ${self.point_cal_getted_graze()}\n\nTOTAL ${self.point_total}',WIDTH * 0.5, HEIGHT * 0.2,)
                # 始めるボタン
                self.image_rect_start.center = WIDTH * 3 / 10, HEIGHT * 7 / 10
                self.screen.blit(self.image_start ,self.image_rect_start)
                # 記録ボタン
                self.image_rect_record.center = WIDTH * 7 / 10, HEIGHT * 7 / 10
                self.screen.blit(self.image_record, self.image_rect_record)
                # お買い物ボタン
                self.image_rect_shopping.center = WIDTH * 5 / 10, HEIGHT * 8 / 10
                self.screen.blit(self.image_shopping, self.image_rect_shopping)
                if self.is_button_clicked(self.image_rect_start, event):
                    # again
                    self.index = 10
                if self.is_button_clicked(self.image_rect_record, event):
                    # record
                    self.index = 2
                if self.is_button_clicked(self.image_rect_shopping, event):
                    # shopping
                    self.index = 40
            elif self.index == 40:
                # お買い物処理準備

                self.index = 41
            elif self.index == 41:
                # お買い物画面
                self.draw_shopping_surface(event)
                # 自機セレクトボタン判定
                for i in range(len(self.chara_list_rect)):
                    for j in range(1, len(self.chara_list_rect[i])):
                        if self.is_button_clicked(self.chara_list_rect[i][j], event, self.scroll_x):
                            if self.collection_looks[SELECT_DICT_CHARA[i][0]] >= j:
                                self.chara_num = i
                                self.chara_color = j
                # 壁セレクトボタン判定
                for i in range(len(self.wall_list_rect)):
                    for j in range(1, len(self.wall_list_rect[i])):
                        if self.is_button_clicked(self.wall_list_rect[i][j], event, self.scroll_x):
                            if self.collection_looks[SELECT_DICT_WALL[i]] >= j:
                                self.wall_num = i
                                self.wall_color = j
                # 背景セレクトボタン判定
                for i in range(len(self.back_list_rect)):
                    if self.is_button_clicked(self.back_list_rect[i], event, self.scroll_x):
                        if self.collection_looks[SELECT_DICT_BACK[i]] >= 1:
                            self.back_num = i
                # お買い物ボタン判定
                for i in range(len(self.button_rect_shopping)):
                   if self.is_button_clicked(self.button_rect_shopping[i], event):
                        if i == 0:
                            # 自機購入ボタンが押された
                            if self.point_total >= self.price_chara():
                                for i in range(len(SELECT_DICT_CHARA)):
                                    if self.collection_looks[SELECT_DICT_CHARA[i][0]] == 7:
                                        continue
                                    elif self.collection_looks[SELECT_DICT_CHARA[i][0]] <= 6:
                                        break
                                if self.collection_looks[SELECT_DICT_CHARA[i][0]] != 7:
                                    self.point_total -= self.price_chara()
                                    self.collection_looks[SELECT_DICT_CHARA[i][0]] += 1

                        elif i == 1:
                            # 壁購入ボタンが押された
                            if self.point_total >= self.price_wall():
                                for i in range(len(SELECT_DICT_WALL)):
                                    if self.collection_looks[SELECT_DICT_WALL[i]] == 7:
                                        continue
                                    elif self.collection_looks[SELECT_DICT_WALL[i]] <= 6:
                                        break
                                if self.collection_looks[SELECT_DICT_WALL[i]] != 7:
                                    self.point_total -= self.price_wall()
                                    self.collection_looks[SELECT_DICT_WALL[i]] += 1
                                    
                        elif i == 2:
                            # 背景購入ボタンが押された
                            if self.point_total >= self.price_back():
                                for i in range(len(SELECT_DICT_BACK)):
                                    if self.collection_looks[SELECT_DICT_BACK[i]] == 0:
                                        break
                                if self.collection_looks[SELECT_DICT_BACK[i]] != 1:
                                    self.point_total -= self.price_back()
                                    self.collection_looks[SELECT_DICT_BACK[i]] += 1

                # 戻るボタン
                if self.is_button_clicked(self.image_rect_turn, event):
                    self.index = 1
            
            elif self.index == 50:
                # ゲーム説明
                image_diagram = pygame.image.load('./img/image_diagram.png').convert()
                rect_diagram = image_diagram.get_rect()
                rect_diagram.centerx = WIDTH * 1 / 2
                rect_diagram.top = 0
                self.screen.blit(image_diagram, rect_diagram)
                # 戻るボタン
                self.image_rect_turn.centerx = WIDTH * 1 / 2
                self.image_rect_turn.bottom = HEIGHT
                self.screen.blit(self.image_turn, self.image_rect_turn)
                rect_sp = pygame.Rect(321, 150, 2, 2)
                if self.is_button_clicked(rect_sp, event):
                    self.SE[1].set_volume(0.5)
                    self.SE[1].play() 
                    self.point_total += 1000
                if self.is_button_clicked(self.image_rect_turn, event):
                    self.index = 1

            pygame.display.update()
            self.clock.tick(60)

def start():
    root = App()
    root.main()

if __name__ == '__main__':
    start()

# 横軸1120(=WITH*0.8)より上のグラフは表示限界で書けなくなるので1120番目の壁で絶対死ぬ。
# スクロールは設定したが本当にスクロールできるのかよくわからん
# お買い物画面
# 下の段に固定ボタン。上の段にセレクト物で上下に分ける。
# ボタンの下に隠れたボタンを押さずに済む。

# num、chara、wall、back
# 0.ufo、ビル、町
# 1.鳥、キリン、山
# 2.泳ぐマリオもどき、土管、水中ステージもどき　
# 3.アラジン、ヤシの木、砂漠
# 4.うつむいて歩く女性、眼だけはっきり見える人の影、群衆、レベルアップでこちらを見る人が増える
# 5.ひらがなの「ぬ」、ひらがなの塊、なにか
# 6.（カレーライス）、（スプーン）、（台所）
# 7.（手裏剣）、（スパイダーマンのポーズの忍者）、（武家屋敷）
# 8.（上空から見た羊）、（上空から見た柵）、（上空から見た牧場）
# 9.（紙ヒコーキ）、（妨害するキッズ）、（小学校）
# 10.（蝶々）、（蜘蛛の巣）、（森）
# 11.（ザルドス）、（岩）、（荒野）
# 12.（上空から見た酔っ払い）、（上空から見たヤクザの集まり）、（上空から見た繁華街）
# 13.（ダーツの矢）、（的）、
# 14.（潜水艦）、（蟹）、（海底洞窟）
# 15.（蝙蝠）、（鍾乳洞）、（洞窟）
# 16.（魚）、（円に近いウニ）、海底
# 17.（寿司）、（湯呑）、（回転ずしのレールの上）
# 18.（上空から見たスーパーカー）、（レース場によくある赤と白のブロック）、（上空から見たレース場）　　
# 19.（ナイフ）、（磔にされている人）、（サーカス、観客表情が変化する）
# 20.（人の鼻）、（象の鼻三日月状の壁）、（鼻のコレクション、段階で目がつく）
# 21.（魂）、（大鎌）、（墓場） 

