#imports
import pandas as pd
from datetime import date, timedelta
import folium
from folium import Marker
from folium.plugins import MarkerCluster
import math
import matplotlib.pyplot as plt
import seaborn as sns

#Population Data
population = pd.read_csv('/kaggle/input/2019-census-us-population-data-by-state/2019_Census_US_Population_Data_By_State_Lat_Long.csv')
statePopulation = population.POPESTIMATE2019


#Getting the most recent date for filtering
freshDate = date.today() - timedelta(days=1)
freshDate = date.strftime(freshDate,"%Y%m%d")
freshDate = freshDate[0:4] + "-" + freshDate[4:6] + "-" + freshDate[6:8]


#Vaccination Data
vaccinationData = pd.read_csv('https://covid.ourworldindata.org/data/vaccinations/us_state_vaccinations.csv')

#Filtering for US locations and most recent Date
firstVaccineData = vaccinationData.loc[(vaccinationData.date == freshDate)& (vaccinationData.location.isin(['Alabama','Alaska',
'Arizona','Arkansas','California','Colorado','Connecticut',
'Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas',
'Kentucky','Louisiana','Maine','Maryland','Massachusetts',
'Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada',
'New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota',
'Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee',
'Texas','Utah','Vermont','Virginia',
'Washington','West Virginia','Wisconsin','Wyoming']))] 
vaccinationPerLocation = firstVaccineData.people_vaccinated
percentVaccinated = []
#Calculating percent vaccinated by population and vaccine data
for i in vaccinationPerLocation:
    for j in statePopulation:
        tempPercent = i/j
        tempPercentString = str(tempPercent)
        tempPercentStringFin = "Percent Vaccinated: " + tempPercentString[0:5] + " %"
        percentVaccinated.append(tempPercentStringFin)
lat = population.lat
long = population.long
percentVaccinatedDF = pd.DataFrame(percentVaccinated, columns=["pct"])

#Creating final dataframe
vaccinationByLocation = pd.DataFrame({'pct': [], 'long': [], 'lat':[]})
vaccinationByLocation['pct'] = percentVaccinatedDF.pct
vaccinationByLocation['long'] = long
vaccinationByLocation['lat'] = lat

#calculating the total percent vaccinated in the US       
totalPopulation = 0
totalVaccinated = 0
for i in vaccinationPerLocation:
    for j in statePopulation:
        totalPopulation += j
        totalVaccinated += i
totalPopulationPercentVaccinated =   totalVaccinated / totalPopulation


# Bar chart showing total vaccinated in the US vs. total population
plt.figure(figsize=(3,3))
plt.title("Total Percent Vaccinated in the US")
sns.barplot(y=totalPopulationPercentVaccinated)
print(totalPopulationPercentVaccinated)    

#Displaying the Vaccine dataframe
vaccinationByLocation.head()

# Create the map
v_map = folium.Map(location=[42.32,-71.0589], tiles='cartodbpositron', zoom_start=4) 

# Add points to the map
mc = MarkerCluster()
for idx, row in vaccinationByLocation.iterrows(): 
    if not math.isnan(row['long']) and not math.isnan(row['lat']):
        mc.add_child(Marker(location=[row['lat'], row['long']],tooltip=[row['pct']]))
v_map.add_child(mc)

# Display the map
v_map
