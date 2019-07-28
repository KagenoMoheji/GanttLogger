# GanttLogger
CLI that Monitors active-tab, mouse-distance and keyboard-count, Logs and Plots various graphs.  
(PyPI)[https://pypi.org/project/ganttlogger/](https://pypi.org/project/ganttlogger/)
- [README - 日本語版](https://github.com/KagenoMoheji/GanttLogger/blob/master/README-ja.md)

***
## <span id="0">AGENDA</span>
- [Requirements(Test Completing)](#1)
- [Get Started](#2)
    - [Install](#2-1)
        - [Windows](#2-1-1)
        - [MacOS](#2-1-2)
    - [Quick Start](#2-2)
    - [Structure of outputed folder "ganttlogger_logs"](#2-3)
- [Command Options](#3)
    - [alone](#a)
    - [observer](#o)
    - [logger](#l)
    - [plotter](#p)
    - [displayer](#d)
    - [merger](#m)
- [Issues](#4)
- [In the future...](#5)
- [License](#6)


***

## <span id="1">Requirements(Test Completing)</span> [▲](#0)
- OS
    - Windows10(64bit)
    - MacOS Sierra ~
- Python
    - 3.6.x
    - 3.7.x

## <span id="2">Get Started</span> [▲](#0)
### <span id="2-1">Install</span> [▲](#0)
- <span id="2-1-1">**Windows**</span>  
There are two ways to install.
    - Install with `pip`.
        1. Install python3.
        2. Install with `pip` like below.
            ```
            > python -m pip install ganttlogger
            ```
    - Install by downloading `ganttlogger-exe-x86_64-<version>.zip`.
        - Read README for executable file.
            - [In English](https://github.com/KagenoMoheji/GanttLogger/blob/master/exe/README.md#w)
            - [日本語版](https://github.com/KagenoMoheji/GanttLogger/blob/master/exe/README-ja.md#w)
- <span id="2-1-2">**MacOS**</span>
There are two ways to install.
    - Install with `pip`.
        1. Install python3 and pip3.
        2. Installl with `pip3` like below.
            ```
            $ pip3 install ganttlogger
            ```
        3. If you can't install with `pip3`, download `ganttlogger-<version>.tar.gz` from [Releases](https://github.com/KagenoMoheji/GanttLogger/releases) or [PyPI](https://pypi.org/project/ganttlogger/), extract it, and run install command below.
            ```
            $ python3 setup.py install
            ```
        4. Add "Terminal.app" to "Accessibility" in "Security & Privacy" in system environment settings to allow Terminal.app to get inputs from keyboard.
    - Install by downloading `ganttlogger-exe-macos-<version>.zip`.
        - Read README for executable file.
            - [In English](https://github.com/KagenoMoheji/GanttLogger/blob/master/exe/README.md#m)
            - [日本語版](https://github.com/KagenoMoheji/GanttLogger/blob/master/exe/README-ja.md#m)

### <span id="2-2">Quick Start</span> [▲](#0)
1. Run as "Alone"(Run both monitoring and logging in a PC).
    ```
    $ ganttlogger
    ```
2. Exit CLI(running as "Alone" or "Observer") **by hitting keys `1`+`0`+`z`+`m` continuously (mashing keys, not long pressing simultaneously)**.
3. Check a created folder `ganttlogger_logs` in current directory.  
When you want a guide about the outputed folder, refer [Structure of outputed folder "ganttlogger_logs"](#2-3).
- If you get the following problems
    - `ModuleNotFoundError: No module named 'win32gui'` on Windows.
        - Try uninstall and install `pywin32`.
            ```
            > python -m pip uninstall pywin32 & python -m pip install pywin32
            ```
    - Appear warning below when plotting graphs.
        ```
        /usr/local/lib/python3.7/site-packages/matplotlib/backends/backend_agg.py:211: RuntimeWarning: Glyph 128266 missing from current font.
        font.set_text(s, 0.0, flags=flags)
        /usr/local/lib/python3.7/site-packages/matplotlib/backends/backend_agg.py:180: RuntimeWarning: Glyph 128266 missing from current font.
        font.set_text(s, 0, flags=flags)
        ```
        - No problem. You can ignore that.

### <span id="2-3">Structure of outputed folder "ganttlogger_logs"</span> [▲](#0)
```
ganttlogger_logs
├ (ID)
    ├ active_tab.log
    ├ mouse.log
    ├ keyboard.log
    └ graphs
        ├ output_(date)_all.pkl
        ├ output_(date)_all.png
        ...
├ (ID)
    ├ active_tab.log
    ...
...
```
- `(ID)`: A unique ID generated by ganttlogger.
- `~.log`: log data.
- `~.pkl`: Dynamic graph data.
- `~.png`: Static graph data(image).

## <span id="3">Command Options</span> [▲](#0)
```
usage: ganttlogger [--observer] [--logger] [--uuid <UUID>] [--help] [--plotter] [--withplot] [--displayer] [--merger]

This CLI will do Observing active-tab, mouse, keyboard,
and Logging them,
and Plotting graphs (active-tab=ganttchart, mouse=line, keyboard=bar).
If you don't set any option, this work both of 'observer' and 'logger'.

optional arguments:
  -h, --help            show this help message and exit
  -o, --observer        The role of this PC is only observing action.
  -l, --logger          The role of this PC is only logging and plotting. You must also set '--uuid'.
  -u UUID, --uuid UUID  When you set '--logger', you must also set this by being informed from 'observer' PC.
  -p, --plotter         Use this option if you want other outputs by a log in the current directory after getting one and a graph.
  --withplot            Use this option when you want to get a graph after running 'Alone'.
  -d, --displayer       Use this option when you want to look a graph from a '.pkl' file.
  -m, --merger          Use this option when you want to merge all logs in folders in 'ganttlogger_logs'.
```
- <span id="o"></span><span id="l"></span>**`--observer` and `--logger` don't work because they're not implemented yet.**
- <span id="a"></span>Run `ganttlogger` without any options if you run CLI as `alone` - both of `observer` and `logger/plotter` -.
    - Add an option `--withplot`, if you want graphs along with logs.  
    Then, CLI will output a graph like No.1 of [Graph Examples](#graphs)
- <span id="p"></span>Change to current directory of logs and add an option `--plotter`, if you want to get other graphs from logs.
    - Then, you'll be required some settings to decide formats to plot graphs.
    - First,  
        ```
        Select plot types separated by ',',  or enter without input.:
        ```
        Select keywords(you can combine) from (set_interval | filter_tab | select_data | xaxis_type | xlim_range).
    - When select `set_interval`, you'll be required a setting.
        ```
        Set the number of interval by seconds:
        ```
        Example graph when set "5" is No.2 of [Graph Examples](#graphs).
    - When select `filter_tab`, you'll be required two settings.
        ```
        (1)Input a file name written a list of tab text you want to filter.:

        (2)Do you want to hide mouse and keyboard graph depictions of the duration filtered regarding tab text?(Y/n) :
        ```
    - When select `select_data`, you'll be required a setting.
        ```
        Select 'all' or names separated by ',' from ('active_tab'|'mouse'|'keyboard'|'mouse-keyboard').:
        ```
        Example graphs when set "active_tab" and "keyboard" are No.5 and No.6 of [Graph Examples](#graphs).
    - When select `xaxis_type`, you'll be required two settings.
        ```
        (1)Select x-axis type for ActiveTab from whether 'active-start' or number of the interval by seconds:

        (2)Select x-axis type for Mouse or Keyboard from whether 'active-start' or number of the interval by seconds:
        ```
        Example graphs when set "(1)active-start(2)active-start" and "(1)15(2)15" are No.3 and No.4 of [Graph Examples](#graphs).
    - When select `xlim_range`, you'll be required two settings.
        ```
        (1)Input start time of graph xlim in the format 'YYYY/mm/dd HH:MM:SS'.:
        (2)Input end time of graph xlim in the format 'YYYY/mm/dd HH:MM:SS'.:
        ```
        Then, you can get a graph during the specified time zone.
- <span id="d"></span>Add an option `--displayer` if you want watch dynamic graph with generated `~.pkl`.
    - Then, you'll be required a setting.
        ```
        Input file name of '.pkl':
        ```
- <span id="m"></span>Add an option `--merger` if you want to merge all logs in folders(these names is ID) in "ganttlogger_logs".
    - Then, you'll be required a setting.
        ```
        Select 'all' or names separated by ',' from ('active_tab'|'mouse'|'keyboard').:
        ```
    - After running, you'll get an outputted folder "merged_\<datetime>".

### <span id="graphs">Graph Examples</span>
- All graphs were plotted **from same logs**.
![Graph Examples](promo/graphs.PNG)

## <span id="4">Issues.</span> [▲](#0)
- When long running on Mac, this cli makes PC out of memory.  
The reason may be in a dependent module `pyobjc`, but I don't know how to release memory.  
[Memory leak pyobjc - stack overflow](https://stackoverflow.com/questions/40720149/memory-leak-pyobjc)
- Like No.2 in [Graph Examples](#graphs), a part of ganttchart disappear from graph when setting `set_interval` more than 2.  
I'm investigating the causes...
- In `Observer.py`, sometimes thread error like below occurs on Windows. I'm investigating the causes...
    ```
    Exception in thread Thread-1:
    Traceback (most recent call last):
    ...
    ```
- Sometimes an error below occurs when plotting from a short term logs.
    ```
    Traceback (most recent call last):
        File "/usr/local/bin/ganttlogger", line 10, in <module>
            sys.exit(main())
        File "/usr/local/lib/python3.7/site-packages/ganttlogger/app.py", line 42, in main
            plotter.start()
        File "/usr/local/lib/python3.7/site-packages/ganttlogger/modules/Plotter.py", line 248, in start
            self.run()
        File "/usr/local/lib/python3.7/site-packages/ganttlogger/modules/Plotter.py", line 272, in run
            self.get_mouse()
        File "/usr/local/lib/python3.7/site-packages/ganttlogger/modules/Plotter.py", line 691, in get_mouse
            current_time = self.plot_active_tab[0][0].replace(microsecond=0)
    IndexError: index 0 is out of bounds for axis 0 with size 0
    ```
- Try implementing flushing stdin buffering. But it's difficury, so I want advices or pull-requests.

## <span id="5">In the future...</span> [▲](#0)
- Implement mode remote '--observer' and '--logger'.

## <span id="6">License</span> [▲](#0)
MIT LICENSE.