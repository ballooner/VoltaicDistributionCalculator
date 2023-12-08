import requests
import pandas as pd
import math
import time

#Takes a player uid and passes a dataframe to calcRank() :
def getAimData(uid):
    url = "https://api.aimlab.gg/graphql"

    payload = {
        "query": '''
            query GetAimlabProfileAgg($where: AimlabPlayWhere!) {
                aimlab {
                    plays_agg(where: $where) {
                        group_by {
                            task_id
                            task_name
                        }
                        aggregate {
                            count
                            avg {
                                score
                                accuracy
                            }
                            max {
                                score
                                accuracy
                                created_at
                            }
                        }
                    }
                }
            }
        ''',
        "variables": {"where": {
            "is_practice": {"_eq": False},
            "score": {"_gt": 0},
            "user_id": {"_eq": uid}
        }}
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Origin": "https://app.voltaic.gg",
        "Connection": "keep-alive",
        "Referer": "https://app.voltaic.gg/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "TE": "trailers"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    data = response.json()
    scenarioData = data['data']['aimlab']['plays_agg']
    
    return pd.json_normalize(scenarioData)
    #getScores(pd.json_normalize(scenarioData))
    

#Returns a python array of the dataframe that contains 1000 players :
def getLeaderboard(offset):
    url = "https://api.aimlabs.com/graphql"
    
    payload = {
            "operationName": "GetLeaderboard",
            "variables": {
                "limit": 50,
                "offset": offset,
                "username": "",
                "taskMode": 0,
                "taskId": "gridshot",
                "weaponId": "9mm"
            },
            "query": """
                query GetLeaderboard($taskMode: Int!, $taskId: String!, $offset: Int!, $limit: Int!, $weaponId: String!, $window: Trainer_LeaderboardWindowInput, $username: String!) {
                    Trainer {
                        aimlab {
                            leaderboard(
                                input: {limit: $limit, offset: $offset, clientId: "aimlab", taskId: $taskId, taskMode: $taskMode, weaponId: $weaponId, username: $username, window: $window}
                            ) {
                                id
                                data
                                metadata {
                                    offset
                                    rows
                                    totalRows
                                    __typename
                                }
                                schema {
                                    fields
                                    id
                                    __typename
                                }
                                profiles {
                                    shepUser {
                                        profileBannerUrl
                                        profileImageUrl
                                        id
                                        __typename
                                    }
                                    __typename
                                }
                                __typename
                            }
                        }
                    }
                }
            """
        }

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://aimlabs.com/",
            "content-type": "application/json",
            "authorization": "",
            "Origin": "https://aimlabs.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "TE": "trailers"
        }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    leaderboardData = data['data']['Trainer']['aimlab']['leaderboard']['data']
        
    df = pd.json_normalize(leaderboardData)
        
    tempArray = df.to_numpy()
    
    return df.to_numpy()

#Put the scores of the player into 3 different arrays
def getScores(scoreDataFrame):  
    scenarios = ['CsLevel.VT Empyrean.VT Angle.RB668Z', 'CsLevel.VT Empyrean.VT Waves.R8TGLS', 'CsLevel.VT Empyrean.VT Sixsh.R8TGD3', 'CsLevel.VT Empyrean.VT Multi.RB6AAB',
                 'CsLevel.canner.VT Suave.R8I6UD', 'CsLevel.VT Empyrean.VT Stead.RB67MZ', 'CsLevel.zcr.VT Pillt.R8KMR0', 'CsLevel.Lowgravity56.VT Axitr.RJF5AX',
                 'CsLevel.VT Empyrean.VT Spher.RB69A4', 'CsLevel.VT Empyrean.VT Skysw.R8TH9B', 'CsLevel.VT Empyrean.VT Angle.R8X0YY', 'CsLevel.VT Empyrean.VT Arcsw.RB6A0U',
                 'CsLevel.VT Empyrean.VT Angle.R8S2XN', 'CsLevel.VT Empyrean.VT Waves.R8S37J', 'CsLevel.VT Empyrean.VT Fives.R8YV6C', 'CsLevel.VT Empyrean.VT Multi.R8S3PL',
                 'CsLevel.canner.VT Suave.R8I6RC', 'CsLevel.VT Empyrean.VT Stead.R8S43X', 'CsLevel.zcr.VT Pillt.R8KMKK', 'CsLevel.Lowgravity56.VT Axitr.RJE095',
                 'CsLevel.VT Empyrean.VT Spher.R8S4B3', 'CsLevel.VT Empyrean.VT Skysw.R8S4IF', 'CsLevel.VT Empyrean.VT Dodge.R8S4N1', 'CsLevel.VT Empyrean.VT Arcsw.R8S4QI',
                 'CsLevel.VT Empyrean.VT mpXY .R7WQSA', 'CsLevel.VT Empyrean.VT Sky C.R7164L', 'CsLevel.VT Empyrean.VT Arc 1.R7WRND', 
                 'CsLevel.VT Empyrean.VT Three.R7WSTK', 'CsLevel.VT Empyrean.VT Twosh.R7WTAX', 'CsLevel.VT Empyrean.VT Multi.R7WTKS',
                 'CsLevel.canner.VT Suave.R9N6JI', 'CsLevel.VT Empyrean.VT Preci.R7ZK29', 'CsLevel.VT Empyrean.VT Mini .R7ZKQO',
                 'CsLevel.zcr.VT React.R8CNGN', 'CsLevel.zcr.VT Pillt.R8DF2N', 'CsLevel.Lowgravity56.VT Axitr.RJE01M',
                 'CsLevel.VT Empyrean.VT evaTS.R7YQ67', 'CsLevel.VT Empyrean.VT Spher.R89MOR', 'CsLevel.VT Empyrean.VT berry.R7ZWKV',
                 'CsLevel.VT Empyrean.VT evaTS.R7ZY84', 'CsLevel.VT Empyrean.VT Angle.R8AH09', 'CsLevel.VT Empyrean.VT Arcsw.R8AOQF']
    
    #Turn dataframe into an array
    scenArray = scoreDataFrame.to_numpy()
    
    #If the current lines id is in one of the arrays change it to the score of the scenario
    for i in range(0, len(scenArray)):
        for j in range(0, len(scenarios)):
            if type(scenarios[j]) != str:
                continue
            if scenarios[j] == scenArray[i][0]:
                scenarios[j] = scenArray[i][5]

    
    #If one of the scenarios wasn't found change the score to a 0
    for i in range(0, len(scenarios)):
        if type(scenarios[i]) == str:
            scenarios[i] = 0
    
    beginnerScenarios = []
    intermediateScenarios = []
    advancedScenarios = []
    
    for i in range(0, 42):
        if i < 12:
            beginnerScenarios.append(scenarios[i])
        elif i <  24:
            intermediateScenarios.append(scenarios[i])
        else:
            advancedScenarios.append(scenarios[i])
    
    return beginnerScenarios, intermediateScenarios, advancedScenarios
    #getEnergy(beginnerScenarios, intermediateScenarios, advancedScenarios)
    
#Google sheets match function
def match(key, range):
        index = len(range)
        
        for num in reversed(range):
            if key >= num:
                return index
            index -= 1
        
        return index
    
#Calls according getEnergy functions
def getEnergy(beginnerScores, intermediateScores, advancedScores): 
    #Make sure they have at least one score in each category
    canBeAdvanced = True
    canBeIntermediate = True
    canBeBeginner = True

    counter = 0
    for i in range(0, len(advancedScores)):
        if i % 3 == 0 and counter != 3:
            counter = 0
        
        if advancedScores[i] == 0:
            counter += 1
            
        if counter == 3:
            canBeAdvanced = False
            
    counter = 0
    for i in range(0, len(intermediateScores)):
        if i % 2 == 0 and counter != 2:
            counter = 0
        
        if intermediateScores[i] == 0:
            counter += 1
            
        if counter == 2:
            canBeIntermediate = False
            
    counter = 0
    for i in range(0, len(beginnerScores)):
        if i % 2 == 0 and counter != 2:
            counter = 0
        
        if beginnerScores[i] == 0:
            counter += 1
            
        if counter == 2:
            canBeBeginner = False
        
    if canBeAdvanced == False and canBeIntermediate == False and canBeBeginner == False:
        return "Unranked"
    
    #Calculate beginner scores
    beginnerRank = getBeginnerEnergy(beginnerScores, 500)
 
    #Calculate intermediate scores
    intermediateRank = getIntermediateEnergy(intermediateScores, 900)
    
    #Calculate advanced scores
    advancedRank = getAdvancedEnergy(advancedScores, 1200)
            
    beginnerRank = harmonicMean(beginnerRank)
    intermediateRank = harmonicMean(intermediateRank)
    advancedRank = harmonicMean(advancedRank)
    
    if advancedRank >= 900 and canBeAdvanced == True:
        if advancedRank >= 1200:
            return "Celestial"
        elif advancedRank >= 1100:
            return "Astra"
        elif advancedRank >= 1000:
            return "Nova"
        else:
            return "Grandmaster"
        
    if intermediateRank >= 500 and canBeIntermediate == True:
        if intermediateRank >= 800:
            return "Master"
        elif intermediateRank >= 700:
            return "Jade"
        elif intermediateRank >= 600:
            return "Diamond"
        else:
            return "Platinum"
    
    if beginnerRank >= 100 and canBeBeginner == True:
        if beginnerRank >= 400:
            return "Gold"
        elif beginnerRank >= 300:
            return "Silver"
        elif beginnerRank >= 200:
            return "Bronze"
        else:
            return "Iron"
        
    return "Unranked"
    
def harmonicMean(arrayOfNums):
    sumOfReciprocals = 0
    
    for num in arrayOfNums:
        if num != 0:
            sumOfReciprocals += 1/num
    
    if sumOfReciprocals != 0:
        return math.floor(len(arrayOfNums) / sumOfReciprocals)
    
    return 0


def getBeginnerEnergy(beginnerScores, lowestIntermediateThreshold):
    beginnerThresholds = [
        [0, 100, 200, 300, 400],
        [0, 400, 460, 520, 650],
        [0, 300, 370, 440, 560],
        [0, 600, 700, 800, 1040],
        [0, 750, 850, 950, 1200],
        [0, 1000, 1300, 1600, 1900],
        [0, 1250, 1550, 1850, 2150],
        [0, 1650, 2050, 2450, 2850],
        [0, 2600, 2900, 3200, 3500],
        [0, 1500, 1600, 1700, 2000],
        [0, 1800, 2000, 2150, 2500],
        [0, 1000, 1200, 1500, 1700],
        [0, 900, 1000, 1100, 1400]
    ]
    
    allCategoryEnergies = []
    
    for i in range(0, 6):
        currScore = 0
        currScen = 1
        twoEnergy = [0, 0]
        
        for j in range(0, 2):
            currScore = (2 * i) + j
            currScen = (2 * i) + j + 1
            
            matchedScore = match(beginnerScores[currScore], beginnerThresholds[currScen]) - 1
            scoreDiff1 = [beginnerThresholds[currScen][1], beginnerThresholds[currScen][2] - beginnerThresholds[currScen][1], beginnerThresholds[currScen][3] - beginnerThresholds[currScen][2], beginnerThresholds[currScen][4] - beginnerThresholds[currScen][3], beginnerThresholds[currScen][4] - beginnerThresholds[currScen][3]]
            scoreDiff2 = [beginnerThresholds[0][1], beginnerThresholds[0][2] - beginnerThresholds[0][1], beginnerThresholds[0][3] - beginnerThresholds[0][2], beginnerThresholds[0][4] - beginnerThresholds[0][3], beginnerThresholds[0][4] - beginnerThresholds[0][3]]

            firstEquation = beginnerThresholds[0][matchedScore]
            secondEquation = beginnerScores[currScore] - (beginnerThresholds[currScen][matchedScore])
            twoEnergy[j] = firstEquation + secondEquation / scoreDiff1[matchedScore] * scoreDiff2[matchedScore]

        allCategoryEnergies.append(math.floor(min(lowestIntermediateThreshold, max(twoEnergy[0], twoEnergy[1])) - .5))
        
    return allCategoryEnergies
    #print("Beginner Scores:")
    #print(allCategoryEnergies)


def getIntermediateEnergy(intermediateScores, lowestAdvancedThreshold):
    intermediateThresholds = [
        [0, 300, 500, 600, 700, 800],
        [0, 660, 720, 800, 900],
        [0, 530, 590, 670, 750],
        [0, 1020, 1120, 1220, 1320],
        [0, 1170, 1270, 1370, 1490],
        [0, 2600, 2900, 3200, 3500],
        [0, 2200, 2500, 2800, 3100],
        [0, 2000, 2350, 2750, 3150],
        [0, 2150, 2450, 2750, 2900],
        [0, 1700, 1900, 2050, 2200],
        [0, 2350, 2550, 2700, 2900],
        [0, 2100, 2250, 2400, 2550],
        [0, 1700, 1830, 1930, 2000]
    ]
    
    allCategoryEnergies = []
    
    for i in range(0, 6):
        currScore = 0
        currScen = 1
        twoEnergy = [0, 0]
        
        for j in range(0, 2):
            currScore = (2 * i) + j
            currScen = (2 * i) + j + 1
            firstAndSecondThreshDiff = intermediateThresholds[currScen][1] - (intermediateThresholds[currScen][2] - intermediateThresholds[currScen][1])
            
            intermediateThresholds[currScen].insert(1, firstAndSecondThreshDiff)
            matchedScore = match(intermediateScores[currScore], intermediateThresholds[currScen]) - 1
            scoreDiff1 = [firstAndSecondThreshDiff, intermediateThresholds[currScen][3] - intermediateThresholds[currScen][2], intermediateThresholds[currScen][3] - intermediateThresholds[currScen][2], intermediateThresholds[currScen][4] - intermediateThresholds[currScen][3], intermediateThresholds[currScen][5] - intermediateThresholds[currScen][4], intermediateThresholds[currScen][5] - intermediateThresholds[currScen][4]]
            scoreDiff2 = [intermediateThresholds[0][1], intermediateThresholds[0][2] - intermediateThresholds[0][1], intermediateThresholds[0][3] - intermediateThresholds[0][2], intermediateThresholds[0][4] - intermediateThresholds[0][3], intermediateThresholds[0][5] - intermediateThresholds[0][4], intermediateThresholds[0][5] - intermediateThresholds[0][4]]

            firstEquation = intermediateThresholds[0][matchedScore]
            secondEquation = intermediateScores[currScore] - (intermediateThresholds[currScen][matchedScore])
            twoEnergy[j] = firstEquation + secondEquation / scoreDiff1[matchedScore] * scoreDiff2[matchedScore]

        allCategoryEnergies.append(math.floor(min(lowestAdvancedThreshold, max(twoEnergy[0], twoEnergy[1])) - .5))
        
    return allCategoryEnergies
    #print("Intermediate Scores:")
    #print(allCategoryEnergies)


def getAdvancedEnergy(advancedScores, maxEnergy):
    advancedThresholds= [
        [0, 800, 900, 1000, 1100, 1200],
        [0, 850, 1020, 1100, 1194],
        [0, 860, 1030, 1120, 1266],
        [0, 900, 1050, 1200, 1325],
        [0, 1550, 1650, 1750, 1870],
        [0, 1250, 1350, 1450, 1530],
        [0, 1490, 1580, 1670, 1750],
        [0, 3530, 4000, 4150, 4377],
        [0, 3000, 3550, 3900, 4112],
        [0, 2450, 3000, 3400, 3650],
        [0, 2500, 2800, 3000, 3253],
        [0, 3200, 3500, 3800, 3925],
        [0, 2250, 2500, 2750, 3076],
        [0, 2670, 2870, 3070, 3225],
        [0, 2370, 2570, 2650, 2800],
        [0, 2950, 3250, 3365, 3478],
        [0, 2680, 2980, 3130, 3255],
        [0, 2100, 2400, 2600, 2682],
        [0, 2000, 2250, 2450, 2585],
    ]
    
    allCategoryEnergies = []
    
    for i in range(0, 6):
        currScore = 0
        currScen = 1
        threeEnergy = [0, 0, 0]
        
        for j in range(0, 3):
            currScore = (3 * i) + j
            currScen = (3 * i) + j + 1
            firstAndSecondThreshDiff = advancedThresholds[currScen][1] - (advancedThresholds[currScen][2] - advancedThresholds[currScen][1])
            advancedThresholds[currScen].insert(1, firstAndSecondThreshDiff)
            matchedScore = match(advancedScores[currScore], advancedThresholds[currScen]) - 1
            scoreDiff1 = [firstAndSecondThreshDiff, advancedThresholds[currScen][3] - advancedThresholds[currScen][2], advancedThresholds[currScen][3] - advancedThresholds[currScen][2], advancedThresholds[currScen][4] - advancedThresholds[currScen][3], advancedThresholds[currScen][5] - advancedThresholds[currScen][4], advancedThresholds[currScen][5] - advancedThresholds[currScen][4]]
            scoreDiff2 = [advancedThresholds[0][1], advancedThresholds[0][2] - advancedThresholds[0][1], advancedThresholds[0][3] - advancedThresholds[0][2], advancedThresholds[0][4] - advancedThresholds[0][3], advancedThresholds[0][5] - advancedThresholds[0][4], advancedThresholds[0][5] - advancedThresholds[0][4]]

            firstEquation = advancedThresholds[0][matchedScore]
            secondEquation = advancedScores[currScore] - (advancedThresholds[currScen][matchedScore])
            threeEnergy[j] = firstEquation + secondEquation / scoreDiff1[matchedScore] * scoreDiff2[matchedScore]


        allCategoryEnergies.append(math.floor(min(maxEnergy, max(threeEnergy[0], threeEnergy[1], threeEnergy[2]))))
        
    return allCategoryEnergies
    #print("Advanced Scores:")
    #print(allCategoryEnergies)


start_time = time.time()

rankStats = {"Unranked":0, "Iron":0, "Bronze":0, "Silver":0, "Gold":0,
             "Platinum":0, "Diamond":0, "Jade":0, "Master":0,
             "Grandmaster":0, "Nova":0, "Astra":0, "Celestial":0}

#print(array[0][1])

scenData = getAimData("5A815E720DEF1BDE")
beginnerScores, intermediateScores, advancedScores = getScores(scenData)
print(getEnergy(beginnerScores, intermediateScores, advancedScores))

offset = 0

#77s for 150

""""
#8694900
while offset <= 100:
    array = getLeaderboard(offset)
    
    for i in range(0, len(array)):
        scenData = getAimData(array[i][1])
        beginnerScores, intermediateScores, advancedScores = getScores(scenData)
        rank = getEnergy(beginnerScores, intermediateScores, advancedScores)
        print("Rank " + str(array[i][0]) + ": " + rank)
        rankStats[rank] = rankStats[rank] + 1
    
    file = open("RankData.txt", "w")
    file.write(str(rankStats))
    file.close()
    
    offset += 50


file.close()
print(rankStats)
"""
print("Process finished --- %s seconds ---" % (time.time() - start_time))


