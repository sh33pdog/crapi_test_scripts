import requests
import json

def get_tokens():
    tokens = {}
    base_url = "https://crapi.f5xc.kermarsh.com"
    login_endpoint = "/identity/api/auth/login"
    password = "IjAtLcBTTF2!"

    for i in range(1, 51):
        email = f"kkmshep{i}@thecal.co.uk"
        try:
            login_url = base_url + login_endpoint
            credentials = {"email": email, "password": password}
            headers = {"Content-Type": "application/json"}
            login_response = requests.post(login_url, json=credentials, headers=headers)
            login_response.raise_for_status()
            login_data = login_response.json()
            token = login_data.get("token") or login_data.get("access_token")
            if token:
                tokens[email] = token
            else:
                print(f"Token not found for {email}")
        except requests.exceptions.RequestException as e:
            print(f"Error for {email}: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON error for {email}: {e}")
        except Exception as e:
            print(f"Unexpected error for {email}: {e}")
    return tokens

def get_vehicle_uuids(tokens):
    base_url = "https://crapi.f5xc.kermarsh.com"
    vehicles_endpoint = "/identity/api/v2/vehicle/vehicles"
    vehicle_uuids = {}

    for email, token in tokens.items():
        try:
            vehicles_url = base_url + vehicles_endpoint
            vehicles_headers = {"Authorization": f"Bearer {token}"}
            vehicles_response = requests.get(vehicles_url, headers=vehicles_headers)
            vehicles_response.raise_for_status()
            vehicles_data = vehicles_response.json()
            uuids = [vehicle["uuid"] for vehicle in vehicles_data]
            vehicle_uuids[email] = uuids
        except requests.exceptions.RequestException as e:
            print(f"Error getting vehicles for {email}: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON error for {email}: {e}")
        except Exception as e:
            print(f"Unexpected error for {email}: {e}")
    return vehicle_uuids

def get_vehicle_locations(tokens, vehicle_uuids):
    base_url = "https://crapi.f5xc.kermarsh.com"
    location_endpoint = "/identity/api/v2/vehicle/{uuid}/location"
    vehicle_locations = {}

    for email, uuids in vehicle_uuids.items():
        vehicle_locations[email] = {}
        token = tokens.get(email, None) #Now using kkmshep emails.
        if not token:
            print(f"Token not found for {email}")
            continue

        for uuid in uuids:
            try:
                location_url = base_url + location_endpoint.replace("{uuid}", uuid)
                location_headers = {"Authorization": f"Bearer {token}"}
                location_response = requests.get(location_url, headers=location_headers)
                location_response.raise_for_status()
                location_data = location_response.json()
                vehicle_locations[email][uuid] = location_data
            except requests.exceptions.RequestException as e:
                print(f"Error getting location for {email}, UUID {uuid}: {e}")
            except json.JSONDecodeError as e:
                print(f"JSON error for {email}, UUID {uuid}: {e}")
            except Exception as e:
                print(f"Unexpected error for {email}, UUID {uuid}: {e}")
    return vehicle_locations

if __name__ == "__main__":
    tokens = get_tokens()
    vehicle_uuids = get_vehicle_uuids(tokens)
    vehicle_locations = get_vehicle_locations(tokens, vehicle_uuids)

    if vehicle_locations:
        print("\nVehicle Locations:")
        for email, uuid_locations in vehicle_locations.items():
            print(f"{email}:")
            for uuid, location in uuid_locations.items():
                print(f"  UUID: {uuid}, Location: {location}")
    else:
        print("\nNo vehicle locations found.")
