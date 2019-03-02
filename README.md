<h2>BESI-C_WatchData_Offload_Terminal</h2>

The GetData.py file contains the function pullData that can be used to offload data collected and stored on an android device connected via USB using ADB. The GetData.pullData may be used inside a periodic loop to automatically download data from the device as soon as it is plugged in, as showcased in test.py. GetData requires a config file in the form:

```java
PLATFORM_TOOLS="Path_to_ADB_Drivers"
DATAPATH="Path_to_data_on_device"
SAVEPATH="Path_to_save_location_of_downloaded_data"
DEVICEID="Device_Serial_Number"
```

Device serial number can be found by using the command 
```
adb devices
```
The data is saved at: DATAPATH\\DEVICEID\\_TimeStamp_\\
