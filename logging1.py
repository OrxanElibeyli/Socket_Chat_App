from datetime import datetime

class Logging1():
    LOG_FILE_PATH='C:\\Users\\ORXAN\\Documents\\log.txt'

    

    def log(self,severity, message):
        file = open(self.LOG_FILE_PATH,'a')
        line = str(datetime.now()) + ':  ' + severity + ':  ' + message + '\n'
        #print(line)
        file.write(line)
        file.close()