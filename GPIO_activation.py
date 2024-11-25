# wires numbers and modes ###
import RPi.GPIO as GPIO

# Pin configuration
lch_pin = 6  # Latch control pin (purple)
rm_dir_pin = 5  # Right motor direction pin (yellow)
lm_dir_pin = 21  # Left motor direction pin (blue)
rm_pin = 13  # Right motor PWM pin (white)
lm_pin = 12  # Left motor PWM pin (white)
arm1_pin = 20  # Arm motor 1 control pin (green)
arm2_pin = 16  # Arm motor 2 control pin (orange)

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Setup pins as output
GPIO.setup(lch_pin, GPIO.OUT)
GPIO.setup(rm_dir_pin, GPIO.OUT)
GPIO.setup(lm_dir_pin, GPIO.OUT)
GPIO.setup(arm1_pin, GPIO.OUT)
GPIO.setup(arm2_pin, GPIO.OUT)

GPIO.setup(rm_pin, GPIO.OUT)  # Right motor
rm_pwm = GPIO.PWM(rm_pin, 1000)  # 1 kHz frequency
GPIO.setup(lm_pin, GPIO.OUT)  # Left motor
lm_pwm = GPIO.PWM(lm_pin, 1000)  # 1 kHz frequency

# Start PWM with 0% duty cycle (off)
rm_pwm.start(0)
lm_pwm.start(0)


def low_output():
    """
        Set all outputs to low, effectively stopping all motors and
        setting the system to an idle state.
    """

    GPIO.output(lch_pin, GPIO.LOW)
    GPIO.output(arm1_pin, GPIO.LOW)
    GPIO.output(arm2_pin, GPIO.LOW)
    GPIO.output(rm_dir_pin, GPIO.LOW)
    GPIO.output(lm_dir_pin, GPIO.LOW)
    rm_pwm.ChangeDutyCycle(10)
    lm_pwm.ChangeDutyCycle(10)


def GPIO_activation(lm, rm, latch, up_arm, down_arm, back_lm, back_rm):
    """
        Activate GPIO pins based on the provided parameters to control the motors and arms.

        Args:
            lm (int): Duty cycle for the left motor (0-100).
            rm (int): Duty cycle for the right motor (0-100).
            latch (int): Latch control signal (0/1).
            up_arm (int): Signal to move the arm up (0/1).
            down_arm (int): Signal to move the arm down (0/1).
            back_lm (int): Signal for backward motion of the left motor (0/1).
            back_rm (int): Signal for backward motion of the right motor (0/1).
    """
    # latch activation
    GPIO.output(lch_pin, GPIO.HIGH if latch else GPIO.LOW)

    # arm activation
    GPIO.output(arm1_pin, GPIO.HIGH if (down_arm or up_arm) else GPIO.LOW)  # arm motor magnitude
    GPIO.output(arm2_pin, GPIO.HIGH if down_arm else GPIO.LOW)  # arm motor direction

    # motors activation
    GPIO.output(rm_dir_pin, GPIO.HIGH if back_rm else GPIO.LOW)  # right motor direction
    GPIO.output(lm_dir_pin, GPIO.HIGH if back_lm else GPIO.LOW)  # left motor direction

    # Set motor speeds
    rm_pwm.ChangeDutyCycle(lm)  # left motor magnitude
    lm_pwm.ChangeDutyCycle(rm)  # right motor magnitude
