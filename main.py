import re
import progressbar
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
from prettytable import  PrettyTable


def parseMovieIMDB(movieName):
    url = "https://www.imdb.com/find?q=" + re.sub(r' ',r'+',movieName)
    request = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'})
    soup = BeautifulSoup(urlopen(request),features="lxml")
    url = soup.find(attrs={'class': 'result_text'}).find('a').get('href')
    if url==None:
        return None

    request = urllib.request.Request("https://www.imdb.com" + url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'})
    soup = BeautifulSoup(urlopen(request),features="lxml")
    result = soup.find(attrs={'itemprop':'ratingValue'})
    if result==None:
        return None
    return result.get_text()

def parseMovieGoogle(movieName):
    url = "https://www.google.de/search?q=" + re.sub(r' ',r'+',movieName)
    request = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'})
    soup = BeautifulSoup(urlopen(request),features="lxml")
    result = soup.find(attrs={'class': 'srBp4 Vrkhme'})
    if result==None:
        return None
    result=result.get_text()
    result=re.search("\\d+.%",result)
    return result.group()

def getNames():
    with open("filmlist.txt","r") as o:
        for l in o:
            yield l.strip()

def display(header,results):
    table = PrettyTable()
    table.field_names = header
    [table.add_row(result) for result in results]
    print(table)

def printToFile(header, results, filename="results.csv"):
    with open(filename,"w+") as o:
        o.write(f"{';'.join(header)}\n")
        o.write('\n'.join(';'.join(result) for result in results).replace(".", ","))

def main():
    header = ["Title","IMDb","Google"]
    results = []
    for title in progressbar.progressbar(list(getNames())):
        result = [title]
        for i in range(2):
            if i==0:
                value = parseMovieIMDB(title)
            else:
                value = parseMovieGoogle(title)

            if value==None:
                result.append("n/a")
            else:
                result.append(value)
        results.append(result)
    results.sort(key=lambda x: x[1],reverse=True)
    display(header,results)
    printToFile(header,results)

if __name__ == '__main__':
    main()
