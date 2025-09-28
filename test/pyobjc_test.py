from CoreLocation import CLLocationManager, kCLLocationAccuracyBest
from PyObjCTools import AppHelper

class LocationDelegate:
    def __init__(self):
        self.location = None
        self.error = None
    
    def locationManager_didUpdateLocations_(self, manager, locations):
        loc = locations[-1]
        self.location = {
            'latitude': loc.coordinate().latitude,
            'longitude': loc.coordinate().longitude
        }
        manager.stopUpdatingLocation()
        AppHelper.stopEventLoop()
    
    def locationManager_didFailWithError_(self, manager, error):
        self.error = error
        manager.stopUpdatingLocation()
        AppHelper.stopEventLoop()

def get_location():
    """Get current location and return latitude, longitude"""
    manager = CLLocationManager.alloc().init()
    delegate = LocationDelegate()
    manager.setDelegate_(delegate)
    manager.setDesiredAccuracy_(kCLLocationAccuracyBest)
    manager.requestWhenInUseAuthorization()
    manager.startUpdatingLocation()
    
    # Start the event loop
    AppHelper.runConsoleEventLoop()
    
    if delegate.error:
        raise Exception(f"Location error: {delegate.error}")
    
    if delegate.location:
        return delegate.location['latitude'], delegate.location['longitude']
    else:
        raise Exception("No location received")

# Example usage
if __name__ == "__main__":
    try:
        lat, lon = get_location()
        print(f"Latitude: {lat}")
        print(f"Longitude: {lon}")
    except Exception as e:
        print(f"Error: {e}")
