import time
import pi2go

pi2go.init()

# Configurazioni per il sensore a ultrasuoni
speed_forward = 50
speed_turn = 50
safe_distance_ultrasonic = 10
loop_delay = 0.1
stop_delay = 0.1
turn_delay = 0.2

# Rilevamento versione Pi2Go
vsn = pi2go.version()
if vsn == 1:
    print("Running on Pi2Go")
else:
    print("Running on Pi2Go-Lite")

try:
    while True:
        distance = pi2go.getDistance()
        print("Distanza ultrasuoni: {:.1f} cm".format(distance))

        # Controllo sensori IR
        ir_left = pi2go.irLeft()
        ir_centre = pi2go.irCentre() if vsn == 1 else False
        ir_right = pi2go.irRight()

        # Logica di movimento
        if distance > safe_distance_ultrasonic and not (ir_left or ir_centre or ir_right):
            pi2go.forward(speed_forward)
        else:
            pi2go.stop()
            time.sleep(stop_delay)
            # Determinare la direzione di rotazione in base ai sensori IR
            if ir_right and not ir_left:
                pi2go.spinLeft(speed_turn)
            elif ir_left and not ir_right:
                pi2go.spinRight(speed_turn)
            else:
                # Se entrambi i sensori IR o nessuno rilevano ostacoli, scegli una direzione casuale
                if random.randint(0, 1) == 0:
                    pi2go.spinLeft(speed_turn)
                else:
                    pi2go.spinRight(speed_turn)
            time.sleep(turn_delay)

        time.sleep(loop_delay)

except KeyboardInterrupt:
    print("Interruzione manuale tramite tastiera.")

finally:
    pi2go.cleanup()
