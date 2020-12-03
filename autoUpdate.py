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


from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
import os
# from pyupdater.client import Client
from client_config import ClientConfig

APP_NAME = ClientConfig().APP_NAME
try:
    from app_version import APP_VERSION
except:
    APP_VERSION = '0.0.1beta1'


class autoUpdaterWorker(QThread):
    sessionUpdateStatus    = pyqtSignal(int,int)
    def __init__(self,update,client):
        super(QThread, self).__init__()

        self.update = update

        client.add_progress_hook(self.print_status_info)


    def print_status_info(self,info):
        self.app_update.updateSignal.emit(info.get(u'total'),info.get(u'downloaded'))
        # self.updateProgressBar.setMaximum(info.get(u'total'))
        # self.updateProgressBar.setValue(info.get(u'downloaded'))
        # self.setStatus('Application update {}'.format(info.get(u'status')))
        pass

    def print_status_info(self,info):
        self.sessionUpdateStatus.emit(info.get(u'total'),info.get(u'downloaded'))

    def run(self):
        self.update.download()
        

import pprint


class autoUpdater(QObject):

    def __init__(self,parent  = None):
        QObject.__init__(self,parent)
        self.msgBox = None
        self.updateAvailable = False

        # self.client = Client(ClientConfig())
        # self.client.refresh()
        
        pp = pprint.PrettyPrinter()
        # self.app_update = self.client.update_check(APP_NAME, APP_VERSION,strict=False)
        # if self.app_update is not None:
        #     pp.pprint(self.app_update.__dict__) 
        #     self.updateAvailable  = True
        #     print('update available')

    def startUpdate(self):

        if self.app_update is None:
            QMessageBox.information(None,APP_NAME,"No software update available")
        else:
                    # create message box
            if self.msgBox == None:
                self.msgBox = QProgressDialog(None)

            #configure the display
            self.msgBox.setLabelText("Downloading update")

            self.updateWorker = autoUpdaterWorker(self.app_update,self.client)
            self.updateWorker.sessionUpdateStatus.connect(self.updateStatusBar)
            self.updateWorker.finished.connect(self.downloadDone)
            self.updateWorker.start()


    def updateStatusBar(self,total,value):
        self.msgBox.setMaximum(total)
        self.msgBox.setValue(value)


    def downloadDone(self):
        self.updateProgressBar = None
        if self.app_update.is_downloaded():
            self.app_update.extract_restart()