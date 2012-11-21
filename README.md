pyrs
======================
pyrs�͑o�t�d�q�H�Ɓi���j�̃R�}���h��T�[�{�ł���[RS�V���[�Y][futaba]�𐧌䂷��Python Script�ł��B 

[futaba]: http://www.futaba.co.jp/robot/command_type_servos/index.html

����m�F��
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

�e�R�}���h�͈ȉ���[��舵������](:http://www.futaba.co.jp/robot/download/manuals.html)�ɏ]��Ă��܂��B   
RS405CB/RS406CB�戵�����iver.1.01�j  
RS301CR/RS302CD�戵�����iver.1.14�j  
RS303MR/RS304MD�戵�����iver.1.13�j  
 
�g����
------
###1. pySerial��C���X�g�[������###
pyrs��[pySerial](:http://pyserial.sourceforge.net/)��g�p���ăV���A���ʐM��s�Ȃ�Ă��܂��B  
pySerial���C���X�g�[������Ă��Ȃ��ꍇ�́A�C���X�g�[�����Ă����s���ĉ������B  

###2. Python Shell����T�[�{�𓮂����Ă݂�###
Python Shell����T�[�{���[�^�iID :1�j�𓮂����Ă݂܂�  
'COM1'�̕����͎����̊��ɍ��킹�ă|�[�g��ݒ肵�Ă�������  
```python  
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
�ȏ�̂悤�ɊȒP�ɃT�[�{���[�^�𐧌䂷�邱�Ƃ��ł��܂��B  

###3. ���\�b�h�̎g����###

    def open_port(port, baudrate, timeout)
�V���A���|�[�g��J���܂�  
 �E `port` :  
    �|�[�g�̔ԍ��̎w��B'COM1'��'/tty/usb0'�̂悤�Ɏw��  
 �E   `baudrate` :  
    �{�[�h���[�g�̎w��B�T�[�{�Ɠ����{�[�h���[�g��w�肵�ĉ�����   
 �E   `timeout` :  
    �ǂݎ�莞�̃^�C���A�E�g�ݒ�  
    None:�ǂݎ���܂ő҂��܂�
    0:��u���b�L���O���[�h�i�ǂݎ�莞�ɂ����߂�܂��j 
    x:x [sec]�҂��܂�  
  �E  `return` :    
    �߂�l�Ȃ��@�@
  
    def close_port()
�V���A���|�[�g����܂�  
  �E  `return` :    
    �߂�l�Ȃ��@
 
    def set_port(baudrate, timeout)
�V���A���|�[�g��Đݒ肵�܂�  
 �E  `baudrate` :  
    �{�[�h���[�g�̎w��B�T�[�{�Ɠ����{�[�h���[�g��w�肵�ĉ�����   
 �E  `timeout` :  
    �ǂݎ�莞�̃^�C���A�E�g�ݒ�  
    None:�ǂݎ���܂ő҂��܂�
    0:��u���b�L���O���[�h�i�ǂݎ�莞�ɂ����߂�܂��j 
    x:x [sec]�҂��܂�

    def torqur_on(id, mode)
�T�[�{�̃g���N�ݒ��s���܂�  
 �E  `id` :  
    �ݒ��s���T�[�{���[�^��ID��w�肵�܂��BID��1~127�̊ԂŎw�肷��K�v������܂�  
 �E  `mode` :  
    �g���N�ێ����[�h��I�т܂�  
    0:�g���N��I�t�ɂ��܂�
    1:�g���N��I���ɂ��܂� 
    2:�u���[�L���[�h�ɂ��܂�  
 �E  `return` :    
    (id, 'ACK'):����ɖ��߂��`�B�Ă��܂�  
    (id, 'NACK)':�R�}���h���������ݒ肳��Ă��܂���i�ʏ�̗��p�ł͌��邱�Ƃ͂Ȃ��ł��傤�j  
    (id, 'unReadable'):�ʐM���Ɉȏオ����܂��B�����̏ꍇ�T�[�{���[�^�̓d�����؂�Ă���Ȃǂ̌���l�����܂� 

    def target_position(id, position, time)
�T�[�{�̈ړ����߂�o���܂�    
 �E  `id` :  
    �ݒ��s���T�[�{���[�^��ID��w�肵�܂��BID��1~127�̊ԂŎw�肷��K�v������܂�   
 �E  `position` :  
    �ړ��ʒu��w�肵�܂��B-1500�`1500 [0.1 deg]�̊ԂŎw�肷��K�v������܂�    
�E  `time` :  
    �ړ����Ԃ�w�肵�܂��B0~16383 [msec]�̊ԂŎw�肵�܂��B0�͍ő呬�x�ňړ��ɂȂ�܂�  
 �E  `return` :    
    (id, 'ACK'):����ɖ��߂��`�B�Ă��܂�  
    (id, 'NACK)':�R�}���h���������ݒ肳��Ă��܂���i�ʏ�̗��p�ł͌��邱�Ƃ͂Ȃ��ł��傤�j  
    (id, 'unReadable'):�ʐM���Ɉȏオ����܂��B�����̏ꍇ�T�[�{���[�^�̓d�����؂�Ă���Ȃǂ̌���l�����܂�  

    def multi_torque_on(servi_data)
�T�[�{�̃g���N�ݒ�𕡐������ɍs���܂�    
 �E  `servo_data` :    
    ���X�g�^�̃f�[�^��[[id1, mode1], [id2, mode2].....]�̂悤�ɐݒ肵�܂�   
 �E  `return`:  
    'multi_torque_on: + str(servo_data)'���Ԃ���܂�
    
    def multi_target_position(servo_data)
�T�[�{�̈ړ����߂𕡐������ɍs���܂�  
 �E  `servo_data` :    
    ���X�g�^�̃f�[�^��[[id1, position1, time1], [id2, position2, time2].....]�̂悤�ɐݒ肵�܂�   
 �E  `return`:  
    'multi_torque_on: + str(servo_data)'���Ԃ���܂�

    def get_data(id, mode)  
�T�[�{���[�^�̃Z���T�f�[�^��擾���܂�  
 �E  `id` :  
    �ݒ��s���T�[�{���[�^��ID��w�肵�܂��BID��1~127�̊ԂŎw�肷��K�v������܂�      
�E  `mode` :  
    ���^�[��������Z���T�l��ݒ肵�܂��B  
�������T�[�{�̎d�l��A�擾����Z���T�l��I��Ă�S�ẴZ���T�l���T�[�{����Ԃ���܂��B
���[�h�I��͂����t�B���^�����O���Ă���ɉ߂��܂���B  
    'all', ���ׂẴZ���T�l��Ԃ��܂�    
    'angle', ���݈ʒu [0.1 deg]��Ԃ��܂�  
    'time', ���ݎ��� [0.1 sec]��Ԃ��܂��B���ݎ��Ԃ̓T�[�{���w�߂��M���A�ړ���J�n���Ă���̌o�ߎ��Ԃł�   
    'speed', ���݃X�s�[�h [deg / sec]��Ԃ��܂��B���݂̉�]�X�s�[�h��擾�ł��܂����A���̒l�͖ڈ�ł��B  
    'load', ���ݕ��� [mA]��Ԃ��܂��B�T�[�{�ɋ�������Ă���d����Ԃ��܂����A���̒l�͖ڈ�ł��B    
    'timepreture', ���݉��x [degree celsius]��Ԃ��܂��B���̒l�̓Z���T�̌̍��ɂ��}3 [degree celsius] ��x�̌덷������܂�     
    'voltage', ���ݓd�� [10 mV]��Ԃ��܂��B���̒l�̓Z���T�̌̍��ɂ��}0.3 [V]��x�̌덷������܂�    
    'list', �I��o���郂�[�h�ꗗ��Ԃ��܂��i�Z���T�l�̕ԓ��͂���܂���B���[�h�m�F�p�ł��j  
 �E  `return` :  
    list:�g�p�o���郂�[�h�ꗗ��Ԃ���܂�  
    (id, angle, time, speed, load, tempreture, voltage):�S�ẴZ���T�l��Ԃ���܂�    
    (id, sens_value):ID�ƑI������[�h�ɑΉ�����Z���T�l��Ԃ���܂�  

    def servo_reset(id)
�T�[�{���[�^��Z�b�g���܂�  
 �E  `id` :    
    �ݒ��s���T�[�{���[�^��ID��w�肵�܂��BID��1~127�̊ԂŎw�肷��K�v������܂�  
 �E  `return` :    
    (id, 'ACK'):����ɖ��߂��`�B�Ă��܂�  
    (id, 'NACK)':�R�}���h���������ݒ肳��Ă��܂���i�ʏ�̗��p�ł͌��邱�Ƃ͂Ȃ��ł��傤�j  
    (id, 'unReadable'):�ʐM���Ɉȏオ����܂��B�����̏ꍇ�T�[�{���[�^�̓d�����؂�Ă���Ȃǂ̌���l�����܂�  

    def set_torque_limit(id, limit)
�g���N���~�b�g��ݒ肵�܂�    
 �E  `id` :  
    �ݒ��s���T�[�{���[�^��ID��w�肵�܂��BID��1~127�̊ԂŎw�肷��K�v������܂�  
 �E  `limit` :  
    �T�[�{���[�^�̋K�i�ɍő�g���N��100 [%]�Ƃ���ƁA1[%]�P�ʂŐݒ�ł��܂�  
 �E  `return` :    
    (id, 'ACK'):����ɖ��߂��`�B�Ă��܂�  
    (id, 'NACK)':�R�}���h���������ݒ肳��Ă��܂���i�ʏ�̗��p�ł͌��邱�Ƃ͂Ȃ��ł��傤�j  
    (id, 'unReadable'):�ʐM���Ɉȏオ����܂��B�����̏ꍇ�T�[�{���[�^�̓d�����؂�Ă���Ȃǂ̌���l�����܂� 
  
    def set_damper(id, damper)
�_���p��ݒ肵�܂�  
 �E  `id` :  
    �ݒ��s���T�[�{���[�^��ID��w�肵�܂��BID��1~127�̊ԂŎw�肷��K�v������܂�  
 �E  `damper` :  
    �n���`���O��N����ɂ��������ʂ�����܂��B0�`255�̊ԂŐݒ肵�ĉ�����  
 �E  `return` :    
    (id, 'ACK'):����ɖ��߂��`�B�Ă��܂�  
    (id, 'NACK)':�R�}���h���������ݒ肳��Ă��܂���i�ʏ�̗��p�ł͌��邱�Ƃ͂Ȃ��ł��傤�j  
    (id, 'unReadable'):�ʐM���Ɉȏオ����܂��B�����̏ꍇ�T�[�{���[�^�̓d�����؂�Ă���Ȃǂ̌���l�����܂�  

    def set_compliance(id, cwcm, ccwcm, cwcs, ccwcs, punch)  �@
�R���v���C�A���X�}�[�W���Ȃǂ�ݒ肵�܂�  
 �E  `id` :  
    �ݒ��s���T�[�{���[�^��ID��w�肵�܂��BID��1~127�̊ԂŎw�肷��K�v������܂�  
 �E  `cwcm` :CW Compliance Margin  
    CW�i���v���j���̃T�[�{�̒�~�ʒu[0.1 degree]�̋��e�͈͂�ݒ肵�܂��B0�`255�̊ԂŐݒ肵�ĉ�����  
 �E  `ccwcm` :CCW Compliance Margin  
    CCW�i�����v���j�T�[�{�̒�~�ʒu[0.1 degree]�̋��e�͈͂�ݒ肵�܂��B0�`255�̊ԂŐݒ肵�ĉ�����  
 �E  `cwcs` :CW Compliance Slope  
    CW�i���v���j���̌��݈ʒu�ƖڕW�ʒu�̌덷�C���g���N�̐ݒ�B0�`255�̊ԂŐݒ肵�ĉ�����  
 �E  `ccwcs` :CCW Compliance Slope  
    CCW�i�����v���j���̌��݈ʒu�ƖڕW�ʒu�̌덷�C���g���N�̐ݒ�B0�`255�̊ԂŐݒ肵�ĉ�����  
 �E  `punch` :    
    ���[�^�쓮���̍ŏ��d����ݒ�ł��܂��B�ݒ�l�̒P�ʂ͍ő�g���N��0.001%�ŁA0�`10000�̊ԂŐݒ肵�ĉ�����  
 �E  `return` :    
    (id, 'ACK'):����ɖ��߂��`�B�Ă��܂�  
    (id, 'NACK)':�R�}���h���������ݒ肳��Ă��܂���i�ʏ�̗��p�ł͌��邱�Ƃ͂Ȃ��ł��傤�j  
    (id, 'unReadable'):�ʐM���Ɉȏオ����܂��B�����̏ꍇ�T�[�{���[�^�̓d�����؂�Ă���Ȃǂ̌���l�����܂�

���C�Z���X
----------
Copyright &copy; 2012 Hiroaki Matsuda  
Licensed under the [Apache License, Version 2.0][Apache]  
Distributed under the [MIT License][mit].  
Dual licensed under the [MIT license][MIT] and [GPL license][GPL].  
 
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
[MIT]: http://www.opensource.org/licenses/mit-license.php
[GPL]: http://www.gnu.org/licenses/gpl.html