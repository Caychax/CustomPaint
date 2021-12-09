# Inspired by PyQt5 Creating Paint Application In 40 Minutes
#  https://www.youtube.com/watch?v=qEgyGyVA1ZQ

# NB If the menus do not work then click on another application ad then click back
# and they will work https://python-forum.io/Thread-Tkinter-macOS-Catalina-and-Python-menu-issue

# PyQt documentation links are prefixed with the word 'documentation' in the code below and can be accessed automatically
#  in PyCharm using the following technique https://www.jetbrains.com/help/pycharm/inline-documentation.html

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QWidget, QLabel, QHBoxLayout, \
    QToolBar, QColorDialog, QSlider, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
import sys
from PyQt5.QtCore import Qt, QPoint, QRect


class PaintingApplication(QMainWindow):  # documentation https://doc.qt.io/qt-5/qmainwindow.html
    '''
    Painting Application class
    '''

    def __init__(self):
        super().__init__()
        self.w = None
        self.layout = QHBoxLayout()
        # set window title
        self.setWindowTitle("Paint Application")

        # set the windows dimensions
        top = 400
        left = 400
        width = 800
        height = 600
        self.setGeometry(top, left, width, height)

        # set the icon
        # windows version
        self.setWindowIcon(
            QIcon("./icons/paint-brush.png"))  # documentation: https://doc.qt.io/qt-5/qwidget.html#windowIcon-prop
        # mac version - not yet working
        # self.setWindowIcon(QIcon(QPixmap("./icons/paint-brush.png")))
        # image settings (default)
        self.image = QImage(self.size(),
                            QImage.Format_RGB32)  # documentation: https://doc.qt.io/qt-5/qimage.html#QImage-1
        self.image.fill(Qt.white)  # documentation: https://doc.qt.io/qt-5/qimage.html#fill-1

        # draw settings (default)
        """These are most of the variables used to change settigns on brushes and pens"""
        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.black  # documenation: https://doc.qt.io/qtforpython/PySide2/QtCore/Qt.html
        self.lineType = Qt.SolidLine
        self.caps = Qt.RoundCap
        # reference to last point recorded by mouse
        self.lastPoint = QPoint()  # documenation: https://doc.qt.io/qt-5/qpoint.html

        # set up menus
        mainMenu = self.menuBar()  # create and a menu bar
        fileMenu = mainMenu.addMenu(
            " File")  # add the file menu to the menu bar, the space is required as "File" is reserved in Mac
        brushSizeMenu = mainMenu.addMenu(" Brush Size")  # add the "Brush Size" menu to the menu bar
        brushColorMenu = mainMenu.addMenu(" Brush Colour")  # add the "Brush Colour" menu to the menu bar
        helpMenu = mainMenu.addMenu("Help")

        # save menu item
        saveAction = QAction(QIcon("./icons/save.png"), "Save",
                             self)  # create a save action with a png as an icon, documenation: https://doc.qt.io/qt-5/qaction.html
        saveAction.setShortcut(
            "Ctrl+S")  # connect this save action to a keyboard shortcut, documentation: https://doc.qt.io/qt-5/qaction.html#shortcut-prop
        fileMenu.addAction(
            saveAction)  # add the save action to the file menu, documentation: https://doc.qt.io/qt-5/qwidget.html#addAction
        saveAction.triggered.connect(
            self.save)  # when the menu option is selected or the shortcut is used the save slot is triggered, documenation: https://doc.qt.io/qt-5/qaction.html#triggered

        # opem menu item
        openAction = QAction(QIcon("./icons/folder.png"), "Open", self)
        openAction.setShortcut("Ctrl+O")
        fileMenu.addAction(openAction)
        openAction.triggered.connect(self.open)
        # clear
        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self)  # create a clear action with a png as an icon
        clearAction.setShortcut("Ctrl+C")  # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)  # add this action to the file menu
        clearAction.triggered.connect(
            self.clear)  # when the menu option is selected or the shortcut is used the clear slot is triggered

        # exit menu item
        exitAction = QAction(QIcon("./icons/exit.png"), "Leave", self)
        fileMenu.addAction(exitAction)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.triggered.connect(self.exitWindow)

        # brush thickness
        threepxAction = QAction(QIcon("./icons/threepx.png"), "3px", self)
        threepxAction.setShortcut("Ctrl+3")  # TODO changed the control options to be numbers
        brushSizeMenu.addAction(threepxAction)  # connect the action to the function below
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon("./icons/fivepx.png"), "5px", self)
        fivepxAction.setShortcut("Ctrl+5")
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon("./icons/sevenpx.png"), "7px", self)
        sevenpxAction.setShortcut("Ctrl+7")
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon("./icons/ninepx.png"), "9px", self)
        ninepxAction.setShortcut("Ctrl+9")
        brushSizeMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)

        # brush colors
        blackAction = QAction(QIcon("./icons/black.png"), "Black", self)
        blackAction.setShortcut("Ctrl+B")
        brushColorMenu.addAction(blackAction);
        blackAction.triggered.connect(self.black)

        redAction = QAction(QIcon("./icons/red.png"), "Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColorMenu.addAction(redAction);
        redAction.triggered.connect(self.red)

        greenAction = QAction(QIcon("./icons/green.png"), "Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColorMenu.addAction(greenAction);
        greenAction.triggered.connect(self.green)

        yellowAction = QAction(QIcon("./icons/yellow.png"), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColorMenu.addAction(yellowAction);
        yellowAction.triggered.connect(self.yellow)

        """Help Menu Section"""
        helpAction = QAction(QIcon("./icons/help.png"), "Help", self)
        helpMenu.addAction(helpAction)
        helpAction.setShortcut("Ctrl+H")
        helpAction.triggered.connect(self.helpWindow)
        """About menu section"""
        aboutAction = QAction(QIcon("./icons/about.png"), "About Me", self)
        helpMenu.addAction(aboutAction)
        aboutAction.setShortcut("Ctrl+A")
        aboutAction.triggered.connect(self.aboutWindow)

        """ToolBar Section"""
        # main tools
        self.mainTools = QToolBar("Tools")
        self.mainTools.setStyleSheet("color: #000;")
        self.tools = self.addToolBar(Qt.TopToolBarArea, self.mainTools)

        # Colour Wheel
        colorsAction = QAction(QIcon("./icons/color-wheel.png"), "Colors", self)
        colorsAction.setShortcut("Ctrl+W")
        brushColorMenu.addAction(colorsAction);
        colorsAction.triggered.connect(self.colorChoice)
        self.mainTools.addAction(colorsAction)
        self.colorBox = QWidget()
        self.colorBox.setFixedSize(80, 20)
        self.mainTools.addWidget(self.colorBox)
        self.colorBox.setStyleSheet("background-color:#000;border-radius: 2px;border: 5px solid #000;")
        self.bgColor = Qt.black

        # Slider
        self.brushSlider = QSlider(Qt.Horizontal)
        self.brushSlider.setMinimum(1)
        self.brushSlider.setMaximum(40)
        self.brushSlider.setTickInterval(5)
        self.brushSlider.setMaximumWidth(100)
        self.brushSlider.setMinimumHeight(30)
        # CSS for the custom slider: https://python.hotexamples.com/examples/PyQt4.QtGui/QSlider/setStyleSheet/python-qslider-setstylesheet-method-examples.html
        self.brushSlider.setStyleSheet("""
                QSlider::handle:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #FFFFFF, stop:1 #E3E3E3);
                    border: 1px solid #707070;
                    width: 10px;
                    margin-top: -4px;
                    margin-bottom: -4px;
                    border-radius: 4px;
                }

                QSlider::handle:horizontal:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #DEDEDE, stop:1 #C9C9C9);
                    border: 1px solid #4F4F4F;
                    border-radius: 4px;
                }

                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
                        stop: 0 #BFBFBF, stop: 1 #9E9E9E);
                    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
                        stop: 0 #9E9E9E, stop: 1 #858585);
                    border: 1px solid #777;
                    height: 10px;
                    border-radius: 4px;
                }

                QSlider::add-page:horizontal {
                    background: #fff;
                    border: 1px solid #707070;
                    height: 10px;
                    border-radius: 4px;
                }""")

        self.brushSlider.valueChanged.connect(self.onSliderChange)
        self.bsTitle = QLabel("Brush size:")
        self.bsTitle.setStyleSheet("text-decoration: underline;")
        self.bsLabel = QLabel(str(self.brushSlider.value()) + "px")
        self.mainTools.addWidget(self.bsTitle)
        self.mainTools.addWidget(self.brushSlider)
        self.mainTools.addWidget(self.bsLabel)

        # Draw Shapes
        # scribble
        self.penScribble = QPushButton()
        self.penScribble.setIcon(QIcon("./icons/scribble.png"))
        self.penScribble.pressed.connect(self.setScribble)
        self.mainTools.addWidget(self.penScribble)

        # squares
        self.penSquare = QPushButton()
        self.penSquare.setIcon(QIcon("./icons/square.png"))
        self.penSquare.pressed.connect(self.setSquares)
        self.mainTools.addWidget(self.penSquare)

        # Eraser
        self.penEraser = QPushButton()
        self.penEraser.setIcon(QIcon("./icons/eraser.png"))
        self.penEraser.pressed.connect(self.setEraser)
        self.mainTools.addWidget(self.penEraser)

        # caps toolbar
        self.capsTools = QToolBar("Cap Type")
        self.capsTools.setStyleSheet("color:#000;")
        self.capLabel = QLabel("Cap Type")
        self.capLabel.setStyleSheet("text-decoration: underline;")
        self.capsTools.addWidget(self.capLabel)

        # flat cap
        self.flatCap = QAction(QIcon("./icons/qpen-flat.png"), "Flat Cap", self)
        self.capsTools.addAction(self.flatCap)
        self.flatCap.triggered.connect(self.setFlatCap)
        # round cap
        self.roundCap = QAction(QIcon("./icons/qpen-roundcap.png"), "Round Cap", self)
        self.capsTools.addAction(self.roundCap)
        self.roundCap.triggered.connect(self.setRoundCap)
        # square cap
        self.squareCap = QAction(QIcon("./icons/qpen-square.png"), "Square Cap", self)
        self.capsTools.addAction(self.squareCap)
        self.squareCap.triggered.connect(self.setSquareCap)

        self.addToolBar(Qt.LeftToolBarArea, self.capsTools)

        # lineStyle toolbar
        self.lineTools = QToolBar("Line Type")
        self.addToolBar(Qt.LeftToolBarArea, self.lineTools)
        self.lineTools.setStyleSheet("color:#000;")
        self.lineLabel = QLabel("Line Type")
        self.lineLabel.setStyleSheet("text-decoration: underline;")
        self.lineTools.addWidget(self.lineLabel)
        # solid Line
        self.solidLine = QAction(QIcon("./icons/solid-line.png"), "Solid line", self)
        self.lineTools.addAction(self.solidLine)
        self.solidLine.triggered.connect(self.setSolidLine)
        # Dotted line
        self.dottedLine = QAction(QIcon("./icons/dotted-line.png"), "Dotted line", self)
        self.lineTools.addAction(self.dottedLine)
        self.dottedLine.triggered.connect(self.setDottedLine)
        # Dashed line
        self.dashLine = QAction(QIcon("./icons/dash-line.png"), "Dash line", self)
        self.lineTools.addAction(self.dashLine)
        self.dashLine.triggered.connect(self.setDashLine)

        self.drawShape = "square"

        self.begin, self.destination = QPoint(), QPoint()

        # pen var to enable modifications dynamically

    # event handlers
    def mousePressEvent(self,
                        event):  # when the mouse is pressed, documentation: https://doc.qt.io/qt-5/qwidget.html#mousePressEvent
        if event.buttons() & Qt.LeftButton:  # if the pressed button is the left button
            if self.drawShape == str("scribble"):
                self.drawing = True  # enter drawing mode
                self.lastPoint = event.pos()  # save the location of the mouse press as the lastPoint
                print(self.lastPoint)  # print the lastPoint for debigging purposes
            if self.drawShape == "square":
                self.begin = event.pos();
                self.destination = self.begin
                self.update()

    def mouseMoveEvent(self,
                       event):  # when the mouse is moved, documenation: documentation: https://doc.qt.io/qt-5/qwidget.html#mouseMoveEvent
        if event.buttons() & Qt.LeftButton:  # if there was a press, and it was the left button and we are in drawing mode
            if self.drawShape == "scribble":
                painter = QPainter(self.image)  # object which allows drawing to take place on an image
                # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here http://doc.qt.io/qt-5/qpen.html
                painter.setPen(QPen(self.brushColor, self.brushSize, self.lineType, self.caps, Qt.RoundJoin))
                painter.drawLine(self.lastPoint,
                                 event.pos())  # draw a line from the point of the orginal press to the point to where the mouse was dragged to
                self.lastPoint = event.pos()  # set the last point to refer to the point we have just moved to, this helps when drawing the next line segment
                self.update()  # call the update method of the widget which calls the paintEvent of this class
            if self.drawShape == "square":
                self.destination = event.pos()
                self.update()

    def mouseReleaseEvent(self,
                          event):  # when the mouse is released, documentation: https://doc.qt.io/qt-5/qwidget.html#mouseReleaseEvent
        if event.button() & Qt.LeftButton:  # if the released button is the left button, documenation: https://doc.qt.io/qt-5/qt.html#MouseButton-enum ,
            if self.drawShape == "scribble":
                self.drawing = False  # exit drawing mode
            if self.drawShape == "square":
                rect = QRect(self.begin, self.destination)
                painter = QPainter(self.image)
                painter.setPen(QPen(self.brushColor, self.brushSize, self.lineType, self.caps, Qt.RoundJoin))
                painter.drawRect(rect.normalized())
                self.begin, self.destination = QPoint(), QPoint()
                self.update()

    # paint events
    def paintEvent(self, event):
        # you should only create and use the QPainter object in this method, it should be a local variable
        canvasPainter = QPainter(
            self)  # create a new QPainter object, documenation: https://doc.qt.io/qt-5/qpainter.html
        canvasPainter.drawImage(self.rect(), self.image,
                                self.image.rect())  # draw the image , documentation: https://doc.qt.io/qt-5/qpainter.html#drawImage-1
        if self.drawShape == "square":
            if not self.begin.isNull() and not self.destination.isNull():
                canvasPainter.setPen(QPen(self.brushColor, self.brushSize, self.lineType, self.caps, Qt.RoundJoin))
                rect = QRect(self.begin, self.destination)
                canvasPainter.drawRect(rect.normalized())

    def setScribble(self):
        self.drawShape = "scribble"
        # this allows the color to be set back to the selected colour after the eraser has been used
        self.brushColor = self.bgColor
        print("scribble")

    def setSquares(self):
        self.drawShape = "square"
        # this allows the color to be set back to the selected colour after the eraser has been used
        self.brushColor = self.bgColor
        print("square")

    def setEraser(self):
        self.setScribble()
        self.brushColor = Qt.white

    # resize event - this fuction is called
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

    # slots
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if the file path is empty
            return  # do nothing and return
        self.image.save(filePath)  # save file image to the file path

    def clear(self):
        self.image.fill(Qt.white)  # fill the image with white, documentaiton: https://doc.qt.io/qt-5/qimage.html#fill-2
        self.update()  # call the update method of the widget which calls the paintEvent of this class

    def helpWindow(self):
        help = QMessageBox()
        help.setWindowIcon(QIcon("./icons/help.png"))
        help.setWindowTitle("Help")
        help.setText(
            "Hello and welcome to the Paint Application:\nHere we will tell you all you need to know to get started and creating your very own art")
        help.exec_()

    def aboutWindow(self):
        about = QMessageBox()
        about.setWindowIcon(QIcon("./icons/help.png"))
        about.setWindowTitle("About")
        about.setText(
            "Created by Roland Blanchard, assignment 2 for Comp Sci module HGP.\n To create and add functionality to a basic paint application")
        about.exec_()

    def threepx(self):  # the brush size is set to 3
        self.brushSize = 3

    def fivepx(self):
        self.brushSize = 5

    def sevenpx(self):
        self.brushSize = 7

    def ninepx(self):
        self.brushSize = 9

    def black(self):  # the brush color is set to black
        self.brushColor = Qt.black

    def black(self):
        self.brushColor = Qt.black

    def red(self):
        self.brushColor = Qt.red

    def green(self):
        self.brushColor = Qt.green

    def yellow(self):
        self.brushColor = Qt.yellow

    def colorChoice(self):
        self.brushColor = QColorDialog.getColor()
        self.bgColor = self.brushColor
        self.colorBox.setStyleSheet("background-color:%s;" % self.brushColor.name())

    def onSliderChange(self):
        self.brushSize = self.brushSlider.value()
        self.bsLabel.setText(str(self.brushSlider.value()) + "px")

    def setRoundCap(self):
        self.caps = Qt.RoundCap
        print(self.caps)

    def setFlatCap(self):
        self.caps = Qt.FlatCap
        print(self.caps)

    def setSquareCap(self):
        self.caps = Qt.SquareCap
        print(self.caps)

    def setSolidLine(self):
        self.lineType = Qt.SolidLine
        print(self.lineType)

    def setDottedLine(self):
        self.lineType = Qt.DotLine
        print(self.lineType)

    def setDashLine(self):
        self.lineType = Qt.DashLine
        print(self.lineType)

    # Exit the application method
    def exitWindow(self):
        self.close()

    # open a file
    def open(self):
        '''
        This is an additional function which is not part of the tutorial. It will allow you to:
         - open a file doalog box,
         - filter the list of files according to file extension
         - set the QImage of your application (self.image) to a scaled version of the file)
         - update the widget
        '''
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if not file is selected exit
            return
        with open(filePath, 'rb') as f:  # open the file in binary mode for reading
            content = f.read()  # read the file
        self.image.loadFromData(content)  # load the data into the file
        width = self.width()  # get the width of the current QImage in your application
        height = self.height()  # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height)  # scale the image from file and put it in your QImage
        self.update()  # call the update method of the widget which calls the paintEvent of this class


# this code will be executed if it is the main module but not if the module is imported
#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaintingApplication()
    window.show()
    app.exec()  # start the event loop running
