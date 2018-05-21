import LoginController
import RegisterController
import TrainingController
import TrainerController

class ViewsNavigator:

    def __init__(self):
        self.login = (1, LoginController.LoginController)
        self.register = (2, RegisterController.RegisterController)
        self.trainings = (3, TrainingController.TrainingController)
        self.trainer = (4, TrainerController.TrainerController)
        self.views = {}

    def navigate_to_view(self, calling_view, view_name_builder):
        view = self.views.get(view_name_builder[0])

        if view == None:
            view = view_name_builder[1](calling_view)
            self.views[view_name_builder[0]] = view

        if calling_view != None:
            calling_view.hide()

        view.show()


navigator = ViewsNavigator()