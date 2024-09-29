#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random
import time


# In[44]:


def print_d(*text, delay=0.01):
    for item in text:
        if isinstance(item, str):
            for char in item:
                print(char, end="", flush=True)
                time.sleep(delay)
        else:
            print(item, end="", flush=True)
            time.sleep(delay)
    print()


# In[46]:


def input_d(*text, delay=0.01):
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


# In[7]:


def dice_roll(dice_list):
    #目的：リストの中から一つ選ぶ
    #入力：リスト
    #処理：リストの中から一つランダムで選ぶ
    #出力：ランダムで出た数値deme
    print_d('勝負の時！')
    input('Press Enter Key')
    deme = random.choice(dice_list)
    print_d(F'{deme}が出た！')
    return (deme)


# In[10]:


def input_int():
    #目的：入力を受け付けて数字かを判断する
    #入力：数字のinput
    #処理：受けたものが数字か判断する
    #出力：受けたintを返す

    flag = True
    while flag:
        suji = input_d('数字を入力:')
        #入力されたものが数字かを判定
        if suji.isdigit():
            suji = int(suji)
            flag = False
            return suji
        else:
            print_d('数値を入力してください　もう一度入力してね')


# In[11]:


def input_yosou(dice_list):
    flag = True
    while flag:
        yosou = input_int()
        if yosou in dice_list:
            flag = False
            return yosou
        else:
            print_d('候補にない数字です')


# In[72]:


def input_kakekin(shojikin , all_in_flag):
    #目的：入力した掛け金が所持金に見合うかを判断
    #入力：数字のinput(内部)、所持金（外部）
    #処理：受けたものが所持金以下か判断する。
    #出力：受けたintを返す

    #flagをTrueにしておく
    flag = True
    #flagがTrueの間実行し続ける
    while flag:
        kakekin = input_int()
        if kakekin == 0:
            all_in_flag = True
            kakekin = shojikin
            return kakekin , all_in_flag
        elif kakekin < shojikin:
            flag = False
            all_in_flag = False
            return kakekin , all_in_flag
        else:
            print_d('そんなに持ってないでしょ')


# In[15]:


def hantei(yosou , deme , kakekin , shojikin , higet_score , all_in_flag):
    #目的：予想と出目があっているか確認してお金計算
    #入力：予想、出目、掛け金、所持金
    #処理：予想と出目の比較して所持金を増減させる
    #出力：現在の所持金
    if yosou ==deme:
        if all_in_flag:
            print_d('特大大当たり！')
            haraimodosi = kakekin * 60
            shojikin = shojikin + haraimodosi
            print_d(f'掛け金{kakekin}円が60倍！現在所持金{shojikin}円')
            all_in_flag = False
        else:
            print_d('>>>当たり！')
            haraimodosi = kakekin * 6
            shojikin = shojikin + haraimodosi
            print_d(f'掛け金{kakekin}円が6倍になり{haraimodosi}円の払い戻しです！現在所持金{shojikin}円')

        if higet_score[1] < haraimodosi:
            higet_score[1] = haraimodosi
        if higet_score[2] < shojikin:
            higet_score[2] = shojikin
        return shojikin , higet_score
    else:
        print_d('>>>残念でした')
        if shojikin <= 0:
            shojikin = 0
        print_d(f'掛け金{kakekin}円は没収です。現在所持金{shojikin}円')
        return shojikin , higet_score


# In[17]:


def sakebi(jumon_list , deme , yosou):
    #目的：叫びを判定して出目を変える
    #入力：叫び（内部）、呪文リスト、出目、予想数（外部）
    #処理：叫びがリスト内と一致すれば出目を予想数に合わせる、一致しなければそのまま
    #出力：出目
    jumon = input('Press Entar Kye')

    if jumon in jumon_list:
        deme = yosou
        print_d(f'>>>チートを使いました！\n出目が{yosou}に変化した')
        return deme
    else:
        return deme


# In[18]:


def count_call(MAX_COUNT , higet_score):
    print_d('-----------------------------------')
    print_d(f'～{higet_score[0]}回目の挑戦～(残り{MAX_COUNT - higet_score[0]}回)')


# In[58]:


def input_twice(shojikin , dice_list):
    #目的：ゲームの開始、予想して所持金からお金を掛ける
    #入力：予想数、掛け金（内部）　所持金（外部）
    #処理：予想数、掛け金をinputして所持金から掛け金を引く
    #出力：予想数、掛け金、所持金

    print_d(f'>>>どの数字が出るか予想せよ{dice_list}')
    yosou = input_yosou(dice_list)
    print_d(f'>>>いくら賭ける？ 所持金は{shojikin}円 ')
    print_d(f'0ならオールイン！')
    all_in_flag = False
    kakekin , all_in_flag = input_kakekin(shojikin , all_in_flag)
    shojikin = shojikin - kakekin
    if all_in_flag:
        print_d(f'>>>{kakekin}円でオールイン！　当たれば掛け金は60倍になります！')
    else:
        print_d(f'>>>{kakekin}円賭けました　残りの所持金は{shojikin}円')
    return shojikin , yosou , kakekin , all_in_flag


# In[42]:


def game_over_hantei(GOAL_SHOJIKIN , shojikin , GAME_continue_flag , player , MAX_COUNT , higet_score):
    #目的：所持金0になったらゲームを終わらせる
    #入力：所持金
    #処理：所持金が0かどうか確認。0ならゲームオーバーを表示、0でないなら続行
    #出力：ゲームオーバーの処理Flag = Falseかpass
    #GAME_continue_flag 2：ゲームクリア,  1：ゲーム続行,　0:ゲームオーバー　

    if GOAL_SHOJIKIN <= shojikin:
        print_d('>>>')
        print_d('###########所持金が100万円を突破した！###########')
        print_d(f'''
            おめでとう！ゲームクリア！
                        ～☆
              † < ﾔｯﾀｰ　　　　　　　† < ﾔｯﾀｰ
            ########################################
            ''')
        GAME_continue_flag = 2
        return GAME_continue_flag        
    elif 0 < shojikin:
        if MAX_COUNT <= higet_score[0]:
            print('\n>>>残念！挑戦回数が上限に達しました！')
            print_d(f'''
                    　  γ´￣￣￣￣￣￣￣￣￣￣￣￣￣￣｀ヽ
                  。〇 |　{player}はゆっくりしすぎた！  |
                †   　 ゝ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿,乂
            ###########GAME　OVER######################
            ''')
            GAME_continue_flag = 0
            return GAME_continue_flag
        else:
            GAME_continue_flag = 1
            return GAME_continue_flag
    elif shojikin <= 0:

        print(f'''
                  ＿人人人人人人人人人人人人＿
                  ＞ {player}は破産しました！＜
        † †  †     ￣^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^￣　†　†
        ###########GAME　OVER######################
        ''')
        GAME_continue_flag = 0
        return GAME_continue_flag


# In[78]:


def kakuchou_iriguti(shojikin , kakuchou_sikin , kakuchou_count):
    #目的：サイコロの拡張を選択
    #入力：拡張資金がたまっていたら拡張の選択肢を出す
    #処理：所持金と拡張資金を比較して以下なら「あと〇〇円で拡張可能」と表示
    #　　　以上なら拡張するかを選択させる
    #出力：以下ならメッセージを、以上なら拡張モジュールへ誘導

    if kakuchou_sikin < shojikin:
        next_laluchou = kakuchou_sikin_cal(kakuchou_count + 1)
        print_d(f'<<<{kakuchou_sikin}円払ってサイコロを拡張できます。拡張しますか？(次回の拡張は{next_laluchou}円)')
        x = input_d('0.はい\n1.いいえ')
        if x == '0' or x == '':
            print_d(f'>>>{kakuchou_sikin}円払うと{shojikin - kakuchou_sikin}円しか残らないけど良いかな？')
            z = input_d('0.はい\n1.いいえ')
            if z == '0' or x == '':
                kakuchou_flag = True
                return kakuchou_flag
            else:
                print_d('##何もしない##')
        else:
            print_d('##何もしない##')
    print_d(f'<<<{kakuchou_sikin}円を超えるとサイコロを拡張できます')
    input('Press Enter Key')


# In[22]:


def kakuchou(dice_list , shojikin , kakuchou_sikin , kakuchou_count):
    #目的：サイコロの拡張をする
    #入力：サイコロリスト、所持金、拡張回数（外部）
    #処理：拡張回数から算出した拡張資金を所持金から引く、サイコロリストに数字を追加する
    #出力：サイコロリスト、所持金、拡張回数
    shojikin = shojikin - kakuchou_sikin
    flag = True
    while flag:
        suji = input_d('追加する数字を入れてね：')
        #入力されたものが数字かを判定
        if suji.isdigit():
            suji = int(suji)
            dice_list.append(suji)
            flag = False
        else:
            print_d('数値を入力してください　もう一度入力してね:')
    print_d(f'>>>{suji}がサイコロリストに追加されました{dice_list}')
    kakuchou_count += 1
    return dice_list , shojikin , kakuchou_count


# In[23]:


def kakuchou_sikin_cal(kakuchou_count):
    #拡張資金の計算
    kakuchou_count += 1
    kakuchou_sikin = 200 * 5**(kakuchou_count - 1)
    kakuchou_count -= 1
    return kakuchou_sikin


# In[68]:


def Saikoro_Kakuchou_GAME():
    dice_list = [0, 1 , 2 , 3]
    shojikin = 100
    jumon_list = ["123"]
    kakuchou_count = 0 #何回目の拡張か
    MAX_COUNT = 10
    GOAL_SHOJIKIN = 1000000
    SUPER_PLAYER = 3
    higet_score = [0 , 0 , shojikin ] #連続挑戦回数[0]、一回で稼いだ最高額[1]、最高所持金[2]
    
    player = 'あなた'#名前入力式でも可
    print_d(f'''
    ###########サイコロ拡張ゲーム######################
    01.出る目を予想してお金を賭けよう
    02.予想が当たれば掛け金は6倍になって返ってきます
    03.オールイン（全額賭け）なら60倍です
    04.稼いだお金でサイコロの目を増やしてさらにお金を増やそう
    05.{MAX_COUNT}回以内に{GOAL_SHOJIKIN}円稼いだらゲームクリア
    ################################################''')
    GAME_continue_flag = 1 #2：ゲームクリア,  1：ゲーム続行,　0:ゲームオーバー　
    while GAME_continue_flag == 1:
        higet_score[0] += 1 #連続回数+1 
        count_call(MAX_COUNT , higet_score)
        shojikin , yosou , kakekin , all_in_flag = input_twice(shojikin , dice_list)
        deme = dice_roll(dice_list)
        deme = sakebi(jumon_list,deme,yosou )
        shojikin , higet_score =  hantei(yosou , deme , kakekin , shojikin , higet_score , all_in_flag)
 
   
        GAME_continue_flag = game_over_hantei(GOAL_SHOJIKIN , shojikin , GAME_continue_flag , player , MAX_COUNT , higet_score)
  
        if GAME_continue_flag == 1:
            
            kakuchou_sikin = kakuchou_sikin_cal(kakuchou_count)
            kakuchou_flag = False
            kakuchou_flag = kakuchou_iriguti(shojikin , kakuchou_sikin , kakuchou_count)
            if kakuchou_flag:
                dice_list , shojikin , kakuchou_count = kakuchou(dice_list , shojikin , kakuchou_sikin , kakuchou_count) 
        else:
            pass  
    print_d(f'～{player}の記録～')
    achievement_rate =  round(higet_score[2]/ GOAL_SHOJIKIN  * 100 , 2)
    print_d(f'今回のスコア：{higet_score[0]}回の挑戦で達成率は{achievement_rate}％でした')
    if GAME_continue_flag == 2 and higet_score[0] <= SUPER_PLAYER:
        print_d(f'''
        
        {SUPER_PLAYER}回以内の挑戦でクリアできた{player}は生粋のギャンブラー！！

                                          _n
                                       （　l　 　　_、_
                                         ＼ ＼　（ <_,`　）
                                           ヽ___￣￣　 ） 　　
                                              / 　 　/

        ''')
    input('Press Enter Key')
    
Saikoro_Kakuchou_GAME()