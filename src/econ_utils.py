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

def iex_cloud_api(request_path, **params):
  """
  Facilitates api calls to IEX cloud
  :param str request_path: IEX cloud path to make request. Requests are made
    to the `stable` endpoint.
  :param params: Additional params to provide for the request. The token is
    provided for you through `IEX_CLOUD_API_TOKEN` environment variable
  :type params: dict or None
  :return: Json response
  :raises RuntimeError: if the request fails with any status code other than 
    `200`.
  """
  base_path = "https://cloud.iexapis.com/stable"
  response = requests.get(f"{base_path}/{request_path}", params={
    "token": config["IEX_CLOUD_API_TOKEN"],
    **params
  })
  if(response.status_code != 200):
    print(response.text)
    raise RuntimeError("IEX cloud access error")
  return response.json()

def coinmarketcap_api(request_path, **params):
  """
  Facilitates api calls to CoinMarketCap
  :param str request_path: the endpoint to make the requesto
  :param dict params: parameters to use for the request
  :return: json response
  :raises RuntimeError: if the request fails with any status code other than
    `200`.
  """
  base_url = "https://pro-api.coinmarketcap.com/v1"
  headers = {
    "Accept": "application/json",
    "X-CMC_PRO_API_KEY": config["COINMARKETCAP_API_KEY"]
  }
  response = requests.get(
    f"{base_url}/{request_path}", 
    params=params, 
    headers=headers
  )
  if response.status_code != 200:
    print(response.text)
    raise RuntimeError("Coinmarketcap access error")
  return response.json()
