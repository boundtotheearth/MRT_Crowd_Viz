import drawsvg as dw
import numpy as np
import textwrap
from data import get_data, prefix_colors, all_lines, extract_same_line_codes, hours, day_types

def draw_heatmap(forward_df, backward_df, data_min=None, data_max=None):
    station_codes = forward_df.reset_index()['START'].to_list() + [backward_df.reset_index()['START'][0]]
    station_names = forward_df.reset_index()['START_NAME'].to_list() + [backward_df.reset_index()['START_NAME'][0]]
    hours = forward_df.columns.to_list()

    print("Drawing heatmap for line: ", station_codes)

    station_spacing = 55
    time_spacing = 55

    left_margin = 130
    top_margin = 50

    data_max = np.max(np.max(forward_df), np.max(backward_df)) if data_max is None else data_max
    data_min = np.min(np.max(forward_df), np.max(backward_df)) if data_min is None else data_min

    canvas_width = 1430
    canvas_height = len(station_codes) * station_spacing + top_margin

    gray = to_rgb((43, 41, 37))

    d = dw.Drawing(canvas_width, canvas_height, id='heatmap_svg', font_family='Verdana')

    # Draw Background
    bg = dw.Rectangle(0, 0, canvas_width, canvas_height, fill='white')
    d.append(bg)

    # Draw Station Axis
    station_sx = left_margin
    station_sy = top_margin + station_spacing / 2
    station_colors = [to_rgb(prefix_colors[c[:2]]) for c in station_codes]
    forward_line = create_line(station_sx, station_sy, station_spacing, station_colors, 'white', station_colors, station_codes, 'down')
    d.append(forward_line)

    # Name Column
    for i, station_name in enumerate(station_names):
        t = dw.Text(textwrap.wrap(station_name, width=10), 11, station_sx - 65, station_sy + i * station_spacing, fill=gray, font_weight='bold', text_anchor='middle', dominant_baseline='middle')
        d.append(t)

    # Draw Time Axis
    time_names = ['{:02d}:00'.format(i) for i in list(range(5, 24)) + [0, 1]]
    time_sx = left_margin + time_spacing / 2
    time_sy = top_margin
    time_line = create_line(time_sx, time_sy, time_spacing, station_colors[0], 'white', station_colors[0], time_names, 'right')
    d.append(time_line)

    forward_backward_gap = 20

    # Draw Forward Data
    forward_grid_origin_x = time_sx + time_spacing / 2 - forward_backward_gap / 2
    forward_grid_origin_y = station_sy + (station_spacing / 2)
    for y, station_code in enumerate(station_codes[:-1]):
        for x, hour in enumerate(hours):
            d.append(create_train(
                forward_grid_origin_x + x * time_spacing, 
                forward_grid_origin_y + y * station_spacing, 
                station_colors[y], 
                forward_df[hour].get(station_code, 0).squeeze(), data_min, data_max,
                'down'
            ))

    # Draw Backward Data
    backward_grid_origin_x = forward_grid_origin_x + forward_backward_gap
    backward_grid_origin_y = forward_grid_origin_y
    for y, station_code in enumerate(station_codes[1:]):
        for x, hour in enumerate(hours):
            d.append(create_train(
                backward_grid_origin_x + x * time_spacing, 
                backward_grid_origin_y + y * station_spacing, 
                station_colors[y], 
                backward_df[hour].get(station_code, 0).squeeze(), data_min, data_max,
                'up'
            ))

    # Draw Color Bar
    color_bar_width = 50
    color_bar_x = left_margin + time_spacing / 2 + len(hours) * time_spacing + time_spacing / 2
    color_bar_y = station_sy
    color_bar_height = (len(station_codes)-1) * station_spacing

    color_bar_grad = dw.LinearGradient(0, 0, 0, color_bar_height)
    color_bar_grad.add_stop(0, 'white')
    color_bar_grad.add_stop(1, station_colors[0])

    color_bar = dw.Rectangle(color_bar_x, color_bar_y, color_bar_width, color_bar_height, fill=color_bar_grad, rx=5, stroke=station_colors[0], stroke_width=1.5)

    tick_font_size = 9
    num_ticks = 5
    tick_values = np.linspace(data_min, data_max, num_ticks)
    ticks = [
        dw.Text(
            f"{value:.0f}", 
            tick_font_size, 
            color_bar_x + color_bar_width + 5, 
            color_bar_y + i * (color_bar_height / (num_ticks-1)), 
            font_weight='bold', 
            fill=gray, 
            text_anchor='left', 
            dominant_baseline='middle'
        )
        for i, value in enumerate(tick_values)
    ]
    d.append(dw.Group([color_bar] + ticks))

    return d

def create_train(cx, cy, color, value, min, max, direction):
    # Creates a train graphic centered at (cx, cy), with a fill amount relative to value, min and max, facing in the specified direction
    train_width = 15
    train_length = train_width * (1 + 5 ** 0.5)
    corner_rounding = 4
    stroke_width = 1.5
    direction_offset = 10

    x_size = train_length if (direction == 'left' or direction == 'right') else train_width
    y_size = train_width if (direction == 'left' or direction == 'right') else train_length

    x = cx - x_size/2
    y = cy - y_size/2

    fill_amount = np.tanh(3 * ((value - min) / (max - min)))

    clip_x = x - direction_offset if direction == 'left' else x + direction_offset if direction == 'right' else x - stroke_width
    clip_y = y - direction_offset if direction == 'up' else y + direction_offset if direction == 'down' else y - stroke_width

    clip = dw.ClipPath([dw.Rectangle(clip_x, clip_y, x_size + 2 * stroke_width, y_size + 2 * stroke_width, stroke_width=stroke_width, fill=color, fill_opacity=0.3)])

    grad_sx = 1 if direction == 'left' else 0
    grad_sy = 1 if direction == 'up' else 0
    grad_ex = 1 if direction == 'right' else 0
    grad_ey = 1 if direction == 'down' else 0

    grad = dw.LinearGradient(grad_sx, grad_sy, grad_ex, grad_ey, 'objectBoundingBox')
    grad.add_stop(0, color, opacity=0)
    grad.add_stop(0.4, color, opacity=1)
    grad.add_stop(1, color, opacity=1)

    outer = dw.Rectangle(x, y, x_size, y_size, ry=corner_rounding, stroke=grad, stroke_width=stroke_width, fill='none', clip_path=clip)

    inner_x = x + direction_offset - corner_rounding + (1-fill_amount) * (x_size - direction_offset) if direction == 'right' else x
    inner_y = y + direction_offset - corner_rounding + (1-fill_amount) * (y_size - direction_offset) if direction == 'down' else y
    inner_x_size = x_size if (direction == 'up' or direction == 'down') else fill_amount * (x_size - direction_offset) + corner_rounding
    inner_y_size = y_size if (direction == 'left' or direction == 'right') else fill_amount * (y_size - direction_offset) + corner_rounding

    inner = dw.Rectangle(inner_x, inner_y, inner_x_size, inner_y_size, ry=corner_rounding, stroke='none', fill=color, fill_opacity=fill_amount)

    return dw.Group([clip, inner, outer])

def create_line(sx, sy, spacing, line_colors, text_colors, marker_colors, names, direction):
    line_colors = [line_colors] * len(names) if type(line_colors) is str else line_colors
    marker_colors = [marker_colors] * len(names) if type(marker_colors) is str else marker_colors
    text_colors = [text_colors] * len(names) if type(text_colors) is str else text_colors

    width = 40
    height = 26
    corner_rounding_x = 7.5
    corner_rounding_y = 15
    stroke_width = 5
    font_size = 9

    n = len(names)

    lsx = sx
    lsy = sy
    lines = []
    for i in range(n-1):
        lex = lsx + (1 if direction == 'right' else -1 if direction == 'left' else 0) * spacing
        ley = lsy + (1 if direction == 'down' else -1 if direction == 'up' else 0) * spacing

        lines.append(dw.Line(lsx, lsy, lex, ley, stroke=line_colors[i], stroke_width=stroke_width))

        lsx = lex
        lsy = ley

    stations = []
    for i, name in enumerate(names):
        x = sx - width / 2 + (i if direction == 'right' else -i if direction == 'left' else 0) * spacing
        y = sy - height / 2 + (i if direction == 'down' else -i if direction == 'up' else 0) * spacing
        station = dw.Rectangle(x, y, width, height, rx=corner_rounding_x, ry=corner_rounding_y, stroke='white', stroke_width=2, fill=marker_colors[i])

        tx = sx + (i if direction == 'right' else -i if direction == 'left' else 0) * spacing
        ty = sy + (i if direction == 'down' else -i if direction == 'up' else 0) * spacing
        name = dw.Text(text=name, x=tx, y=ty, font_size=font_size, font_weight='bold', fill=text_colors[i], text_anchor='middle', dominant_baseline='middle')

        stations.append(dw.Group([station, name]))
    
    return dw.Group(lines + stations)

def to_rgb(rgb):
    return 'rgb'+ str(rgb)

if __name__ == '__main__':
    print(prefix_colors)
    for line_code, data in all_lines.items():
        station_codes = extract_same_line_codes(data['station_codes'], data['line_prefixes'])
        
        for day_type in day_types:
            forward_df, backward_df = get_data(station_codes, hours, day_type)
            d = draw_heatmap(forward_df, backward_df, data_min=0, data_max=100)

            d.save_svg(f'graphics/{line_code}_{day_type.replace("/", "_")}.svg')
            d.save_png(f'graphics/{line_code}_{day_type.replace("/", "_")}.png')