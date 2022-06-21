from datetime import datetime as dt

class KowanasTime:
    @classmethod
    def dateToString(self, date, format='%Y%m%d'):
        return date.strftime(format)
        
    @classmethod
    def nowToString(self, format='%Y%m%d %H%M%S'):
        return dt.now().strftime(format)