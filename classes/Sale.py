class Sale:
    def __init__(self, period, store, country, release, song, method, units, total):
        self.period = period
        self.store = store
        self.country = country
        self.release = release
        self.song = song
        self.method = method
        self.units = int(units)
        self.total = float(total)
