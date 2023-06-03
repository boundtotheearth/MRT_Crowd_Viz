from flask import Flask
from flask_cors import CORS
from drawing import draw_heatmap
from data import get_shortest_path, get_data, hours

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/<day_type>/<start_station>/<end_station>")
def generate_viz(day_type, start_station, end_station):
    day_type = 'WEEKENDS/HOLIDAY' if day_type == 'WEEKEND' else day_type
    custom_line = get_shortest_path(start_station, end_station)
    forward_df, backward_df = get_data(custom_line, hours, day_type)

    d = draw_heatmap(forward_df, backward_df, data_min=0, data_max=100)
    
    return d.as_svg()

if __name__ == '__main__':
    custom_line = get_shortest_path('NS16', 'EW20')
    forward_df, backward_df = get_data(custom_line, hours, 'WEEKDAY')
    print(backward_df.index)

    d = draw_heatmap(forward_df, backward_df, data_min=0, data_max=100)