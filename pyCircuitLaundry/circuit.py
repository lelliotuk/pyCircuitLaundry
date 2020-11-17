import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup as BS
from .exceptions import *

_CIRCUIT_URL_BASE = "https://www.circuit.co.uk/circuit-view/"
_API_URL_BASE = "https://358n2fyyol.execute-api.eu-west-1.amazonaws.com/prod/api/v1/search/cs3/"

APP_STATE = {
    "A": "Active", 
    "I": "InActive", 
    "X": "Idle", 
    "?": "Unknown", 
    "B": "Broken"
}
APP_TYPE = {
    "W": "Washer", 
    "D": "Dryer", 
    "ST": "Stack"
}

def _api_url(api_id):
    return _API_URL_BASE + str(api_id) + "?full=Y"

def _datetime(timestamp):
    return datetime.strptime(timestamp, "%Y%m%d%H%M%S")

def _search_form(city_id = 0, provider_id = 0, site_id = 0):
    return {
        "CityID": str(city_id),
        "OrganisationID": str(provider_id),
        "TopupPointID": str(site_id),
        "Ajax": "true"
    }

def _get_select_options(field, city_id = 0, provider_id = 0):
    form = _search_form(
        city_id=city_id, 
        provider_id=provider_id, 
    )
    response = requests.post(_CIRCUIT_URL_BASE, data=form).content
    soup = BS(response, 'html.parser')
    soup = soup.find(id=field)
    soup = soup.find_all("option")[1:]
    return {option.text:option["value"] for option in soup}


def get_cities():
    return _get_select_options("CityID")
   
   
def get_providers(city_id):
    return _get_select_options("OrganisationID", city_id=city_id)


def get_sites(city_id, provider_id):
    return _get_select_options("TopupPointID", city_id=city_id, provider_id=provider_id)


def get_api_id(city_id = 0, provider_id = 0, site_id = 0):
    form = _search_form(
        city_id=city_id, 
        provider_id=provider_id, 
        site_id=site_id
    )
    url = _CIRCUIT_URL_BASE + "laundry-site/?site=" + str(site_id)
    response = requests.post(url , data=form)
    if "/circuit-view/site-unavailable/" in response.url:
        raise CircuitSiteUnavailableError(city_id, provider_id, site_id)
    response_content = response.content
    soup = BS(response_content, 'html.parser')
    soup = soup.find("iframe", {"class":"circuit-view-iframe"})
    return soup["src"].split("/")[-1]


class Circuit:
    def __init__(self, api_id):
        self._id = api_id
        self.update()
    
    def update(self):
        response = requests.get(_api_url(str(self._id))).content
        data = json.loads(response)
        self._data = data
        
        
        if data["exists"] == False:
            raise CircuitSiteNotFoundError(self._id)
        
        self._name = data["site"]["displayName"]
        self._created =  _datetime(data["site"]["createdTimeUtc"])
        self._last_updated = _datetime(data["site"]["lastUpdatedUtc"])
        
        size = data["site"]["room"]["size"]
        self._size = (size["D"], size["W"], size["H"]) # d,w,h
        
        walls = []
        for wall_data in data["site"]["room"]["walls"]:
            walls.append(Wall(wall_data))
        self._walls = tuple(walls)
        
        self._machines = []
        for app_data in data["site"]["room"]["apps"]:
            if app_data["t"] == "ST":
                pos_data = app_data["pos"]
                rot = app_data["rot"]
                self._machines.append(Machine(app_data["top"], pos_data, rot, True))
                self._machines.append(Machine(app_data["bottom"], pos_data, rot))
            else:
                self._machines.append(Machine(app_data))
        #self._machines = machines
        
    @property
    def data(self): return self._data
    
    @property
    def name(self): return self._name
    
    @property
    def machines(self): return self._machines
    
    @property
    def size(self): return self._size
    
    @property
    def walls(self): return self._tuples
    
    @property
    def id(self): return self._id
    
    @property
    def created(self): return self._created
    
    @property
    def last_updated(self): return self._last_updated
