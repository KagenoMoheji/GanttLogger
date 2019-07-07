'''
●ログファイルを読み込んでガントチャート生成・出力
・ファイル名にタイムスタンプつけとく
'''
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from modules.Public import StrFormatter

'''
References:
    http://ailaby.com/matplotlib_fig/#id4_1
    https://qiita.com/fujiy/items/f738aa9d0bb7427e07a4#%E8%A7%A3%E6%B1%BA%E7%AD%96
    https://www.haya-programming.com/entry/2018/05/26/031355
    https://note.nkmk.me/python-list-common/
    https://github.com/spyder-ide/spyder/issues/5401
    https://note.nkmk.me/python-check-int-float/
    https://pythondatascience.plavox.info/numpy/%E6%95%B0%E5%AD%A6%E7%B3%BB%E3%81%AE%E9%96%A2%E6%95%B0
    https://yukun.info/python-file/
'''

class Plotter:
    uuid = "" # If empty, this variable is unused
    dirname = ""
    sec_interval = 1 # The minimum interval is value is 1 second
    filter_tab_list = []
    hide_filtered_tab_duration = False
    select_data = ["all"]
    strfmr = None
    def __init__(self, uuid=""):
        '''
        When arg "uuid" is empty, the mode is "plotter".
        -> Get data from current directory.
        When it is not empty, the mode is "alone" or "logger".
        -> Specify the output directory.
        '''
        self.strfmr = StrFormatter()
        if uuid:
            self.uuid = uuid
            self.dirname = "ganttlogger_logs/{}".format(uuid)
        else:
            self.dirname = os.getcwd()
        print(self.dirname)
        self.sec_interval = 1
        self.filter_tab_list = []
        self.hide_filtered_tab_duration = False
        self.select_data = ["all"]

    def start(self):
        '''
        ●標準入力で
        (1)出力モードの選択(filter_tab/set_interval)
        (2)出力モードに合わせた必須項目への回答
        ・set_interval -> デルタtの数値指定(単位は秒)
        ・fiter_tab -> 不要なタブ名(ログからコピペ)をまとめたテキストファイルの指定
        ・select_data -> 3つのデータをサブプロットでまとめて出力するか，選択したデータで独立のプロットを出力するか(例えば，"all"なら1つの出力に3つのサブプロットが入っているが，一方3つのデータを選択した入力なら3つの出力が出る)
        '''
        try:
            plot_types_labels = set(["set_interval", "filter_tab", "select_data"])
            plot_types_flags = {
                "set_interval": False,
                "filter_tab": False,
                "select_data": False
            }

            print(self.strfmr.get_colored_console_log("yellow",
                "===============[select plot types]==============="))
            print("""\
'set_interval': Set interval by seconds.
'filter_tab'  : Filter unnecessary tab texts in a text file before plotting.
'select_data' : Select whether you use all data to plot to an output or some data plot to each output. 
                Default - when you don't input in 'select_data' - is the former.''""")
            while True:
                print(self.strfmr.get_colored_console_log("yellow",
                    "Select plot types separated by ',',  or enter without input.: "), end="")
                plot_types = list(map(lambda s: s.strip(), (input().strip()).split(",")))
                if not plot_types[0]:
                    print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input."))
                    continue
                xor_plot_types = set(plot_types) ^ plot_types_labels
                if len(xor_plot_types) == 0 or \
                    all(x in plot_types_labels for x in xor_plot_types):
                    break
                else:
                    print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input."))
            # Update flags following 'plot_types'
            for plot_type in plot_types:
                plot_types_flags[plot_type] = True
            # Get arguments from stdin following 'plot_types_flags'
            if plot_types_flags["set_interval"]:
                print(self.strfmr.get_colored_console_log("yellow",
                    "-----------------[set_interval]-----------------"))
                print("There are a required setting.")
                while True:
                    print(self.strfmr.get_colored_console_log("yellow",
                        "Set the number of interval by seconds: "), end="")
                    self.sec_interval = input().strip()
                    if re.compile(r'^[0-9]+$').match(self.sec_interval):
                        break
                    else:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input.\n(Example)If you want set 2 seconds for the interval, input '2'."))
            if plot_types_flags["filter_tab"]:
                print(self.strfmr.get_colored_console_log("yellow",
                    "-----------------[filter_tab]-----------------"))
                print("There are two required settings.")
                while True:
                    try:
                        print(self.strfmr.get_colored_console_log("yellow",
                        "(1)Input a file name written a list of tab text you want to filter.: "), end="")
                        txtname = "{dirname}/{filename}".format(dirname=self.dirname, filename=input().strip())
                        with open(txtname, "r", encoding="utf-8") as f:
                            self.filter_tab_list = f.read().split("\n")
                            break
                    except FileNotFoundError:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: File not found."))
                while True:
                    print(self.strfmr.get_colored_console_log("yellow",
                        "(2)Do you want to hide mouse and keyboard graph depictions of the duration filtered regarding tab text?(Y/n) : "), end="")
                    st_input = input().strip()
                    if st_input == "Y":
                        self.hide_filtered_tab_duration = True
                        break
                    elif st_input == "n":
                        # self.hide_filtered_tab_duration = False
                        break
                    print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input."))
            if plot_types_flags["select_data"]:
                print(self.strfmr.get_colored_console_log("yellow",
                    "-----------------[select_data]-----------------"))
                while True:
                    print(self.strfmr.get_colored_console_log("yellow",
                        "Select 'all' or list separated by ',' with some csv file names like 'active_tab'.: "), end="")
                    print("There are a required setting.")
                    input_select_data = list(map(lambda s: s.strip(), (input().strip()).split(",")))
                    if not input_select_data[0]:
                        # No need to update self.select_data
                        break
                    elif "all" in input_select_data: 
                        if len(input_select_data) == 1:
                            # No need to update self.select_data
                            break
                        else:
                            print(self.strfmr.get_colored_console_log("red",
                                "Error: Too many select despite 'all'."))
                            continue
                    else:
                        select_data_labels = set(["active_tab", "mouse", "keyboard"])
                        xor_select_data = set(input_select_data) ^ select_data_labels
                        if len(xor_select_data) == 0 or \
                            all(x in select_data_labels for x in xor_select_data):
                            self.select_data = input_select_data
                            break
                        else:
                            print(self.strfmr.get_colored_console_log("red",
                                "Error: There are some Invalid names of csv files."))

            print("sec_interval: {}".format(self.sec_interval))
            print(self.filter_tab_list)
            print("select_data: {}".format(self.select_data))
            if self.select_data[0] == "all":
                self.run()
            else:
                self.run_each()
        except KeyboardInterrupt:
            print("Exit")
            exit()

    def run(self): # plot(self)
        '''
        ●get_activetab，get_mouse，get_keyboardの全部を行う．
        ●plotで3つのサブプロットを用意するとして，どうやってサブプロットを
        上記3つの関数に渡すのか？？？？
        ●上記3つの関数でファイル読み込み・データ加工したリストを用意して，ここで
        サブプロットにプロット？

        References:
            http://pineplanter.moo.jp/non-it-salaryman/2018/03/23/python-2axis-graph/
            https://qiita.com/supersaiakujin/items/e2ee4019adefce08e381
        '''
        print("Run, Plotter!")
        self.get_activetab()

    def run_each(self): # plot_each(self)
        '''
        ●run()が3つのサブプロットで1つのファイル出力をするのに対し，run_each()は
        1つのプロットで1つのファイル出力をする，つまり独立した出力をする関数．
        ●self.select_dataに従って，get_activetab，get_mouse，get_keyboardのいずれかを実行して各々の独立ファイルを出力．
        ●各出力ファイル名に日時を追加する．
        '''
        print("Run, Plotter-Each!")

    def get_activetab(self):
        '''
        ファイル読み込み・データ加工をここで行い，縦軸と横軸のリストを返す
        
        References:

        '''
        try:
            df = pd.read_csv("{dirname}/active_tab.csv".format(dirname=self.dirname), sep=",", encoding="utf-8")
            if len(self.filter_tab_list) > 0:
                print("Fitering tabs done!")
            print(list(df.columns))
            print(df)
        except FileNotFoundError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: 'active_tab.csv' not found."))
            exit()
    
    def get_mouse(self):
        '''
        ●get_activetab()で削除したタブの期間のデータの削除も必要ありそうかな．
        これやるのはget_activetab()を行った場合のみにするか．
        でもグラフでどう表現する？データの削除というより0埋め？でも0だったとグラフで示すのもな…
        ●None埋めとかにして，グラフプロット前にデータをNone期間で分割していってそれぞれでグラフプロットして後から重ねていくとか？
        http://natsutan.hatenablog.com/entry/20110713/1310513258
        というか普通に同じとこに，同じ色でプロットしていけばよくね？でも空白期間の表現できるのかな？
        ●(Pandasで)NaN埋めしていけばPandasとmatplotlibの組み合わせで途切れさせられる？
        ちなみにcsvで部分セルを空にしてPandasに読み込んでもNaNにはなった．これは関係ない．
        https://qiita.com/damyarou/items/19f19658b618fd05b3b6
        https://teratail.com/questions/106411
        というかnp.nanでいけるっぽい？
        https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/nan_test.html
        ●それともget_activetab()で除去した部分のマークをしないようにNone埋めする？
        https://stackoverflow.com/questions/14399689/matplotlib-drawing-lines-between-points-ignoring-missing-data
        ●その他よくわからんけど参考になりそうな…
        https://codeday.me/jp/qa/20190318/374532.html

        ※ただし，self.hide_filtered_tab_duration=Trueの場合にNaN・None埋めする．Falseならmouse・keyboardはactive_tabでフィルタリングされた期間もグラフ描写する．
        '''
        try:
            df = pd.read_csv("{dirname}/mouse.csv".format(dirname=self.dirname), sep=",", encoding="utf-8")
        except FileNotFoundError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: 'mouse.csv' not found."))
            exit()

    def get_keyboard(self):
        '''
        ●get_activetab()で削除したタブの期間のデータの削除も必要ありそうかな．
        これやるのはget_activetab()を行った場合のみにするか．
        でもグラフでどう表現する？データの削除というより0埋め？でも0だったとグラフで示すのもな…
        ●None埋めとかにして，グラフプロット前にデータをNone期間で分割していってそれぞれでグラフプロットして後から重ねていくとか？
        http://natsutan.hatenablog.com/entry/20110713/1310513258
        というか普通に同じとこに，同じ色でプロットしていけばよくね？でも空白期間の表現できるのかな？
        ●(Pandasで)NaN埋めしていけばPandasとmatplotlibの組み合わせで途切れさせられる？
        ちなみにcsvで部分セルを空にしてPandasに読み込んでもNaNにはなった．これは関係ない．
        https://qiita.com/damyarou/items/19f19658b618fd05b3b6
        https://teratail.com/questions/106411
        というかnp.nanでいけるっぽい？
        https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/nan_test.html
        ●それともget_activetab()で除去した部分のマークをしないようにNone埋めする？
        https://stackoverflow.com/questions/14399689/matplotlib-drawing-lines-between-points-ignoring-missing-data
        ●その他よくわからんけど参考になりそうな…
        https://codeday.me/jp/qa/20190318/374532.html

        ※ただし，self.hide_filtered_tab_duration=Trueの場合にNaN・None埋めする．Falseならmouse・keyboardはactive_tabでフィルタリングされた期間もグラフ描写する．
        '''
        try:
            df = pd.read_csv("{dirname}/keyboard.csv".format(dirname=self.dirname), sep=",", encoding="utf-8")
        except FileNotFoundError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: 'keyboard.csv' not found."))
            exit()