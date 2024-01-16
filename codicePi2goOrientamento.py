import pi2go
import time
import sys
import tty
import termios

# Funzioni per la lettura dei tasti
def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

def remote_control():
    speed = 60
    print("Modalità controllo remoto attivata. Usa 'w', 'a', 's', 'd' per muoverti, '+' e '-' per regolare la velocità, ' ' per fermarti. Premi 'q' per uscire.")
    while True:
        keyp = readkey()
        if keyp == 'w' or ord(keyp) == 16:
            pi2go.forward(speed)
            print('Avanti', speed)
        elif keyp == 'z' or ord(keyp) == 17:
            pi2go.reverse(speed)
            print('Indietro', speed)
        elif keyp == 'd' or ord(keyp) == 18:
            pi2go.spinRight(speed)
            print('Gira a destra', speed)
        elif keyp == 'a' or ord(keyp) == 19:
            pi2go.spinLeft(speed)
            print('Gira a sinistra', speed)
        elif keyp == '.' or keyp == '>':
            speed = min(100, speed+10)
            print('Velocità aumentata:', speed)
        elif keyp == ',' or keyp == '<':
            speed = max(0, speed-10)
            print('Velocità ridotta:', speed)
        elif keyp == ' ':
            pi2go.stop()
            print('Fermo')
        elif keyp == 'q':
            print("Uscita dalla modalità controllo remoto.")
            break

def automatic_mode():
    print("Modalità automatica attivata. Premi 'q' per uscire.")
    while True:
        keyp = readkey()
        dist = pi2go.getDistance()
        if dist > 0.2:  # Valore soglia per l'ostacolo
            pi2go.forward(30)
            print(f'Movimento avanti: Distanza rilevata = {dist:.2f}m')
        else:
            pi2go.spinRight(30)
            print(f'Gira a destra: Ostacolo rilevato a {dist:.2f}m')
            time.sleep(1)
        if keyp == 'q':
            print("Uscita dalla modalità automatica.")
            break

def testLED():
    vsn = pi2go.version()
    try:
        if vsn != 1:
            print("This program only runs on the full Pi2Go")
        else:
            while True:
                pi2go.setAllLEDs(0, 0, 0)  # start with all OFF
                for i in range(4):
                    pi2go.setLED(i, 4095, 0, 0)  # set to Red
                    print('Red')
                    time.sleep(0.2)
                    pi2go.setLED(i, 0, 0, 0)
                for i in range(4):
                    pi2go.setLED(i, 0, 4095, 0)  # set to Green
                    print('Green')
                    time.sleep(0.2)
                    pi2go.setLED(i, 0, 0, 0)
                for i in range(4):
                    pi2go.setLED(i, 0, 0, 4095)  # set to Blue
                    print('Blue')
                    time.sleep(0.2)
                    pi2go.setLED(i, 0, 0, 0)
                for i in range(4):
                    pi2go.setLED(i, 4095, 4095, 4095)  # set to White
                    print('White')
                    time.sleep(0.2)
                    pi2go.setLED(i, 0, 0, 0)
                keyp = readkey()
                if keyp == 'q':  # Controllo per uscire
                    break
    except KeyboardInterrupt:
        pi2go.cleanup()


def LEDtest():
    LEDon = 4095
    LEDoff = 0

    vsn = pi2go.version()
    try:
        if vsn != 1:
            print("This program only runs on the full Pi2Go")
        else:
            while True:
                pi2go.setAllLEDs(LEDon, LEDoff, LEDoff)
                print("Red")
                time.sleep(2)
                pi2go.setAllLEDs(LEDoff, LEDon, LEDoff)
                print("Green")
                time.sleep(2)
                pi2go.setAllLEDs(LEDoff, LEDoff, LEDon)
                print("Blue")
                time.sleep(2)
                pi2go.setAllLEDs(LEDon, LEDon, LEDon)
                print("White")
                time.sleep(2)
                pi2go.setAllLEDs(LEDoff, LEDoff, LEDoff)
                keyp = readkey()
                if keyp == 'q':  # Controllo per uscire
                    break
    except KeyboardInterrupt:
        print("Programma interrotto dall'utente")
    finally:
        pi2go.cleanup()

# Inizializzazione
pi2go.init()

try:
    while True:
        print("1: Controllo remoto\n2: Modalità automatica\n3: testLED\n4: LEDtest")
        mode = readchar()
        if mode == '1':
            remote_control()
        elif mode == '2':
            automatic_mode()
        elif mode == '3':
            testLED()
        elif mode == '4':
            LEDtest()
        elif ord(mode) == 3:
            break

except KeyboardInterrupt:
    print("Programma interrotto dall'utente")

finally:
    pi2go.cleanup()
