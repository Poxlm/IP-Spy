import requests

def get_ip_info(ip):
    url = f'http://api.ipapi.com/{ip}?access_key=257f87ecd464099ce0faa6db1cde5516&format=1'
    response = requests.get(url)
    data = response.json()
    return data

ip_address = input("Enter the IP address: ")
location_data = get_ip_info(ip_address)

print("IP:", location_data['ip'])
print("Capital:", location_data['location']['capital'])
print("Region:", location_data['region_name'])
print("Country:", location_data['country_name'])
print("Postal Code:", location_data['zip'])
print("Latitude:", location_data['latitude'])
print("Longitude:", location_data['longitude'])
print("Country Flag Emoji: 🏳️ " + location_data['location']['country_flag_emoji'])
print("Language:", ", ".join([lang['name'] for lang in location_data['location']['languages']]))
print("Calling Code:", location_data['location']['calling_code'])
print("Zip Code:", location_data['region_code'])
print("Continent Code:", location_data['continent_code'])
print("Continent Name:", location_data['continent_name'])
