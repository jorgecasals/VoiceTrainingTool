
class PlotModel:
    def __init__(self, x_data, y_data):
        if len(x_data) != len(y_data) :
            raise ValueError("In order to create a valid plot model, the x data needs have same values number as y data.")
        self.x_data = x_data
        self.y_data = y_data
