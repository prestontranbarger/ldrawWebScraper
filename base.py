from bs4 import BeautifulSoup
import requests

def requestPart(partID, outputFolder):
    receiveOffical = requests.get('https://www.ldraw.org/library/official/parts/' + str(partID) + '.dat')
    receiveUnoffical = requests.get('https://www.ldraw.org/library/unofficial/parts/' + str(partID) + '.dat')
    if str(receiveOffical.content)[2] == '<' and str(receiveUnoffical.content)[2] == '<':
        return (False, False)
    else:
        fileName = str(partID).split("/")[-1]
        if str(receiveOffical.content)[2] == '<':
            with open(outputFolder + '\\' + fileName + '.dat', 'wb') as f:
                f.write(receiveUnoffical.content)
            return (True, False)
        else:
            with open(outputFolder + '\\' + fileName + '.dat', 'wb') as f:
                f.write(receiveOffical.content)
            return (True, True)

def urlScrape(partID, outputFolder):
    url = ""
    status, official = requestPart(partID, outputFolder)
    if status:
        if official:
            url = 'https://www.ldraw.org/official-part-lookup.htm?folder=parts&partid=' + str(partID) + '.dat'
        else:
            url = 'https://www.ldraw.org/cgi-bin/ptdetail.cgi?f=parts/' + str(partID) + '.dat'
    else:
        return (False, [])
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        url = str(link.get('href'))
        if 'official-part-lookup.htm?folder=parts&partid=' in url or 'cgi-bin/ptdetail.cgi?f=parts/' in url:
            urls.append(url)
    if official:
        return (True, urls)
    else:
        return (True, urls[2:-2])

def recurrsionModule(partIDs, outputFolder, visited):
    if len(partIDs) == 0:
        return []
    else:
        for i in range(len(partIDs)):
            status, urls = urlScrape(partIDs[i], outputFolder)
            partIDsRecur = []
            if status:
                for url in urls:
                    if url[1:2] == 'o':
                        if url[46:-4] not in visited:
                            partIDsRecur.append(url[46:-4])
                    if url[1:2] == 'c' not in visited:
                        if url[30:-4] not in visited:
                            partIDsRecur.append(url[30:-4])
            visited.append(partIDs[i])
            partIDs[i] = [recurrsionModule(partIDsRecur, outputFolder, visited)]
        return partIDs