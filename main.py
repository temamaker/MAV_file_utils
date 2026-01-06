import diff
import mission2csv

def diffOption():

    print("Filename 1 (.param file): ")
    filename1 = input()
    print("Filename 2 (.param file): ")
    filename2 = input()
    diff.generate_diff(filename1, filename2)

def waypointToCsvOption():
    print("Waypoint file name: ")
    filename1 = input()
    mission2csv.pass2csv(filename1)
    

def menu():
    options = {
        1:diffOption,
        2:waypointToCsvOption,
        0:exit
    }
    option = int(input())

    return options[option]

if __name__ == '__main__':
    menu()()
