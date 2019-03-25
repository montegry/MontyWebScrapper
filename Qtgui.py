from PyQt5 import  QtGui, QtCore, QtWidgets
from urllib.request import urlopen, urljoin
import sys
import re


class MWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Site Parser")

        #  Elements
        self.hbox_1 = QtWidgets.QHBoxLayout()
        self.hbox_2 = QtWidgets.QHBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.t_bowser = QtWidgets.QTextBrowser()
        self.t_bowser_2 = QtWidgets.QTextBrowser()
        self.open_button = QtWidgets.QPushButton("Open URL")
        self.parse_button = QtWidgets.QPushButton("Parse Page")
        self.url_string_edit = QtWidgets.QLineEdit('http://www.whiteguide-nordic.com/')
        self.parse_string_edit = QtWidgets.QLineEdit('<a[^>]+href=["\'](.*?)["\']')
        self.list_view = QtWidgets.QListView()
        self.item_model = QtGui.QStandardItemModel()

        # Storage
        self.url_str = ''
        self.parse_str = ''
        self.parsed_list = []
        self.page = ''

        # Connections
        self.open_button.clicked.connect(self.on_open_button_clicked)
        self.parse_button.clicked.connect(self.on_parse_button_clicked)
        self.url_string_edit.editingFinished.connect(self.on_url_edit_finish)
        self.parse_string_edit.editingFinished.connect(self.on_parse_edit_finish)

        # Layout connect

        self.hbox_1.addWidget(self.url_string_edit)
        self.hbox_1.addWidget(self.open_button)
        self.hbox_2.addWidget(self.parse_string_edit)
        self.hbox_2.addWidget(self.parse_button)
        self.form_layout.addRow(self.t_bowser)
        self.form_layout.addRow(self.hbox_1)
        self.form_layout.addRow(self.hbox_2)
        self.form_layout.addRow(self.t_bowser_2)

        self.setLayout(self.form_layout)

    def on_open_button_clicked(self):
        if self.url_str == '':
            self.t_bowser.setText("NO URL INSERTED")
        else:
            self.page = urlopen(self.url_str).read().decode('utf-8')
            self.t_bowser.setText(str(self.page))
        pass

    def on_parse_button_clicked(self):
        link_reg = re.compile(self.parse_string_edit.text(), re.IGNORECASE)
        self.parsed_list = link_reg.findall(self.page)
        self.list_view_update()

    def on_url_edit_finish(self):
        self.url_str = self.url_string_edit.text()
        self.on_open_button_clicked()
        pass

    def on_parse_edit_finish(self):
        pass

    def list_view_update(self):
        self.t_bowser_2.setText(str(self.parsed_list))
        print(self.parsed_list)

qapp = QtWidgets.QApplication(sys.argv)
mw = MWindow()
mw.show()
sys.exit(qapp.exec_())