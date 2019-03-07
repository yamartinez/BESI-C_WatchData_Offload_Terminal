import os
import subprocess
import datetime


"""
Created by Yudel Martinez 2019 for Univeristy of Virginia School of Engineering and Applied Sciences
--------------------------------------------------------------------------------------------------------------------------
GetData is a python program that is used to get data form an ADB device to a specified folder accecible from the host system
This project requires that Google ADB Tools be installed or that Platform-tools has been downloaded, as that directory is used
to generate ADB commands.

How to use:
    1.Make config file
    2.Call GetData.init()
    3.Call GetData.pullData() on demand or in an always running while loop to have automatic download of data as soon as device 
    is plugged in
"""

# --- Initialization ---
variables = open('config').read().strip().replace('"','').split('\n')
for i in range(len(variables)):
    variables[i] = variables[i].strip().split('=')


platform_tools = variables[0][1]
data_path = variables[1][1]
save_path = variables[2][1]
backup_path = variables[3][1]
device_ids = variables[4][1].split(',')
# ----------------------


devices_connected = []
data_saved = []


def init():
    """Initializes variables required for operation"""
    for i in range(len(device_ids)):
        devices_connected.append(False)
        data_saved.append(False)
    return

def storeData(device_id):
    """Gets data from device with device ID and stores the data in the determined data save path in config file"""
    timestamp = str(datetime.datetime.now()).replace(' ','_').replace(':','-').replace('.','-')
    this_save_path = save_path+'/'+device_id+'/'+timestamp+'/'
    os.makedirs(this_save_path)
    process = subprocess.Popen([platform_tools,'-s',device_id,'pull',data_path,this_save_path], stdout=subprocess.PIPE,shell=True)
    output =''
    while process.poll() == None:
        output+=str(process.stdout.read())
        pass
    
    if ('0 files pulled' in output):
        print("Data Acquisition Failed...")
        return False
    elif ('Not a directory' in output):
        print("Failed")
        return False
    else:
        dataBackup(timestamp,device_id)
        return this_save_path

def dataBackup(timestamp,device_id):
    """Moves the data from the specified data directory to the specified backup directory in a new timestamped directory"""
    this_backup_path = backup_path +timestamp+'/'
    process = subprocess.Popen([platform_tools,'-s',device_id,'shell','mkdir',this_backup_path], stdout=subprocess.PIPE)
    process = subprocess.Popen([platform_tools,'-s',device_id,'shell','mv',data_path+'*', backup_path], stdout=subprocess.PIPE)
    while process.poll() == None:
        pass
    return


def pullData():
    """Checks if device is connected and if it is and has not been downloaded and takes appropriate action"""
    global devices_connected,data_saved

    for i in range(len(device_ids)):
        with subprocess.Popen([platform_tools,'devices'], stdout=subprocess.PIPE) as process:
            output = str(process.stdout.read())
        
            if device_ids[i] in output:
                if (not devices_connected[i]) or (data_saved[i] == False):
                    print('Device Connected\nGathering Device Data...')
                    datapath = storeData(device_ids[i])
                    devices_connected[i] = True

                    if datapath:
                        data_saved[i] = True
                        print('Data saved to: ' + datapath)
                    else:
                        data_saved[i] = False

            else:
                devices_connected[i] = False
                data_saved[i] = False
            
            process.kill()
