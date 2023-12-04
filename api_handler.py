import requests


def get_distance(osm_url, current_location, target_location):
    try:
        response = requests.get(f'{osm_url}/route?start={current_location}&end={target_location}')
        data = response.json()

        # Extract distance information from the response
        distance = data.get('distance')

        return {'distance': distance}
    except Exception as e:
        return {'error': str(e)}, 500


# Example usage
osm_url = 'https://router.project-osrm.org'
current_location = '13.388860,52.517037'  # Latitude and longitude of the current location
target_location = '13.397634,52.529407'  # Latitude and longitude of the target location

result = get_distance(osm_url, current_location, target_location)
print(result)
