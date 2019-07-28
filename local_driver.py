import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


class motor:
    def __init__(self, pwm, i1, i2):  # (22,17,27) (16.20,21) (23,24,18)
        self.pwm = pwm
        self.i1 = i1
        self.i2 = i2
        GPIO.setup(pwm, GPIO.OUT)
        GPIO.setup(i1, GPIO.OUT)
        GPIO.setup(i2, GPIO.OUT)
        self.p = GPIO.PWM(pwm, 80)

    def start(self, qwq):
        if qwq < 0:
            GPIO.output(self.i1, GPIO.HIGH)
            GPIO.output(self.i2, GPIO.LOW)
        elif qwq > 0:
            GPIO.output(self.i1, GPIO.LOW)
            GPIO.output(self.i2, GPIO.HIGH)
        self.p.start(abs(qwq))


if __name__ == '__main__':
    p = motor(22, 17, 27)
    q = motor(16,20, 21)
    r = motor(23, 24, 18)
    time.sleep(1)
    try:
        while True:
            p.start(0)
            q.start(100)
            r.start(0)
            pass
    except:
        # GPIO.cleanup()
        pass
    GPIO.cleanup()
