import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
import utils
import math


class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.timer_id = -1
        self.init_ui()

    def init_ui(self):
        self.image_to_process = QLineEdit('square')
        self.noSteps = QLineEdit('200')
        self.noDetectors = QLineEdit('50')
        self.coneSpan = QLineEdit('0.5')

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
        h_box_parameters.addWidget(self.image_to_process)
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

        self.imageSinogram = QLabel(self)
        sinogramPixmap = QPixmap('test_images/sinogram.bmp').scaledToHeight(600)
        self.imageSinogram.setPixmap(sinogramPixmap)


        h_box_images = QtWidgets.QHBoxLayout()
        h_box_images.addLayout(images_grid)
        h_box_images.addWidget(self.imageSinogram)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box_parameters)
        v_box.addLayout(h_box_slider)
        v_box.addLayout(h_box_images)
        v_box.setAlignment(Qt.AlignTop)

        self.setLayout(v_box)
        self.setWindowTitle('Tomography')
        self.resize(1200, 700)
        self.show()

    def timerEvent(self, event):
        self.killTimer(self.timer_id)
        self.timer_id = -1
        detector_pixmap = QPixmap("out_detectors/" + str(self.slider.value()) + ".bmp").scaled(300, 300)
        self.imageTwo.setPixmap(detector_pixmap)
        intermediate_step = QPixmap("out_end/" + str(self.slider.value()) + ".bmp").scaled(300, 300)
        self.imageThree.setPixmap(intermediate_step)

    def value_changed(self):
        self.sliderValueLabel.setText(str(self.slider.value()))
        if self.timer_id != -1:
            self.killTimer(self.timer_id)

        self.timer_id = self.startTimer(60)

    def button_pushed(self):
        print("started tomography")
        image_name = self.image_to_process.text()
        image_to_process = QPixmap("test_images/" + image_name + ".bmp").scaled(300, 300)
        self.imageOne.setPixmap(image_to_process)
        QApplication.processEvents()
        steps = int(self.noSteps.text())
        detectors = int(self.noDetectors.text())
        scope_string = self.coneSpan.text()
        scope = float(self.coneSpan.text()) * math.pi
        self.slider.setMaximum(steps-1)
        self.slider.setValue(0)
        image = Image.open("test_images/" + image_name + ".bmp")
        pixels = image.load()
        radius = image.size[0] // 2
        sinogram = utils.doTomography(scope, steps, detectors, radius, pixels, image_name)
        img = Image.new('RGB', (detectors, steps))
        img.putdata(sinogram)
        file_name = image_name + "_" + str(steps) + "_" + str(detectors) + "_" + scope_string + ".bmp"
        img.save("out_sinogram/" + file_name, "BMP")
        sinogram_pixmap = QPixmap("out_sinogram/" + file_name).scaledToHeight(600)
        self.imageSinogram.setPixmap(sinogram_pixmap)
        sinogram_image = Image.open("out_sinogram/" + file_name)
        sinogram_pixels = sinogram_image.load()
        utils.generate_out_images(scope, radius, steps, detectors, sinogram_pixels)

        end_pixmap = QPixmap("out_end/" + str(steps-1) + ".bmp").scaled(300, 300)
        self.imageFour.setPixmap(end_pixmap)

        intermediate_step = QPixmap("out_end/" + str(self.slider.value()) + ".bmp").scaled(300, 300)
        self.imageThree.setPixmap(intermediate_step)

        detector_pixmap = QPixmap("out_detectors/" + str(self.slider.value()) + ".bmp").scaled(300, 300)
        self.imageTwo.setPixmap(detector_pixmap)
        print("ended tomography")



app = QtWidgets.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())