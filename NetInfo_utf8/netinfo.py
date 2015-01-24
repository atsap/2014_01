# -*- coding: utf8 -*-
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import ConfigParser,sys,os,tempfile,re, subprocess
def initnetview():
    current_Path = os.path.dirname(os.path.abspath(__file__)) + '\\'
    temp_Path = tempfile.gettempdir()+ '\\'
    os.system(current_Path + 'NetworkInterfacesView.exe ' +  '/sxml ' + temp_Path + 'netviewraw.xml')
    return
def xmlparaser():
    temp_Path = tempfile.gettempdir()+ '\\'
    cfg=[]
    tree = ET.ElementTree(file=temp_Path + 'netviewraw.xml')
    root = tree.getroot()
    count=1
    entry = 'aaa' # registry entry of nic
    for elem in tree.iter():
        if elem.tag == 'device_name' and device_name == '1':
            count = count + 1
            if elem.text is not None:
                cfg.append('[Interface '+ str(count) + ']')# Section number for configuration file
                cfg.append('device_name = ' +elem.text.encode('utf8'))
                ###############################################################################
                #find NIC entry in registry#
                regaddr = 'reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318} /s /c /e /f '
                proc = subprocess.Popen(regaddr + '\"' + elem.text.encode('utf8') + '\"' +' | find \"HKEY_LOCAL_MACHINE\"', stdout=subprocess.PIPE,shell=True,stderr=subprocess.STDOUT)
                out, err = proc.communicate()
                pin = out
                #get registry entry of nic
                entry = pin.split('\\')[len(pin.split('\\')) - 1]
                cfg.append('registry_index =' + entry)
                #print out
                #print 'aaaaaaaaaaaaaaaaaa=    ' + str(out)
            else:
                cfg.append('device_name = ')
        elif elem.tag == 'connection_name' and connection_name == '1':
            if elem.text is not None:
                cfg.append('connection_name = ' + elem.text.encode('utf8'))
            else:
                cfg.append('connection_name = ')
        elif elem.tag == 'ip_address' and ip_address == '1':
            if elem.text is not None:
                cfg.append('ip_address = ' + elem.text.encode('utf8'))
            else:
                cfg.append('ip_address = ')
        elif elem.tag == 'subnet_mask' and subnet_mask == '1':
            if elem.text is not None:
                cfg.append('subnet_mask = ' + elem.text.encode('utf8'))
            else:
                cfg.append('subnet_mask = ')
        elif elem.tag == 'default_gateway' and default_gateway == '1':
            if elem.text is not None:
                cfg.append('default_gateway = ' + elem.text.encode('utf8'))
            else:
                cfg.append('default_gateway = ')

        elif elem.tag == 'name_servers' and name_servers == '1':
            if elem.text is not None:
                cfg.append('name_servers = ' + elem.text.encode('utf8'))
            else:
                cfg.append('name_servers = ')

        elif elem.tag == 'dhcp_enabled' and dhcp_enabled == '1':
            if elem.text is not None:
                cfg.append('dhcp_enabled = ' + elem.text.encode('utf8'))
            else:
                cfg.append('dhcp_enabled = ')

        elif elem.tag == 'dhcp_server' and dhcp_server == '1':
            if elem.text is not None:
                cfg.append('dhcp_server = ' + elem.text.encode('utf8'))
            else:
                cfg.append('dhcp_server = ')

        elif elem.tag == 'instance_id' and instance_id == '1':
            if elem.text is not None:
                cfg.append('instance_id = ' + elem.text.encode('utf8'))
            else:
                cfg.append('instance_id = ')

        elif elem.tag == 'interface_guid' and interface_guid == '1':
            if elem.text is not None:
                cfg.append('interface_guid = ' + elem.text.encode('utf8'))
            else:
                cfg.append('interface_guid = ')

        elif elem.tag == 'mtu' and mtu == '1':
            if elem.text is not None:
                cfg.append('mtu = ' + elem.text.encode('utf8'))
            else:
                cfg.append('mtu = ')

        elif elem.tag == 'lease_obtained_time' and lease_obtained_time == '1':
            if elem.text is not None:
                cfg.append('lease_obtained_time = ' + elem.text.encode('utf8'))
            else:
                cfg.append('lease_obtained_time = ')

        elif elem.tag == 'lease_terminates_time' and lease_terminates_time == '1':
            if elem.text is not None:
                cfg.append('lease_terminates_time = ' + elem.text.encode('utf8'))
            else:
                cfg.append('lease_terminates_time = ')

        elif elem.tag == 't1_time' and t1_time == '1':
            if elem.text is not None:
                cfg.append('t1_time = ' + elem.text.encode('utf8'))
            else:
                cfg.append('t1_time = ')

        elif elem.tag == 't2_time' and t2_time == '1':
            if elem.text is not None:
                cfg.append('t2_time = ' + elem.text.encode('utf8'))
            else:
                cfg.append('t2_time = ')

        elif elem.tag == 'registry_time' and registry_time == '1':
            if elem.text is not None:
                cfg.append('registry_time = ' + elem.text.encode('utf8'))
            else:
                cfg.append('registry_time = ')
        elif elem.tag == 'mac_address' and mac_address == '1':
            if elem.text is not None:
                cfg.append('mac_address = ' + elem.text.encode('utf8'))
            else:
                cfg.append('mac_address = ')
        elif elem.tag == 'status' and status == '1':
            cfg.append('status = ' + elem.text.encode('utf8'))
    fn = temp_Path + 'netview.tmp'
    f = open(fn, 'w')
    for text in cfg:
        f.write(text+ '\n')
    f.close()
    return


def netfilter():
    temp_Path = tempfile.gettempdir()+ '\\'
    listactive = [] # Non Hardware Disconnected list
    config = ConfigParser.ConfigParser()
    config.optionxform = str  #reference: http://docs.python.org/library/configparser.html
    config.read(temp_Path + 'netview.tmp')

    total_section = config.sections()
    for sSection in total_section:
        status = config.get(sSection, 'status')# remove "Hardware Disconnected" cofiguration
        if (Hardware_Disconnected == '1' and status == 'Hardware Disconnected') or (Operational == '1' and status == 'Operational') or (Non_Operational == '1' and status == 'Non-Operational'):
            listactive.append(sSection)
    print 'Removed list =' + str(listactive)
    for rev in listactive:
        config.remove_section(rev)
    config.write(open('netinfo.def', 'wb'))

    return

def loadini():
    config = ConfigParser.ConfigParser()
    config.read('NetworkInterfacesViewpy.ini')
    global device_name,connection_name,ip_address,subnet_mask,default_gateway,name_servers,dhcp_enabled,dhcp_server
    global instance_id,interface_guid,mtu,lease_obtained_time,lease_terminates_time,t1_time,t2_time,registry_time,status,mac_address
    global Hardware_Disconnected,Operational,Non_Operational
    device_name =  config.get('NetworkInterfacesView', 'device_name')
    connection_name =  config.get('NetworkInterfacesView', 'connection_name')
    ip_address =  config.get('NetworkInterfacesView', 'ip_address')
    subnet_mask =  config.get('NetworkInterfacesView', 'subnet_mask')
    default_gateway =  config.get('NetworkInterfacesView', 'default_gateway')
    name_servers =  config.get('NetworkInterfacesView', 'name_servers')
    dhcp_enabled =  config.get('NetworkInterfacesView', 'dhcp_enabled')
    dhcp_server =  config.get('NetworkInterfacesView', 'dhcp_server')
    instance_id =  config.get('NetworkInterfacesView', 'instance_id')
    interface_guid =  config.get('NetworkInterfacesView', 'interface_guid')
    mtu =  config.get('NetworkInterfacesView', 'mtu')
    lease_obtained_time =  config.get('NetworkInterfacesView', 'lease_obtained_time')
    lease_terminates_time =  config.get('NetworkInterfacesView', 'lease_terminates_time')
    t1_time =  config.get('NetworkInterfacesView', 't1_time')
    t2_time =  config.get('NetworkInterfacesView', 't2_time')
    registry_time =  config.get('NetworkInterfacesView', 'registry_time')
    status =  config.get('NetworkInterfacesView', 'status')
    mac_address =  config.get('NetworkInterfacesView', 'mac_address')
    Hardware_Disconnected =  config.get('Filter', 'Hardware_Disconnected')
    Operational =  config.get('Filter', 'Operational')
    Non_Operational =  config.get('Filter', 'Non_Operational')
    return

def reassignintfacenumber():
    count = 0
    cfg = []
    for line in open('netinfo.def', 'r'):
        if ('[Interface' in line) and ('[' in line):
            count = count + 1
            line = '[Interface ' + str(count) + ']' + '\n'
        cfg.append(line)
    f = open('netinfo.def', 'w')
    for text in cfg:
        f.write(text)
    f.close()
    return

def returnUTF8(unicode):
    return unicode.encode('utf8').decode('utf8')

def main():
    initnetview()
    loadini()
    xmlparaser()
    netfilter()
    reassignintfacenumber()
    return
if __name__ == "__main__":
    main()