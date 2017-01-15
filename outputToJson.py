import re, json
outputFile = open('part-r-00000', 'r');
jsonOutput = {}
chars_to_remove = [',', ':', '...', '.', ')', ']', '\'', '{', '!', '}', '\"', '.....', '?', ';', '[', '(', '+']
url_formats = ['http://', 'https://']
for line in outputFile:
    splitLine = line.strip('\n').replace('\t', ' ').split(' ')
    locationList = {}
    locationSplit = []
    for mline in splitLine[3:]:
        for l in re.split('(position:\d+)', mline):
            if len(l):
                if 'position' in l and l[-1] == '1':
                    locationSplit.append(l[0:-1])
                else:
                    locationSplit.append(l)
    while len(locationSplit) > 1:
        tempKey = locationSplit.pop(0).split('-IMDb.txt')[0]
        tempValue = locationSplit.pop(0).split('position:').pop()
        if 'position:' not in tempKey and len(tempKey):
            if tempKey not in locationList:
                locationList[tempKey] = []
                locationList[tempKey].append(tempValue)
            else:
                locationList[tempKey].append(tempValue)
    if not any(str in splitLine[0] for str in url_formats):
        key = splitLine[0].replace('u\'', '').replace('\\n', '').replace('&nbsp', '').replace('\\', '').replace('/', '').replace('&amp;', ' ').translate(None, ''.join(chars_to_remove))
        key = key.lower()
        if len(key):
            if key not in jsonOutput:
                jsonOutput[key] = {}
                jsonOutput[key]["locations"] = {}
                for Lkey in locationList:
                    jsonOutput[key]["locations"][Lkey] = []
                    for location in locationList[Lkey]:
                        jsonOutput[key]["locations"][Lkey].append(location)
                    if 'count' not in jsonOutput[key]:
                        jsonOutput[key]["count"] = len(locationList[Lkey])
                    else:
                        jsonOutput[key]["count"] += len(locationList[Lkey])
            else:
                for Lkey in locationList:
                    if Lkey not in jsonOutput[key]["locations"]:
                        jsonOutput[key]["locations"][Lkey] = []
                        for location in locationList[Lkey]:
                            jsonOutput[key]["locations"][Lkey].append(location)
                            jsonOutput[key]["count"] += len(locationList[Lkey])
with open('jsonFormat', 'w') as outfile:
    json.dump(jsonOutput, outfile)
