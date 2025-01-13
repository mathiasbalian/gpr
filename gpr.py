import random
import csv
import math

field_width = 50
field_height = 20

path_spacing = 1
paths = []
for x in range(0, field_width, path_spacing):
    paths.append([(x, 0), (x, field_height)])

landmines = [
    {'center': (2, 2), 'radius': 2, 'depth': 1.2},
    {'center': (20, 15), 'radius': 1.5, 'depth': 0.8},
    {'center': (5, 7), 'radius': 3, 'depth': 2.0},
]


def is_detected(x, y, landmine):
    dist = math.sqrt((x - landmine['center'][0]) ** 2 + (y - landmine['center'][1]) ** 2)
    return dist <= landmine['radius']


def simulate_gpr():
    data = []
    for path in paths:
        start, end = path
        x_start, y_start = start
        x_end, y_end = end

        y = y_start
        while y <= y_end:
            detected = 0
            detected_depth = 0.0
            for landmine in landmines:
                if is_detected(x_start, y, landmine):
                    detected = 1
                    detected_depth = landmine['depth']
                    break
            data.append({
                'latitude': x_start,
                'longitude': y,
                'detected': detected,
                'depth': detected_depth if detected else None
            })
            y += 0.5
    return data


data = simulate_gpr()

output_file = 'gpr_simulation_data.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['latitude', 'longitude', 'detected', 'depth'])
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print(f"Simulation data saved to {output_file}")
