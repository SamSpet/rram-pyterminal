import serial
from Lib import CommandMap as CM
import USER
from Applications import MNIST
from Lib import DEMO, UTF8, RRAM, VECTOR, DNN, TEST
from Board import EEPROM, PM, LED, DF, DAC, TC, BOARD

VID = '0x03EB'    # Atmel
PID = '0x204B'    # LUFA USB to Serial Demo Application
BAUDRATE = 115200 # Baudrate for COM port connections
TIMEOUT = 30       # Seconds


def connect():
    """ Automatically connect to the board based on the VID and PID information, and get the board version to make
        sure the correct board is connected.
    """
    from serial.tools import list_ports
    for port in list_ports.comports():
        if port.vid == int(VID, 0) and port.pid == int(PID, 0):
            global ser
            ser = serial.Serial(port.name, baudrate=BAUDRATE, timeout=TIMEOUT)
            try:
                version = BOARD.version(False)
                print('[INFO] Evaluation board with version ' + version + ' connected @ ' + port.name)
                # Fix the problem so that we don't have to init the TC every time we relaunch PyTerminal
                ser.write(str.encode(CM.CM_RRAM + ' \n'))
                return True
            except:
                print('[ERROR] Unable to retrieve board version')
                break
    return False

def alive():
    """ Check if the board is still connected, if not we try to connect it again
    """
    try:
        ser.in_waiting
        return True
    except:
        return connect()

def send_command(command, verbal):
    """ Send the command to the board through COM port, print the response, and return the response.

    Args:
        verbal (bool): Whether to print the response or not.
        parameters (list): Command in List form.
    """
    # Send out the command and Give it some time to process
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.write(str.encode(command + '\n'))

    # Wait for EOT
    response = b''
    while 1:
        char = ser.read(1)
        if char == b'':
            print('Read Timeout')
            break
        elif char == UTF8.EOT:
            # For readability, we insert \n for some cases
            if verbal and response != b'' and response.decode('utf-8')[-1] != '\n':
                print('')
            break
        else:
            if   char[0] & 0x80 == 0:
                extra_byte = 0
            elif char[0] & 0x20 == 0:
                extra_byte = 1
            elif char[0] & 0x10 == 0:
                extra_byte = 2
            elif char[0] & 0x08 == 0:
                extra_byte = 3
            char += ser.read(extra_byte)
            if verbal:
                print(char.decode('utf-8'), end='', flush=True)
        response += char

    return response.decode('utf-8')


def unknown(parameters):
    """ Print out the unknown command

    Args:
        parameters (list): Command in List form.
    """
    print('Unknown Command: ' + ' '.join(parameters) + '(From PyTerminal)')


def decode_command(command):
    """ Split the command and decode it based on the first parameter

    Args:
        command (str): Original human readable command
    """
    try:
        # Split the command and fill up to 8 list elements
        parameters = command.split()
        for i in range(len(parameters), 16):
            parameters.append('')

        if   parameters[0] == "BOARD" :  BOARD.decode(parameters)
        elif parameters[0] == "PM"    :     PM.decode(parameters)
        elif parameters[0] == "DAC"   :    DAC.decode(parameters)
        elif parameters[0] == "DF"    :     DF.decode(parameters)
        elif parameters[0] == "EEPROM": EEPROM.decode(parameters)
        elif parameters[0] == "LED"   :    LED.decode(parameters)
        elif parameters[0] == "TC"    :     TC.decode(parameters)
        elif parameters[0] == "DEMO"  :   DEMO.decode(parameters)
        elif parameters[0] == "RRAM"  :   RRAM.decode(parameters)
        elif parameters[0] == "VECTOR": VECTOR.decode(parameters)
        elif parameters[0] == "DNN"   :    DNN.decode(parameters)
        elif parameters[0] == "TEST"  :   TEST.decode(parameters)
        elif parameters[0] == "USER"  :   USER.decode(parameters)
        elif parameters[0] == "MNIST" :  MNIST.decode(parameters)
        else: unknown(parameters)

    # If the atmel is reset, we need to reopen it again
    except serial.SerialException:
        ser.close()
        ser.open()
        decode_command(command)
    except Exception as e:
        print('[ERROR] Wrong command format')
        print(e)