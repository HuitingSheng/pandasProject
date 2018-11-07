# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 22:41:01 2018

@author: Huiting
"""
# =============================================================================
# import  and encoding the file 
# =============================================================================
import pandas as pd
autos=pd.read_csv("autos.csv", encoding="Latin-1")

#print(autos.info())
#print(autos.head())

# =============================================================================
# cleaning column Names, 
#Change the columns from camelcase to snakecase.
#Change a few wordings to more accurately describe the columns.
# =============================================================================

autos.columns

# =============================================================================
# def clean_col(col):
#     col=col.replace("yearOfRegistration", "registration_year")
#     col=col.replace("monthofRegistration", "registration_month")
#     col=col.replace("notRepairredDamage", "unrepaired_damage")
#     col=col.replace("dateCreated", "ad_created")
#     col=col.strip()
#     col=col.lower()
#     col=col.replace(" ", "_")
#     return col
#
#autos.columns=[clean_col(c) for c in autos.columns]
# =============================================================================

autos.columns=['date_Crawled', 'name', 'seller', 'offer_type', 'price', 'ab_test',
       'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
       'odometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_Damage', 'ad_created', 'num_photos', 'postal_code',
       'last_seen']

#print(autos.columns)

#print(autos.head())
#print(autos["num_photos"].value_counts())
#print(autos.describe(include='all'))
autos.drop(['num_photos','seller', 'offer_type'], axis=1)
autos["price"]=autos["price"].str.replace("$", "").str.replace(",", "").astype(int)
autos["odometer"]=autos["odometer"].str.replace("km", "").str.replace(",", "").astype(int)
autos.rename({"odometer": 'odometer_km'}, axis=1, inplace=True)
#autos["price"]=autos["price"]
#print(autos.describe(include='all'))

#print(autos["odometer_km"].unique().shape)
#print(autos["odometer_km"].describe())
#print(autos["odometer_km"].value_counts())
#print(autos["price"].unique().shape)
#print(autos["price"].describe())
#print(autos["price"].value_counts().head(20))
#print(autos["price"].value_counts().sort_index(ascending=False).head(20))
#print(autos["price"].value_counts().sort_index(ascending=True).head(20))
# =============================================================================
# There are a number of listings with prices below \$30, including about 1,500 at \$0. 
#There are also a small number of listings with very high values, including 14 at around or over $1 million.
# =============================================================================

#autos=autos[autos["price"].between(1,1351000)]
#print(autos["price"].describe())

autos[['date_Crawled','ad_created','last_seen']][0:5]
print(autos["date_Crawled"].str[:10].value_counts(normalize=True, dropna=False) .sort_index())
print(autos["date_Crawled"].str[:10].value_counts(normalize=True, dropna=False) .sort_values())
# =============================================================================
# 
# Looks like the site was crawled daily over roughly a one month period in March and April 2016.
#  The distribution of listings crawled on each day is roughly uniform.
# =============================================================================

print(autos["last_seen"].str[:10].value_counts(normalize=True, dropna=False).sort_index(ascending=True))


# =============================================================================
# The crawler recorded the date it last saw any listing, which allows us to determine on what day a listing was removed,
#  presumably because the car was sold.
# 
# The last three days contain a disproportionate amount of 'last seen' values. 
# Given that these are 6-10x the values from the previous days, 
# it's unlikely that there was a massive spike in sales, and more likely that these values 
# are to do with the crawling period ending and don't indicate car sales.
# =============================================================================


print(autos["ad_created"].str[:10].unique().shape)
print(autos["ad_created"].str[:10].value_counts(normalize=True, dropna=False).sort_index(ascending=True))

# =============================================================================
# There is a large variety of ad created dates. Most fall within 1-2 months of the listing date, 
# but a few are quite old, with the oldest at around 9 months.
# =============================================================================


print(autos["registration_year"].describe())
# =============================================================================
# car cannot registrate in year of 1000 and year of 9999
# =============================================================================
autos=autos[autos["registration_year"].between(1900,2016)]
print(autos["registration_year"].value_counts(normalize=True).head(10))

# =============================================================================
# most of the vehicles were first registered in the past 20 years
# =============================================================================
print( autos["brand"].value_counts(normalize=True))

# =============================================================================
# 
# German manufacturers represent four out of the top five brands, almost 50% of the overall listings. 
# Volkswagen is by far the most popular brand, with approximately double the cars for sale of the next two brands combined.
# 
# There are lots of brands that don't have a significant percentage of listings, so we will limit our analysis to brands
#  representing more than 5% of total listings.
# 
# =============================================================================
brand_counts=autos['brand'].value_counts(normalize=True)
common_brands=brand_counts[brand_counts>0.05].index
print(common_brands)

brand_mean_prices={}
for brand in common_brands:
    brand_only=autos[autos["brand"]==brand]
    mean_price=brand_only["price"].mean()
    brand_mean_prices[brand]=int(mean_price)
print(brand_mean_prices)

# =============================================================================
# Audi, BMW and Mercedes Benz are more expensive
# Ford and Opel are less expensive
# Volkswagen is in between - this may explain its popularity, it may be a 'best of 'both worlds' option.
# =============================================================================

bmp_series=pd.Series(brand_mean_prices)
print(bmp_series)
pd.DataFrame(bmp_series,columns=["mean_mileage"])
brand_mean_mileage={}
for brand in common_brands:
    brand_only=autos[autos["brand"]==brand]
    mean_mileage=brand_only["odometer_km"].mean()
    brand_mean_mileage[brand]=int(mean_mileage)
    
mean_mileage=pd.Series(brand_mean_mileage).sort_values(ascending=False)
mean_prices=pd.Series(brand_mean_prices).sort_values(ascending=False)
brand_info=pd.DataFrame(mean_mileage,columns=["mean_mileage"])
print(brand_info)
print(mean_price)
brand_info["mean_price"]=mean_prices
print(brand_info)