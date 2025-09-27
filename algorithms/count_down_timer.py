import time

countdown = 10

for time_left in range(countdown, 0, -1):
    print(f"Time left: {time_left} seconds")
    time.sleep(1)

print(f"Time is up!")