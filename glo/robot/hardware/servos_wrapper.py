import subprocess


class ServosWrapper:
    '''	Class to easily use the servos using python, (linux)
	'''

    baseCommand = ['mono', './robot/hardware/servoControllers/UscCmd']
    settingsFile = './robot/hardware/servoControllers/robotDesignSettings.txt'
    limits = [[0, 0], [0, 0], [0, 0], [0, 0]]

    def __init__(self):
        pass

    def execute(self, args):
        command = self.baseCommand + args
        exe = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        while exe.poll() == None:
            pass
        if exe.returncode != 0:
            raise Exception(exe.stderr.read())
        return exe.stdout.read()

    def set_position(self, num, target):
        target = self.limitate(num, target)
        self.execute(['--servo', "%i,%i" % (num, target)])
        pos = self.get_position(num)
        while pos != target:
            pos = self.get_position(num)
        return pos

    def limitate(self, num, value):
        value = max(self.limits[num][0], value)
        value = min(self.limits[num][1], value)
        return value

    def get_target(self, num):
        val = self.execute(['--status'])
        table = self.map_status(val)
        return table[num][1]

    def get_position(self, num):
        val = self.execute(['--status'])
        table = self.map_status(val)
        return int(table[num][4])

    def map_status(self, txt):
        table = []
        for l in txt.split('\n')[1:7]:
            line = []
            for column in l.split(' '):
                if column != '':
                    line.append(column)
            table.append(line)
        return table

    def set_limits(self, num, min, max):
        self.limits[num][0] = min
        self.limits[num][1] = max


if __name__ == "__main__":
    subprocess.call('clear')
    serv = ServosWrapper()
    serv.set_position(0, 0)
    print(serv.get_position(0))
    print ('done')

'''
Actions available with the executable:
  --list                   list available devices
  --configure FILE         load configuration file into device
  --getconf FILE           read device settings and write configuration file
  --restoredefaults        restore factory settings
  --program FILE           compile and load bytecode program
  --status                 display complete device status
  --bootloader             put device into bootloader (firmware upgrade) mode
  --stop                   stops the script running on the device
  --start                  starts the script running on the device
  --restart                restarts the script at the beginning
  --step                   runs a single instruction of the script
  --sub NUM                calls subroutine n (can be hex or decimal)
  --sub NUM,PARAMETER      calls subroutine n with a parameter (hex or decimal)
                           placed on the stack
  --servo NUM,TARGET       sets the target of servo NUM in units of
                           1/4 microsecond
  --speed NUM,SPEED        sets the speed limit of servo NUM
  --accel NUM,ACCEL        sets the acceleration of servo NUM to a value 0-255
Select which device to perform the action on (optional):
  --device 00001430        (optional) select device #00001430
  
  
 "--status" example: 
 #  target   speed   accel     pos
 0       0       0       0       0
 1    8000       0       0    8000
 2       0       0       0       0
 3       0       0       0       0
 4       0       0       0       0
 5       0       0       0       0
  
  
  
  
  
  
  
'''
