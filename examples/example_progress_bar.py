import pyprogresslib.pyprogresslib as pyprogresslib
import time
results = []
bar = pyprogresslib.progressBar(barLength=20, timeDelay=0.1)
bar.run()  
# This starts the progress bar. from here, don't use the print statement until it's complete.
# If you must display text to the user with the bar, use the log argument of the updateBar() method.

for i in range(17):
    results.append(i*i/2)
    bar.updateBar(f"[{i+1}] Done calculation", withDelay=0.1)
    # updateBar and calculations can be placed in a loop.
# or, they can be programmed sequentially 
try:
    f = open("test.py")
    bar.updateBar("[18] Open File", withDelay=1)
# use the withDelay command to speed up and slow down the progressbar updating manually. Most of the time, you
# may want to invoke a delay of ~0.1, because most calculations on smaller projects take very little time to complete,
# causing the progress bar to finish almost instantly.
except FileNotFoundError:
    bar.forceEndBar()
# forceEndBar() causes the progress bar to finish, no matter its state. If this is placed in a loop, it's important you
# also put the break statement. Not doing this will cause the output thread to close, but your operations to continue, 
# but silently. This can also be used to your advantage if you so wish.

contents = f.read()
bar.updateBar("[19] Read File", withDelay=1)
f.close()
bar.updateBar("[20] Close File", withDelay=1)

# It is recommended to call time.sleep(0.01) to allow the library to clear the screen one last time. 
time.sleep(0.01)
# From here, continue your program like usual.
input("All done!\n")