from calendar import month_abbr
from matplotlib.pyplot import plot, stackplot, pie, bar, xlim, ylim, xticks, legend, show
from utils import prepare, getstores, getsongs, getcountries


def streamsbystoreovertime(data):
    """Streams by store over time"""
    stores = getstores(data)
    periods = []
    streams = [[] for _ in stores]

    for period in data:
        count = [0]*len(stores)
        periods.append(month_abbr[period.month] + ' ' + period.year[2:])

        for sale in period.sales:
            if sale.method == 'Streaming':
                for i in range(len(stores)):
                    if sale.store == stores[i]:
                        count[i] += sale.units
                        break

        for i in range(len(count)):
            streams[i].append(count[i])

    cloud = 0
    mp3 = 0
    unlimited = 0

    for i in range(len(stores)):
        if stores[i] == 'Amazon Cloud':
            cloud = i
            stores[i] = 'Amazon'
        elif stores[i] == 'Amazon MP3':
            mp3 = i
        elif stores[i] == 'Amazon Unlimited':
            unlimited = i
        elif stores[i] == 'YouTube Music Key':
            stores[i] = 'YouTube'

    for i in range(len(streams[0])):
        streams[cloud][i] += streams[unlimited][i] + streams[mp3][i]

    for i in sorted([mp3, unlimited], reverse=True):
        del stores[i], streams[i]

    plots = range(len(periods))
    prepare('line')
    stackplot(plots, streams, labels=stores)
    xlim(0, len(periods) - 1)
    xticks(plots, periods, rotation=90)
    legend()
    show()


def streamsbysongovertime(data):
    """Streams by song over time"""
    songs = getsongs(data)
    periods = []
    streams = [[] for _ in songs]

    for period in data:
        count = [0]*len(songs)
        periods.append(month_abbr[period.month] + ' ' + period.year[2:])

        for sale in period.sales:
            if sale.method == 'Streaming':
                for i in range(len(songs)):
                    if sale.song == songs[i]:
                        count[i] += sale.units
                        break

        for i in range(len(count)):
            streams[i].append(count[i])

    plots = range(len(periods))
    prepare('line')
    stackplot(plots, streams, labels=songs)
    xlim(0, len(periods) - 1)
    xticks(plots, periods, rotation=90)
    legend()
    show()


def streamsbycountry(data):
    """Streams by country"""
    countries = getcountries(data)
    streams = [0]*len(countries)

    for period in data:
        for sale in period.sales:
            if sale.method == 'Streaming':
                for i in range(len(countries)):
                    if sale.country == countries[i]:
                        streams[i] += sale.units
                        break

    sort = sorted(zip(streams, countries))
    streams = [count for count, country in sort]
    countries = [country for count, country in sort]
    prepare('pie')
    pie(streams, labels=countries, startangle=90)
    show()


def valuebycountry(data):
    """Value by country"""
    countries = getcountries(data)
    totals = [0]*len(countries)
    streams = [0]*len(countries)
    plots = range(len(countries))

    for period in data:
        for sale in period.sales:
            if sale.method == 'Streaming':
                for i in plots:
                    if sale.country == countries[i]:
                        totals[i] += sale.total
                        streams[i] += sale.units
                        break

    values = [totals[i]/streams[i] for i in plots]
    sort = sorted(zip(values, countries), reverse=True)
    values = [value for value, country in sort]
    countries = [country for value, country in sort]
    prepare('bar')
    bar(plots, values)
    xticks(plots, countries)
    show()


def valuebystore(data):
    """Value by store"""
    stores = getstores(data)

    for i in range(len(stores)):
        if stores[i] == 'Amazon MP3':
            del stores[i]
            break

    totals = [0] * len(stores)
    streams = [0] * len(stores)
    plots = range(len(stores))

    for period in data:
        for sale in period.sales:
            if sale.method == 'Streaming':
                for i in plots:
                    if sale.store == stores[i]:
                        totals[i] += sale.total
                        streams[i] += sale.units
                        break

    values = [totals[i] / streams[i] for i in plots]
    sort = sorted(zip(values, stores), reverse=True)
    values = [value for value, store in sort]
    stores = [store for value, store in sort]
    prepare('bar')
    bar(plots, values)
    xticks(plots, stores)
    show()


def downloadsovertime(data):
    """Downloads over time"""
    periods = []
    downloads = []

    for period in data:
        count = 0
        periods.append(month_abbr[period.month] + ' ' + period.year[2:])

        for sale in period.sales:
            if sale.method == 'Download':
                count += sale.units

        downloads.append(count)

    plots = range(len(periods))
    prepare('line')
    plot(plots, downloads)
    xlim(0, len(periods) - 1)
    ylim(bottom=0)
    xticks(plots, periods, rotation=90)
    show()


def totalbystore(data):
    """Total by store"""
    stores = getstores(data)

    for i in range(len(stores)):
        if stores[i] == 'Amazon MP3':
            del stores[i]
            break

    totals = [0] * len(stores)

    for period in data:
        for sale in period.sales:
            if sale.method == 'Streaming':
                for i in range(len(stores)):
                    if sale.store == stores[i]:
                        totals[i] += sale.total
                        break

    cloud = 0
    unlimited = 0

    for i in range(len(stores)):
        if stores[i] == 'Amazon Cloud':
            cloud = i
            stores[i] = 'Amazon'
        elif stores[i] == 'Amazon Unlimited':
            unlimited = i
        elif stores[i] == 'YouTube Music Key':
            stores[i] = 'YouTube'

    totals[cloud] += totals[unlimited]

    for i in sorted([unlimited], reverse=True):
        del stores[i], totals[i]

    sort = sorted(zip(totals, stores), reverse=True)
    totals = [total for total, store in sort]
    stores = [store for total, store in sort]
    prepare('bar')
    plots = range(len(stores))
    bar(plots, totals)
    xticks(plots, stores)
    show()
