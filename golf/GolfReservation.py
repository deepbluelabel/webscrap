from kowanas_util_python import KowanasTime

class GolfReservation:
    def __init__(self, date, status):
        self.date = date    
        self.status = status

    def __str__(self):
        return f'{KowanasTime.dateToString(self.date)} {self.status}'