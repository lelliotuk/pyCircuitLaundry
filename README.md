
# pyCircuitLaundry
 Circuit Laundry Circuit View API wrapper

## Install
`pip install git+https://github.com/lelliotuk/pyCircuitLaundry/`

## Usage
If you're looking for random laundry rooms, don't be surprised if a lot of them don't work because a lot of them are out of service on the website.

You currently need to make 4 requests to find the API ID for a specific site:

`get_cities()`  
Get dict of cities with their internal IDs

`get_providers(city_id)`  
Get dict of providers from a city using its internal ID

`get_sites(city_id, provider_id)`  
Get dict of sites from a provider (both parameters are necessary)

`get_api_id(site_id)`
Finally, get the API ID for the site

Then you can create a laundry room oject using the API ID:
`room = Circuit(api_id)`

---
### `Circuit` object
Laundry room

**Methods**  
`update()` - Updates data from API  

**Attributes**  
`data` - Dict of raw API values  
`api_id` - API ID  
`site_id` - Site ID  
`name` - External name of the site  
`machines` - Tuple of `Machine` objects  
`dimensions` - Tuple of room dimensions (width, depth, height)  
`layout` - Tuple of walls defining layout of room  
`created` - Datetime of when site was created (probably when Circuit/online functionality was added to the site/room)  
`last_updated` - Datetime of last update to the API from the site  
`wall_colour` - Default wall colour tuple (R,G,B) 0-255  
`floor_colour` - Colour of room floor  

---
### `Machine` object
A single washing machine or dryer

**Attributes**  
`app_type` - Appliance type string
- `"W"` Washer
- `"D"` Dryer

`state` - Appliance state string
- `"A"` Active, currently in use
- `"I"` Inactive, not in use
- `"X"` Idle, finished but still in use
- `"?"` Unknown
- `"B"` Broken, out of service

`number` - Machine number int (`machines` index is not guaranteed to match)  
`label` - Machine name, usually just a string of the number  
`model` - Machine model, some kind of internal name  
`dimensions` - Tuple of machine dimensions (width, depth, height)  
`position` - Tuple of machine position in room (last is height)  
`rotation` - Int rotation of machine in room  
`started` - Datetime of when machine was started  
`finished` - Datetime of when machine was last finished  
`est_finish` - Datetime of estimated finish  
`average_cycle` - Timedelta of average cycle time  
`cycle_count` - Int of total cycles  

---
### `Wall` object
A wall within the laundry room  

**Attributes**  
`dimensions` - Tuple of points `((x1, y1), (x2, y2))` (height is probably same as room)  
`visible` - Is the wall visible, bool (no idea why this would be used)  
`label` - Wall name (`"front"`, `"left"`, etc)  

:o)
