import os
import time

for entry in os.listdir('./dumps'):
    os.system("clear")
    with open(f"./dumps/{entry}", "r") as f:
        print(f"{entry}\n{'-' * 40}\n{f.read()}")
    time.sleep(1)
