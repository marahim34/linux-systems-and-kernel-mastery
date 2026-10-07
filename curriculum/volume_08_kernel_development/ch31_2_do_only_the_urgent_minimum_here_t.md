2. Do only the urgent minimum here — this context is time-critical and cannot sleep.
3. schedule_work DEFERS the slow processing to a safer context that CAN sleep (the 'bottom half').