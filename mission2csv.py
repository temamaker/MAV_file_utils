import csv
import mav_definitions_parser as mavcmd

WP_MAP = {
    0:  "INDEX",         # Waypoint ID (0 is usually Home)
    1:  "CURRENT",       # 1 = currently active, 0 = inactive
    2:  "COORD_FRAME",   # 0=Global, 3=GlobalRelativeAlt, 10=LocalNed
    3:  "COMMAND",       # The MAV_CMD ID (e.g., 16, 3000)
    11: "AUTOCONTINUE"   # 1 = move to next WP automatically
}

#The filename of the .xml you downloaded from 
#https://github.com/mavlink/mavlink/blob/master/message_definitions/v1.0/common.xml
LIBNAME = 'common.xml'

class Waypoint:
    def __init__(self, mission_line):
        self.paramvalues = {}
        for i,item in enumerate(mission_line):
            if i in list(WP_MAP.keys()):
                setattr(self, WP_MAP[i], float(item))
        for i in range(1,8):
            self.paramvalues[i] = mission_line[i+3]




def loadfile(missionfile):
    Mission = []
    with open(missionfile, 'r') as M:
        for line in M.readlines():
            line = line.strip().split(sep="\t")
            if len(line) == 12:
                Mission.append(Waypoint(line))
    return Mission

def save_to_csv(mission):
    MAVDICT = mavcmd.build_mav_cmd_dict(LIBNAME)
    MAVFRAME = mavcmd.build_mav_frame_dict(LIBNAME)
    Template = ["Index", "Command","Parameters","Coordinate frame"]
    itemList = []
    for missionitem in mission:
        index = missionitem.INDEX
        try:
            command = MAVDICT[missionitem.COMMAND].name     
        except KeyError:
            command = f"Unknown command: {missionitem.COMMAND}"
            parameters = f"Parameters (1-7):"
            for i in range(1,8):
                parameters += f"{float(missionitem.paramvalues[i]):.3f}; "
            coordinate_frame = "Not Available"
        else:
            coordinate_frame = MAVFRAME[missionitem.COORD_FRAME]['name']
            parameters = ""
            for i,parameter in MAVDICT[missionitem.COMMAND].params.items():
                label = parameter.label
                units = parameter.units
                value = missionitem.paramvalues[i]
                if label != '':
                    parameters += f"{label}:{float(value):.3f} {units}; "
        
        itemList.append({'Index':index,
                            'Command':command, 
                            'Parameters':parameters,
                            "Coordinate frame":coordinate_frame})    



    csv_filename = "mission_output.csv"

    with open(csv_filename, 'w',newline='') as csv_file:
        writer = csv.DictWriter(csv_file,fieldnames=Template)
        writer.writeheader()
        for item in itemList:
            writer.writerow(item)


def pass2csv(missionfile):
    mission = loadfile(missionfile)
    save_to_csv(mission)