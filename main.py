import json
import math
import os
import sys
from pathlib import Path
from random import randrange
from typing import Literal

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox

from src.config import read_config
from src.data import AudioFileData, AudioSetData, PlayerStatus, WindowProp

# must be set before IMPORT
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from pygame import mixer as pmixer

MAX_NUM_CHANNELS = 10  # Number of channels in GUI mixer


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.cfg = read_config(f"src/config.json")
        ui_file_name = "src/gui.ui"
        ui_file = QtCore.QFile(ui_file_name)
        if not ui_file.open(QtCore.QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        window = loader.load(ui_file)
        ui_file.close()
        if not window:
            print(loader.errorString())
            sys.exit(-1)
        self.ui = window
        self.current_folder = self.cfg.default_album_folder
        self.slider_start_position = self.cfg.default_channel_volume
        self.player_status = None
        self.albums = []
        self.current_album = None
        self.used_channels = []

        self.ui.setWindowTitle(WindowProp.TITLE)
        self.ui.setWindowIcon(
            QtGui.QIcon(f"{self.cfg.svg_path}{self.cfg.svg_app_icon}")
        )
        self.ui.setGeometry(
            WindowProp.LEFT, WindowProp.TOP, WindowProp.WIDTH, WindowProp.HEIGHT
        )

        self.center()
        self.sliders_reset()
        self.sliders_disable()

        self.ui.vertical_slider_0a.valueChanged.connect(
            lambda position, channel=0: self.sliders_change(position, channel)
        )
        self.ui.vertical_slider_1a.valueChanged.connect(
            lambda position, channel=1: self.sliders_change(position, channel)
        )
        self.ui.vertical_slider_2a.valueChanged.connect(
            lambda position, channel=2: self.sliders_change(position, channel)
        )
        self.ui.vertical_slider_3a.valueChanged.connect(
            lambda position, channel=3: self.sliders_change(position, channel)
        )
        self.ui.vertical_slider_4a.valueChanged.connect(
            lambda position, channel=4: self.sliders_change(position, channel)
        )
        self.ui.vertical_slider_5a.valueChanged.connect(
            lambda position, channel=5: self.sliders_change(position, channel)
        )
        self.ui.vertical_slider_6a.valueChanged.connect(
            lambda position, channel=6: self.sliders_change(position, channel)
        )
        self.ui.vertical_slider_7a.valueChanged.connect(
            lambda position, channel=7: self.sliders_change(position, channel)
        )
        self.ui.vertical_slider_8a.valueChanged.connect(
            lambda position, channel=8: self.sliders_change(position, channel)
        )
        self.ui.vertical_slider_9a.valueChanged.connect(
            lambda position, channel=9: self.sliders_change(position, channel)
        )

        self.combobox_populate()

        self.ui.btn_pause_play.clicked.connect(self.player_play)
        self.ui.btn_pause_play.setIcon(
            QtGui.QIcon(f"{self.cfg.svg_path}{self.cfg.svg_btn_play}")
        )
        self.ui.btn_stop.clicked.connect(self.player_stop)
        self.ui.btn_stop.setIcon(
            QtGui.QIcon(f"{self.cfg.svg_path}{self.cfg.svg_btn_stop}")
        )

        self.ui.btn_reset.clicked.connect(self.sliders_reset)
        self.ui.btn_all_up_volume.clicked.connect(self.sliders_up)
        self.ui.btn_all_down_volume.clicked.connect(self.sliders_down)
        self.ui.btn_random.clicked.connect(self.sliders_random)
        self.ui.select_album.currentIndexChanged.connect(self.combobox_on_change)

        self.ui.show()

        if self.cfg.auto_play:
            self.player_play()

    def center(self) -> None:
        """Center app window position"""
        qr = self.frameGeometry()
        cp = QtGui.QScreen.availableGeometry(
            QtWidgets.QApplication.primaryScreen()
        ).center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def albums_build(self) -> None:
        """Generate list of available albums from audio collection folder"""
        list_to_be_sorted = []
        folders = next(os.walk("audioset"))[1]
        for dir in folders:
            try:
                with open(f"{self.cfg.collection_folder}{dir}/data.json", "r") as f:
                    parsed_json = json.load(f)
                    channels = []
                    if parsed_json is not None:
                        for file in parsed_json["files"]:
                            channels.append(
                                AudioFileData(
                                    channel=int(file["channel"]),
                                    title=file["title"],
                                    file=f"{self.cfg.collection_folder}{dir}/{file['file']}",
                                )
                            )
                list_to_be_sorted.append(
                    AudioSetData(dir=dir, title=parsed_json["title"], files=channels)
                )
            except IOError:
                print("data.json not found in dir: " + dir)
            self.albums = sorted(list_to_be_sorted, key=lambda item: item.title)

    def combobox_populate(self) -> None:
        """Populate dropdown list"""
        self.albums_build()
        for album in self.albums:
            self.ui.select_album.addItem(album.title)

        if self.current_folder is not None:
            if self.current_album is None:
                self.current_album = self.search(key="dir", value=self.current_folder)

            if self.current_album.title is not None:
                index = self.ui.select_album.findText(
                    self.current_album.title, QtCore.Qt.MatchFixedString
                )
                if index >= 0:
                    self.ui.select_album.setCurrentIndex(index)

    def combobox_on_change(self) -> None:
        """Play music after selecting it on dropdown list"""
        selected = self.ui.select_album.currentText()
        album = self.search(key="title", value=selected)
        self.current_album = album
        self.current_folder = album.dir

        if self.cfg.auto_play:
            if pmixer.get_init() is not None:
                self.player_stop()
                self.player_play()

    def player_play(self) -> None:
        # self.sliders_enable()
        self.ui.setWindowTitle(f"{self.current_album.title} - {WindowProp.TITLE}")
        self.player_status = PlayerStatus.PLAYING
        self.ui.btn_pause_play.setIcon(
            QtGui.QIcon(f"{self.cfg.svg_path}{self.cfg.svg_btn_pause}")
        )
        self.ui.btn_pause_play.clicked.disconnect()
        self.ui.btn_pause_play.clicked.connect(self.player_pause)
        f_len = len(self.current_album.files)
        pmixer.init(frequency=22050, size=-16, channels=4)
        pmixer.set_num_channels(f_len)
        self.used_channels = []
        for ch in self.current_album.files:
            slider = getattr(self.ui, "vertical_slider_%da" % ch.channel)
            slider.setToolTip("")
            slider.setDisabled(True)
            if os.path.isfile(ch.file):
                slider.setToolTip(ch.title)
                slider.setDisabled(False)
                pmixer.Channel(ch.channel).play(pmixer.Sound(ch.file), loops=-1)
                position = slider.value()
                pmixer.Channel(ch.channel).set_volume(self.position_to_volume(position))
                self.used_channels.append(ch.channel)
            else:
                self.alert_message(
                    header="Missing File", text=f"File does not exist:\n {ch.file}"
                )

        for ch in range(0, MAX_NUM_CHANNELS):
            if ch not in self.used_channels:
                slider = getattr(self.ui, "vertical_slider_%da" % ch)
                slider.setToolTip("")
                slider.setDisabled(True)

    def player_pause(self) -> None:
        pmixer.pause()
        self.player_status = PlayerStatus.PAUSED
        self.ui.btn_pause_play.setIcon(
            QtGui.QIcon(f"{self.cfg.svg_path}{self.cfg.svg_btn_play}")
        )
        self.ui.btn_pause_play.clicked.disconnect()
        self.ui.btn_pause_play.clicked.connect(self.player_unpause)

    def player_unpause(self) -> None:
        pmixer.unpause()
        self.player_status = PlayerStatus.PLAYING
        self.ui.btn_pause_play.setIcon(
            QtGui.QIcon(f"{self.cfg.svg_path}{self.cfg.svg_btn_pause}")
        )
        self.ui.btn_pause_play.clicked.disconnect()
        self.ui.btn_pause_play.clicked.connect(self.player_pause)

    def player_stop(self) -> None:
        pmixer.stop()
        self.player_status = PlayerStatus.STOPPED
        self.ui.btn_pause_play.setIcon(
            QtGui.QIcon(f"{self.cfg.svg_path}{self.cfg.svg_btn_play}")
        )
        self.ui.btn_pause_play.clicked.disconnect()
        self.ui.btn_pause_play.clicked.connect(self.player_play)
        # self.sliders_disable()

    def sliders_change(self, position, channel) -> None:
        """Change slider position"""
        channel = int(channel)
        # position scale is 0-100, pmixer is 0-1
        vol = self.position_to_volume(position)
        pmixer.Channel(channel).set_volume(vol)

    def sliders_disable(self, channel_list=None) -> None:
        """Disable (grayed) any change on slider position/volume"""
        for channel in range(0, MAX_NUM_CHANNELS):
            slider = getattr(self.ui, "vertical_slider_%da" % channel)
            slider.setDisabled(True)

    def sliders_enable(self) -> None:
        """Enable changes in slider position"""
        for channel in range(0, MAX_NUM_CHANNELS):
            slider = getattr(self.ui, "vertical_slider_%da" % channel)
            slider.setDisabled(False)

    def sliders_up(self) -> None:
        """Make all sliders positions to go UP"""
        for channel in range(0, MAX_NUM_CHANNELS):
            slider = getattr(self.ui, "vertical_slider_%da" % channel)
            position = slider.value() + 5
            slider.setValue(position)
            pmixer.Channel(channel).set_volume(self.position_to_volume(position))

    def sliders_down(self) -> None:
        """Make all sliders positions to go DOWN"""
        for channel in range(0, MAX_NUM_CHANNELS):
            slider = getattr(self.ui, "vertical_slider_%da" % channel)
            position = slider.value() - 5
            if position <= 0:
                slider.setValue(0)
                position = 0
            else:
                slider.setValue(position)
            pmixer.Channel(channel).set_volume(self.position_to_volume(position))

    def sliders_random(self) -> None:
        """Randomize position of all sliders"""
        for channel in range(0, MAX_NUM_CHANNELS):
            if channel in self.used_channels:
                slider = getattr(self.ui, "vertical_slider_%da" % channel)
                position = randrange(0, 60, 1)
                slider.setValue(position)
                pmixer.Channel(channel).set_volume(self.position_to_volume(position))

    def sliders_reset(self) -> None:
        """Reset position of all sliders"""
        for channel in range(0, MAX_NUM_CHANNELS):
            position = self.slider_start_position
            slider = getattr(self.ui, "vertical_slider_%da" % channel)
            slider.setValue(position)
            if self.player_status is not None:
                pmixer.Channel(channel).set_volume(self.position_to_volume(position))

    def search(self, key: Literal["title", "dir"], value=str) -> AudioSetData:
        """Get AudioSetData using specify keyword"""
        try:
            if key == "title":
                for item in self.albums:
                    if item.title == value:
                        return item
            elif key == "dir":
                for item in self.albums:
                    if item.dir == value:
                        return item
            raise NameError("Error")
        except NameError:
            print(f'used key "{key}" not allowed')
            exit()

    def alert_message(self, header: str, text: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Alert")
        msg.setText(header)
        msg.setInformativeText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.exec()

    @staticmethod
    def position_to_volume(position: int = 0) -> float:
        """Logarithmic slider : Position from 0-100 convert to pmixer volume 0-1"""
        if position == 0:
            return 0
        #  position is between 0 and 100
        min_pos = 0
        max_pos = 100
        min_val = math.log(1)
        max_val = math.log(100)

        #  calculate adjustment factor
        scale = (max_val - min_val) / (max_pos - min_pos)
        vol = math.exp((position - min_pos) * scale + min_val)
        #  The result should be float between 0 and 1
        return float("{0:.2f}".format(vol / 100))

    @staticmethod
    def volume_to_position(volume: int = 0) -> int:
        """Get poistion 0-100 from by pmixer volume 0 - 1"""
        if volume == 0:
            return 0
        #  position is between 0 and 100
        min_pos = 0
        max_pos = 100
        min_val = math.log(1)
        max_val = math.log(100)

        #  The result should be between 0 and 100
        conv_volume = volume * 100
        scale = (max_val - min_val) / (max_pos - min_pos)
        pos = min_pos + (math.log(conv_volume) - min_val) / scale
        return int(pos)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    sys.exit(app.exec())
