import PyProgressLib_ThatOneCoder.pyprogresslib as pyprogresslib
import time
results = []

progressIcon = pyprogresslib.progressIcon(symbolVersion=1, textColour="red", finishedTextColour="green", timeDelay=1)
progressIcon.run()
# This starts the progress bar. from here, don't use the print statement until it's complete.
# If you must display text to the user with the bar, use the log() method to do so. 

# Please note that the time.sleep() calls, unless noted, are simply to slow the program down enough that the icon
# doesn't finish immediately.

for i in range(17):
    results.append(i*i/2)
    time.sleep(0.1)
progressIcon.log("Moving onto larger tasks...")
f = open("test.py")
time.sleep(1)
contents = f.read()
time.sleep(1)
f.close()
time.sleep(1)
progressIcon.finish()
# calling the finish method stops the waiting icon and advances the program. the thread is ended. Printing to the screen
# will work normally now.
# It is recommended to call time.sleep(1) to allow the library to clear the screen one last time. 
time.sleep(1)
input("All done!\n")
# ------------------------------------------------------------------
# To create a custom set of icons, do the following:

# 1. in a standard python list, put all of the outputs, e.g.:

# icons = [".","..","...","....","....."]

# add to the end the message you want displayed when the finish() method is called:

# icons = [".","..","...","....",".....", "All done!"]

# create a new progressIcon class, if you haven't already:

# p = progressIcon()

# run the addCustomIcon() function like so:

# id = p.addCustomIcon(icons)

# the returned value is the symbolVersion to use the next time you use the progressIcon class.