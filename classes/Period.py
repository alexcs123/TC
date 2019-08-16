class Period:
    def __init__(self, month, year, sales=None):
        if sales is None:
            sales = []

        self.month = int(month)
        self.year = year
        self.sales = sales
