from geopy.geocoders import Nominatim

def test_get_geolocation():
    geolocator = Nominatim(user_agent="help_to")
    location = geolocator.geocode("Q. 704 Sul Avenida NS 2,  Arse, Palmas | CEP 77022-328")
    assert location is not None
    if location:
        print("\n")
        print(location.raw.get("lat"))
        print(location.raw.get("lon"))
