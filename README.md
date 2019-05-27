# Machinetron

## Getting Started

### Prerequisites

To run Team 2 Machinetron, you need to connect to the main control unit Raspberry Pi Zero through ssh. 

## Deployment

Follow the user manual to deploy Machinetron. The code to be run can be found through the Raspberry Pi Zero and the submachine boards shouldn't need to be touched until unless they need to be reprogrammed. To run the main code, save the desired STL file into the Machinetron folder. Inside the main.py file, inside line stlProcessor.generateCommands(), add your STL filename into the function input. Then run main.py inside terminal and press the GO button to start.

## Built with

[PyCharm] (https://www.jetbrains.com/pycharm/) - The IDE used to produce and run Python code

[Keil UVision] (http://www2.keil.com/mdk5/uvision/) - The IDE used to produce and run STM code

## Authors

* **Dion Lao** - *Python Raspberry Pi Code* - [DioNode] (https://github.com/dioNode)
* **Liam Chester** - *STM Microcontroller Code* - [LiamChester] (https://github.com/LiamChester)
* **Peter Hohl** - *STL Processing and Automation* - [peterhohl] (https://github.com/peterhohl)