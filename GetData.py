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
backup_path = variables[3][1]
device_1_id = variables[4][1].split(',')
# ----------------------


device_1_connected = []
data_saved = []


def init():
    for i in range(len(device_1_id)):
        device_1_connected.append(False)
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
    this_backup_path = backup_path +timestamp+'/'
    process = subprocess.Popen([platform_tools,'-s',device_id,'shell','mkdir',this_backup_path], stdout=subprocess.PIPE)
    process = subprocess.Popen([platform_tools,'-s',device_id,'shell','mv',data_path+'*', backup_path], stdout=subprocess.PIPE)
    while process.poll() == None:
        pass
    return


def pullData():
    """Checks if device is connected and if it is and has not been downloaded and takes appropriate action"""
    global device_1_connected,data_saved

    for i in range(len(device_1_id)):
        with subprocess.Popen([platform_tools,'devices'], stdout=subprocess.PIPE) as process:
            output = str(process.stdout.read())
        
            if device_1_id[i] in output:
                if (not device_1_connected[i]) or (data_saved[i] == False):
                    print('Device Connected\nGathering Device Data...')
                    datapath = storeData(device_1_id[i])
                    device_1_connected[i] = True

                    if datapath:
                        data_saved[i] = True
                        print('Data saved to: ' + datapath)
                    else:
                        data_saved[i] = False

            else:
                device_1_connected[i] = False
                data_saved[i] = False
            
            process.kill()
