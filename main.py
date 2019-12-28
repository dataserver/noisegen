from PySide2 import QtCore, QtGui, QtWidgets, QtUiTools
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QObject

import os
import sys
import random
import math
import configparser
import json

# must be set before IMPORT
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_file = QtCore.QFile('gui.ui')
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        config = configparser.ConfigParser()
        config.read('config.ini')
        self.cfg = config['DEFAULT']

        self.title = 'Noise Generator'
        self.left = 100
        self.top = 100
        self.width = 480
        self.height = 300
        self.album_dir = self.cfg['album_dir']
        self.slider_start_position = int(self.cfg['volume'])
        self.auto_play = int(self.cfg['auto_play'])
        self.player_status = None
        self.albums_list = []

        self.ui.setWindowTitle(self.title)
        self.ui.setWindowIcon(QtGui.QIcon('resources/icon.svg'))
        self.ui.setGeometry(self.left, self.top, self.width, self.height)

        self.__center()
        self.sliders_reset()
        self.disable_sliders()

        self.ui.vertical_slider_0a.valueChanged.connect(
            lambda position, channel=0: self.change_slider(position, channel))
        self.ui.vertical_slider_1a.valueChanged.connect(
            lambda position, channel=1: self.change_slider(position, channel))
        self.ui.vertical_slider_2a.valueChanged.connect(
            lambda position, channel=2: self.change_slider(position, channel))
        self.ui.vertical_slider_3a.valueChanged.connect(
            lambda position, channel=3: self.change_slider(position, channel))
        self.ui.vertical_slider_4a.valueChanged.connect(
            lambda position, channel=4: self.change_slider(position, channel))
        self.ui.vertical_slider_5a.valueChanged.connect(
            lambda position, channel=5: self.change_slider(position, channel))
        self.ui.vertical_slider_6a.valueChanged.connect(
            lambda position, channel=6: self.change_slider(position, channel))
        self.ui.vertical_slider_7a.valueChanged.connect(
            lambda position, channel=7: self.change_slider(position, channel))
        self.ui.vertical_slider_8a.valueChanged.connect(
            lambda position, channel=8: self.change_slider(position, channel))
        self.ui.vertical_slider_9a.valueChanged.connect(
            lambda position, channel=9: self.change_slider(position, channel))

        self.combobox_populate()

        self.ui.btn_play.clicked.connect(self.player_play)
        self.ui.btn_pause.clicked.connect(self.player_pause)
        self.ui.btn_stop.clicked.connect(self.player_stop)

        self.ui.btn_reset.clicked.connect(self.sliders_reset)
        self.ui.btn_all_up_volume.clicked.connect(self.sliders_up)
        self.ui.btn_all_down_volume.clicked.connect(self.sliders_down)
        self.ui.btn_random.clicked.connect(self.sliders_random)
        self.ui.select_album.currentIndexChanged.connect(self.combobox_on_change)

        self.ui.show()

        if self.auto_play == 1:
            self.player_play()

    def __center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def build_albums_list(self):
        list_to_be_sorted = []
        dirs = next(os.walk('audioset'))[1]
        for dir_name in dirs:
            try:    
                with open(self.cfg['collection_dir'] + '/' + dir_name + '/data.json', 'r') as f:
                    parsed_json = json.load(f)

                list_to_be_sorted.append({
                    'dir': dir_name,
                    'title': parsed_json['title'],
                })
            except IOError:
                print('data.json not found in dir: ' + dir_name)
            
            self.albums_list = sorted(list_to_be_sorted, key=lambda item: item['title'])


    # COMBOBOX
    def combobox_populate(self):
        self.build_albums_list()
        for album in self.albums_list:
            self.ui.select_album.addItem(album['title'])

        if self.album_dir is not None:
            album = self.search(self.albums_list, 'dir', self.album_dir)
            album_title = album['title']
            if album_title is not None:
                index = self.ui.select_album.findText(album_title, QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.ui.select_album.setCurrentIndex(index)

    def combobox_on_change(self):
        selected = self.ui.select_album.currentText()
        album = self.search(self.albums_list, 'title', selected)
        self.album_dir = album['dir']

        if pygame.mixer.get_init() is not None:
            self.player_stop()
            self.player_play()

    # PLAYER
    def player_pause(self):
        if self.player_status is not None:
            if self.player_status == "play":
                self.ui.btn_pause.setText("UnPause")
                self.player_status = "pause"
                pygame.mixer.pause()
            else:
                pygame.mixer.unpause()
                self.ui.btn_pause.setText("Pause")
                self.player_status = "play"

    def player_stop(self):
        pygame.mixer.stop()
        self.ui.btn_pause.setText("Pause")
        self.player_status = None
        self.disable_sliders()

    def player_play(self):
        self.enable_sliders()

        pygame.mixer.init(frequency=22050, size=-16, channels=4)
        pygame.mixer.set_num_channels(10)
        self.player_status = "play"
        parsed_json = None
        try:   
            with open(self.cfg['collection_dir'] + '/' + self.album_dir + '/data.json', 'r') as f:
                parsed_json = json.load(f)
        except IOError:
            print('data.json not found in dir: ' + self.album_dir)

        if parsed_json is not None:
            self.ui.setWindowTitle(parsed_json['title'] + ' - ' + self.title)
            for info in parsed_json['files']:
                channel = int(info['channel'])
                slider = getattr(self.ui, 'vertical_slider_%da' % channel)
                slider.setToolTip(info['title'])
                if os.path.isfile(self.cfg['collection_dir'] + '/' + self.album_dir + '/' + info['file']):
                    pygame.mixer.Channel(channel).play(pygame.mixer.Sound(
                        self.cfg['collection_dir'] + '/' + self.album_dir + '/' + info['file']), loops=-1)
                    position = slider.value()
                    pygame.mixer.Channel(channel).set_volume(
                        self.position_to_volume(position))
                else:
                    slider.setDisabled(True)
                    print ("File not exist: " + self.album_dir + '/' + info['file'])

    # SLIDERS
    def change_slider(self, position, channel):
        if self.player_status is not None:
            channel = int(channel)
            # position scale is 0-100, pygame.mixer is 0-1
            vol = self.position_to_volume(position)
            pygame.mixer.Channel(channel).set_volume(vol)

    def disable_sliders(self):
        for channel in range(0, 10):
            slider = getattr(self.ui, 'vertical_slider_%da' % channel)
            slider.setDisabled(True)

    def enable_sliders(self):
        for channel in range(0, 10):
            slider = getattr(self.ui, 'vertical_slider_%da' % channel)
            slider.setDisabled(False)

    def sliders_up(self):
        if self.player_status is not None:
            for channel in range(0, 10):
                slider = getattr(self.ui, 'vertical_slider_%da' % channel)
                position = slider.value() + 5
                slider.setValue(position)
                pygame.mixer.Channel(channel).set_volume(
                    self.position_to_volume(position))

    def sliders_down(self):
        if self.player_status is not None:
            for channel in range(0, 10):
                slider = getattr(self.ui, 'vertical_slider_%da' % channel)
                position = slider.value() - 5
                if position <= 0:
                    slider.setValue(0)
                    position = 0
                else:
                    slider.setValue(position)
                pygame.mixer.Channel(channel).set_volume(
                    self.position_to_volume(position))

    def sliders_random(self):
        if self.player_status is not None:
            for channel in range(0, 10):
                slider = getattr(self.ui, 'vertical_slider_%da' % channel)
                position = random.randrange(0, 60, 1)
                slider.setValue(position)
                pygame.mixer.Channel(channel).set_volume(
                    self.position_to_volume(position))

    def sliders_reset(self):
        for channel in range(0, 10):
            position = self.slider_start_position
            slider = getattr(self.ui, 'vertical_slider_%da' % channel)
            slider.setValue(position)
            if self.player_status is not None:
                pygame.mixer.Channel(channel).set_volume(
                    self.position_to_volume(position))

    # Helper functions
    def search(self, list, key, value):
        for item in list:
            if item[key] == value:
                return item

    # Logarithmic slider
    # Position from 0-100 convert to pygame.mixer volume 0-1
    def position_to_volume(self, position=0):
        if position == 0:
            return 0
        #  position is between 0 and 100
        min_pos = 0
        max_pos = 100
        min_val = math.log(1)
        max_val = math.log(100)

        #  calculate adjustment factor
        scale = (max_val-min_val) / (max_pos-min_pos)
        vol = math.exp((position - min_pos) * scale + min_val)
        #  The result should be float between 0 and 1
        return float("{0:.2f}".format(vol/100))

    # get poistion 0-100 from by pygame.mixer volume 0 - 1
    def volume_to_position(self, volume=0):
        if volume == 0:
            return 0
        #  position is between 0 and 100
        min_pos = 0
        max_pos = 100
        min_val = math.log(1)
        max_val = math.log(100)

        #  The result should be between 0 and 100
        conv_volume = volume * 100
        scale = (max_val-min_val) / (max_pos-min_pos)
        pos = min_pos + (math.log(conv_volume) - min_val) / scale
        return int(pos)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    sys.exit(app.exec_())
