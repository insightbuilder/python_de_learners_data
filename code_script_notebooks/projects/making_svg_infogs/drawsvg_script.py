import drawsvg as draw

# Data for visualization
customer_ids = [
    'DD37Cf93aecA6Dc', '1Ef7b82A4CAAD10', '6F94879bDAfE5a6', '5Cef8BFA16c5e3c',
    '053d585Ab6b3159', '2d08FB17EE273F4', 'EA4d384DfDbBf77', '0e04AFde9f225dE',
    'C2dE4dEEc489ae0', '8C2811a503C7c5a', '216E205d6eBb815', 'CEDec94deE6d69B',
    'e35426EbDEceaFF', 'A08A8aF8BE9FaD4'
]
subscription_dates = [
    '2020-08-24', '2021-04-23', '2020-03-25', '2020-06-02',
    '2021-04-17', '2020-02-25', '2021-08-24', '2021-04-12',
    '2020-01-13', '2021-11-08', '2021-10-20', '2020-11-29',
    '2021-12-02', '2021-02-08'
]
subscriptions_per_year = {'2020': 6, '2021': 8}
countries = ['Chile', 'Djibouti', 'Antigua and Barbuda', 'Dominican Republic', 'Slovakia', 'Bosnia and Herzegovina', 'Pitcairn Islands', 'Bulgaria', 'Cyprus', 'Timor-Leste', 'Guernsey', 'Vietnam', 'Togo', 'Sri Lanka']
subscriptions_per_country = {'Chile': 1, 'Djibouti': 1, 'Antigua and Barbuda': 1, 'Dominican Republic': 1, 'Slovakia': 1, 'Bosnia and Herzegovina': 1, 'Pitcairn Islands': 1, 'Bulgaria': 1, 'Cyprus': 1, 'Timor-Leste': 1, 'Guernsey': 1, 'Vietnam': 1, 'Togo': 1, 'Sri Lanka': 1}

# Create a drawing
d = draw.Drawing(800, 600, origin='center', displayInline=False)

# Bar Chart for Subscriptions per Year
d.append(draw.Text('Subscriptions per Year', 15, -380, 260))
bar_x_start = -360
bar_width = 50
max_height = 100
max_value = max(subscriptions_per_year.values())

for i, (year, count) in enumerate(subscriptions_per_year.items()):
    bar_height = (count / max_value) * max_height
    d.append(draw.Rectangle(bar_x_start + (i * (bar_width + 10)), 250 - bar_height, bar_width, bar_height, fill='blue'))
    d.append(draw.Text(str(count), 12, bar_x_start + (i * (bar_width + 10)) + bar_width / 2 - 6, 250 - bar_height - 10))
    d.append(draw.Text(year, 12, bar_x_start + (i * (bar_width + 10)) + bar_width / 2 - 10, 260))

# Line Chart for Subscriptions over Time
d.append(draw.Text('Subscriptions over Time', 15, -380, 60))
line_x_start = -360
line_y_start = 50
line_gap = 50
dates_sorted = sorted(subscription_dates)

for i, date in enumerate(dates_sorted):
    d.append(draw.Circle(line_x_start + i * line_gap, line_y_start - i * 10, 5, fill='red'))
    if i > 0:
        d.append(draw.Line(line_x_start + (i - 1) * line_gap, line_y_start - (i - 1) * 10, line_x_start + i * line_gap, line_y_start - i * 10, stroke='red', stroke_width=2))

# Pie Chart for Subscriptions per Country
d.append(draw.Text('Subscriptions per Country', 15, 100, 260))
import math

center_x = 250
center_y = 250
radius = 100
total_subs = sum(subscriptions_per_country.values())
start_angle = 0

for country, count in subscriptions_per_country.items():
    slice_angle = (count / total_subs) * 360
    end_angle = start_angle + slice_angle
    x1 = center_x + radius * math.cos(math.radians(start_angle))
    y1 = center_y + radius * math.sin(math.radians(start_angle))
    x2 = center_x + radius * math.cos(math.radians(end_angle))
    y2 = center_y + radius * math.sin(math.radians(end_angle))
    d.append(draw.Path(f'M{center_x},{center_y} L{x1},{y1} A{radius},{radius} 0 {(1 if slice_angle > 180 else 0)},{1} {x2},{y2} z', fill='orange', stroke='black'))
    d.append(draw.Text(country, 10, center_x + radius * math.cos(math.radians((start_angle + end_angle) / 2)) / 1.5 - 10, center_y + radius * math.sin(math.radians((start_angle + end_angle) / 2)) / 1.5))
    start_angle = end_angle

# Display the drawing
# d.setPixelScale(2)  not a correct method
d.set_pixel_scale(2)
# d.saveSvg('infographic.svg')  not correct method
d.save_svg('infographic.svg')
