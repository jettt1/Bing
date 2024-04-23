import os
path = "city_coordinates_Australia.txt"
cities = dict()

if os.path.exists(path):
    try:
        with open(path, 'r') as file:
            for line in file:
                parts = line.strip().split(': ')
                city_name = parts[0]
                coordinates = list(map(int, parts[1].split()))
                cities[city_name] = coordinates
    except Exception as e:
        print("An error occurred while reading the file:", e)
else:
    print("File not found:", path)

print("Parsed cities:", cities)
