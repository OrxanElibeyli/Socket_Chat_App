from datetime import datetime

class Logging1():
    LOG_FILE_PATH='C:\\Users\\ORXAN\\Documents\\log.txt'

    
    def log(self,severity, message):
        with open(self.LOG_FILE_PATH, 'a', encoding='utf8') as file:
            line = str(datetime.now()) + ':  ' + severity + ':  ' + message + '\n'
            file.write(line)
