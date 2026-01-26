import json
import os
import math

# Markers Data from js/displaymap.js
markersData = [
  { "name": "Banda Aceh", "lat": 5.5483, "lng": 95.3238 },
  { "name": "Medan", "lat": 3.5952, "lng": 98.6722 },
  { "name": "Padang", "lat": -0.9471, "lng": 100.4172 },
  { "name": "Pekanbaru", "lat": 0.5071, "lng": 101.4478 },
  { "name": "Tanjung Pinang", "lat": 0.9186, "lng": 104.4575 },
  { "name": "Jambi", "lat": -1.6101, "lng": 103.6131 },
  { "name": "Palembang", "lat": -2.9761, "lng": 104.7754 },
  { "name": "Bengkulu", "lat": -3.7928, "lng": 102.2608 },
  { "name": "Bandar Lampung", "lat": -5.4292, "lng": 105.2625 },
  { "name": "Pangkal Pinang", "lat": -2.1154, "lng": 106.1168 },
  { "name": "Jakarta", "lat": -6.2088, "lng": 106.8456 },
  { "name": "Serang", "lat": -6.1203, "lng": 106.1502 },
  { "name": "Bandung", "lat": -6.9175, "lng": 107.6191 },
  { "name": "Semarang", "lat": -6.9932, "lng": 110.4203 },
  { "name": "Yogyakarta", "lat": -7.7956, "lng": 110.3695 },
  { "name": "Surabaya", "lat": -7.2575, "lng": 112.7521 },
  { "name": "Denpasar", "lat": -8.6705, "lng": 115.2126 },
  { "name": "Mataram", "lat": -8.5833, "lng": 116.1167 },
  { "name": "Kupang", "lat": -10.1772, "lng": 123.5972 },
  { "name": "Pontianak", "lat": -0.0263, "lng": 109.3425 },
  { "name": "Palangkaraya", "lat": -2.2089, "lng": 113.9214 },
  { "name": "Banjarmasin", "lat": -3.3194, "lng": 114.5903 },
  { "name": "Samarinda", "lat": -0.5022, "lng": 117.1536 },
  { "name": "Tanjung Selor", "lat": 2.8441, "lng": 117.3662 },
  { "name": "Manado", "lat": 1.4748, "lng": 124.8421 },
  { "name": "Palu", "lat": -0.8999, "lng": 119.8707 },
  { "name": "Makassar", "lat": -5.1477, "lng": 119.4327 },
  { "name": "Kendari", "lat": -3.9450, "lng": 122.5989 },
  { "name": "Gorontalo", "lat": 0.5435, "lng": 123.0585 },
  { "name": "Mamuju", "lat": -2.6747, "lng": 118.8893 },
  { "name": "Ambon", "lat": -3.6954, "lng": 128.1814 },
  { "name": "Sofifi", "lat": 0.7443, "lng": 127.5662 },
  { "name": "Jayapura", "lat": -2.5920, "lng": 140.6682 },
  { "name": "Manokwari", "lat": -0.8618, "lng": 134.0640 },
  { "name": "Nabire", "lat": -3.3667, "lng": 135.4833 },
  { "name": "Jayawijaya", "lat": -3.9167, "lng": 138.9167 },
  { "name": "Merauke", "lat": -8.4667, "lng": 140.4000 },
  { "name": "Sorong", "lat": -0.8667, "lng": 131.2500 }
];

months = [
    "januari", "februari", "maret", "april", "mei", "juni",
    "juli", "agustus", "september", "oktober", "november", "desember"
]

base_path = "CCIP/data/rata_rata_historis"
output_file = "CCIP/data/city_rainfall_data.json"

# Initialize structure
results = { m["name"]: [] for m in markersData }

# Helper to find nearest point
def find_nearest_value(target_lat, target_lon, grid_data):
    nearest_val = 0
    min_dist = float('inf')
    
    # Optimization: Filter roughly first
    # Grid points are typically within 0.1 degree
    
    # We can assume gridData is iterable of {lat, lon, value}
    # Iterate and find min distance.
    for point in grid_data:
        lat = point['lat']
        lon = point['lon']
        # Euclidean distance is sufficient for small distances
        dist = math.sqrt((lat - target_lat)**2 + (lon - target_lon)**2)
        if dist < min_dist:
            min_dist = dist
            nearest_val = point['value']
            
        # Optimization: if very close, break (e.g. within 0.02)
        # But grid points might not be exact.
        
    return nearest_val

# Ideally we should identify the indices of the nearest points ONCE from the first file
# assuming all files have the same grid structure.
grid_indices = {} # City Name -> Index in grid array

print("Starting data extraction...")

for i, month in enumerate(months):
    filename = f"hujan_klimatologi_{month}_1991-2020.json"
    file_path = os.path.join(base_path, filename)
    print(f"Processing {month}...")
    
    try:
        with open(file_path, 'r') as f:
            grid_data = json.load(f)
            
        if i == 0:
            # First month: Find nearest indices for all cities
            print("  Finding nearest grid points...")
            for city in markersData:
                target_lat = city['lat']
                target_lon = city['lng']
                
                best_idx = -1
                min_dist = float('inf')
                
                for idx, point in enumerate(grid_data):
                    dist = math.sqrt((point['lat'] - target_lat)**2 + (point['lon'] - target_lon)**2)
                    if dist < min_dist:
                        min_dist = dist
                        best_idx = idx
                
                grid_indices[city['name']] = best_idx
                # Store first month value
                val = grid_data[best_idx]['value'] if best_idx != -1 else 0
                results[city['name']].append(val)
        else:
            # Subsequent months: use indices
            for city_name in results:
                idx = grid_indices.get(city_name, -1)
                if idx != -1 and idx < len(grid_data):
                    val = grid_data[idx]['value']
                    results[city_name].append(val)
                else:
                    results[city_name].append(0)
                    
    except Exception as e:
        print(f"Error processing {filename}: {e}")

# Save results
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"Finished. Data saved to {output_file}")
