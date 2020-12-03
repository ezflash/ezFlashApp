# The MIT License (MIT)
# Copyright (c) 2019 ezflash
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import logging
import site

from intelhex import IntelHex
from flask import Flask, render_template
from flask_socketio import SocketIO

from ezFlashCLI.ezFlash.pyjlink import pyjlink
from ezFlashCLI.ezFlash.smartbond.smartbondDevices import *

from PyQt5.QtCore       import *

from autoUpdate import APP_VERSION


class FlaskThread(QThread):

    PORT = 35879

    PORT_REFRESH_RATE = 1000 # scan interval in ms
    serverError = pyqtSignal(str)
    updateRequest = pyqtSignal()

    def __init__(self,port=None,logLevel= logging.DEBUG,parent=None):

        QThread.__init__(self,parent=parent)
        
        self.devices = []

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logLevel)


        self.refreshTimer = QTimer()
        self.refreshTimer.timeout.connect(self.refreshPort)  # Let the interpreter run each 500 ms.
        self.refreshTimer.start(self.PORT_REFRESH_RATE)  # You may change this if you wish.

        if port != None:
            self.PORT = port
        self.ROOT_URL = 'http://localhost:{}'.format(self.PORT)


        static_folder= os.path.join(os.path.dirname(os.path.abspath(__file__)),'frontend','dist','frontend')

        self.app = Flask(__name__,static_url_path='',static_folder=static_folder)
        self.app.config['SECRET_KEY'] = 'c7e34fed-deb7-4772-b69f-54984828db03'
        self.app.logger.setLevel(logLevel)


        self.app.add_url_rule('/<short_link>','short_link', self.short_link)
        self.app.add_url_rule('/','root', self.root)


        self.socketioApp = SocketIO(self.app,port=self.PORT)

        self.socketioApp.on_event('getDeviceList',self.handle_getDeviceList)
        self.socketioApp.on_event('browseDevice' ,self.handle_browseDevice)
        self.socketioApp.on_event('resetAndRun'  ,self.handle_resetAndRun)
        self.socketioApp.on_event('resetAndHalt' ,self.handle_resetAndHalt)
        self.socketioApp.on_event('eraseFlashDevice',self.handle_eraseFlashDevice)
        self.socketioApp.on_event('programFlashDevice',self.handle_programFlashDevice)
        self.socketioApp.on_event('backendVersion',self.handle_backendVersion)
        self.socketioApp.on_event('appUpdate',self.handle_appUpdate)



        # logging.basicConfig(level=logging.DEBUG)
        if getattr(sys, 'frozen', False):
            fdbpath = os.path.join(os.path.dirname(__file__), 'flash_database.json')
        else:
            fdbpath = os.path.join(site.getsitepackages()[-1],'ezFlashCLI','flash_database.json')

        with open(fdbpath) as json_file:
            self.flash_db = json.load(json_file)

            json_file.close()
        self.logger.debug('init pyjlink')
        self.link = pyjlink()
        self.link.init()

    def run(self):
        try:
            self.socketioApp.run(self.app,port=self.PORT)
        except Exception as inst:
            logging.error("Flask Error: {}".format(inst))
            self.serverError.emit(str(inst))


    def short_link(self,short_link):
        self.logger.debug('shortlink {}'.format(short_link))
        if short_link.split(';')[0] in ('suota','flashprog'):
            return self.app.send_static_file('index.html')
        else:
            return self.app.send_static_file(short_link)
    
    def root(self):
        self.logger.debug('root')
        return self.app.send_static_file('index.html')
        

    def handle_appUpdate(self,json):
        self.updateRequest.emit()


    def handle_backendVersion(self,json):
        json['version'] = APP_VERSION
        json['update'] = self.parent().autoupdater.updateAvailable
        self.socketioApp.emit('backendVersion',json,json=True)


    def handle_getDeviceList(self,json):
        self.logger.info('received json: ' + str(json))
        self.refreshPort()
        json['resp'] = self.devices
        self.socketioApp.emit('getDeviceList',json,json=True)

    def handle_browseDevice(self,json):
        self.logger.info('browseDevice json: ' + str(json))
        try:
            json['deviceType'] = SMARTBOND_IDENTIFIER[self.link.connect(int(json['deviceId']))]

        except Exception as inst:
            self.logger.warning("Device not responding: {}".format(inst))
            json['deviceType'] = "Device not responding"
            self.link.close()
            return

        self.link.close()

        # look for attached flash
        try:
            da =  eval(json['deviceType'])()
            devid = da.connect(int(json['deviceId']))
            da.flash_init()
            dev = da.flash_probe()
            self.logger.debug("Found device: {}".format(SMARTBOND_IDENTIFIER[devid]))
            self.logger.debug(("Found Flash:".format(da.get_flash(dev,self.flash_db)['name'])))

            json['flashType'] = da.get_flash(dev,self.flash_db)['name']
            da.link.close()
        except Exception as inst:
            json['flashType'] = "Not probed"
            self.logger.debug("not probed:",inst)
            


        self.socketioApp.emit('browseDevice',json,json=True)

    def handle_resetAndRun(self,json):

        da =  eval(json['deviceType'])()
        da.connect(int(json['deviceId']))
        da.link.resetNoHalt()
        self.socketioApp.emit('deviceStatus', {'deviceIsRunning': not bool(da.link.jl.JLINKARM_IsHalted())})
        da.link.close()



    def handle_resetAndHalt(self,json):
        da =  eval(json['deviceType'])()
        da.connect(int(json['deviceId']))
        da.link.reset()
        self.socketioApp.emit('deviceStatus', {'deviceIsRunning': not bool(da.link.jl.JLINKARM_IsHalted())})
        da.link.close()

    def handle_eraseFlashDevice(self,json):
        da =  eval(json['deviceType'])()
        da.connect(int(json['deviceId']))
        self.socketioApp.emit('eraseFlashDevice', {'status': da.flash_erase()})
        da.link.close()

    def handle_programFlashDevice(self,json):
        self.logger.debug('Program file size {}'.format(len(json['file'])))
        da =  eval(json['deviceType'])()
        da.connect(int(json['deviceId']))
        da.flash_init()
        dev = da.flash_probe()

        da.flash_program_image(json['file'],da.get_flash(dev,self.flash_db))
        self.socketioApp.emit('programFlashDevice', {'status': 'done'})


    def refreshPort(self):
        inf = self.link.browse()
        newDevices = []
        json = {}
        if inf:
            for dev in inf:
                if dev.SerialNumber != 0:
                    newDevices.append( {"deviceId" :dev.SerialNumber, "deviceName" : ''.join([chr(i) for i in dev.acProduct]).rstrip('\x00')})


        # check new devices
        for device in newDevices:
            if not device in self.devices:
                self.updateDeviceList(newDevices)
                break
        # check removed devices
        for device in self.devices:
            if not device in newDevices:
                self.updateDeviceList(newDevices)
                break
            
    def updateDeviceList(self,newList):
        self.logger.info("update device list")
        self.devices = newList
        json = {'resp':  self.devices}
        self.socketioApp.emit('getDeviceList',json,json=True)




if __name__ == '__main__':
    os.environ['FLASK_ENV']='development'
    socketioApp.run(app,debug=True)
