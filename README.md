pyrs
======================
pyrsは双葉電子工業（株）のコマンド方式サーボである[RSシリーズ][futaba]を制御するPython Scriptです。 

[futaba]: http://www.futaba.co.jp/robot/command_type_servos/index.html

動作確認環境
------
Python:  
2.6.6  

OS:  
Windows 7 64bit / 32bit  
Ubuntu 10.04 LTS / 12.04 LTS 32bit  

Servo:  
RS301, 302, 303, 405   

Serial:  
 [RSC-U485](:http://www.futaba.co.jp/robot/rsc/index.html)  

各コマンドは以下の[取り扱い説明書](:http://www.futaba.co.jp/robot/download/manuals.html)に従っています。   
RS405CB/RS406CB取扱説明書（ver.1.01）  
RS301CR/RS302CD取扱説明書（ver.1.14）  
RS303MR/RS304MD取扱説明書（ver.1.13）  
 
使い方
------
###1. pySerialをインストールする###
pyrsは[pySerial](:http://pyserial.sourceforge.net/)を使用してシリアル通信を行なっています。  
pySerialがインストールされていない場合は、インストールしてから実行して下さい。  

###2. Python Shellからサーボを動かしてみる###
Python Shellからサーボモータ（ID :1）を動かしてみます  
'COM1'の部分は自分の環境に合わせてポートを設定してください  
```pyton  
import pyrs  
import time  
rs = pyrs.Rs()  
rs.open_port('COM1', 115200, 1 )   
rs.torque_on(1, 1)  
rs.target_position(1, 900, 200)
time.sleep(1)  
print rs.get_data(1, 'angle')
time.sleep(1)  
rs.torque_on(1, 0)  
rs.close_port()  
```  
以上のように簡単にサーボモータを制御することができます。  

###3. メソッドの使い方###

    def open_port(port, baudrate, timeout)
シリアルポートを開きます  
 ・ `port` :  
    ポートの番号の指定。'COM1'や'/tty/usb0'のように指定  
 ・   `baudrate` :  
    ボードレートの指定。サーボと同じボードレートを指定して下さい   
 ・   `timeout` :  
    読み取り時のタイムアウト設定  
    None:読み取れるまで待ちます
    0:非ブロッキングモード（読み取り時にすぐ戻ります） 
    x:x [sec]待ちます  
  ・  `return` :    
    戻り値なし　　
  
    def close_port()
シリアルポートを閉じます  
  ・  `return` :    
    戻り値なし　
 
    def set_port(baudrate, timeout)
シリアルポートを再設定します  
 ・  `baudrate` :  
    ボードレートの指定。サーボと同じボードレートを指定して下さい   
 ・  `timeout` :  
    読み取り時のタイムアウト設定  
    None:読み取れるまで待ちます
    0:非ブロッキングモード（読み取り時にすぐ戻ります） 
    x:x [sec]待ちます

    def torqur_on(id, mode)
サーボのトルク設定を行います  
 ・  `id` :  
    設定を行うサーボモータのIDを指定します。IDは1~127の間で指定する必要があります  
 ・  `mode` :  
    トルク保持モードを選びます  
    0:トルクをオフにします
    1:トルクをオンにします 
    2:ブレーキモードにします  
 ・  `return` :    
    (id, 'ACK'):正常に命令が伝達ています  
    (id, 'NACK)':コマンドが正しく設定されていません（通常の利用では見ることはないでしょう）  
    (id, 'unReadable'):通信環境に以上があります。多くの場合サーボモータの電源が切れているなどの原因が考えられます 

    def target_position(id, position, time)
サーボの移動命令を出します    
 ・  `id` :  
    設定を行うサーボモータのIDを指定します。IDは1~127の間で指定する必要があります   
 ・  `position` :  
    移動位置を指定します。-1500～1500 [0.1 deg]の間で指定する必要があります    
・  `time` :  
    移動時間を指定します。0~16383 [msec]の間で指定します。0は最大速度で移動になります  
 ・  `return` :    
    (id, 'ACK'):正常に命令が伝達ています  
    (id, 'NACK)':コマンドが正しく設定されていません（通常の利用では見ることはないでしょう）  
    (id, 'unReadable'):通信環境に以上があります。多くの場合サーボモータの電源が切れているなどの原因が考えられます  

    def multi_torque_on(servi_data)
サーボのトルク設定を複数個同時に行います    
 ・  `servo_data` :    
    リスト型のデータで[[id1, mode1], [id2, mode2].....]のように設定します   
 ・  `return`:  
    'multi_torque_on: + str(servo_data)'が返されます
    
    def multi_target_position(servo_data)
サーボの移動命令を複数個同時に行います  
 ・  `servo_data` :    
    リスト型のデータで[[id1, position1, time1], [id2, position2, time2].....]のように設定します   
 ・  `return`:  
    'multi_torque_on: + str(servo_data)'が返されます

    def get_data(id, mode)  
サーボモータのセンサデータを取得します  
 ・  `id` :  
    設定を行うサーボモータのIDを指定します。IDは1~127の間で指定する必要があります      
・  `mode` :  
    リターンさせるセンサ値を設定します。  
ただしサーボの仕様上、取得するセンサ値を選択しても全てのセンサ値がサーボから返されます。
モード選択はそれをフィルタリングしているに過ぎません。  
    'all', すべてのセンサ値を返します    
    'angle', 現在位置 [0.1 deg]を返します  
    'time', 現在時間 [0.1 sec]を返します。現在時間はサーボが指令を受信し、移動を開始してからの経過時間です   
    'speed', 現在スピード [deg / sec]を返します。現在の回転スピードを取得できますが、この値は目安です。  
    'load', 現在負荷 [mA]を返します。サーボに供給されている電流を返しますが、この値は目安です。    
    'timepreture', 現在温度 [degree celsius]を返します。この値はセンサの個体差により±3 [degree celsius] 程度の誤差があります     
    'voltage', 現在電圧 [10 mV]を返します。この値はセンサの個体差により±0.3 [V]程度の誤差があります    
    'list', 選択出来るモード一覧を返します（センサ値の返答はありません。モード確認用です）  
 ・  `return` :  
    list:使用出来るモード一覧を返されます  
    (id, angle, time, speed, load, tempreture, voltage):全てのセンサ値を返されます    
    (id, sens_value):IDと選択したモードに対応するセンサ値を返されます  

    def servo_reset(id)
サーボモータをリセットします  
 ・  `id` :    
    設定を行うサーボモータのIDを指定します。IDは1~127の間で指定する必要があります  
 ・  `return` :    
    (id, 'ACK'):正常に命令が伝達ています  
    (id, 'NACK)':コマンドが正しく設定されていません（通常の利用では見ることはないでしょう）  
    (id, 'unReadable'):通信環境に以上があります。多くの場合サーボモータの電源が切れているなどの原因が考えられます  

    def set_torque_limit(id, limit)
トルクリミットを設定します    
 ・  `id` :  
    設定を行うサーボモータのIDを指定します。IDは1~127の間で指定する必要があります  
 ・  `limit` :  
    サーボモータの規格に最大トルクを100 [%]とすると、1[%]単位で設定できます  
 ・  `return` :    
    (id, 'ACK'):正常に命令が伝達ています  
    (id, 'NACK)':コマンドが正しく設定されていません（通常の利用では見ることはないでしょう）  
    (id, 'unReadable'):通信環境に以上があります。多くの場合サーボモータの電源が切れているなどの原因が考えられます 
  
    def set_damper(id, damper)
ダンパを設定します  
 ・  `id` :  
    設定を行うサーボモータのIDを指定します。IDは1~127の間で指定する必要があります  
 ・  `damper` :  
    ハンチングを起こりにくくする効果があります。0～255の間で設定して下さい  
 ・  `return` :    
    (id, 'ACK'):正常に命令が伝達ています  
    (id, 'NACK)':コマンドが正しく設定されていません（通常の利用では見ることはないでしょう）  
    (id, 'unReadable'):通信環境に以上があります。多くの場合サーボモータの電源が切れているなどの原因が考えられます  

    def set_compliance(id, cwcm, ccwcm, cwcs, ccwcs, punch)  　
コンプライアンスマージンなどを設定します  
 ・  `id` :  
    設定を行うサーボモータのIDを指定します。IDは1~127の間で指定する必要があります  
 ・  `cwcm` :CW Compliance Margin  
    CW（時計回り）方向のサーボの停止位置[0.1 degree]の許容範囲を設定します。0～255の間で設定して下さい  
 ・  `ccwcm` :CCW Compliance Margin  
    CCW（反時計回り）サーボの停止位置[0.1 degree]の許容範囲を設定します。0～255の間で設定して下さい  
 ・  `cwcs` :CW Compliance Slope  
    CW（時計回り）方向の現在位置と目標位置の誤差修正トルクの設定。0～255の間で設定して下さい  
 ・  `ccwcs` :CCW Compliance Slope  
    CCW（反時計回り）方向の現在位置と目標位置の誤差修正トルクの設定。0～255の間で設定して下さい  
 ・  `punch` :    
    モータ駆動時の最小電流を設定できます。設定値の単位は最大トルクの0.001%で、0～10000の間で設定して下さい  
 ・  `return` :    
    (id, 'ACK'):正常に命令が伝達ています  
    (id, 'NACK)':コマンドが正しく設定されていません（通常の利用では見ることはないでしょう）  
    (id, 'unReadable'):通信環境に以上があります。多くの場合サーボモータの電源が切れているなどの原因が考えられます

ライセンス
----------
Copyright &copy; 2012 Hiroaki Matsuda  
Licensed under the [Apache License, Version 2.0][Apache]  
Distributed under the [MIT License][mit].  
Dual licensed under the [MIT license][MIT] and [GPL license][GPL].  
 
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
[MIT]: http://www.opensource.org/licenses/mit-license.php
[GPL]: http://www.gnu.org/licenses/gpl.html