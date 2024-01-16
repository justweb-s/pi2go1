import time
import pi2go

pi2go.init()

# Definizione delle velocità
speed_forward = 60
speed_turn = 60

# Definizione della distanza di sicurezza (in cm)
safe_distance = 5

try:
    while True:
        # Misurazione della distanza dall'ostacolo
        distance = pi2go.getDistance()

        # Stampa della distanza (con le parentesi come richiesto)
        print("Distanza: {:.1f} cm".format(distance))

        # Controllo della distanza dall'ostacolo
        if distance > safe_distance:
            # Se non ci sono ostacoli, continua ad andare avanti
            pi2go.forward(speed_forward)
        else:
            # Se c'è un ostacolo, si ferma e gira
            pi2go.stop()
            time.sleep(0.5)  # Breve pausa
            pi2go.spinRight(speed_turn)
            time.sleep(1)  # Tempo di rotazione

except KeyboardInterrupt:
    # Interruzione con Ctrl+C
    pass

finally:
    # Pulizia e rilascio delle risorse
    pi2go.cleanup()
