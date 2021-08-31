# Advanced-Operating-System-Course-Project

In the code size visualizer of a binary executable project, we aim at starting from a dump of every symbol in a Miosix executable and design a tool to show a breakdown of the code size.

mapCode.py contains the code for parsing the uploaded .map file.


-------- Qt --------

The frontend is done with PyQt5. The user can upload a .map file and the breakdown of the code size will be displayed. The application supports a chartview of libraries and non-libraries present in the executable. A table view displays the contents of the chosen library.

CodeSizeVisualizer.py prompts the user to upload a .map file. The size distribution after parsing the contents will be visualized using a chartview.


#Instructions to run the application:

Install the following python libraries
 - python3-pyqt5.qtchar
 - python3-numpy

Once installed run: 
 - python3 CodeSizeVisualizer.py
 - upload a .map file 
