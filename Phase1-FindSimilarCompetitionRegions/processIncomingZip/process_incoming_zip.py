import sys
import pandas as pd
import numpy as np
sys.path.append('water/')
sys.path.append('demographics/')
sys.path.append('../Phase0-DefineCompetitionRegions/03-ParseUserZip/')
#sys.path.append('../manipulation_scripts/')
import preprocess_water as pw
import census_scrape as cs
import scrape_ewg as se
import extract_lat_lon as ell
#import centroid_txt_to_csv as ctc

aggregated_data_path = 'Phase1-FindSimilarCompetitionRegions/data/aggregated_data.csv'
water_columns_path = 'Phase1-FindSimilarCompetitionRegions/data/water_columns.txt'




def get_water_data(user_location):
  ## takes in df with one row with location data about user input
  ## returns a dict where keys are water col names and values are counts of the contams

  target_water_columns = eval(open(water_columns_path, 'r').read())

  water_counts = {}

  for e in target_water_columns:
    water_counts[e] = 0

  user_water = se.scrape_ewg(user_location.rename(columns = {'zipcode':'zip'})[['zip', 'state_id']])

  for city in user_water:
    for contam in city['contaminants_above_hbl']:
      if 'contam_' + contam in water_counts:
        water_counts['contam_' + contam] += 1
    for contam in city['contaminants_other']:
      if 'contam_' + contam in water_counts:
        water_counts['contam_' + contam] += 1


  return water_counts



def process_incoming_zip(user_zip):

  ## takes as input zipcode from user
  ## returns a one-line df with same columns as centroid data
    ## elements are *counts*

  ## translate zip code to location
  user_location = ell.extract_lat_lon(user_zip)

  if user_location == 'ZIPCODE INVALID':
    return 'The zipcode you entered is invalid. Please enter a valid US zipcode.', 1
    

  del(user_location['geopoint'])
  user_location = pd.DataFrame(user_location, index = [0])
  user_location = user_location.rename(columns = {'zip': 'zipcode', 'state': 'state_id'}).astype({'zipcode': str}).dropna(subset = ['zipcode'])
  user_location = user_location[user_location['zipcode'].map(len) == 5]


  ## get water data -- comes in as dict where keys are cols and vals are counts
  user_water = pd.DataFrame(get_water_data(user_location), index = [0])

  ## get census data -- comes in as df with one row
  user_demo = cs.webScrape([user_zip]).drop('zipcode', axis = 1)

  user_base = user_location[['zipcode', 'latitude', 'longitude']]

  user_data = pd.concat([user_base, user_water, user_demo], axis = 1)

  return user_location, user_data


if __name__ == '__main__':

  args = sys.argv[1:]

  if len(args) != 1:
    print('Usage: zipcode')
    sys.exit(1)

  user_zip = args[0]

  print(process_incoming_zip(user_zip))