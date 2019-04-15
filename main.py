import re
import progressbar
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
from prettytable import  PrettyTable


def parseMovieIMDB(movieName):
    url = "https://www.imdb.com/find?q=" + re.sub(r' ',r'+',movieName)
    soup = BeautifulSoup(urlopen(url),'html.parser')
    link = soup.find(attrs={'class': 'result_text'}).find('a').get('href')
    return BeautifulSoup(urlopen("https://www.imdb.com" + link),'html.parser').find(attrs={'itemprop':'ratingValue'}).get_text()

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
    header = ["Title","IMDb"]
    results = [ [title,parseMovieIMDB(title)] for title in progressbar.progressbar(list(getNames()))]
    results.sort(key=lambda x: x[1],reverse=True)
    display(header,results)
    printToFile(header,results)

if __name__ == '__main__':
    main()
