import tkinter as tk
from w1thermsensor import W1ThermSensor

from typing import Union

import RPi.GPIO as GPIO


# TODO: check if the GPIO pins are correct
# TODO: check if the PWM frequency is correct
# TODO: check if the bouncetime is correct

# TODO: check if the registered callbacks are correct
# TODO: check if the callbacks are called correctly

class Controller:
    """Class for controlling the Raspberry Pi GPIO pins"""

    def __init__(self, input_pin: int, output_pin: int, pwm_pin: int, pwm_frequency: Union[int, float]):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.input_pin = input_pin
        self.output_pin = output_pin
        self.pwm_pin = pwm_pin

        self.ouput_states = (GPIO.LOW, GPIO.HIGH)

        GPIO.setup(self.input_pin, GPIO.IN)
        GPIO.setup(self.output_pin, GPIO.OUT)
        GPIO.setup(self.pwm_pin, GPIO.OUT)

        self.sensor = W1ThermSensor()
        self.PWM = GPIO.PWM(self.pwm_pin, pwm_frequency)

    def set_pwm(self, value) -> None:
        self.PWM.start(value)

    def set_duty_cycle(self, value) -> None:
        self.PWM.ChangeDutyCycle(value)

    def set_frequency(self, value) -> None:
        self.PWM.ChangeFrequency(value)

    def get_temperature(self) -> float:
        return self.sensor.get_temperature()

    # TODO: implement the calbacks with bouncetime
    # TODO: tune for the best bounce time
    def register_input_callback(self, callback) -> None:
        GPIO.add_event_detect(self.input_pin, GPIO.BOTH, callback=callback)

    def register_output_callback(self, callback) -> None:
        GPIO.add_event_detect(self.output_pin, GPIO.BOTH, callback=callback)

    def register_pwm_callback(self, callback) -> None:
        GPIO.add_event_detect(self.pwm_pin, GPIO.BOTH, callback=callback)

    def __del__(self):
        GPIO.cleanup()
        pass


class App(tk.Tk):
    def __init__(self, controller: Controller):
        super().__init__()
        self.title("App")
        self.geometry("300x400")
        self.resizable(False, False)

        self.controller = controller

        # Light switch on/off button
        self.button_pressed = False
        self.states = ("Switch on", "Switch off")
        self.button = tk.Button(self, text=self.states[self.button_pressed], command=self.click, width=10)
        self.button.grid(row=0, column=0, padx=10, pady=10)

        # Intensity slider for the light
        self.scale = tk.Scale(self, from_=0, to=100, resolution=1, orient=tk.HORIZONTAL, command=self.scale_change)
        self.scale.grid(row=0, column=1, padx=10, pady=10)

        # Temperature label
        self.temperature_label = tk.Label(self, text=f"Temperature: {self.controller.get_temperature()}°C")
        self.temperature_label.grid(row=1, column=0, padx=10, pady=10)

        # TODO register callbacks for the GPIO pins

    def click(self):
        self.button_pressed = not self.button_pressed
        self.button["text"] = self.states[self.button_pressed]
        GPIO.output(self.controller.output_pin, self.controller.ouput_states[self.button_pressed])
        # TODO process the button press with GPIO
        pass

    def scale_change(self, event):
        # TODO process the scale change with GPIO
        pass

    def update_temperature(self):
        temperature = self.controller.get_temperature()
        self.temperature_label["text"] = f"Temperature: {temperature}°C"
        self.after(1000, self.update_temperature)


if __name__ == "__main__":
    input_pin = 0
    output_pin = 0
    pwm_pin = 0
    pwm_frequency = 0

    controller = Controller(0, 0, 0, 0)
    app = App(controller)
    app.mainloop()
