class CircuitSiteUnavailableError(Exception):
    def __init__(self, cid, pid, rid):
        self.message = f"Laundry site unavailable\nCity ID: {cid}\nProvider ID: {pid}\nSite ID: {rid}"
    
    def __str__(self):
        return self.message

class CircuitSiteNotFoundError(Exception):
    def __init__(self, id):
        self.message = f"Laundry site API ID {id} does not exist"
    
    def __str__(self):
        return self.message