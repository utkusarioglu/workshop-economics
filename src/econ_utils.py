from dotenv import dotenv_values
import json
import requests
import pandas as pd

config = dotenv_values()

def bea_api(**params):
  """
  Returns the api response from bureau of economic analysis of usa
  params for this method are provided to the get query.
  Refer to bea api documentation for details on the params:
  https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf

  :param dict params: parameters to provide to the endpint. `UserID` and 
    `ResultFormat` are already provided for you.
  :returns: a tuple of request data, results, and result keys
  :raises TypeError: if the results object doesn't have any keys. 
    This indicates that something went wrong with the request.
  """
  bea_response_text = requests.get("https://apps.bea.gov/api/data", params={
    "UserID": config["BEA_API_KEY"],
    "ResultFormat": "JSON",
    **params  
  }).text
  bea_json = json.loads(bea_response_text)["BEAAPI"]
  
  if(not bea_json["Results"]):
    print(bea_json)
    raise TypeError("Results key doesn't appear in the response")

  return bea_json["Request"], bea_json["Results"], bea_json.keys()

def create_df(data):
  """ Creates a vanilla dataframe """
  return pd.DataFrame([pd.Series(row.values(), index=row.keys()) for row in data])
