# :fire: Arduino + Python + PowerBi

This code shows how to implement the integration between Arduino and Power Bi with Python using serial communication.

# :notebook_with_decorative_cover: How it works?

Python Script creates a serial connection to Arduino and stores the data in the sqlite3 database.
This data is used in PowerBi to generate reports.

# :rocket: How use this code?

You need run 3 interfaces:

## Arduino interface
1. Upload *.ino code into your board
2. Connect with your PC using USB cable
3. Ensure the serial monitor is closed

## Python Interface
1. Run *.py code in your PC
2. Choose the baude rate

## PowerBI Interface
In this point, you can star a new connection with sqlite3 ou use the model *.pbix into project folder.

# :test_tube: Enjoy and test

You can use this basic stack to generate awnsome real time charts. 
