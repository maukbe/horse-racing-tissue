class HorseData:
    def __init__(self, number, race_info, form, trainer_form, jockey_form):
        self.number = number
        self.race_info = race_info
        self.form = form
        self.trainer_form = trainer_form
        self.jockey_form = jockey_form
        
    @property
    def number(self):
        return self.__number
        
    @number.setter
    def number(self, number):
        self.__number = number
        
    @property
    def race_info(self):
        return self.__race_info
        
    @race_info.setter
    def race_info(self, race_info):
        self.__race_info = race_info
    
    @property
    def form(self):
        return self.__form

    @form.setter
    def form(self, form):
        self.__form = form
        
    @property
    def trainer_form(self):
        return self.__trainer_form
    
    @trainer_form.setter
    def trainer_form(self, trainer_form):
        self.__trainer_form = trainer_form
    
    @property
    def jockey_form(self):
        return self.__jockey_form
    
    @jockey_form.setter
    def jockey_form(self, jockey_form):
        self.__jockey_form = jockey_form