import requests
from PyObjCTools import AppHelper
from CoreLocation import CLLocationManager, kCLLocationAccuracyBest

def get_address_from_coords(lat: float, lon: float) -> str:
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    try:
        response = requests.get(url, headers={"User-Agent": "iMessageAgent/1.0"})
        data = response.json()
        return data["display_name"]
    except Exception as e:
        print(f"Error getting address from ({lat}, {lon}): {e}")
        return None

class LocationDelegate:
    def __init__(self):
        self.latitude = None
        self.longitude = None
        self.error = None
    
    def locationManager_didUpdateLocations_(self, manager, locations):
        loc = locations[-1]
        self.latitude = loc.coordinate().latitude
        self.longitude = loc.coordinate().longitude
        manager.stopUpdatingLocation()
        AppHelper.stopEventLoop()
    
    def locationManager_didFailWithError_(self, manager, error):
        self.error = error
        manager.stopUpdatingLocation()
        AppHelper.stopEventLoop()

def get_current_location():
    manager = CLLocationManager.alloc().init()
    delegate = LocationDelegate()
    manager.setDelegate_(delegate)
    manager.setDesiredAccuracy_(kCLLocationAccuracyBest)
    manager.requestWhenInUseAuthorization()
    manager.startUpdatingLocation()
    
    # Start the event loop
    AppHelper.runConsoleEventLoop()
    
    if delegate.error:
        print(f"Error getting current location: {delegate.error}")
        return None

    address = get_address_from_coords(delegate.latitude, delegate.longitude)
    return {
        "latitude": delegate.latitude,
        "longitude": delegate.longitude,
        "address": address
    }

print(get_current_location())