# Get total list of levels
levelListFile = open('level_list.txt')
levelList = [x.strip('\n') for x in levelListFile.readlines()]

levelString = './level_data/level_'

levels = []


# Generate array of level objects (parsing)
for y in range(len(levelList)):
    levelFile = open(levelString + levelList[y] + '.txt')
    current_level = levelFile.readlines()
    for x in range(len(current_level)):
        current_level[x] = current_level[x].strip('\n')
        current_level[x] = list(current_level[x])
    levels.append(current_level)