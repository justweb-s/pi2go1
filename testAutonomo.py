import time
import pi2go

pi2go.init()

# Configurazioni
speed_forward = 60
speed_turn = 60
safe_distance = 30
loop_delay = 0.1
turn_direction = 1
stop_delay = 0.5
turn_delay = 1

try:
    while True:
        distance = pi2go.getDistance()
        print("Distanza: {:.1f} cm".format(distance))

        if distance > safe_distance:
            pi2go.forward(speed_forward)
        else:
            pi2go.stop()
            time.sleep(stop_delay)
            pi2go.spinRight(speed_turn)
        time.sleep(loop_delay)

except KeyboardInterrupt:
    print("Interruzione manuale tramite tastiera.")

finally:
    pi2go.cleanup()
