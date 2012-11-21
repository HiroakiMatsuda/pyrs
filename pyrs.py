#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module provides a class that controls the serial servo motor manufactured by Futaba Corp.
# ver1.21121
# This module has been tested on python ver.2.6.6
# It need pySerial(http://pyserial.sourceforge.net/)
# (C) 2012 Matsuda Hiroaki

import serial

class Rs(object):

        def __init__(self):
                self.myserial = serial.Serial()
                print('Generated the serial object')
	
        def open_port(self, port = 'COM1', baudrate = 115200, timeout = 1):
                self.myserial.port = port
                self.myserial.baudrate = baudrate
                self.myserial.timeout = timeout
                self.myserial.parity = serial.PARITY_NONE
                try:
                        self.myserial.open()
                except IOError:
                        print('Failed to open port, check the device and port number')
                else:
                        print('Succeede to open port: ' + port)

        def close_port(self):
                self.myserial.close()

        def set_port(self, baudrate = 115200, timeout = 1):
                self.myserial.baudrate = baudrate
                self.myserial.timeout = timeout
                self.myserial._reconfigurePort()
                print('Succeede to set baudrate:%d, timeout:%d' %(baudrate, timeout))
                   
        def torque_on(self, id, mode):
                self._check_range(id  , 1, 127, 'id')
                self._check_range(mode, 0, 2  , 'mode')
                
                send = [0xFA, 0xAF, id, 0x01, 0x24, 0x01, 0x01, mode & 0x00FF]
                send.append(self._calc_checksum(send))

                self._write_command(send)

                return self._check_ack(id)    
  
        def target_position(self, id, position, time):
                self._check_range(id      , 1    , 127  , 'id')
                self._check_range(position, -1500, 1500 , 'position')
                self._check_range(time    , 0    , 16383, 'time')
                
                send = [0xFA, 0xAF, id, 0x01, 0x1E, 0x04, 0x01, position & 0x00FF,
                        (position & 0xFF00) >> 8, time & 0x00FF, (time & 0xFF00) >> 8]
                send.append(self._calc_checksum(send))
                
                self._write_command(send)

                return self._check_ack(id)
        
        def multi_torque_on(self, servo_data):
                for servo in servo_data:
                        self._check_range(servo[0], 1, 127, 'id')
                        self._check_range(servo[1], 0, 2  , 'mode')
                
                send = [0xFA, 0xAF, 0x00, 0x00, 0x24, 0x02, len(servo_data)]
                for servo in servo_data:
                        send.append(servo[0])
                        send.append(servo[1])
                send.append(self._calc_checksum(send))
                
                self._write_command(send)

                return 'multi_torque_on:' + str(servo_data)

        def multi_target_position(self, servo_data):
                for servo in servo_data:
                        self._check_range(servo[0], 1    , 127  , 'id')
                        self._check_range(servo[1], -1500, 1500 , 'position')
                        self._check_range(servo[2], 0    , 16383, 'time')
                
                send = [0xFA, 0xAF, 0x00, 0x00, 0x1E, 0x05, len(servo_data)]
                for servo in servo_data:
                        send.append(servo[0])
                        send.append(servo[1] & 0x00FF)
                        send.append((servo[1] & 0xFF00) >> 8)
                        send.append(servo[2] & 0x00FF)
                        send.append((servo[2] & 0xFF00) >> 8)
                send.append(self._calc_checksum(send))
                
                self._write_command(send)

                return 'multi_target_position:' + str(servo_data)

        def get_data(self, id, mode = 'all'):
                self._check_range(id, 1, 127, 'id')

                modes = ('all', 'angle', 'time', 'speed', 'load', 'tempreture','voltage', 'list')
                if mode not in modes:
                       raise ValueError('mode is not defined, select from the list below\n'
                                        + str(modes))

                elif mode is 'list':
                        return modes
                
                send = [0xFA, 0xAF, id, 0x09, 0x00, 0x00, 0x01]
                send.append(self._calc_checksum(send))
                
                self._write_command(send)
              
                receive = self.myserial.read(26)
                try:
                        angle      = ((ord(receive[8]) << 8) & 0x0000FF00) | (ord(receive[7])  & 0x000000FF)
                        time       = ((ord(receive[10])<< 8) & 0x0000FF00) | (ord(receive[9])  & 0x000000FF)
                        speed      = ((ord(receive[12])<< 8) & 0x0000FF00) | (ord(receive[11]) & 0x000000FF)
                        load       = ((ord(receive[14])<< 8) & 0x0000FF00) | (ord(receive[13]) & 0x000000FF)
                        tempreture = ((ord(receive[16])<< 8) & 0x0000FF00) | (ord(receive[15]) & 0x000000FF)
                        voltage    = ((ord(receive[18])<< 8) & 0x0000FF00) | (ord(receive[17]) & 0x000000FF)
                except IndexError:
                        print('Could not get the data.Check the cables, connectors, and a power supply.')

                else:
                        if angle > 1800:
                                angle = -((angle - 1) ^ 0xFFFF)
                        
                        if mode is 'all':
                                return id, angle, time, speed, load, tempreture, voltage
                        elif mode is 'angle':
                                return id, angle
                        elif mode is 'time':
                                return id, time
                        elif mode is 'speed':
                                return id, speed
                        elif mode is 'load':
                                return id, load
                        elif mode is 'tempreture':
                                return id, tempreture
                        elif mode is 'voltage':
                                return id, voltage       

        def servo_reset(self, id):
                self._check_range(id, 1, 127, 'id')
                
                send = [0xFA, 0xAF, id, 0x20, 0xFF, 0x00, 0x00]
                send.append(self._calc_checksum(send))
                
                self._write_command(send)

        def set_torque_limit(self, id, limit = 100):
                self._check_range(id    , 1, 127, 'id')
                self._check_range(limit , 0, 100, 'limit')
                
                send = [0xFA, 0xAF, id, 0x01, 0x23, 0x01, 0x01, limit & 0x00FF]
                send.append(self._calc_checksum(send))
                
                self._write_command(send)

                return self._check_ack(id)

        def set_damper(self, id, damper = 16):
                self._check_range(id     , 1, 127, 'id')
                self._check_range(damper , 0, 255, 'damper')

                send = [0xFA, 0xAF, id, 0x01, 0x20, 0x01, 0x01, damper & 0x00FF]
                send.append(self._calc_checksum(send))
                
                self._write_command(send)

                return self._check_ack(id)

        def set_compliance(self, id, cwcm = 1, ccwcm = 1, cwcs = 4, ccwcs = 4, punch = 1300):
                self._check_range(id   , 1, 127  , 'id')
                self._check_range(cwcm , 0, 255  , 'cwcm')
                self._check_range(ccwcm, 0, 255  , 'ccwcm')
                self._check_range(cwcs , 0, 255  , 'cwcs')
                self._check_range(ccwcs, 0, 255  , 'ccwcs')
                self._check_range(punch, 0, 10000, 'punch')
                
                send = [0xFA, 0xAF, id, 0x01, 0x18, 0x06, 0x01, cwcm & 0x00FF, ccwcm & 0x00FF,
                        cwcs&0x00FF, ccwcs & 0x00FF, punch & 0x00FF, (punch & 0xFF00) >> 8]
                send.append(self._calc_checksum(send))
                
                self._write_command(send)

                return self._check_ack(id)
                
# The following functions are provided for use in PRS class
        def _calc_checksum(self, send):
                checksum = send[2]
                for i in range(3, len(send)):
                        checksum ^= send[i]               
                return checksum

        def _check_range(self, value, lower_range, upper_range, name = 'value'):
                if value < lower_range or value > upper_range:
                        raise ValueError(name + ' must be set in the range from '
                                         + str(lower_range) + ' to ' + str(upper_range))

        def _check_ack(self, id):
                receive = self.myserial.read(1)
                length = len(receive)
                
                if length == 1:
                        ack = ord(receive)
                        if ack == 0x07:
                                return id, 'ACK'
                        elif ack == 0x08:
                                return id, 'NACK'
                        else:
                                return id, 'unKnown'
                elif length != 1:
                        return id, 'unReadable'

        def _write_command(self, send):
                self.myserial.flushOutput()
                self.myserial.flushInput()
                self.myserial.write(bytearray(send[0:]))

if __name__ == '__main__':
        import pyrs
        import time
        rs = pyrs.Rs()
        rs = pyrs.Rs()  
        rs.open_port('COM11', 115200, 1 )   
        rs.torque_on(1, 1)
        rs.target_position(1, 900, 200)
        time.sleep(1)
        print rs.get_data(1, 'angle')
        time.sleep(1)
        rs.torque_on(1, 0)  
        rs.close_port()
        
