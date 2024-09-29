#泥棒ゲーム
import random
import time

def print_d(*text, delay=0.02):
    #print()のディレイ版
    for item in text:
        if isinstance(item, str):
            for char in item:
                print(char, end="", flush=True)
                time.sleep(delay)
        else:
            print(item, end="", flush=True)
            time.sleep(delay)
    print()


def input_d(*text, delay=0.02):
    #input()のディレイ版
        for item in text:
            if isinstance(item, str):
                for char in item:
                    print(char, end="", flush=True)
                    time.sleep(delay)
            else:
                print(item, end="", flush=True)
                time.sleep(delay)
        x = input()
        return x

def Press_Enter_Key():
    input_d('Press Enter Key')

def name_input(name = '名前を入力：'):
    return input(name) or 'あなた'


def opening(player , DAYS_MAX):
    print_d(f'''
～～～～～～～～～～～～～オープニング～～～～～～～～～～～～～～～
{DAYS_MAX}日後、美術館に大変貴重な美術品が集結する――――。
それを知った{player}はそれらを盗み出して一獲千金を夢見ています。
しかし{player}は素人泥棒なのでこのままでは計画は失敗するでしょう。
根性もないので重いものを持つことも、それを持って逃げることもできません。
これから{player}は{DAYS_MAX}日間、筋トレして根性を鍛え、
たくさんの物を盗んで窃盗スキルを磨かねばなりません。
来るべき日に備えて。
～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
    ''',delay=0.01)


class MuscleType():
    #筋トレのクラス
    def __init__(self , name , muscle_up , muscle_cal , muscle_time , execution_text_list):
        self.__name = name
        self.__muscle_up = muscle_up
        self.__muscle_time = muscle_time
        self.__execution_text_list = execution_text_list
        self.__muscle_cal = muscle_cal

    def get_name(self):
        return self.__name

    def get_muscle_up(self):
        if self.__muscle_cal == '乗算':
            return self.__muscle_up
        elif self.__muscle_cal == '加算':
            self.__muscle_up = random.choice([3 , 3 , 3 , 3 , 4 , 4 , 4 , 5 , 5 , 7])
        return self.__muscle_up
    
    def get_muscle_cal(self):
        return self.__muscle_cal

    def get_muscle_time(self):
        return self.__muscle_time

    def muscle_execution_text(self):
        muscle_text = random.choice(self.__execution_text_list)
        return f'{self.__muscle_time}時間も{self.__name}した。{muscle_text}\n'


class BlackItem():
    #盗品のクラス
    def __init__(self , name , black_place_rate , counter  , rarity = -11):
        self.__name = name
        self.__rarity = rarity
        self.__counter = counter
        self.__black_place_rate = black_place_rate
        self.__weight = self.generate_weight()
        self.__price = self.generate_price()

    def introduce(self):
        introduce_text = ''
        if 1 <= self.__rarity:
            introduce_text = introduce_text +'☆'
        else:
            introduce_text = introduce_text +'　'
        introduce_text = introduce_text +f'『{self.__name}』　{self.get_weight()}kg　{self.get_price()}円\n'
        return introduce_text
    

    def skilful_up_point(self):
        self.__skilful_up_point = ((self.__weight + self.__price) / 50) * (self.__black_place_rate /2+ 1 )
        if self.__skilful_up_point <= 0:
            self.__skilful_up_point = 1
        return self.__skilful_up_point
        
    def get_name(self):
        return f'『{self.__name}』'

    def generate_weight(self):
        if self.__rarity == -11:
        #普通のアイテムの場合
            if self.__black_place_rate == 0:
                self.__weight = random.randint(5, 25)
            elif self.__black_place_rate == 1:
                self.__weight = random.randint(25, 50)
            elif self.__black_place_rate == 2:
                self.__weight = random.randint(50, 150)
        else:
        #レアアイテム（各場所に一つだけ）の場合
            self.__weight = self.__black_place_rate + 1
        return self.__weight

    def generate_price(self):
        if self.__rarity == -11:
        #普通のアイテムの場合
            if self.__black_place_rate == 0:
                self.__price = random.randint(1, 100)
            elif self.__black_place_rate == 1:
                self.__price = random.randint(300, 3000)
            elif self.__black_place_rate == 2:
                self.__price = random.randint(3000, 10000)
        else:
        #レアアイテム（各場所に一つだけ）の場合
            self.__price = 1000 * (self.__black_place_rate + 1)**self.__black_place_rate
        return self.__price

    def get_rarity(self):
        return self.__rarity

    def get_counter(self):
        return self.__counter
    
    def get_weight(self):
        return self.__weight
    
    def get_price(self):
        return self.__price



class BlackPlace():
    #盗み場所のクラス
    def __init__(self , name , travel_time , landscape , security_guard, closed_message):
        self.__name = name
        self.__travel_time = travel_time
        self.__landscape = landscape
        self.__security_guard = security_guard
        self.__closed_message = closed_message

    def introduce(self):
        return f'{self.__name}:所要{self.__travel_time}時間\n'
    
    def closed_message_output(self):
        return self.__closed_message
        
    def get_name(self):
        return self.__name

    def get_travel_time(self):
        return self.__travel_time
        
    def get_landscape(self):
        return self.__landscape

    def get_security_guard(self):
        return self.__security_guard

class DarkPETraining():
    #闇の体育教師のメニュー
    def __init__(self , name , up_type , up , price):
        self.__name = name
        self.__up_type = up_type
        self.__up = up
        self.__price = price

    def introduce(self):
        return f'{self.__name}　{self.__up_type}+{self.__up} {self.__price}円 '

    def get_name(self):
        return self.__name
    
    def get_up_type(self):
        return self.__up_type

    def get_up(self):
        return self.__up

    def get_price(self):
        return self.__price
    
class Artwork():
    # 美術品のクラス
    def __init__(self , DAYS_MAX , name , level , message):
        self.__name = name
        self.__level = level
        self.__DAYS_MAX = DAYS_MAX
        self.__difficulty = self._generate_difficulty()
        self.__message = message


    def introduce(self):
        return f'『{self.__name}』・・・{self.__message}' 
    
    def _generate_difficulty(self):
        self.__difficulty = self.__DAYS_MAX **self.__level * 500000
        return self.__difficulty

    def get_level(self):
        return self.__level
    
    def get_name(self):
        return self.__name
    
    def get_message(self):
        return self.__message

    def get_difficulty(self):
        return self.__difficulty

def unti_cal(unti_min, unti_max):
    #今日の運を決める
    unti = random.randint(unti_min, unti_max)
    return unti


def unti_notation_text(player , unti):
    #運値のあいまいな表現処理
    if -10 <=unti <= -9:
        print_d(f"今日{player}は吐きそうなほど気分が悪く最低な気分だ")
    elif -8 <= unti <= -7:
        print_d(f"今日{player}は何をしてもうまくいかない気がする")
    elif -6 <= unti <= -5:
        print_d(f"今日{player}は嫌な予感を感じている")
    elif -4 <= unti <= -3:
        print_d(f"今日{player}は体がだるいのに気づいた")
    elif -2 <= unti <= -1:
        print_d(f"今日{player}はちょと嫌な気分であるのに気づいた")
    elif 0 <= unti <= 2:
        print_d( f"今日{player}はふつうの日だ")
    elif 3 <= unti <= 4:
        print_d(f"今日{player}はちょっと気が軽い")
    elif 5 <= unti <= 6:
        print_d(f"今日{player}は調子が良い")
    elif 7 <= unti <= 8:
        print_d(f"今日{player}は良いことが起こる予感がする")
    elif 9 <= unti <= 10:
        print_d(f"今日{player}は世界が祝福しているのを感じる")


def steal_skill_definition(skilful , physical):
    #盗みスキル算出
    exphysical = physical -40
    if exphysical < 0:
        exphysical = 0
    steal_skill = skilful *1.5 + exphysical
    if steal_skill <=0:
        steal_skill = 1
    return steal_skill


def today_status(player , today , DAYS_MAX , unti , physical , skilful , steal_skill , money):
    #一日の始まりアナウンスとステータス表示
    print_d(f'～～～～～～～～{today}日目～～～～～～～～ （あと{DAYS_MAX - today}日）')
    unti_notation_text(player , unti)
    steal_skill = steal_skill_definition(skilful , physical)
    print_d(f'''
    --------
    根性：{round(physical):,}
    窃盗スキル：{round(steal_skill):,}
    所持金：{money}円
    --------
    ''')


def now_steatus(physical , skilful):
    steal_skill = steal_skill_definition(skilful , physical)
    return f'根性：{round(physical):,}\n窃盗スキル：{round(steal_skill):,}'


def daytime_check(daytime , DAYTIME_MAX):
    if daytime < DAYTIME_MAX:
        return True
    else:
        return False


def daytime_now(daytime):
    YORU = 19
    YUGATA = 16
    HIRU = 11
    ASA = 6
    SOUCHO = 4
    SINYA = 0
    if YORU <= daytime:
        jikantai = '夜'
    elif YUGATA <= daytime:
        jikantai = '夕方'
    elif HIRU <= daytime:
        jikantai = '昼'
    elif ASA <= daytime:
        jikantai = '朝'
    elif SOUCHO <= daytime:
        jikantai = '早朝'
    elif SINYA <= daytime:
        jikantai = '深夜'
    return f'現在：{jikantai}{daytime}時'


def DAYTIME_MAX_caution(DAYTIME_MAX):
    return f'（夜{DAYTIME_MAX}時、本日の活動終了）'


def muscle_training_or_steal():
    #筋トレか盗みかの分岐処理
    flag = True
    while flag: 
        dotti = input_d('0.筋トレ\n1.盗みに行く\n')
        if dotti == '0':
            flag = False
            return 'muscle_training'
        elif dotti == '1':
            flag = False
            return 'steal'
        else:
            print_d('受け付け不可')


def muscle_choice_text(muscle_list):
    #筋トレ選択肢の文字列を出す
    m_choice_text = f''
    for i , x in enumerate(muscle_list):
        m_choice_text = m_choice_text + f'{i}. {x.get_name()}：{x.get_muscle_time()}時間 \n'
    return m_choice_text


def muscle_training_execution(daytime , DAYTIME_MAX , muscle_which , muscle_list , physical, muscle_limit, MUSCLE_LIMET_TIME):
    #筋トレの実行：独自のメッセージ出す、時間経過、時間を返す
    kasan = muscle_list[muscle_which].get_muscle_time()
    daytime = daytime + kasan
    if DAYTIME_MAX < daytime:
        if 10 < muscle_limit:
            print_d(f'闇の体育教師が現れた\n闇の体育教師「筋トレは一日{MUSCLE_LIMET_TIME}時間！」\n'
                    f'説教を受けていたら一日が終わった。')
        else:
            print_d(f'{muscle_list[muscle_which].get_name()}を頑張っていたら一日が終わった。\n{daytime_now(daytime)}'
                    '時間オーバーしたので根性は上がらない')
    else:
        if muscle_limit < 10:
            print_d(f'{muscle_list[muscle_which].muscle_execution_text()}')
            mucle_cal_way = muscle_list[muscle_which].get_muscle_cal()
            moto = physical
            if mucle_cal_way == '加算':
                physical = physical + muscle_list[muscle_which].get_muscle_up()
            elif mucle_cal_way == '乗算':
                physical = physical * muscle_list[muscle_which].get_muscle_up()
            agarihaba = physical - moto
            print_d(f'　↑↑ 根性が「{round(agarihaba, 2):,}」増えた ↑↑')
            muscle_limit = muscle_limit + muscle_list[muscle_which].get_muscle_time()
        else:
            print_d(f'闇の体育教師が現れた\n闇の体育教師「筋トレは一日{MUSCLE_LIMET_TIME}時間！実践で力を付けろ！」\n'
                    f'{muscle_list[muscle_which].get_muscle_time()}時間の説教を受けた。盗みに出なければ！')
    return daytime , physical, muscle_limit


def steal_position_choice_text(black_place_list):
    #盗み選択肢の文字列を出す
    s_p_choice_text = ''
    for i , x in enumerate(black_place_list):
        s_p_choice_text = s_p_choice_text + f'{i}.{x.introduce()}'
    s_p_choice_text =  s_p_choice_text + f'99.戻る　　　　　　　　 :所要1時間\n'
    return s_p_choice_text


def black_place_moving(where_BlackPlace , black_place_list , daytime, serial_theft_count_place, SERIAL_THEFT_LIMIT):
    if serial_theft_count_place[where_BlackPlace] <= SERIAL_THEFT_LIMIT:
        daytime += black_place_list[where_BlackPlace].get_travel_time()
        print_d(f'{black_place_list[where_BlackPlace].get_travel_time()}時間かけて"そこ"にやってきた'
                f'\n{daytime_now(daytime)}')
        #時間経過処理
        enter_shop_flag = True
        return daytime, enter_shop_flag
    else:
        print_d(f'{black_place_list[where_BlackPlace].closed_message_output()}')
        if black_place_list[where_BlackPlace].get_name() == '高級店『ブランド狂い』':
            enter_shop_flag = True
        else:
            enter_shop_flag = False
        return daytime, enter_shop_flag




def black_list_generate(where_BlackPlace , black_place_list , BLACK_ITME_LIST_LIST , ITEM_UPPER_LIMIT , unti):
    landscape_text =f'\n{black_place_list[where_BlackPlace].get_landscape()}'
    item_candidacy_list = []
    kari_list = []

    for i in range(len(BLACK_ITME_LIST_LIST[where_BlackPlace])):
        if BLACK_ITME_LIST_LIST[where_BlackPlace][i].get_rarity() == -11:
            kari_list.append(BLACK_ITME_LIST_LIST[where_BlackPlace][i])
    if 9 <= unti:
        # 運値9以上（世界の祝福）の時にレアアイテム出現
        for i in range(len(BLACK_ITME_LIST_LIST[where_BlackPlace])):
            if 0 < BLACK_ITME_LIST_LIST[where_BlackPlace][i].get_rarity():
                item_candidacy_list.append(BLACK_ITME_LIST_LIST[where_BlackPlace][i])
    item_candidacy_text = ''
    for i in range(ITEM_UPPER_LIMIT):
        item_candidacy_list.append(random.choice(kari_list))
        #上限までランダムにitem_candidacy_listに格納
    for i in range(len(item_candidacy_list)):
        item_candidacy_text = f'{item_candidacy_text}{i}.{item_candidacy_list[i].introduce()}'
        #ラインナップの文字列を出力
    item_candidacy_text = item_candidacy_text + f'99.　　窃盗のコツを聞く'
    return item_candidacy_text , item_candidacy_list , landscape_text

def steal_explanation_text(player , physical , skilful):
    steal_skill = steal_skill_definition(skilful , physical)
    st_text = now_steatus(physical , skilful)
    print_d(f'''
    　　「～～窃盗のコツ～～」
{player}の現在のステータスは
{st_text}
{round(physical):,}kgより重いものは必ず盗みに失敗します。
{round(steal_skill):,}円以上のものは失敗の可能性があります。
最初は軽くて安いものを盗んで経験を積みましょう。''')

def again(item_candidacy_list , choice_item, serial_theft_count_once, SERIAL_THEFT_LIMIT):
    if serial_theft_count_once <= SERIAL_THEFT_LIMIT:
        while True:
            print_d(f'もう1{item_candidacy_list[choice_item].get_counter()}いっとく？\n')
            a = input_d(f'0.はい\n1.いいえ\n2.10{item_candidacy_list[choice_item].get_counter()}まとめてくすねる\n')
            if a == '0':
                return 0
            elif a == '1':
                return 1
            elif a == '2':
                return 2
            else:
                print_d('(受け付け不可)\n0か1\n')
    else:
        print_d(f'もう十分に盗んだ\n見つからないうちに早く逃げよう')
        Press_Enter_Key()
        return 1



def steal_unti_hantei(unti):
    randomint = random.randint(1, 100)
    success_or_fail = randomint + (unti * 3)
    if 50 <= success_or_fail:
        return True
    else:
        return False



def skilful_up(chain , skilful_up_point , skilful):
    kasan = (skilful_up_point ) + chain*1.5
    skilful += kasan
    return skilful


def steal_action(unti , choice_item , item_candidacy_list , player , physical , skilful ,
                  black_place_list , where_BlackPlace , stolen_items_list ,
                    STEAL_ACTION_TEXT_LIST_CONF , STEAL_ACTION_TEXT_LIST_LUCK,
                    serial_theft_count_once, SERIAL_THEFT_LIMIT):
    #盗みの成功失敗の処理。続けて盗む
    #成功か失敗、盗んだものリスト、器用の上り具合を返す
    print_d(f'{player}は周りの目を気にしつつ素早く仕事にとりかかる')
    
    steal_skill = steal_skill_definition(skilful , physical)
    weight = item_candidacy_list[choice_item].get_weight()
    price = item_candidacy_list[choice_item].get_price()
    skilful_up_point = item_candidacy_list[choice_item].skilful_up_point()
    chain = 0
    if weight <= physical:
    #重さ判定。根性不足なら即失敗
        one_or_ten_flag = 1
        while True:
            if one_or_ten_flag == 1:
                stolen_items_list.append(item_candidacy_list[choice_item])
            elif one_or_ten_flag == 10:
                for i in range(10):
                    stolen_items_list.append(item_candidacy_list[choice_item])
            if price <= steal_skill:
            #値段判定。値段<スキルなら成功
                action_txt = random.choice(STEAL_ACTION_TEXT_LIST_CONF)
                if one_or_ten_flag == 1:
                    serial_theft_count_once += 1
                elif one_or_ten_flag == 10:
                    serial_theft_count_once += 10
                print_d(f'{player}は{action_txt}{item_candidacy_list[choice_item].get_name()}を盗んだ')
            
            else:
            #スキルが値段未満の場合 運値によって成功
                action_txt = random.choice(STEAL_ACTION_TEXT_LIST_LUCK)
                print_d(f'{player}は{action_txt}{item_candidacy_list[choice_item].get_name()}を盗んだ')
                success_or_fail = steal_unti_hantei(unti)
                if success_or_fail == True:
                    if one_or_ten_flag == 1:
                        serial_theft_count_once += 1
                    elif one_or_ten_flag == 10:
                        serial_theft_count_once += 10
                    pass
                #成功の場合
                else:
                #失敗の場合
                    print_d(f'しまった！！{player}は{black_place_list[where_BlackPlace].get_security_guard()}'
                            f'に見つかった！逃げろ！')
                    if one_or_ten_flag == 1:
                        serial_theft_count_once += 1
                    elif one_or_ten_flag == 10:
                        serial_theft_count_once += 10
                    #skilful_up_pointを保持した状態で失敗判定。逃走フェーズで逃げ切れれば加算される
                    return False , stolen_items_list , skilful_up_point, serial_theft_count_once
            if one_or_ten_flag == 1:
                chain += 1
            elif one_or_ten_flag == 10:
                chain += 10
            print_d(f'{player}は{item_candidacy_list[choice_item].get_name()}を'
                    f'{chain}{item_candidacy_list[choice_item].get_counter()}'
                    f'{'も' if 1 < chain else ''}くすねている')
            conti = again(item_candidacy_list , choice_item, serial_theft_count_once, SERIAL_THEFT_LIMIT)
            if conti == 0:
            #もう1個いく
                price = price * 1.1
                one_or_ten_flag = 1
                skilful_up_point = skilful_up_point * 1.3
            elif conti == 2:
            #10個まとめて
                for i in range(10):
                    price = price * 1.1
                    skilful_up_point = skilful_up_point * 1.3
                one_or_ten_flag = 10
            else:
            #もう一個いかない
                print_d(f'{player}は{black_place_list[where_BlackPlace].get_security_guard()}'
                        f'に見つかる前にその場を離れた')
                return True , stolen_items_list , skilful_up_point, serial_theft_count_once
    else:
        print_d(f'重い！手間取っている内に{player}は'
                f'{black_place_list[where_BlackPlace].get_security_guard()}に見つかった！逃げろ！')
        skilful_up_point = 0
        return False , stolen_items_list , skilful_up_point, serial_theft_count_once


def escape(player , physical , stolen_items_list , money ,
            black_place_list , where_BlackPlace , unti ,
            skilful_up_point , GAMEOVER_flag, serial_theft_count_place, serial_theft_count_once):
    #逃走フェーズ
    #第一判定 盗んだ総重量/3　＜　フィジカルならば逃げ切れる　盗品もスキルアップも取得
    #第二判定 盗んだ総金額に対して運が高ければ逃げ切れる　盗品もスキルアップも取得
    #第三判定 盗んだものを全て置いて逃げれば　運値によっては逃げ切れる　盗品はなくなりスキルアップだけ取得
    #第四判定 所持金を全て渡せば許してもらえる　盗品はなくなりスキルアップもなくなり所持金もなくなる
    #第五判定 所持金0ならGAMEOVER
    total_weight = 0
    for i in stolen_items_list:
        total_weight += i.get_weight()
    input_d('Press Enter Key')
    if total_weight == 0:
    #フィジカル不足で盗みに失敗しリストに何も入っていない場合
        print_d(f'{player}は逃げきった！ しかし何も得るものはなくスキルも上がらず無駄に時間を消費した')
        GAMEOVER_flag = False
        stolen_items_list = []
        skilful_up_point = 0
        serial_theft_count_once = 0
        return GAMEOVER_flag , skilful_up_point , stolen_items_list , money, serial_theft_count_place
    else:
        if total_weight / 3 < physical:
        #第一判定　総重量とフィジカル比較
            print_d(f'{player}は盗品を両手に抱えて走っている…。')
            Press_Enter_Key()
            print_d(f'日ごろ鍛え上げた根性:{round(physical):,}により'
                    f'{player}は総重量{total_weight:,}kgの盗品をものともしない！\n\n'
                    f'{player}は逃げ切ることに成功した！')
            input_d('Press Enter Key')
            serial_theft_count_place[where_BlackPlace] += serial_theft_count_once
            GAMEOVER_flag = False
            return GAMEOVER_flag , skilful_up_point , stolen_items_list , money , serial_theft_count_place
        else:
        #第二判定　総金額と運値比較
            total_price =0
            for i in range(len(stolen_items_list)):
                total_price += stolen_items_list[i].get_price()
                black_place_list[where_BlackPlace].get_travel_time()
            if total_price  * 0.01 < unti:
                print_d(f'{player}は盗品を両手に抱えて走っている…。')
                Press_Enter_Key()
                print_d(f'{player}の根性:{round(physical):,}では'
                        f'総重量{total_weight}kgの盗品には耐えられない\n')
                Press_Enter_Key()
                print_d(f'しかしその時都合よくも{black_place_list[where_BlackPlace].get_security_guard()}は'
                        f'石につまずいて転んだ。\n'
                        f'{player}は運よく逃げ切った！')
                GAMEOVER_flag = False
                input_d('Press Enter Key')
                serial_theft_count_place[where_BlackPlace] += serial_theft_count_once
                return GAMEOVER_flag , skilful_up_point , stolen_items_list , money, serial_theft_count_place
            else:
                #第三判定　盗品を捨てるか
                print_d(f'{player}は{black_place_list[where_BlackPlace].get_security_guard()}に追いかけられている…')
                Press_Enter_Key()
                print_d(f'しかし{player}の根性:{round(physical):,}では総重量{total_weight}kgの盗品の重さに耐えられない！')
                if 0 < money:
                #お金がある場合
                    throw_flag = True
                    while throw_flag:
                        print_d('盗品を全て捨てて逃げますか？')
                        throw_dotti = input_d('0.はい\n1.いいえ\n')
                        if throw_dotti == '0':
                        #お金がある場合盗品を捨てる場合
                            stolen_items_list = []
                            if 5 <= unti:
                                print_d(f'{player}は盗んだものを全て捨てて逃げきった！\n' 
                                        f'しかし何も得るものはなくスキルも上がらず無駄に時間を消費した')
                                GAMEOVER_flag = False
                                skilful_up_point = 0
                                serial_theft_count_once = 0
                                input_d('Press Enter Key')
                                return GAMEOVER_flag , skilful_up_point , stolen_items_list , money, serial_theft_count_place
                            else:
                                print_d(f'{player}は盗んだものを全て捨てたにも関わらず運悪くも'
                                        f'{black_place_list[where_BlackPlace].get_security_guard()}に追いつかれた！')
                                skilful_up_point = 0
                                serial_theft_count_once = 0
                                while True:
                                    stolen_items_list = []
                                    print_d('盗品はすべて没収されてしまった。刑務所にぶち込まれるかもしれない…。')
                                    wairo_dotti = input_d('賄賂を渡して見逃してもらいますか？\n0.はい\n1.いいえ')
                                    if wairo_dotti =='0':
                                    #お金がある場合盗品を捨てる場合賄賂を渡す場合
                                        print_d(f'有り金{money}円全てを支払って許してもらった…。\n'
                                                f'{player}はお金を失いスキルも上がらず無駄に時間を消費した')
                                        money = 0
                                        skilful_up_point = 0
                                        GAMEOVER_flag = False
                                        input_d('Press Enter Key')
                                        return GAMEOVER_flag , skilful_up_point , stolen_items_list , money, serial_theft_count_place
                                    elif wairo_dotti == '1':
                                    #お金がある場合盗品を捨てる場合賄賂を渡さない場合
                                        print_d(F'{player}に助かる道はない')
                                        skilful_up_point = 0
                                        GAMEOVER_flag = True
                                        input_d('Press Enter Key')
                                        return GAMEOVER_flag , skilful_up_point , stolen_items_list , money, serial_theft_count_place
                                    else:
                                        print_d('0か1')
                        elif throw_dotti == '1':
                        #お金がある場合盗品を捨てない場合
                            if 7 <= unti:
                            #お金がある場合盗品を捨てない場合運がある場合
                                Press_Enter_Key()
                                print_d(f'{black_place_list[where_BlackPlace].get_security_guard()}は石につまずいて転んだ\n'
                                        f'{player}は運よく逃げ切れた！')
                                input_d('Press Enter Key')
                                serial_theft_count_place[where_BlackPlace] += serial_theft_count_once
                                GAMEOVER_flag = False
                                return GAMEOVER_flag , skilful_up_point , stolen_items_list , money, serial_theft_count_place
                            else:
                            #お金がある場合盗品を捨てない場合運がない場合
                                stolen_items_list = []
                                print_d(f'欲深い{player}は重たい盗品に足を取られて'
                                        f'{black_place_list[where_BlackPlace].get_security_guard()}に追いつかれた！')
                                print_d('盗品はすべて没収されてしまった。刑務所にぶち込まれるかもしれない…。')
                                serial_theft_count_once = 0
                                while True:
                                    wairo_dotti = input_d('賄賂を渡して見逃してもらいますか？\n0.はい\n1.いいえ')
                                    if wairo_dotti =='0':
                                    #お金がある場合盗品を捨てない場合運がない場合賄賂を渡す場合
                                        print_d(f'有り金{money}円全てを支払って許してもらった…。\n'
                                                f'{player}はお金を失いスキルも上がらず無駄に時間を消費した')
                                        money = 0
                                        skilful_up_point = 0
                                        GAMEOVER_flag = False
                                        input_d('Press Enter Key')
                                        return GAMEOVER_flag , skilful_up_point , stolen_items_list , money, serial_theft_count_place
                                    elif wairo_dotti == '1':
                                    #お金がある場合盗品を捨てない場合運がない場合賄賂を渡さない場合
                                        print_d(F'{player}に助かる道はない')
                                        skilful_up_point = 0
                                        GAMEOVER_flag = True
                                        input_d('Press Enter Key')
                                        return GAMEOVER_flag , skilful_up_point , stolen_items_list , money, serial_theft_count_place
                                    else:
                                        print_d('0か1')
                        else:
                            print_d('0か1')
                else:
                #お金がない場合
                    while True:
                        print_d('盗品を全て捨てて逃げますか？')
                        throw_dotti = input_d('0.はい\n1.いいえ\n')
                        if throw_dotti == '0':
                        #お金がない場合盗品を捨てる場合
                            serial_theft_count_once = 0
                            stolen_items_list = []
                            if 0 <= unti:
                                print_d(f'{player}は盗んだものを全て捨てて逃げきった！\n' 
                                        f'しかし何も得るものはなくスキルも上がらず無駄に時間を消費した')
                                GAMEOVER_flag = False
                                skilful_up_point = 0
                                Press_Enter_Key()
                                return GAMEOVER_flag , skilful_up_point , stolen_items_list , money, serial_theft_count_place
                            else:
                                print_d(f'{player}は盗んだものを全て捨てたにも関わらず運悪くも'
                                        f'{black_place_list[where_BlackPlace].get_security_guard()}に追いつかれた！')
                                skilful_up_point = 0
                                GAMEOVER_flag = True
                                return GAMEOVER_flag , skilful_up_point , stolen_items_list , money, serial_theft_count_place
                        elif throw_dotti == '1':
                        #お金がない場合盗品を捨てない場合
                            if 7 <= unti:
                                Press_Enter_Key()
                                print_d(f'{black_place_list[where_BlackPlace].get_security_guard()}は石につまずいて転んだ\n'
                                        f'{player}は運よく逃げ切れた！')
                                input_d('Press Enter Key')
                                serial_theft_count_place[where_BlackPlace] += serial_theft_count_once
                                GAMEOVER_flag = False
                                return GAMEOVER_flag , skilful_up_point , stolen_items_list , money, serial_theft_count_place
                            else:
                                Press_Enter_Key()
                                serial_theft_count_once = 0
                                print_d(f'{black_place_list[where_BlackPlace].get_security_guard()}に追いつかれた！')
                                print_d(F'{player}に助かる道はない')
                                input_d('Press Enter Key')
                                GAMEOVER_flag = True
                                return GAMEOVER_flag , skilful_up_point , stolen_items_list , money, serial_theft_count_place
                        else:
                            print_d('0か1')
                            
def DarkPE_exchange(player , stolen_items_list , money , physical ,
                     PETRAINING_LIST , unti_min, unti_max):
        print_d('闇の体育教師が現れた。')
        Press_Enter_Key()
        print_d('闇の体育教師「足がつく前にその盗品を全部買い取ってやろう」')
        Press_Enter_Key()
        total_price = 0
        souryou = len(stolen_items_list)
        for i in range(len(stolen_items_list)):
            total_price = total_price + stolen_items_list[i].get_price()
        money = money + total_price
        print_d(f'{player}は盗品{souryou}品を全て売り払い{total_price}円手に入れた。\n{player}は身軽になった。')
        Press_Enter_Key()
        stolen_items_list = []
        if 0 <= money:
            print_d(f'闇の体育教師「金を払うなら筋トレを指示してやろう」\n'
                    f'（{player}の所持金は{money}円だ） \n')
            training_menu = ''
            for i , x in enumerate(PETRAINING_LIST):
                training_menu = training_menu + f'{i}.{x.introduce()}\n'
            training_menu = training_menu + f'{i + 1}.必要ない\n'
            max_menu = i + 1
            training_menu_flag = True
            while training_menu_flag:
                while True:
                    print_d(f'{training_menu}')
                    DarkPE_dore = input_d('どれする？')
                    if DarkPE_dore.isdecimal():
                        DarkPE_dore = int(DarkPE_dore)
                        break
                    else:
                        print_d('受け付け不可')
                if DarkPE_dore == max_menu:
                    print_d(f'必要ない')
                    training_menu_flag = False 
                    return money , stolen_items_list , money , physical , unti_min
                elif 0 <= DarkPE_dore < max_menu:
                    if PETRAINING_LIST[DarkPE_dore].get_price() <= money:
                        money = money - PETRAINING_LIST[DarkPE_dore].get_price()
                        print_d(f'{PETRAINING_LIST[DarkPE_dore].get_price()}円支払った')
                        if PETRAINING_LIST[DarkPE_dore].get_up_type() == '根性':
                            physical = physical + PETRAINING_LIST[DarkPE_dore].get_up()
                            print_d(f'闇の体育教師「気合いだ！気合いだ！気合いだ！」\n')
                            Press_Enter_Key()
                            print_d(f' ↑↑根性が「{PETRAINING_LIST[DarkPE_dore].get_up()}」増えた↑↑')
                            return money , stolen_items_list , money , physical , unti_min
                        elif PETRAINING_LIST[DarkPE_dore].get_up_type() == '運':
                            unti_min = unti_min + PETRAINING_LIST[DarkPE_dore].get_up()
                            if unti_max <= unti_min:
                                unti_min = unti_max 
                            print_d('闇の体育教師「うおー！！！」')
                            Press_Enter_Key()
                            print_d('運がよくなったような…？')
                            return money , stolen_items_list , money , physical , unti_min
                    else:
                        print_d('闇の体育教師「足りないよ」')
                else:
                    print_d(f'受け付け不可')
        else:
            return money , stolen_items_list , money , physical , unti_min
            
def last_steal(player , DAYS_MAX , physical , skilful ,
                STEAL_ACTION_TEXT_LIST_CONF , STEAL_ACTION_TEXT_LIST_LUCK ,
                ARTWORK_LIST , SUCCESS_TEXT_LIST, diversionary_flag, DIVERSIONARY_LIST):
    print_d(f'####################決戦の日####################\n'
            f'ついにこの日がやってきた\n'
            f'{player}は{DAYS_MAX}日の修行の末についにこの日を迎えた。')
    steal_skill = steal_skill_definition(skilful , physical)
    print_d(now_steatus(physical , skilful))
    Press_Enter_Key()
    print_d(f'{player}は静かに美術館に現れた')
    i = 0
    while True:
        print_d(f'{i + 1}品目 {ARTWORK_LIST[i].introduce()}')
        Press_Enter_Key()
        if diversionary_flag == True:
            # 陽動作戦を頼んでいる場合、陽動作戦テキストが出る
            diversionary_txt = random.choice(DIVERSIONARY_LIST)
            print_d(f'{diversionary_txt}')
            Press_Enter_Key()
        else:
            pass
        difficulty = ARTWORK_LIST[i].get_difficulty()
        if difficulty < steal_skill:
            action_txt = random.choice(STEAL_ACTION_TEXT_LIST_CONF)
        else:
            action_txt = random.choice(STEAL_ACTION_TEXT_LIST_LUCK)
        print_d(f'{player}は{action_txt}『{ARTWORK_LIST[i].get_name()}』を盗み始めた…' , delay=0.01)
        print_d('・・・・・・・・・・・・・・・・・・・・・・・・・・・・・')
        Press_Enter_Key()
        i += 1
        if len(ARTWORK_LIST) == i:
            if difficulty < steal_skill:
                print_d(f'ついにやった！　{player}は最後の美術品を盗み出し美術館を空にした！' , delay=0.01)
                if diversionary_flag == True:
                    print_d('闇の体育教師「さすがは俺の弟子だ」')
                else:
                    pass
                rank = i - 1
                GAMEOVER_flag = False
                record_today = DAYS_MAX
                return GAMEOVER_flag , record_today , rank
            else:
                print_d(f'しまった！警備員に声をかけられた！最後の一品だったのに！！\n'
                        f'いつの間にか{player}は警備員に囲まれているのに気が付いた！')
                if diversionary_flag == True:
                    print_d('闇の体育教師はすでにその場から逃げおおせている！')
                else:
                    pass
                Press_Enter_Key()
                rank = i - 1
                record_today = DAYS_MAX
                GAMEOVER_flag = True
                return GAMEOVER_flag , record_today , rank
        if difficulty < steal_skill:
            surper_text = random.choice(SUCCESS_TEXT_LIST)
            print_d(f'{surper_text}')
            print_d(f'{player}は続けて次の得物に近づいた' , delay=0.01)
            Press_Enter_Key()
        else:
            print_d(f'しまった！挙動不審さゆえに警備員に声をかけられた！ \nいつの間にか{player}は警備員に囲まれていた！')
            if diversionary_flag == True:
                print_d('闇の体育教師は必死で他人のふりをしている！')
            else:
                pass
            Press_Enter_Key()
            rank = i - 1
            record_today = DAYS_MAX
            GAMEOVER_flag = True
            return GAMEOVER_flag , record_today , rank
        
def GAMEOVER(player , record_today , physical , skilful , rank , ARTWORK_LIST):
    print_d(f'{player}は刑務所にぶち込まれた！\n'
            f'泥棒の修行は{record_today}日で終わり最悪の結果を迎えた\n'
            f'!!!!!!!!!!!!!!!!!!!!GAME OVER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    steal_skill = steal_skill_definition(skilful , physical)
    rank_text = ''
    if rank == -1:
        rank_text = '窃盗ランク0. 美術館への挑戦以前の問題'
    elif 0 <= rank:
        rank_text = f'窃盗ランク{ARTWORK_LIST[rank].get_level()}. 『{ARTWORK_LIST[rank].get_name()}』'
    last_text = (f'\n{player}\n根性：{round(physical):,}\n窃盗スキル：{round(steal_skill):,}\n{rank_text}')
    print_d(last_text)
    print()# 改行
    TIPS()
    
def GAMECLEAR(player , physical , skilful , rank , ARTWORK_LIST, serial_theft_count_place, SERIAL_THEFT_LIMIT):
    print_d(f'おめでとう！ゲームクリア！{player}は生粋の泥棒だ！')
    steal_skill = steal_skill_definition(skilful , physical)
    xFlag = True
    for i in serial_theft_count_place:
        if i < SERIAL_THEFT_LIMIT:
            xFlag = False
            # 各ブラックプレイスを制覇しているかのチェック
    if xFlag == True:
        # 各ブラックプレイスを制覇していたら完全クリア、最高ランク12のオニ・ババの覇者
        rank_text = f'最高ランク☆ {ARTWORK_LIST[rank].get_level() + 2}  ☆ 『{ARTWORK_LIST[rank].get_name()}』の覇者'
    else:
        rank_text = f'窃盗ランク {ARTWORK_LIST[rank].get_level() + 1}  『{ARTWORK_LIST[rank].get_name()}』の所有者'
    last_text = f'\n{player}\n根性：{round(physical):,}\n窃盗スキル：{round(steal_skill):,}\n{rank_text}'
    print_d(last_text)
    if xFlag == True:
        Press_Enter_Key()
        print_d(f'～～～完全クリア特典　チートコードの紹介～～～\n'
                f'特定の名前にするとステータスにボーナスが入った状態でゲームを始められます！\n'
                f'☆ラッキーマン　割と運が良いです\n'
                f'☆お金持ちマン　金持ち状態でゲームが始まります\n'
                f'☆筋骨隆々マン　最初から根性がそれなりにあります\n'
                f'☆元から怪盗マン　最初から窃盗スキルがそれなりにあります\n'
                f'☆めちゃくちゃ早起きマン　早起きなので一日の活動時間が長いです\n'
                f'★借金マン　借金した状態でゲームが始まります\n'
                f'★アンラッキーマン　とても運が悪いです\n'
                f'★昼起きマン　昼起きなので一日の活動時間が短いです')
    print_d(f'\n2024.08.03制作')

def TIPS():
    TIPS01 = '盗みからの帰宅に時間を多く消費する\nだからギリギリまで筋トレしてから盗みに行くべき'
    TIPS02 = '陽動作戦は内部的には全く意味がない\nしかし所持金を最後まで持ち越したところで全く意味はない'
    TIPS03 = '盗みに入るときの「慣れた手つきで～」などの文章には二種類ある\n確実に盗める時と確率が絡む時'
    TIPS04 = '高額なものほどスキルは上がりやすく、軽いもの程連続で盗みやすい\nそれゆえ軽くて高額なものがねらい目となる'
    TIPS05 = 'お金の使い道はあまりない\nそれゆえ惜しみなく使った方が良い'
    TIPS06 = '筋トレは一日10時間の制約がある\nかといって毎回10時間全部を筋トレに使う必要もない'
    TIPS07 = '一か所で盗める上限は決められている\n三か所すべてを制覇できれば完全クリアも近い'
    TIPS08 = '一か所で盗める上限は決められている\n一か所を完封できれば残り二か所も時間の問題である'
    TIPS09 = 'リザルトに表示されるプレイヤーランクは0～12まである\n美術品をいくつ盗めたか等が基準になる'
    TIPS10 = 'リザルトに表示されるプレイヤーランクは0～12まである\n最高の12ランクを取るには美術館を空にするだけでは足りない'
    TIPS11 = 'テーマはインフレ\n窃盗スキルがおよそ140兆以上あれば最後の美術品を盗むことができる'
    TIPS12 = 'テーマはインフレ\n窃盗スキルが1万を超え始めてからが本番'
    TIPS13 = '根性が高ければ盗みがばれてもそのまま持ち逃げできる\nだが盗品の総重量が大きすぎると根性でカバーできなくなる'
    TIPS14 = '根性が高ければ盗みがばれてもそのまま持ち逃げできる\n根性は高いに越したことはない'
    TIPS15 = '連続して盗めば窃盗スキルはぐーんと上がる\nそれゆえ軽いアイテムはねらい目となる'
    TIPS16 = '連続して盗めば窃盗スキルはぐーんと上がる\n安いアイテムでも連続で100も盗めばその上り幅は尋常ではない'
    TIPS17 = '連続して盗めば窃盗スキルはぐーんと上がる\n逆に言えば少量ずつ盗んでいてはスキルは全く上がらない'
    TIPS18 = '連続して盗めば窃盗スキルはぐーんと上がる\nしかし連続で盗むほど失敗のリスクも跳ね上がり逃走も失敗しやすくなる'
    TIPS19 = '各盗み場所のアイテムにはそれぞれ5kg、25kg、50kgと重さに最低値が設定されている\n筋トレの目安に'
    TIPS20 = '各盗み場所のアイテムにはそれぞれ1円、300円、3000円と価格に最低値が設定されている\n盗みの目安に'
    TIPS21 = '重量挙げによる根性の上り幅は3～7\nそれゆえ闇の体育教師にお金を払った方が楽に根性を上げることができる'
    TIPS22 = '重量挙げによる根性の上り幅は3～7\n4割の確率で3しか上がらないが、1割の確率で7上がる'
    TIPS23 = '重量挙げによる根性の上り幅は3～7\n反復横跳びの上り幅は1.1倍'
    TIPS24 = 'どんなに軽いアイテムも最低値は5kg\nしかしレアアイテムはその限りではない'
    TIPS25 = 'どんなに軽いアイテムも最低値は5kg\nそれゆえ根性を5以上に上げてから盗みに行くべきである'
    TIPS26 = '名前の頭に☆のついたアイテムはレアアイテム\n見つけたら是非盗むべきだ'
    TIPS27 = '名前の頭に☆のついたアイテムはレアアイテム\n軽い割に高額なので一気にスキルを上げるチャンス'
    TIPS28 = '名前の頭に☆のついたアイテムはレアアイテム\n出現するには相応の条件がある'
    TIPS29 = '名前の頭に☆のついたアイテムはレアアイテム\nゲームバランスが壊れるくらいには強力'
    TIPS30 = '窃盗がバレて逃走フェーズに入ると大きく時間を消費する\nしかしばれなくても家に帰るまでにそれなりに時間を消費する'
    TIPS31 = '窃盗がバレて逃走フェーズに入ると大きく時間を消費する\n逃げ切れなければスキルも上がらないので全くの時間の無駄になる'
    TIPS32 = '一日に行動できるのは18時間\n盗み場への移動時間や筋トレの時間などは考慮した方が良い'
    TIPS33 = '一日に行動できるのは18時間\n筋トレに時間を使いすぎて窃盗の時間がなくなるのは注意すべき'
    TIPS34 = '一日の最初に表示される謎の言葉はその日の運勢を意味している\n運勢は盗みの成功率やレアアイテムの出現率などに関わってくる'
    TIPS35 = '一日の最初に表示される謎の言葉はその日の運勢を意味している\n盗みや逃走の際に思い出すと選択のヒントになる'
    TIPS36 = '一日の最初に表示される謎の言葉はその日の運勢を意味している\n「吐きそうなほど気分が悪く最低な気分」の日は賭け事はやめたほうが良い'
    TIPS37 = '一日の最初に表示される謎の言葉はその日の運勢を意味している\n「世界が祝福しているのを感じる」日はぜひ品ぞろえを見に行った方が良い'
    TIPS38 = '逃走に失敗しても所持金全てを渡せばゲームオーバーにはならない\nだから文無しの場合は盗品を置いて逃げたほうが良い'
    TIPS39 = '逃走に失敗しても所持金全てを渡せばゲームオーバーにはならない\nそれゆえ常に1円以上は所持していたい'
    TIPS40 = '逃走に失敗しても所持金全てを渡せばゲームオーバーにはならない\nTIPSを読むためにあえてゲームオーバーになるのもあり'
    TIPS41 = 'アイテムの重さと価格は毎回ランダムで決まる\nしかしレアアイテムだけは例外'
    TIPS42 = 'アイテムの重さと価格は毎回ランダムで決まる\nそれゆえプレイするたびにねらい目のアイテムは変わる'

    TIPS_LIST = [TIPS01, TIPS02, TIPS03, TIPS04, TIPS05, TIPS06, TIPS07,
                 TIPS08, TIPS09, TIPS10, TIPS11, TIPS12, TIPS13, TIPS14,
                 TIPS15, TIPS16, TIPS17, TIPS18, TIPS19, TIPS20, TIPS21,
                 TIPS22, TIPS23, TIPS24, TIPS25, TIPS26, TIPS27, TIPS28,
                 TIPS29, TIPS30, TIPS31, TIPS32, TIPS33, TIPS34, TIPS35,
                 TIPS36, TIPS37, TIPS38, TIPS39, TIPS40, TIPS41, TIPS42 ]
    tip = (random.randint(0, len(TIPS_LIST)-1))
    Press_Enter_Key()
    print_d(f'☆攻略情報☆\nTIPS No.{tip + 1}\n{TIPS_LIST[tip]}')


##############################################################################################################
def DOROBOU_GAME():
    player = name_input()
    #プレイヤー名
    
    physical = 1
    #根性値
    skilful = 0
    #器用値
    steal_skill = steal_skill_definition(skilful , physical)
    #窃盗スキル算出

    unti_max = 10
    unti_min = -10
    #運値最大・運値最小
    
    money = 0
    #所持金
    

    today = 1
    DAYS_MAX = 7
    START_DAY_TIME = 6
    DAYTIME_MAX = 23
    #今日の日付・最終日定数・一日の時間・一日の最大時間定数

    serial_theft_count_once = 0
    # 一回の連続窃盗数初期化
    MUSCLE_LIMET_TIME = 10
    # 一日の筋トレ最大時間

    #～筋トレ種別のインスタンス化～
    HANPUKU = MuscleType('反復横跳び' , 1.1 , '乗算' , 1 , ['変な人だと思われそうだ' , '逃げ足が速くなった気がする' , '小回りの効く泥棒になりそうだ'])
    JUURYOU = MuscleType('重量挙げ' , 4  , '加算' , 5 , ['腕がパンパンだ！' , '上腕二頭筋が震えている' , 'アメコミみたいな体系になりそう'])
    # name , muscle_up , muscle_cal , muscle_time , execution_text_list
    muscle_list = [HANPUKU , JUURYOU]
    #筋トレリスト
    
    #～盗みに入る場所のインスタンス化～
    HATAKE = BlackPlace('荒地『節子と清太の畑』' , 4 , '貧相で狭い畑には乾いた風が吹いている…。' , '節子と清太',
                        'ひどく荒らされた畑だ。もう雑草一本すら生えないだろう')
    MARKET = BlackPlace('スーパー『万引き主婦』' , 6 , '店内はそれなりに混んでいる。万引きのチャンスだ。' , '万引きGメン',
                        '万引きの被害があまりにも甚大だったので、この店は廃業に追い込まれた')
    BRANDED = BlackPlace('高級店『ブランド狂い』' , 8 , 'ブランドものしか置いてない高級店。警備員があちこちにいる。' , '特殊警備隊',
                         '世界に金持ちがいる限り、この店は潰れたりなどしないのだ')
    #畑・スーパー・高級店
    black_place_list = [HATAKE , MARKET , BRANDED ]
    #場所リスト
    
    serial_theft_count_place = []
    for i in range(len(black_place_list)):
        serial_theft_count_place.append(0)
    # 各場所の窃盗回数初期化
    SERIAL_THEFT_LIMIT = 100
    # 一か所で盗める最大数


    #～盗みアイテムのインスタンス化～
    DAIKON = BlackItem('貧相な細い大根' , 0 , '本')
    INE = BlackItem('ほとんど実のない小さな稲' , 0 , '束')
    KYABETU = BlackItem('紙屑のようなキャベツ', 0 , '枚')
    HOTARUNOHAKA = BlackItem('火垂るの墓' , 0 , '基')
    TOMATO = BlackItem('未成熟の小さなミニトマト' , 0 , '粒')
    DONGURI = BlackItem('虫が食ったどんぐり' , 0 , 'どんぐり')
    KYUURI = BlackItem('とても短いきゅうり' , 0 , '本')
    KAKASI = BlackItem('壊れた手作りかかし' , 0 , '体')
    HOURENSOU = BlackItem('ちじれたほうれん草' , 0 , '束' )
    KABUTOMUSI = BlackItem('頭の部分だけのカブトムシ' , 0 , '頭' )
    SISO = BlackItem('雑草に紛れて生えた紫蘇' , 0 , '枚')
    NAGANEGI = BlackItem('くたびれた長ネギ' , 0 , '本')
    SUIKA = BlackItem('握りこぶしくらいのスイカ' , 0 , '握り')
    BOROBOROMATUBOKKURI = BlackItem('ボロボロまつぼっくり' , 0 , '個')
    AMEDAMA = BlackItem('秘蔵の飴玉' , 0 , '缶', 8)
    JAGAIMO = BlackItem('じゃりかと思ったらじゃがいも' , 0 , '個')
    ASAGAOHANABIRA = BlackItem('鮮やかなアサガオ' , 0 , '輪')
    SAYAENDOU = BlackItem('からからに干からびたさやえんどう' , 0 , '本')
    SIBOMINASU = BlackItem('しぼんで干からびたナス' , 0 , '本')
    NINJINNOKOSI = BlackItem('動物に食い散らかされてもかろうじて残ってた人参' , 0 , 'かけら')
    #畑の盗みアイテム
    HATAKE_LIST = [DAIKON , INE , KYABETU , HOTARUNOHAKA , TOMATO , DONGURI ,
                  KYUURI , KAKASI , HOURENSOU , KABUTOMUSI , SISO , NAGANEGI ,
                  SUIKA , BOROBOROMATUBOKKURI , AMEDAMA , JAGAIMO ,ASAGAOHANABIRA ,
                  SAYAENDOU , SIBOMINASU , NINJINNOKOSI]
    # = BlackItem('盗むには罪悪感を感じる貧相な農作物' , 0 , '助数詞' , レアアイテム一つ)
    #畑のアイテムリスト
    
    
    HAMIGAKIKO = BlackItem('安っぽい歯磨き粉' , 1 , '本')
    SENZAI = BlackItem('罪を清める洗剤' , 1 , 'リットル')
    KOMEDAWARA = BlackItem('大特価米俵' , 1 , '俵')
    OSOUZAI = BlackItem('大安売り劣悪惣菜' , 1 , '品')
    DOGFOOD = BlackItem('在庫あまり過ぎドッグフード' , 1 , '粒')
    KOROKKE = BlackItem('売れ残りコロッケ100個セット' , 1 , 'セット')
    NAMAZAKANA = BlackItem('期限ギリギリ生魚100匹セット' , 1 , 'セット')
    ZOUKIN = BlackItem('すでにボロボロの雑巾' , 1 , '枚')
    ONIGOROSI = BlackItem('鬼を殺す液体' , 1 , '升')
    KAGAMIMOTI = BlackItem('季節外れ鏡餅' , 1 , '重ね')
    KARENDAA = BlackItem('去年の新品カレンダー' , 1 , '部')
    KESHOUSUI = BlackItem('変な匂いがする化粧水' , 1 , 'cc')
    GYUUDONMOTO = BlackItem('豚肉の牛丼の素' , 1 , 'パック')
    MAGUROKAITAI = BlackItem('マグロの解体ショー観覧チケット' , 1 , '枚')
    KAPPUMEN = BlackItem('超高級カップ麺' , 1 , '杯')
    TAMAGOWARESOU = BlackItem('今にも割れそうな生卵' , 1 , 'かけら')
    BIIRUKAN = BlackItem('フルシェイク缶ビール' , 1 , '本')
    POKEMONPAN = BlackItem('パチモンポケモンパン' , 1 , '枚')
    KOOHII = BlackItem('期限ギリギリ安売りアイスコーヒー' , 1 , '本')
    MAYONEEZU = BlackItem('10割油のマヨネーズ' , 1 , 'リットル')
    FURIKAKE = BlackItem('イチゴパフェ味のふりかけ' , 1 , '袋', 8)

    # = BlackItem('スーパーにありそうな癖の強い物体' , 1 , '助数詞', レアアイテム一つ)
    #スーパーの盗みアイテム
    
    MARKET_LIST = [HAMIGAKIKO , SENZAI , KOMEDAWARA , OSOUZAI , DOGFOOD ,
                  KOROKKE , NAMAZAKANA , ZOUKIN , ONIGOROSI , KAGAMIMOTI ,
                  KARENDAA , KESHOUSUI , GYUUDONMOTO , MAGUROKAITAI , KAPPUMEN ,
                  TAMAGOWARESOU , BIIRUKAN , POKEMONPAN , KOOHII , MAYONEEZU ,
                  FURIKAKE]
    #スーパーのアイテムリスト
    
    GUCCISHOKKI = BlackItem('グッチの食器' , 2 , '枚')
    GUCCINIKKI = BlackItem('グッチの日記' , 2 , '冊')
    GUCCISEKKI = BlackItem('グッチの石器' , 2 , '点')
    GUCCIGAKKI = BlackItem('グッチの楽器' , 2 , '台')
    GUCCIKOKKI = BlackItem('グッチの国旗' , 2 , '流')
    GUCCIZASSI = BlackItem('グッチの雑誌' , 2 , '冊')
    GUCCIMATTI = BlackItem('グッチのマッチ' , 2 , '箱')
    GUCCIUNTI = BlackItem('グッチのウンチ' , 2 , 'つかみ' , 9)
    VUIITONFUTON = BlackItem('ヴィトンの布団' , 2 , '組')
    VUIITONMITON = BlackItem('ヴィトンのミトン' , 2 , '組')
    VUIITONRIBON = BlackItem('ヴィトンのリボン' , 2 , 'm')
    VUIITONSIHON = BlackItem('ヴィトンの資本' , 2 , '銀行')
    VUIITONBIJON = BlackItem('ヴィトンのヴィジョン' , 2 , 'ディオプター')
    VUIITONRIRON = BlackItem('ヴィトンの理論' , 2 , '論')
    VUIITONMIHON = BlackItem('ヴィトンの見本' , 2 , '点')
    HERMESEXCEL = BlackItem('エルメスのエクセル' , 2 , '本')
    HERMESOMURETU = BlackItem('エルメスのオムレツ' , 2 , '食')
    HERMESAKUSERU = BlackItem('エルメスのアクセル' , 2 , '本')
    HERMESKARUPISU = BlackItem('エルメスのカルピス' , 2 , 'リットル')
    HERMESENAMERU = BlackItem('エルメスのエナメル' , 2 , 'ガロン')
    HERMESWIRUSU = BlackItem('エルメスのウィルス' , 2 , 'VP/mL')
    HERMESFZERO = BlackItem('エルメスのF-ZERO' , 2 , '本')
    CHANELKYABETU = BlackItem('シャネルのキャベツ' , 2 , '玉')
    CHANELSHABERU = BlackItem('シャネルのシャベル' , 2 , '振')
    CHANELPAZURU = BlackItem('シャネルのパズル' , 2 , 'ピース')
    CHANELSADORU = BlackItem('シャネルのサドル' , 2 , '個')
    CHANELSHATORU = BlackItem('シャネルのシャトル' , 2 , '機')
    ROLEXNEKKURESU = BlackItem('ロレックスのネックレス' , 2 , '連')
    ROLEXDERAKKUSU = BlackItem('ロレックスのデラックス' , 2 , 'びっくり')
    ROLEXFENIKKUSU = BlackItem('ロレックスのフェニックス' , 2 , '頭')
    ROLEXWAKKUSU = BlackItem('ロレックスのワックス' , 2 , 'ガロン')
    ROLEXDETOKKUSU = BlackItem('ロレックスのデトックス' , 2 , '回')
    ROLEXROKKUFESU = BlackItem('ロレックスのロック・フェス' , 2 , '回')
    # = BlackItem('ブランド名と物体のダジャレ' , 2 , '助数詞', レアアイテム一つ)
    #高級店の盗みアイテム

    BRANDED_LIST = [GUCCISHOKKI , GUCCINIKKI , GUCCISEKKI , GUCCIGAKKI , GUCCIKOKKI ,
                   GUCCIZASSI , GUCCIMATTI , GUCCIUNTI , VUIITONFUTON , VUIITONMITON ,
                   VUIITONRIBON , VUIITONSIHON , VUIITONBIJON , VUIITONRIRON , VUIITONMIHON ,
                   HERMESEXCEL , HERMESOMURETU , HERMESAKUSERU , HERMESKARUPISU , HERMESENAMERU ,
                   HERMESWIRUSU , HERMESFZERO , CHANELKYABETU , CHANELSHABERU , CHANELPAZURU ,
                   CHANELSADORU , CHANELSADORU , CHANELSHATORU , ROLEXNEKKURESU , ROLEXDERAKKUSU ,
                   ROLEXFENIKKUSU , ROLEXWAKKUSU , ROLEXDETOKKUSU , ROLEXROKKUFESU]
    #高級店のアイテムリスト
    
    BLACK_ITME_LIST_LIST = [HATAKE_LIST , MARKET_LIST , BRANDED_LIST]
     #アイテムリストのリスト

    ITEM_UPPER_LIMIT = 5
    #並ぶ商品の上限数
    stolen_items_list = []
    #playerが盗んだものリスト

    STEAL_ACTION_TEXT_LIST_CONF = ['慣れた手つきで' , '熟練の手さばきで' , '息を吸って吐くように' ,
                                   '目にも止まらぬ素早さで' ,'素人とは思えない動きで' , 'ごく自然な動作で' ,
                                   '手際よく' , '隙をついて' , '鮮やかな手つきで' ,'巧みな手腕で' , '警戒しつつも' ,
                                   '目にも止まらぬ早業で' , '流れで', '警戒しつつも' , '隙をついて' ,
                                     '一か八かの賭けに出つつ' ,'神に祈りつつ' ,'どさくさに紛れて' ,'祈るような気持ちで' ,
                                       'ごく自然な動作で' , '流れで','手際よく' , 'ぎこちなく' , 'もたつきつつも' ,
                                         '不慣れな手つきで' ,'場慣れしていない手つきで']
    STEAL_ACTION_TEXT_LIST_LUCK = ['警戒しつつも' , '隙をついて' , '一か八かの賭けに出つつ' , '神に祈りつつ' ,
                                    'どさくさに紛れて' ,'祈るような気持ちで' , 'ごく自然な動作で' , '流れで',
                                    '手際よく' , 'ぎこちなく' , 'もたつきつつも' , '不慣れな手つきで' ,
                                    '場慣れしていない手つきで']
    #盗みアクションリスト、確定演出と運要素演出、すこしダブっている　「あなたは{}おもちを盗んだ」

    SUCCESS_TEXT_LIST = ['余裕の窃盗スキルだ！' , '流石の手癖の悪さだ！' , '惚れ惚れする鮮やかさだ！',
                     '最早芸術の域だ！' , '国宝級の手腕だ！' , 'まるでルパンだ！' , '手品のようだ！' ,
                     '信じられない神業だ！' , '名人のような手さばきだ！' , 'まさに才能の持ち主だ！']
    # ラストスティール専用の盗みテキスト 「{}あなたはおもちを盗んだ」

    DIVERSIONARY_LIST = ['闇の体育教師はマッスルポーズで彫刻に混ざることで人目を集めている',
                         '闇の体育教師は全身青く塗って歩き回ることで奇怪なアートとして人目を集めている',
                         '闇の体育教師はオレンジジュースを絵画にぶっかけることで一悶着起こして人目を集めている',
                         '闇の体育教師はパントマイム集団にうざがらみして人目を集めている',
                         '闇の体育教師はレプリカの横にその元絵のポスターを張ることで本当に価値があるのはどちらなのかを問い人目を集めている',
                         '闇の体育教師はホームセンターで買ってきた便器をしれっと美術館の空きスペースに設置して人目を集めている',
                         '闇の体育教師は道行く人の似顔絵を奇怪な画風で描いて人目を集めている',
                         '闇の体育教師は覆面姿で歩き回ることでそれが不審者なのか何かのアートなのかのギリギリのラインをせめることで人目を集めている',
                         '闇の体育教師は10憶の値が付いた絵画の横で10円で自分の絵を売り物議をかもすことで人目を集めている',
                         '闇の体育教師は学芸員のふりをして道行く人に絵の解説をしてウソがばれると大声で笑って人目を集めている',
                         '闇の体育教師は道のど真ん中で座禅を組んで瞑想することでこれもなにかのアートなのかと人目を集めている',
                         '闇の体育教師はミュージアムショップで勝手に自作の詩集を並べることで物議をかもし人目を集めている']
    # 陽動作戦テキスト

    SUPARUTACHUU = DarkPETraining('スパルタ教育（体験版）' , '根性' , 15 , 1000)
    SUPARUTAOMAJINAI = DarkPETraining('スパルタおまじない' , '運' , 5 , 2000)
    SUPARUTADAI = DarkPETraining('スパルタ教育（本番）' , '根性' , 100 , 5000)
    SUPARUTAKAMIDANOMI = DarkPETraining('スパルタ神頼み' , '運' , 10 , 20000)
    

    #= DarkPETraining(名前 , 根性か運 , 上り幅 , 値段)
    #闇の体育教師のトレーニング　インスタンス化

    PETRAINING_LIST = [SUPARUTACHUU , SUPARUTAOMAJINAI , SUPARUTADAI, SUPARUTAKAMIDANOMI]
    #闇の体育教師のトレーニングリスト

    SAKEBI = Artwork(DAYS_MAX , '文句の叫び' , 1 ,
                      '怒鳴り散らしているクレーマーを描いた名作庶民絵画')
    OTIBA = Artwork(DAYS_MAX , '命拾い' , 2 ,
                      '藁をつかむことで命拾いした百姓の農民絵画')
    REIKO = Artwork(DAYS_MAX , '迷路微増' , 3 ,
                      '目を離した瞬間に微妙に増えている迷路のインタラクティブ幽霊絵画' )
    KONGOU = Artwork(DAYS_MAX , 'こんがり詐欺師像' , 4 ,
                      '火刑に処せられて苦しむ詐欺師の世界遺産ブロンズ彫刻' )
    SEIBOSI = Artwork(DAYS_MAX , '整備士像' , 5 ,
                      '横たわる自動車を介抱する整備士の庶民絵画' )
    FUUJINRAIJIN = Artwork(DAYS_MAX , '通信対戦図' , 6 ,
                      '通信ケーブルを使ってポケモン交換する歴史的記録絵画' )
    GYUUNYUUWOSOSOGU = Artwork(DAYS_MAX , '恐竜をそしるおんな' , 7 ,
                      '隕石ごときで絶滅したと恐竜への悪口を言って炎上した女の自撮り' )
    CHOUJUUGIGA = Artwork(DAYS_MAX , '超重量ピザ' , 8 ,
                      '巨大なピザに群がるウサギとカエルの風刺画' )
    MIKAERIBIJIN = Artwork(DAYS_MAX , '日帰り邪神図' , 9 ,
                      '地獄からの日帰りでこの世を終わらせる邪神の宗教画' )
    MONARIZA = Artwork(DAYS_MAX , 'オニ・ババ' , 10 ,
                      '鬼婆がこちらに微笑みかけている世界的名作絵画' )
    # = Artwork(DAYS_MAX , 名前 , レベル , 説明文)
    # 美術品　インスタント化
    ARTWORK_LIST = [SAKEBI , OTIBA , REIKO , KONGOU , SEIBOSI , FUUJINRAIJIN ,
                    GYUUNYUUWOSOSOGU , CHOUJUUGIGA , MIKAERIBIJIN , MONARIZA]
    # 美術品のリスト（10個）

    ################################################
    # cheat code
    if player == '☆ラッキーマン':
        unti_min = 5
    if player == '★アンラッキーマン':
        unti_max = -5
    if player == '☆お金持ちマン':
        money = 10000
    if player == '★借金マン':
        money = -10000
    if player == '☆筋骨隆々マン':
        physical = 40
    if player == '☆元から怪盗マン':
        skilful = 6670
    if player == '☆めちゃくちゃ早起きマン':
        START_DAY_TIME = 0
    if player == '★昼起きマン':
        START_DAY_TIME = 13

    ################################################


    opening(player , DAYS_MAX)
    #ゲーム説明
    GAMEOVER_flag = False
    while today < DAYS_MAX:
    #最終日まで一日がループ
        unti = unti_cal(unti_min, unti_max )
        #今日の運勢算出
        today_status(player , today , DAYS_MAX , unti , physical , skilful , steal_skill , money)
        #現在ステータスの表示 
        daytime = START_DAY_TIME
        #１日の始まり
        muscle_limit = 0
        # 筋トレ上限をリセット
        while  daytime < DAYTIME_MAX:
        #daytimeがDAYTIME_MAXになるまでループ
            print_d(daytime_now(daytime) , DAYTIME_MAX_caution(DAYTIME_MAX))
            print_d()
            #時間表示
            serial_theft_count_once = 0
            # 一回の連続窃盗回数を初期化
            MorS = muscle_training_or_steal()
            #筋トレか盗みに行くか
            if MorS == 'muscle_training':
            #筋トレを選んだ場合
                m_choice_flag = True
                while m_choice_flag:
                #筋トレの種類を選ぶ
                    m_choice_text = muscle_choice_text(muscle_list)
                    while True:
                        muscle_which = input_d(f'どれやる？（{daytime_now(daytime)}）\n{m_choice_text}')
                        if muscle_which.isdecimal():
                            muscle_which = int(muscle_which)
                            break
                        else:
                            print_d('受け付け不可')
                    if 0 <= muscle_which < len(muscle_list):
                        m_choice_flag = False
                    else:
                        print_d('受け付け不可')
                daytime , physical, muscle_limit = muscle_training_execution(daytime , DAYTIME_MAX ,
                                                                              muscle_which , muscle_list ,
                                                                                physical, muscle_limit,
                                                                                 MUSCLE_LIMET_TIME)
                #それぞれの種目の筋トレメッセージ、時間の加算、根性の加算
    
            else:
            #盗みに行く場合
                s_p_choice_text = steal_position_choice_text(black_place_list)
                s_p_choice_flag = True
                while s_p_choice_flag:
                    while True:
                        where_BlackPlace = input_d(f'どこ行く？（{daytime_now(daytime)}）\n{s_p_choice_text}')
                        if where_BlackPlace.isdecimal():
                            where_BlackPlace = int(where_BlackPlace)
                            break
                        else:
                            print_d('受け付け不可')
                    #盗みに行く場所を選ぶ
                    black_place_list_len = len(black_place_list)
                    if 0 <= where_BlackPlace < black_place_list_len:
                        s_p_choice_flag = False
                        daytime, enter_shop_flag = black_place_moving(where_BlackPlace , black_place_list ,
                                                                       daytime, serial_theft_count_place,
                                                                        SERIAL_THEFT_LIMIT)
                        if enter_shop_flag == True:
                            # その場所での窃盗回数が上限に届いていない場合
                            daytimeflag = daytime_check(daytime , DAYTIME_MAX)
                            #時間経過チェック
                            if daytimeflag == False:
                                break
                            item_candidacy_text , item_candidacy_list ,landscape_text = black_list_generate(where_BlackPlace ,
                                                                                                            black_place_list ,
                                                                                                            BLACK_ITME_LIST_LIST,
                                                                                                                ITEM_UPPER_LIMIT ,
                                                                                                                unti)
                            #盗めるものの一覧とリストと情景を確定
                            choice_item_flag = True
                            while choice_item_flag:
                                print_d(landscape_text)
                                print_d(item_candidacy_text)
                                while True:
                                    choice_item = input_d('どれ盗む？')
                                    if choice_item.isdecimal():
                                        choice_item = int(choice_item)
                                        break
                                    else:
                                        print_d('受け付け不可')
                                if choice_item == 99:
                                    steal_explanation_text(player , physical , skilful)
                                elif 0 <= choice_item < len(item_candidacy_list):
                                    choice_item_flag = False
                                else:
                                    print_d('受け付け不可')
                            succes_or_fail, stolen_items_list , skilful_up_point, serial_theft_count_once = steal_action(unti ,
                                                                                                choice_item ,
                                                                                                item_candidacy_list ,
                                                                                                player , physical ,
                                                                                                    skilful ,black_place_list ,
                                                                                                    where_BlackPlace ,
                                                                                                        stolen_items_list ,
                                                                                                        STEAL_ACTION_TEXT_LIST_CONF ,
                                                                                                        STEAL_ACTION_TEXT_LIST_LUCK,
                                                                                                        serial_theft_count_once,
                                                                                                        SERIAL_THEFT_LIMIT)      
                            #窃盗判定、「成功か失敗」と「盗んだものリスト」を返す
                            if succes_or_fail ==True:
                                #成功の場合。器用加算、時間経過
                                skilful = skilful + skilful_up_point
                                moto = steal_skill
                                steal_skill = steal_skill_definition(skilful , physical)
                                agarihaba = steal_skill - moto
                                daytime += black_place_list[where_BlackPlace].get_travel_time()
                                serial_theft_count_place[where_BlackPlace] += serial_theft_count_once
                                print_d(f' ↑↑窃盗スキルが{round(agarihaba, 2):,}増えた↑↑\n'
                                        f'{black_place_list[where_BlackPlace].get_travel_time()}時間が経過していた\n'
                                        f'{daytime_now(daytime)}')
                            else:
                                #失敗の場合。逃走フェイズ
                                GAMEOVER_flag , skilful_up_point , stolen_items_list , money, serial_theft_count_place, = escape(player , physical ,
                                                                                stolen_items_list , money ,black_place_list ,
                                                                                    where_BlackPlace , unti , skilful_up_point ,
                                                                                        GAMEOVER_flag, serial_theft_count_place,
                                                                                        serial_theft_count_once)
                                if GAMEOVER_flag == False:
                                    if 0 < skilful_up_point:
                                        #逃走成功
                                        skilful = skilful + skilful_up_point
                                        moto = steal_skill
                                        steal_skill = steal_skill_definition(skilful , physical)
                                        agarihaba = steal_skill - moto
                                        daytime += black_place_list[where_BlackPlace].get_travel_time()*2
                                        print_d(f' ↑↑窃盗スキルが{round(agarihaba, 2):,}増えた↑↑\n'
                                                f'{black_place_list[where_BlackPlace].get_travel_time()*2}時間が経過していた\n'
                                                f'{daytime_now(daytime)}')
                                        
                                    elif skilful_up_point == 0:
                                        #逃走成功　フィジカル不足で盗み失敗したが逃げおおせた場合
                                        daytime += black_place_list[where_BlackPlace].get_travel_time()*2
                                        print_d(f'{black_place_list[where_BlackPlace].get_travel_time()*2}時間が経過していた\n'
                                                f'{daytime_now(daytime)}')
                                elif GAMEOVER_flag == True:
                                    record_today = today
                                    daytime = DAYTIME_MAX
                                    today = DAYS_MAX
                                    break
                                #逃走失敗＝ループの外に出てGAMEOVER処理、リザルト
                                #これで外出られる？？？？？
                        else:
                            pass
                            # その場所での窃盗回数が上限に届いている場合


                    elif where_BlackPlace ==99:
                        #「戻る」の処理
                        daytime += 1
                        print_d('　（1時間掛けて家に戻った）')
                        s_p_choice_flag = False
                        break
                    else:
                        print_d('受け付け不可')
            if GAMEOVER_flag == False:
                daytime_last_text = now_steatus(physical , skilful)
                print_d(daytime_last_text)
            else:
                pass
        if GAMEOVER_flag == False:
            print_d(f'\n{DAYTIME_MAX}時を超えた。　今日という一日が終わった\n')
            if 1 <= len(stolen_items_list):
                money , stolen_items_list , money , physical , unti_min = DarkPE_exchange(player ,
                                                                                           stolen_items_list ,
                                                                                             money ,
                                                                                               physical ,
                                                                                               PETRAINING_LIST ,
                                                                                                 unti_min,
                                                                                                 unti_max)
            #　盗品を持っていると闇の体育教師が現れる処理
            else:
                pass
            today += 1
            if today == DAYS_MAX:
                print_d('闇の体育教師「よく頑張ったな！全額払うなら明日の本番に俺が手伝ってやろう。」')
                while True:
                    choice_diversionary = input_d('全額払って陽動作戦を頼みますか？\n0.はい\n1.いいえ\n')
                    if choice_diversionary == '0':
                        if money <= 0:
                            print_d(f'闇の体育教師「文無しではないか！」\nそれでも{player}は頼み込んだ')
                        else:
                            print_d(f'{money}円全額払って陽動作戦を頼んだ')
                            money = 0
                        diversionary_flag = True
                        break
                    elif choice_diversionary == '1':
                        print_d(f'{player}は丁重に断った。闇の体育教師はすごすごと帰っていった')
                        diversionary_flag = False
                        break
                    else:
                        print_d('0か1')
            else:
                pass
            print_d(f'日はまた昇る\n')
            Press_Enter_Key()
            #一日の終わり
        else:
            pass
    if GAMEOVER_flag == True:
        # 美術館に行く以前に捕まるパターン。ランク0（内部的にはランク-1）
        rank = -1
        GAMEOVER(player , record_today , physical , skilful , rank , ARTWORK_LIST)
    else:
        # ゲームオーバーフラグがたってないならラストスティール
        GAMEOVER_flag , record_today , rank= last_steal(player , DAYS_MAX , physical , skilful ,
                STEAL_ACTION_TEXT_LIST_CONF , STEAL_ACTION_TEXT_LIST_LUCK ,
                ARTWORK_LIST , SUCCESS_TEXT_LIST, diversionary_flag, DIVERSIONARY_LIST)
        if GAMEOVER_flag ==True:
            #ラストスティールでしくじった場合
            GAMEOVER(player , record_today , physical , skilful , rank , ARTWORK_LIST)
        elif GAMEOVER_flag == False:
            #ラストスティールをクリアした場合
            GAMECLEAR(player, physical , skilful , rank , ARTWORK_LIST, serial_theft_count_place, SERIAL_THEFT_LIMIT)
    Press_Enter_Key()
    
         
DOROBOU_GAME()


