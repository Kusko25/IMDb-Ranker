import re
import progressbar
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup


def parseMovieIMDB(movieName):
    url = re.sub(r' ',r'+',movieName)
    url = "https://www.imdb.com/find?q=" + url
    page = urlopen(url)
    soup = BeautifulSoup(page,'html.parser')
    link = soup.find(attrs={'class': 'result_text'}).find('a').get('href')
    page = urlopen("https://www.imdb.com" + link)
    soup = BeautifulSoup(page,'html.parser')
    rating = soup.find(attrs={'itemprop':'ratingValue'}).get_text()
    return rating

# def parseMovieGoogle(movieName):
#     url = re.sub(r' ',r'+',movieName)
#     url = "https://www.google.com/search?q=" + url
#     opener = urllib.request.build_opener()
#     opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
#     page = opener.open(url)
#     soup = BeautifulSoup(page,'html.parser')
#     print(soup.find(attrs={'class': 'srBp4 Vrkhme'}))
#     # rating = re.search(r'\d{1,3} %',link)
#     # return rating
#
# def parseMovieRoTo(movieName):
#     url = re.sub(r' ',r'%20',movieName)
#     url = "https://www.rottentomatoes.com/search/?search=" + url
#     page = urlopen(url)
#     soup = BeautifulSoup(page,'html.parser')
#     soup = soup.find(attrs={'id': 'movieSection'}).find('ul',{'class':'results_ul'})
#     matchedString = ""
#     while matchedString != movieName:
#         rating = soup.findNext('span',{'class':'tMeterScore'}).get_text()
#         matchedString = soup.findNext('a',{'class':'unstyled articleLink'}).get_text()
#     print(matchedString + "|" + rating)
#     return rating


def getNames():
    content = []
    for line in open("filmlist.txt","r"):
        content.append(line.strip())
    return content

def display(header,results):
    for column in header:
        print(column+"\t",end='')
    print()
    for line in results:
        for column in line:
            print(column+"\t",end='')
        print()

def printToFile(header, results, filename="results.csv"):
    o = open(filename,"w+")
    first = True
    for column in header:
        if first:
            first=False
        else:
            o.write(";")
        o.write(column)
    o.write("\n")
    for line in results:
        first = True
        for column in line:
            if first:
                first=False
            else:
                o.write(";")
            o.write(column)
        o.write("\n")

def main():
    content = getNames()
    header = ["Title","IMDb"]
    results = []
    for title in progressbar.progressbar(content):
        line = [title,parseMovieIMDB(title)]
        results = results + [line]
    results.sort(key=lambda x: x[1],reverse=True)
    display(header,results)
    printToFile(header,results)

main()
