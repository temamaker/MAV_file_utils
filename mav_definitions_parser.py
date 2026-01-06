#A script that create a lookup-table for each of the command numbers
#Source XML: https://github.com/mavlink/mavlink/blob/master/message_definitions/v1.0/common.xml
#Idea:
#Dictionary: LUT[22] -> "Name" : "MAV_CMD_NAV_TAKEOFF"
# LUT[22][PARAM1] = ["Pitch","deg","Minimum pitch (if airspeed sensor present), desired pitch without sensor"]
#LUT[22][PARAM1][0] = "Pitch" 
#LUT[22]["Name"] = "MAV_CMD_NAV_TAKEOFF"

#We have to distinguish between those that have PARAMS 5,6,7 as Lat,Lon,Alt and those that use them 
#for data (Like local X,Y,Z position)

import xml.etree.ElementTree as ET

class Parameter:
    def __init__(self, param):
        self.index = int(param.attrib['index'])
        self.label = param.attrib.get('label','')
        self.units = param.attrib.get('units','')
        self.description = param.text

class MavCommand:
    def __init__(self, mavcommand):
        attributes = mavcommand.attrib
        #Init the basics
        self.name = attributes['name']
        self.value = int(attributes['value'])
        converter = {'false':False, 'true': True}
        self.hasLocation = converter[attributes.get('hasLocation','false').lower()]
        self.isDestination = converter[attributes.get('isDestination','false').lower()]
        self.description = mavcommand.find('description').text
        #Reach for the internal params
        self.params = {}
        for item in mavcommand:
            if item.tag == 'param':
                param = Parameter(item)
                self.params[param.index] = param


def build_mav_cmd_dict(filename):
    tree = ET.parse(filename)
    root = tree.getroot()              
    mavcmd = root.find("./enums/enum[@name='MAV_CMD']")
    MAVCMD_DICT = {}

    for entry in mavcmd:
        if entry.tag == 'entry':
            command = MavCommand(entry)
            index = command.value
            MAVCMD_DICT[index] = command
        else:
            print(f"Info: skipping entry with tag {entry.tag}")
    print(f"Read {len(MAVCMD_DICT)} entries successfully")
    return MAVCMD_DICT

#number -> name, description
def build_mav_frame_dict(filename):
    tree = ET.parse(filename)
    root = tree.getroot()              
    mavframe = root.find("./enums/enum[@name='MAV_FRAME']")
    MAVFRAME_DICT = {}
    for item in mavframe:
        if item.tag == 'entry': 
            value = int(item.attrib.get('value','-1'))
            name = item.attrib.get('name','')
            description = item.find('description').text.strip()
            MAVFRAME_DICT[value] = {'name':name,'description':description}
    return MAVFRAME_DICT   
