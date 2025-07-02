#!/usr/bin/env python3

class PIDController:
    def __init__(self):
        self.kp = 1.0
        self.ki = 0.0
        self.kd = 0.0
        self.integral_error = 0
        self.last_error = 0
        self.time_interval = 0.1

    def compute(self, error):
        self.integral_error += error * self.time_interval
        derivative_error = (error - self.last_error) / self.time_interval
        control_output = (self.kp * error) + (self.ki * self.integral_error) + (self.kd * derivative_error)
        self.last_error = error
        return control_output
