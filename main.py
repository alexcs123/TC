from reports import *
from utils import ui


if __name__ == '__main__':
    reports = [streamsbystoreovertime,
               streamsbysongovertime,
               streamsbycountry,
               valuebycountry,
               valuebystore,
               downloadsovertime,
               totalbystore]

    ui(reports)
