
# pyCircuitLaundry
Circuit Laundry Circuit View API wrapper
https://www.circuit.co.uk/circuit-view/

There is a similar service by a similar name called LaundryView, however this is not compatible. I might consider making it work in the future.

## Dependencies
- requests
- bs4

## Install
`pip install git+https://github.com/lelliotuk/pyCircuitLaundry/`

## Usage
If you're looking for random laundry rooms, don't be surprised if a lot of them don't work because a lot of them are out of service on the website.

You currently need to make 4 requests to find the API ID for a specific site:

```python
import pyCircuitLaundry as circuit

# Get dict of cities with their internal IDs
circuit.get_cities()

# Get dict of providers from a city using its internal ID
circuit.get_providers(city_id)

# Get dict of sites from a provider (both parameters are necessary)
circuit.get_sites(city_id, provider_id)

# Finally, get the API ID for the site (again, all 3 parameters are necessary)
circuit.get_api_id(city_id, provider_id, site_id)


# Then you can create a laundry room oject using the API ID:
room = circuit.Circuit(api_id)
```

**Note: the API is not guaranteed to provide values for certain attributes in every laundry room, so you should check attributes with an asterisk next to them for `None`**

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
`postcode` **\*** - Postcode of the site  
`machines` - Set of `Machine` objects  
`washers` - Set of washers  
`dryers` - Set of dryers  
`available_machines` - Set of machines that are available for use (`"I"` inactive state only)  
`available_washers` - Set of available washers  
`available_dryers` - Set of available dryers  
`dimensions` - Set of room dimensions (width, depth, height)  
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
`started` **\*** - Datetime of when machine was started  
`finished` **\*** - Datetime of when machine was last finished (if this is `None`, `est_finish` may provide a similar time)  
`est_finish` **\*** - Datetime of estimated finish  
`average_cycle` **\*** - Timedelta of average cycle time  
`cycle_count` - Int of total cycles  

---
### `Wall` object
A wall within the laundry room  

**Attributes**  
`dimensions` - Tuple of points `((x1, y1), (x2, y2))` (height is probably same as room)  
`visible` - Is the wall visible, bool (no idea why this would be used)  
`label` - Wall name (`"front"`, `"left"`, etc)  

:o)
