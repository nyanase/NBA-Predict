from bs4 import BeautifulSoup
import urllib.request
import csv

#specify the url
urlpage = 'https://www.basketball-reference.com/leagues/NBA_2015_games.html'

page = urllib.request.urlopen(urlpage)

soup = BeautifulSoup(page, 'html.parser')

current = soup.find_all(attrs={'class': 'current'})[-2]

rows = []
rows.append(['Date', 'Start(ET)', 'Visitor', 'PTS Visitor', 'Home', 'PTS Home', 'OT', 'Attending'])

def getData(results):
  for result in results:
    if not result.find('td'):
      return False
    
    date = result.find('th').find('a').getText()
    
    data = result.find_all('td')
    
    start = data[0].getText()
    visitor = data[1].find('a').getText()
    pts_visitor = data[2].getText()
    home = data[3].find('a').getText()
    pts_home = data[4].getText()
    ot = data[6].getText()
    attending = data[7].getText()
    
    rows.append([date, start, visitor, pts_visitor, home, pts_home, ot, attending])
    
    print(rows[-1])
  
  return True

while current.next_sibling:
  table = soup.find('table', attrs={'id':'schedule'})
  table_body = table.find('tbody')
  results = table_body.find_all('tr')
  
  if getData(results) == False:
    break
  
  current = current.next_sibling
  urlpage = current.find('a').get('href')
  page = urllib.request.urlopen("https://www.basketball-reference.com/" + urlpage)
  soup = BeautifulSoup(page, 'html.parser')
  
with open('test.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(rows)