# rram-pyterminal

PyTerminal was developed in PyCharm with Python 3.10.0rc2, the purpose of this is to provide an interactive and simple platform for end users to get hands on the RRAM test chip.

### Required Python Packages
- pyserial

### Evaluation Board
#### Structure
![Structure](https://user-images.githubusercontent.com/4018299/140850588-7cd2da58-717a-46f9-90fd-8df5c18abf03.png)
#### Block Diagram
![Block Diagram](https://user-images.githubusercontent.com/4018299/140850607-568fab2c-8d2b-47f8-9299-e08c622d739e.png)
#### Mother Board
![Mother Board](https://user-images.githubusercontent.com/4018299/140850611-f4fd9769-1034-425f-a181-0ed47ddad647.png)
#### Daughter Board
![Daughter Board](https://user-images.githubusercontent.com/4018299/140850609-052c539d-31b6-4576-bfc6-f63140e24af5.png)


### Voltage Sources
| Voltage Source | Regulator Type | Power/Value Control Method | Voltage Range (V) | Step Resolution (mV) | Max Supported Current |                
| :----:         | :----:         | :----:                     | :----:            | :----:               | :----:                |
| 3V3 Always On  | LDO            | -  /Potentiometer          | 0.73 ~ VCC        | -                    | 25 mA                 |
| VDD            | LDO            | I2C/Potentiometer          | 0.73 ~ VCC        | -                    | 300 mA                |
| AVDD_SRAM      | LDO            | I2C/Potentiometer          | 0.73 ~ VCC        | -                    | 300 mA                |
| 3V3            | DC/DC          | I2C/I2C                    | 2.06 ~ 4.00       | 62.50                | 1.5 A                 |
| AVDD_WR        | DC/DC          | I2C/I2C                    | 1.08 ~ 4.00       | 32.63 & 62.50        | 1.5 A                 |
| AVDD_WL        | DC/DC          | I2C/I2C                    | 0.83 ~ 3.08       | 25.00 & 48.13        | 2.5 A                 |
| AVDD_RRAM      | DC/DC          | I2C/I2C                    | 0.83 ~ 1.60       | 25.00                | 2.5 A                 |

### DAC Sources
There are two DAC sources: "**VTGT_BL**" and "**ADC_CAL**", where each of them can be 0 ~ 3V3 with 12 bit resolution.
- **VTGT_BL**: Target voltage for the bit lines. (Nominal range: 20 ~ 200 mV)
- **ADC_CAL**: Used for ADC calibration mode, where the input of ADC would be this voltage source instead of bit lines.

### Command List
The commands can first be categorized into two types (or mix of the two): 1) Low level component driver. 2) High level library.
The detail command lists for each module are listed below: 

#### Board component driver 
    - BOARD
2)  detail description of the functions below are inside each .py files

### Suggested Form/Set/Reset/Read Parameters
| Type   | AVDD_WR(mV) | AVDD_WL(mV) | Cycles | Times
| :----: | :----:      | :----:      | :----: | :----:      
| Form   | 3200        | 1600        | 20     | 2     
| Set    | 2200        | 2200        | 100    | 2        
| Reset  | 2800        | 2800        | 200    | 8        
| Read   | N/A         | 1100        | 5      | N/A

### Firmware Update
To update the firmwares, please refer to [rram-programmer](https://github.com/muyachang/rram-programmer)
