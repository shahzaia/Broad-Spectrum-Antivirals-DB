# importing libraries
import sys
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QCheckBox
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
from pubmed import parse

class Window(QDialog):
    def showDialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    def __init__(self, mw_home="", op_filter="All files (*.*)", sv_filter="All files (*.*)"):
        super(Window, self).__init__()
        self.msg = QMessageBox()
        self.setWindowTitle("Pubmed Scraper")
        self.setFixedHeight(650)
        self.setFixedWidth(400)
        # self.image_label = QLabel(self)
        # self.image_label.setAlignment(Qt.AlignCenter)

        self.formGroupBox = QGroupBox("Enter required inputs and hit OK")
        self.label_start_date = QLabel("Start Date", self)
        self.start_date_calendar = QDateEdit(self, calendarPopup=True)
        self.start_date_calendar.setDate(datetime.now().date())
        self.label_end_date = QLabel("End Date", self)
        self.end_date_calendar = QDateEdit(self, calendarPopup=True)
        self.end_date_calendar.setDate(datetime.now().date())
        self.file_name = QLabel("Enter Keyword", self)
        self.textbox = QLineEdit(self)
        self.__target = mw_home
        self.__open_f = op_filter
        self.__save_f = sv_filter
        self.createForm()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(self.reject)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)


    def clicker(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open File", self.__target, self.__open_f,
                                               options=QFileDialog.DontUseNativeDialog)
        if fname:
            return self.label.setText(fname)

    def getInfo(self):
        start_date = self.start_date_calendar.date()
        start_date = start_date.toString('yyyy/MM/dd')
        end_date = self.end_date_calendar.date()
        end_date = end_date.toString('yyyy/MM/dd')

        ###########################################################################

        # if self.textbox.text():
        #     file_name = '{}.{}'.format(self.textbox.text(), "csv")
        # else:
        #     file_name = '{}.{}'.format(datetime.now().strftime("%Y%m%d%H%M%S"), "csv")
        #     file_name = f"{spider.name}_{file_name}"
        # local_setting = get_project_settings()
        # local_setting['FEED_FORMAT'] = 'csv'
        # local_setting['FEED_URI'] = file_name
        # local_setting['CONCURRENT_REQUESTS'] = 2
        # local_setting['ROBOTSTXT_OBEY'] = False
        # local_setting[
        #     'USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
        # local_setting['LOG_LEVEL'] = 'DEBUG'
        # process = CrawlerProcess(local_setting)
        # crawler = process.create_crawler(spider)
        # process.crawl(crawler, start_date=start_date, end_date=end_date, filter=self.filter)
        # process.start()

        # stats = crawler.stats.get_stats()
        # filter_stats = spider.close
        parse(keyword=self.textbox.text(), start_date=start_date, end_date=end_date)
        self.msg.setWindowTitle("Process Finished")
        self.msg.setIcon(QMessageBox.Information)
        # self.msg.setText(
            # f"Processed finished Successfully.\nTotal Scraped Items: {stats.get('item_scraped_count', 0)},\n Total filtered items {stats.get('filtered', 0)}")
        self.msg.exec_()
        self.close()

    def createForm(self):
        layout = QVBoxLayout()
        # layout.addWidget(self.image_label)
        layout.addWidget(self.label_start_date)
        layout.addWidget(self.start_date_calendar)
        layout.addWidget(self.label_end_date)
        layout.addWidget(self.end_date_calendar)
        # layout.addWidget(self.checkbox)
        layout.addWidget(self.file_name)
        layout.addWidget(self.textbox)
        self.formGroupBox.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
