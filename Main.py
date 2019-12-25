#  Question: Is there any correlation between GDP per capita and military spending of a country? And to what extend?
#  2 datasets from Kaggle.com: gdp.csv and Military_Expenditure.csv

#  imports
import pandas as pd
import numpy as np

#  Data loading / preparing
#  Here I loaded the data using pandas and selected the needed columns
gdp = pd.read_csv('gdp.csv', usecols=['CountryName', 'CountryCode', 'GDP_PerCapita_2000_US$', 'GDP_PerCapita_2005_US$',
                                      'GDP_PerCapita_2010_US$', 'GDP_PerCapita_2015 US$', 'GDP_PerCapita_2016_US$'])

military_spending = pd.read_csv("Military_Expenditure.csv", usecols=['Name', 'Code', '2000', '2005', '2010',
                                                                     '2015', '2016'])

population = pd.read_csv("POP_TOTAL_DS2_en_v2.csv", usecols=["Country Name", "Country Code", "2000", "2005", "2010",
                                                             "2015", "2016"])
#  Here I checked if all the countries that are in the gdp file, are actually in the military spending file.
countries = list(military_spending.Code)
pop_countries = list(population['Country Code'])
good_list = list()
bad_list = list()

#  This is the for loop that check the country codes and appends them into the corresponding list
for country in list(gdp.CountryCode):
    if country in countries and country in pop_countries:
        good_list.append(country)
    else:
        bad_list.append(country)

#  Here I check whenever the list is empty, what indicates the every country that is in gdp is also in Military spending
if len(bad_list) == 0:
    print('True, every country which is in gdp, is also in military spending!\n')

#  So now I want to create a matrix which has all the combined values of a country from the two files as values.
merged = list()
for row in gdp.values:
    for row1 in military_spending.values:
        if row[1] == row1[1]:
            for row2 in population.values:
                if row[1] == row2[1]:
                    mixed = np.concatenate((row[1:], row1[2:], row2[2:]))
                    merged.append(mixed)

#  Here I check if the matrix 'merged' has all the countries
check_list = list()
for index, country in enumerate(list(gdp.CountryCode)):
    if country == merged[:][index][0]:
        check_list.append(1)
    else:
        check_list.append(0)

#  Here I check whenever the list only has 1 which indicates that all the countries are correctly placed in 'merged'
if all(check_list) == 1:
    print('All the values are in the list "merged" \n')

#  here I go country by country in the 'merged' matrix and look if the increase in gdp also results in increase of
#  military spending
country_mixed = list()
for country in merged[:][:]:
    gdp = list(country[1:6])
    spending = list(country[6:11])
    population_ = list(country[11:])
    zipped = tuple(zip(gdp, spending, population_))

    country_mixed.append(zipped)

# Here is where the analysis part starts, above I've prepared my data and now we can manipulate it
# now I will get the percentages of military spending per person per 5 year since 2000 to 2015 and also including 2016
index1 = 0
percentages = list()
for country in country_mixed:
    #  print('\n----------country: ' + str(merged[:][index1][0]) + ' -----------')
    index1 += 1
    for zipped in country:
        gdp_country = zipped[0] * zipped[2]
        military_spending_pp = zipped[1] / zipped[2]
        military_spending_gdp = zipped[1] / gdp_country * 100
        percentages.append(military_spending_gdp)
        #  print(f"{round(gdp_country, 2)}$ GDP in USD     :     {round(military_spending_pp, 2)}"
        #  f"$ Military spending per person in USD     :     {round(military_spending_gdp,1)}"
        #  f"% Military spending as percent of GDP in USD")

#  Here I group the percentages for every year for every country and then I can measure the change over time
list_percentages = list()
hold_list = list()

for percentage in percentages:
    if len(hold_list) <= 5:
        hold_list.append(round(percentage, 1))
    if len(hold_list) == 5:
        list_percentages.append(list(hold_list))
        hold_list.clear()


#  Here I will be finding if there is any correlation between the GDP and the military spending
difference_list = list()
hold_list_ = list()
for list__ in list_percentages:
    for index in range(1, 5):
        difference = list__[index] - list__[index - 1]
        if len(hold_list_) <= 4:
            hold_list_.append(round(difference, 1))
        if len(hold_list_) == 4:
            difference_list.append(np.array(hold_list_))
            hold_list_.clear()


#  here I add the percentages to see the overall effect per country
sums = list()
for list___ in difference_list:
    sum_ = round(np.nansum(list___), 2)
    sums.append(np.array(sum_))

#    Here I display the info (the difference in military spending as percentage of gdp per years: 2000, 2005, 2010, 2015
#    ,2016)
#    according to the corresponding country
country_value = tuple(zip(sums, good_list))
for country_ in country_value:
    print(*country_)


def info_display(x):
    values = [merged, country_mixed, list_percentages, difference_list, sums, country_value]
    print(values[x])


print(info_display(x))  # here you need to fill in which variable you want to display
