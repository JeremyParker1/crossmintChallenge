import requests
import json

# PHASE 2

# Gets the goal map and the coordinates of the non-spaces within the map
def getGoalMap(baseUrl, candidateId):
    url = '{baseUrl}/map/{candidateId}/goal'.format(baseUrl=baseUrl, candidateId=candidateId)

    goalMap = requests.get(url).json()['goal']
    coords = set()
    rows = len(goalMap)
    cols = len(goalMap[0])
    for x in range(rows):
        for y in range(cols):
            if goalMap[x][y] != "SPACE":
                coords.add((x,y))
    return goalMap, coords

# Prints or resets the candidate map depending on user input
def modifyCandidateMap(baseUrl, candidateId, goalMap, coords, action):

    successfulModifications = 0
    totalItems = len(coords)

    for (x,y) in coords:
            astralObj = ''
            goalItem = goalMap[x][y]
            myObj = {
                'candidateId': candidateId,
                'row': x,
                'column': y
            }


            if goalItem == 'POLYANET':
                astralObj = 'polyanets'
            else:
                directionOrColor, item = goalItem.split("_")

                if item == 'COMETH':
                    astralObj = 'comeths'
                    myObj['direction'] = directionOrColor.lower()
                elif item == 'SOLOON':
                    astralObj = 'soloons'
                    myObj['color'] = directionOrColor.lower()


            url = '{baseUrl}/{astralObj}/'.format(baseUrl=baseUrl,astralObj=astralObj)

            if action == "print":
                req = requests.post(url, json = myObj)
            else:
                req = requests.delete(url, json = myObj)

            print("working...")
            if req.status_code == 200:
                successfulModifications += 1
    print("{successfulModifications} items out of {totalItems} non-spaces were successfully modified in the candidate map".format(successfulModifications=successfulModifications,totalItems=totalItems))

def main():
    baseUrl = 'https://challenge.crossmint.io/api'
    candidateId = '18b50761-10ca-486d-a390-bb5b829344e9'
    action = input("Enter 'print' to modify the candidate's map. Or 'delete' to reverse the action\n\n")

    if action == "print" or action == "delete":
        goalMap, coords = getGoalMap(baseUrl,candidateId)
        modifyCandidateMap(baseUrl, candidateId, goalMap, coords, action)
    else:
        print("User entered in an invalid action")

main()


# PHASE 1
# rows = 11
# columns = 11
# candidateId = '18b50761-10ca-486d-a390-bb5b829344e9'
# for x in range(2,rows-2):
#     myobj = {
#     'candidateId': candidateId,
#     'row': x,
#     'column': x
#     }
#     req = requests.post(url, json = myobj)

# i = 2
# for y in range(columns-3, 1, -1):
#     myobj = {
#     'candidateId': candidateId,
#     'row': i,
#     'column': y
#     }
#     i += 1
#     req = requests.post(url, json = myobj)
