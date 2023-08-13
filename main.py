from bs4 import BeautifulSoup as bs
import requests
import os
import csv

state = input("Enter the state you want: ")
city = input("Enter the city you want to scrape weather for: ")
city = city.replace(" ", "-")

url = "https://weather-us.com/en/" + state + "-usa/" + city

response = requests.get(url)
html_content = response.content

soup = bs(html_content, 'html.parser')

# this dict has 3 data points, time, temp and weather
hourlyWeather = []

time = []
temp = []
weather = []

#finds every time, weather and temp data point on the page

for i in soup.find_all('div', class_='col-4 text-sm-center'):
    selTime = i.find('span').text.strip()
    time.append(selTime)
    

for i in soup.find_all('li', class_='fs-2'):
    selTemp = i.text.strip()
    selTemp = selTemp.replace('Â', '')
    temp.append(selTemp)




for i in soup.find_all('div', class_='col-sm-7 col-md-7 col-lg-6 px-0 ps-sm-2'):
    selWeather = i.find('span').text.strip()
    weather.append(selWeather)

#adding the data to the dict
for i, item in enumerate(weather):
    hourlyWeather.append({'Time': time[i], 'Temperature': temp[i], 'Weather': weather[i]})

response.close()

#Outputs data to a csv

scriptDir = os.path.dirname(os.path.abspath(__file__))

csvName = os.path.join(scriptDir, 'weatherFor' + city + '.csv')

with open(csvName, 'w', newline='', encoding='utf-8') as csvFile:
    fieldnames = ['Time', 'Temperature', 'Weather']
    writer=  csv.DictWriter(csvFile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(hourlyWeather)

print("Data saved to " + csvName)




