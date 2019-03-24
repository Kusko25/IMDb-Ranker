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
    with open("filmlist.txt","r") as o:
        for l in o:
            yield l.strip()

def display(header,results):
    print('\t'.join(header))
    print('\n'.join('\t'.join(result) for result in results))

def printToFile(header, results, filename="results.csv"):
    with open(filename,"w+") as o:
        o.write(f"{';'.join(header)}\n")
        o.write('\n'.join(';'.join(result) for result in results).replace(".", ","))

def main():
    header = ["Title","IMDb"]
    results = [ [title,parseMovieIMDB(title)] for title in progressbar.progressbar(list(getNames()))]
    print(results)
    results.sort(key=lambda x: x[1],reverse=True)
    display(header,results)
    printToFile(header,results)

if __name__ == '__main__':
    main()
