import sys
from PyQt6 import QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow) :
    def __init__(self) :
        super(MainWindow, self).__init__()
        print("Initializing GUI")
        self.initUI()

    def initUI(self) :
        #self.setWindowTitle("Main Window")

        self.paper_widget_conainer = QtWidgets.QWidget()
        self.paper_widget_conainer_layout = QtWidgets.QVBoxLayout()
        self.paper_widget_conainer.setLayout(self.paper_widget_conainer_layout)

        paper_list_scroll_area = QtWidgets.QScrollArea()
        paper_list_scroll_area.setWidget(self.paper_widget_conainer)
        paper_list_scroll_area.setWidgetResizable(True)  # Make the scroll area resize with the window

        self.reference_widget_container = QtWidgets.QWidget()
        self.reference_widget_container_layout = QtWidgets.QVBoxLayout()
        self.reference_widget_container.setLayout(self.reference_widget_container_layout)

        reference_list_scroll_area = QtWidgets.QScrollArea()
        reference_list_scroll_area.setWidget(self.reference_widget_container)
        reference_list_scroll_area.setWidgetResizable(True)


        paper_list_layout = QtWidgets.QVBoxLayout()
        paper_list_layout.addWidget(paper_list_scroll_area)

        paper_info_layout = QtWidgets.QVBoxLayout()
        paper_info_layout.addWidget(reference_list_scroll_area)

        paper_list_widget = QtWidgets.QWidget()
        paper_info_widget = QtWidgets.QWidget()
        center_widget = QtWidgets.QWidget()

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(paper_list_widget)
        main_layout.addWidget(center_widget)
        main_layout.addWidget(paper_info_widget)

        self.cetntral_widget = QtWidgets.QWidget()
        self.cetntral_widget.setLayout(main_layout)
        self.setCentralWidget(self.cetntral_widget)

        print("GUI initialized")

        

if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)

    print("--------")

    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec())