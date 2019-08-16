from csv import reader
from matplotlib.pyplot import figure, subplots_adjust
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QDesktopWidget
from classes.Sale import Sale
from classes.Period import Period


def collect():
    year = '2000'
    collection = []
    running = False

    try:
        while True:
            for month in range(12):
                month = str(month + 1).zfill(2)

                try:
                    csv = open('reports/tunecore-musicsales-sales_period-' + month + '-' + year + '.csv')
                    running = True
                    period = Period(month, year)
                    scanner = reader(csv)
                    next(scanner)

                    for row in scanner:
                        period.sales.append(Sale(row[0], row[2], row[3], row[6], row[7], row[13], row[14], row[19]))

                    csv.close()
                    collection.append(period)
                except IOError:
                    if running:
                        raise EOFError

            year = str(int(year) + 1)
    except EOFError:
        return collection


def ui(reports):
    tc = collect()

    app = QApplication([])
    win = QWidget()
    lay = QVBoxLayout()

    for report in reports:
        button = QPushButton(report.__doc__)
        button.clicked.connect(call(report, tc))
        lay.addWidget(button)

    win.setLayout(lay)
    win.show()

    screen = QDesktopWidget.screenGeometry(QDesktopWidget())
    window = win.geometry()
    win.move(screen.width() - window.width() - 100, (screen.height() - window.height()) / 2)

    app.exec_()


def call(function, argument):
    return lambda: function(argument)


def prepare(chart):
    if chart == 'line':
        figure(figsize=[8, 6])
        subplots_adjust(left=0.08, bottom=0.13, right=0.95, top=0.95)
    elif chart == 'pie':
        figure(figsize=[6, 6])
        subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
    elif chart == 'bar':
        figure(figsize=[8, 6])
        subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.95)


def getstores(data):
    stores = []

    for period in data:
        for sale in period.sales:
            if sale.store not in stores:
                stores.append(sale.store)

    return stores


def getsongs(data):
    songs = []

    for period in data:
        for sale in period.sales:
            if sale.song not in songs:
                songs.append(sale.song)

    return songs


def getcountries(data):
    countries = []

    for period in data:
        for sale in period.sales:
            if sale.country not in countries:
                countries.append(sale.country)

    return countries
