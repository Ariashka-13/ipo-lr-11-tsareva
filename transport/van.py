from .vehicle import Vehicle

class Van(Vehicle):
    def __init__(self, vehicle_id, capacity, is_refrigerated = False):
        super().__init__(vehicle_id, capacity)
        self.is_refrigerated = is_refrigerated

    def __str__(self): 
        return super().__str__() + f". Наличие холодильника: {self.is_refrigerated}"