import os
import subprocess
import datetime

# --- Initialization ---
variables = open('config').read().strip().replace('"','').split('\n')
for i in range(len(variables)):
    variables[i] = variables[i].strip().split('=')


platform_tools = variables[0][1]
data_path = variables[1][1]
save_path = variables[2][1]
device_1_id = variables[3][1]
# ----------------------


device_1_connected = False
data_saved = False


def storeData():
    """Gets data from device with device ID and stores the data in the determined data save path in config file"""
    this_save_path = save_path+'/'+device_1_id+'/'+str(datetime.datetime.now()).replace(' ','_').replace(':','-').replace('.','-')+'/'
    os.makedirs(this_save_path)
    process = subprocess.Popen([platform_tools,'-s',device_1_id,'pull',data_path,this_save_path])
    while process.poll() == None:
        pass
    return this_save_path


def pullData():
    """Checks if device is connected and if it is and has not been downloaded and takes appropriate action"""
    global device_1_connected,data_saved

    with subprocess.Popen([platform_tools,'devices'], stdout=subprocess.PIPE) as process:
        output = str(process.stdout.read())
       
        if device_1_id in output:
            if (not device_1_connected) or (data_saved == False):
                print('Device Connected\nGathering Device Data...')
                datapath = storeData()
                device_1_connected = True

                if os.path.isdir(datapath+data_path.split('/')[-2]):
                    data_saved = True
                    print('Data saved to: ' + datapath)
                else:
                    data_saved = False

        else:
            device_1_connected = False
            data_saved = False
        
        process.kill()
