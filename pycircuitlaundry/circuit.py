import requests
import json
from bs4 import BeautifulSoup as BS
from .exceptions import *
from .machine import *
from .wall import *
from .timestamp import *

_CIRCUIT_URL_BASE = "https://www.circuit.co.uk/circuit-view/"
_API_URL_BASE = "https://358n2fyyol.execute-api.eu-west-1.amazonaws.com/prod/api/v1/"

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
    return _API_URL_BASE + "search/cs3/" + str(api_id) + "?full=Y"


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


# def api_get_cities():
    # response = requests.get(_API_URL_BASE + "locations").content
    # data = json.loads(response)
    # return tuple(data)

# def api_get_providers(city):
    # response = requests.get(_API_URL_BASE + "search/location/" + city + "/campus").content
    # data = json.loads(response)
    # return {p["name"]:p["id"] for p in data}

class Circuit:
    def __init__(self, api_id):
        self._api_id = api_id
        
        self._layout = []
        self._washers = []
        self._dryers = []
        self._available_washers = []
        self._available_dryers = []
        
        self.update()
    
    def update(self):
        response = requests.get(_api_url(self._api_id)).content
        data = json.loads(response)
        self._data = data
        
        
        if data["exists"] == False:
            raise CircuitSiteNotFoundError(self._id)
        
        self._name = data["site"]["displayName"]
        self._available = data["site"]["available"]
        self._postcode = data["site"]["postcode"] if "postcode" in data["site"] else None
        self._created =  to_datetime(data["site"]["createdTimeUtc"])
        self._last_updated = to_datetime(data["site"]["lastUpdatedUtc"])
        self._site_id = data["site"]["siteNumber"]
        
        size = data["site"]["room"]["size"]
        self._size = (size["W"], size["D"], size["H"]) # d,w,h
        
        
        for wall_data in data["site"]["room"]["walls"]:
            self._layout.append(Wall(wall_data))


        
        for app_data in data["site"]["room"]["apps"]:
            if app_data["t"] == "ST":
                pos_data = app_data["pos"]
                rot = app_data["rot"]
                
                type_list = self._washers if app_data["top"]["t"] == "W" else self._dryers
                type_list.append(Machine(app_data["top"], pos_data, rot, True))
                
                type_list = self._washers if app_data["bottom"]["t"] == "W" else self._dryers
                type_list.append(Machine(app_data["bottom"], pos_data, rot))
            else:
                type_list = self._washers if app_data["t"] == "W" else self._dryers
                type_list.append(Machine(app_data))

        
        floor_colour = data["site"]["room"]["colours"]["ground"]
        self._floor_colour = (
            floor_colour["r"] * 255, floor_colour["g"] * 255, floor_colour["b"] * 255)
        
        wall_colour = data["site"]["room"]["colours"]["wallDefault"]
        self._wall_colour = (
            wall_colour["r"] * 255, wall_colour["g"] * 255, wall_colour["b"] * 255)
        
        for w in self._washers:
            if w.state == "I": self._available_washers.append(w)
            
        for d in self._dryers:
            if d.state == "I": self._available_dryers.append(d)
        
        self._layout = tuple(self._layout)
        self._washers = tuple(self._washers)
        self._dryers = tuple(self._dryers)
        self._available_washers = tuple(self._available_washers)
        self._available_dryers = tuple(self._available_dryers)
        
    @property
    def data(self): return self._data
    
    @property
    def name(self): return self._name
    
    @property
    def available(self): return self._available
    
    @property
    def postcode(self): return self._postcode
    
    @property
    def machines(self): return self._washers + self._dryers
    
    @property
    def washers(self): return self._washers
    
    @property
    def dryers(self): return self._dryers
    
    @property
    def available_machines(self): return self._available_washers + self._available_dryers
    
    @property
    def available_washers(self): return self._available_washers
    
    @property
    def available_dryers(self): return self._available_dryers
    
    @property
    def dimensions(self): return self._dimensions
    
    @property
    def layout(self): return self._layout
    
    @property
    def api_id(self): return self._api_id
    
    @property
    def created(self): return self._created
    
    @property
    def last_updated(self): return self._last_updated
    
    @property
    def site_id(self): return self._site_id
    
    @property
    def wall_colour(self): return self._wall_colour
    
    @property
    def floor_colour(self): return self._floor_colour
