from PyQt5 import QtGui, QtCore, QtWidgets
from urllib.request import urlopen, urljoin
import sys
import pandas as pd
from bs4 import BeautifulSoup
"""Parser wth Gui, that can show page by url, and parse it by reg ex"""


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
        self.one_more_t_browser = QtWidgets.QTextBrowser()
        self.main_parse_t_browser = QtWidgets.QTextBrowser()
        self.open_button = QtWidgets.QPushButton("Open URL")
        self.parse_button = QtWidgets.QPushButton("Parse Page")
        self.url_string_edit = QtWidgets.QLineEdit('http://www.whiteguide-nordic.com/')
        self.parse_string_edit = QtWidgets.QLineEdit('for parsing')
        self.list_view = QtWidgets.QListView()
        self.item_model = QtGui.QStandardItemModel()

        # Storage
        self.url_str = 'http://www.whiteguide-nordic.com/'
        self.parse_str = ''
        self.parsed_list = []
        self.page = urlopen(self.url_str).read().decode('utf-8')

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
        self.form_layout.addRow(self.one_more_t_browser)
        self.form_layout.addRow(self.main_parse_t_browser)
        self.setLayout(self.form_layout)

    def on_open_button_clicked(self):
        self.url_str = self.url_string_edit.text()
        if self.url_str == '':
            self.t_bowser.setText("NO URL INSERTED")
        else:
            self.page = urlopen(self.url_str).read().decode('utf-8')
            self.t_bowser.setText(str(self.page))
        pass

    def on_parse_button_clicked(self):
        result = []
        soup = BeautifulSoup(self.page)
        self.parsed_list = soup.find('ul', {'class': "states"})
        self.parsed_list = self.parsed_list.find_all('li')
        for item in self.parsed_list:
            try:
                result.append(item.find('a').get('href'))
            except Exception as e:
                print(e)
        self.parsed_list = result
        # link_reg = re.compile(self.parse_string_edit.text(), re.IGNORECASE)
        # self.parsed_list = link_reg.findall(self.page)
        self.list_view_update()
        self.parse_all_countries()
        self.main_parse()

    def on_url_edit_finish(self):
        self.url_str = self.url_string_edit.text()
        self.on_open_button_clicked()
        pass

    def on_parse_edit_finish(self):
        pass

    def list_view_update(self):
        self.t_bowser_2.setText(str(self.parsed_list))
        print(self.parsed_list)

    def parse_all_countries(self):
        result = []
        for item in self.parsed_list:
            joined_url = urljoin(self.url_str, item)
            print("PARSING COUNTRIES:", self.parsed_list.index(item), "/", len(self.parsed_list))
            self.page = urlopen(joined_url)
            soup = BeautifulSoup(self.page)
            try:
                div_all = soup.find_all('div', {'class': 'node node-type-restaurant node-teaser'})
                # print("Dv_firt", div_first)

                for h2 in div_all:
                    # print("H@:", h2.find('h2').find('a').get("href"))
                    result.append(h2.find('h2').find('a').get("href"))

            except Exception as e:
                print("Got problem in parse all countries fun", e)
        # print("RESULT", result)
        self.parsed_list = result
        try:
            self.update_one_more_t_browser()
        except Exception as e:
            print("Got problem in calling update one more t browser:", e)

    def update_one_more_t_browser(self):
        self.one_more_t_browser.setText(str(self.parsed_list))

    def main_parse(self):
        result = []

        for item in self.parsed_list:
            try:
                print("MAIN PARSING IN PROCESS>>>", "PAGE:", self.parsed_list.index(item), '/', len(self.parsed_list))
                joined_url = urljoin(self.url_str, item)
                self.page = urlopen(joined_url)
                soup = BeautifulSoup(self.page)
                dev_0 = soup.find('div', {'class': "node node-type-restaurant node-full"})
                rest_name = dev_0.find('h1').text
                rest_total_points = dev_0.find('div', {"class": "points"})
                rest_points_all = rest_total_points.find_all('span')
                rest_points = {}
                for row in rest_points_all:
                    if len(row.text.split(':')) > 1:
                        rest_points[row.text.split(':')[0]] = row.text.split(':')[1].lstrip().rstrip()
                    else:
                        rest_points["main_point"] = row.text
                # print("Rest POINTS", rest_points)
                rest_symbols_div = dev_0.find("div", {'id': 'symbols'})
                rest_symbols_all = rest_symbols_div.find_all('img')
                rest_symbols = []
                for symbol in rest_symbols_all:
                    rest_symbols.append(symbol.get('alt'))
                rest_info = dev_0.find('ul', {'class': 'restaurant-info'})
                rest_info_all = rest_info.find_all('li')
                rest_info_result = {}

                for row in rest_info_all:
                    rest_info_result[row.text.split('\n')[1]] = row.text.split('\n')[2].lstrip().rstrip()
                # print("REST IFO RESULT:", rest_info_result)
                rest_description = dev_0.find_all('p')
                result.append({
                    'rest_name': rest_name,
                    'rest_points': rest_points.pop("main_point", "None"),
                    'food_points': rest_points.pop("Food rating", "None"),
                    'service_points': rest_points.pop("Service rating", "None"),
                    'rest_symbols': rest_symbols,
                    'rest_address': rest_info_result.pop("Address:", "None"),
                    'rest_phone': rest_info_result.pop("Phone:", "None"),
                    'rest_web_address': rest_info_result.pop("Web:", "None"),
                    'rest_seats': rest_info_result.pop("Seats:", "None"),
                    'opening_hours': rest_info_result.pop("Opening hours:", "None"),
                    'rest_description': rest_description
                })
            except Exception as e:
                print("Got error in main parse:", e, "On page", joined_url, "\n", rest_info_all)
        self.parsed_list = result
        self.main_parse_t_browser_update()
        data_frame = pd.DataFrame(self.parsed_list, columns=self.parsed_list[0].keys())

        data_frame.to_csv('rest.csv', ';', index=False)

    def main_parse_t_browser_update(self):
        self.main_parse_t_browser.setText(str(self.parsed_list))


qapp = QtWidgets.QApplication(sys.argv)
mw = MWindow()
mw.show()
sys.exit(qapp.exec_())
