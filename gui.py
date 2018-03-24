import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.timer_id = -1
        self.init_ui()

    def init_ui(self):
        self.noSteps = QLineEdit('Steps No.')
        self.noDetectors = QLineEdit('Detectors No.')
        self.coneSpan = QLineEdit('Cone span (radians)')

        self.doTomographyButton = QPushButton('doTomography()')
        self.doTomographyButton.clicked.connect(self.button_pushed)
        self.sliderValueLabel = QLabel('0')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.value_changed)

        self.imageOne = QLabel(self)
        pixmapOne = QPixmap('out/rectangle_down.bmp').scaled(300, 300)
        self.imageOne.setPixmap(pixmapOne)

        self.imageTwo = QLabel(self)
        pixmapTwo = QPixmap('out/rectangle_down.bmp').scaled(300, 300)
        self.imageTwo.setPixmap(pixmapTwo)

        self.imageThree = QLabel(self)
        pixmapThree = QPixmap('out/rectangle_down.bmp').scaled(300, 300)
        self.imageThree.setPixmap(pixmapThree)

        self.imageFour = QLabel(self)
        pixmapFour = QPixmap('out/rectangle_down.bmp').scaled(300, 300)
        self.imageFour.setPixmap(pixmapFour)

        h_box_parameters = QtWidgets.QHBoxLayout()
        h_box_parameters.addWidget(self.noSteps)
        h_box_parameters.addWidget(self.noDetectors)
        h_box_parameters.addWidget(self.coneSpan)
        h_box_parameters.addWidget(self.doTomographyButton)

        h_box_slider = QtWidgets.QHBoxLayout()
        h_box_slider.addWidget(self.sliderValueLabel)
        h_box_slider.addWidget(self.slider)

        images_grid = QGridLayout()
        images_grid.addWidget(self.imageOne, 0, 0)
        images_grid.addWidget(self.imageTwo, 1, 0)
        images_grid.addWidget(self.imageThree, 0, 1)
        images_grid.addWidget(self.imageFour, 1, 1)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box_parameters)
        v_box.addLayout(h_box_slider)
        v_box.addLayout(images_grid)
        v_box.setAlignment(Qt.AlignTop)

        h_box_main = QtWidgets.QHBoxLayout()
        h_box_main.addLayout(v_box)

        self.imageSinogram = QLabel(self)
        sinogramPixmap = QPixmap('test_images/sinogram.bmp').scaledToHeight(600)
        self.imageSinogram.setPixmap(sinogramPixmap)

        h_box_main.addWidget(self.imageSinogram)

        self.setLayout(h_box_main)
        self.setWindowTitle('Tomography')
        self.resize(700, 700)
        self.show()

    def timerEvent(self, event):
        self.killTimer(self.timer_id)
        self.timer_id = -1
        print(self.slider.value())

    def value_changed(self):
        self.sliderValueLabel.setText(str(self.slider.value()))
        if self.timer_id != -1:
            self.killTimer(self.timer_id)

        self.timer_id = self.startTimer(800)

    def button_pushed(self):
        steps = int(self.noSteps.text())
        dectors = int(self.noDetectors.text())
        scope = float(self.coneSpan.text())
        self.slider.setMaximum(steps)
        print(str(steps) + ' ' + str(dectors) + ' ' + str(scope))



app = QtWidgets.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())