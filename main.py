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
import logging
import signal
import platform
import socket


import sys

from autoUpdate import autoUpdater,APP_NAME,APP_VERSION

from PyQt5.Qt import QEvent
from PyQt5.QtCore import Qt, QThread, QUrl, QCoreApplication, QSettings, pyqtSlot, QByteArray
from PyQt5.QtWidgets import QSystemTrayIcon, QApplication, QMenu, QMessageBox, QMainWindow, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
from PyQt5.QtGui import QIcon, QDesktopServices, QPixmap, QCloseEvent


class ezFlashAppWindow(QMainWindow):

    def __init__(self, url):
        super(ezFlashAppWindow, self).__init__()

        self.settings = QCoreApplication.instance().settings

        menuBar = self.menuBar()

        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(os.path.join('assets','link.png')))


        self.webview = QWebEngineView()
        self.webview.page().profile().setHttpCacheType(QWebEngineProfile.MemoryHttpCache)
        

        self.webview.loadFinished.connect(self.show)
        self.setCentralWidget(self.webview)
      
        self.fmenu = QMenu('&File', self)
        self.fmenu.addAction(' &Quit', self.close,Qt.CTRL + Qt.Key_W)
        menuBar.addMenu(self.fmenu)

        self.help_menu = QMenu(' &Help', self)
        self.help_menu.addAction(' &about',self.about)

        menuBar.addMenu(self.help_menu)
        

        #restore windows size
        try:
            self.restoreGeometry(self.settings.value("mainWindow/geometry",QByteArray()))
            self.restoreState(self.settings.value("mainWindow/windowState"))
        except:
            pass

        self.webview.load(QUrl(url))

    @pyqtSlot(QCloseEvent)
    def closeEvent(self, event):
        self.settings.setValue("mainWindow/geometry", self.saveGeometry())
        self.settings.setValue("mainWindow/windowState", self.saveState())
        QMainWindow.closeEvent(self, event)

    def about(self):
        

        msgBox = QMessageBox(self)
        msgBox.setWindowTitle('About {}'.format(APP_NAME))
        msgBox.setTextFormat(Qt.RichText)
        msg = '{} {}'.format(APP_NAME,APP_VERSION,)
        if getattr(sys, 'frozen', False):
            # frozen
            dir_ = os.path.dirname(sys.executable)
        else:
            # unfrozen
            dir_ = os.path.dirname(os.path.realpath(__file__))

        msgBox.setIconPixmap(QPixmap(os.path.join(dir_,'assets','link.png')).scaledToHeight(100))
        msgBox.setText(msg)
        
        msgBox.show()
        



class ezFlashApp(QApplication):
    
         
    def __init__(self):

        # probably need to do that only when frozen
        QApplication.__init__(self,sys.argv)

        logging.basicConfig(level=logging.DEBUG)
        
        # handle the application settings
        QCoreApplication.setOrganizationName("ezFlash")
        QCoreApplication.setOrganizationDomain("ezFlash.org")
        QCoreApplication.setApplicationName(APP_NAME)

        self.settings = QSettings(QSettings.IniFormat,QSettings.UserScope,QCoreApplication.organizationDomain(),APP_NAME)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        port = sock.getsockname()[1]
        sock.close()


        from flaskServer import FlaskThread
        self.webserver = FlaskThread(parent=self,port=port)

        self.webserver.serverError.connect(self.serverErrorHandler)
        self.webserver.updateRequest.connect(self.updateRequestHandler)
        self.webserver.start()

        self.aboutToQuit.connect(self.webserver.terminate)

        #auto updater
        self.autoupdater = autoUpdater(self)

        # if not platform.system() in 'Darwin':
        #     if getattr(sys, 'frozen', False):
        #         # frozen
        #         dir_ = sys._MEIPASS
        #     else:
        #         # unfrozen
        #         dir_ = os.path.dirname(os.path.realpath(__file__))

        #     logging.info('dir {} {} {}'.format(dir_,os.path.realpath(__file__),os.path.realpath(sys.executable)))
        # else:
        #     if getattr(sys, 'frozen', False):
        #         # frozen
        #         dir_ = os.path.dirname(sys.executable)
        #     else:
        #         # unfrozen
        #         dir_ = os.path.dirname(os.path.realpath(__file__))

        # self.iconPict = QIcon(os.path.join(dir_,'assets','link.png'))
        # self.icon = QSystemTrayIcon(self.iconPict, self)

        # self.icon.setToolTip("{} Application".format(APP_NAME))
        
        # menu = QMenu()
        # menu.addAction('&Open',self.openView)
        # menu.addAction('&About',self.about)
        # menu.addSeparator()
        # menu.addAction('&Quit',self.quit)
        # self.icon.setContextMenu(menu)
        # self.icon.activated.connect(self.iconActivated)


        # self.icon.show()
        # if getattr(sys, 'frozen', False):
        #     self.openView()
        #     self.icon.showMessage(APP_NAME, "Application Started in background".format(APP_NAME),self.iconPict,1000)

        self.mainWin= ezFlashAppWindow(self.webserver.ROOT_URL)

        # self.mainWin.show()


    def updateRequestHandler(self):

        self.autoupdater.startUpdate()

        pass


    def serverErrorHandler(self,msg):
        logging.error("Server Error {}".format(msg))
        QMessageBox.critical(self.mainWin,"Server Error",msg)


    
    def openView(self):
        QDesktopServices.openUrl(QUrl(self.webserver.ROOT_URL))



    
def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    qtapp.quit()

if __name__ == '__main__':

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    qtapp = ezFlashApp()

    sys.exit(qtapp.exec_())
