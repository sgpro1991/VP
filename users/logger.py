from .models import Logging

class Logger:
    """Класс который добавляет логирование.
       Аргументы кто что создал
    """
    def __init__(self,user,filter_actions,message):
        insert = Logging(user=user,message=message,filter_actions=filter_actions)
        insert.save()
        print('good')
