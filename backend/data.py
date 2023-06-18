from itertools import combinations, product, islice
import pickle
import pandas as pd
import numpy as np
import networkx as nx

hours = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0]
day_types = ['WEEKDAY', 'WEEKENDS/HOLIDAY']

num_weekdays = 18
num_weekends_holidays = 12

weekday_peak_freq = 3
weekday_nonpeak_freq = 7
weekend_peak_freq = 5
weekend_nonpeak_freq = 7

weekday_peak_hours = [7, 8, 9, 17, 18, 19]
weekend_peak_hours = [12, 13, 14, 18, 19, 20, 21, 22, 23]

all_lines = {
    'NSL': {
        'station_codes': ["EW24/NS1", "NS2", "NS3", "NS4/BP1", "NS5", "NS7", "NS8", "NS9/TE2", "NS10", "NS11", "NS12", "NS13", "NS14", "NS15", "NS16", "NS17/CC15", "NS18", "NS19", "NS20", "NS21/DT11", "TE14/NS22", "NS23", "NS24/NE6/CC1", "NS25/EW13", "EW14/NS26", "NS27/CE2/TE20", "NS28"],
        'travel_times': [3, 2, 5, 2, 5, 3, 2, 3, 4, 2, 3, 3, 5, 3, 3, 3, 2, 3, 2, 3, 2, 2, 2, 3, 2, 2],
        'line_prefixes': ['NS'],
        'line_color': (209, 60, 50),
        'train_capacity': 1920,
        'seat_capacity': 264
    },
    'EWL': {
        'station_codes': ['EW1', 'EW2/DT32', 'EW3', 'EW4', 'EW5', 'EW6', 'EW7', 'EW8/CC9', 'EW9', 'EW10', 'EW11', 'EW12/DT14', 'NS25/EW13', 'EW14/NS26', 'EW15', 'EW16/NE3/TE17', 'EW17', 'EW18', 'EW19', 'EW20', 'EW21/CC22', 'EW22', 'EW23', 'EW24/NS1', 'EW25', 'EW26', 'EW27', 'EW28', 'EW29', 'EW30', 'EW31', 'EW32', 'EW33'],
        'travel_times': [3, 3, 3, 3, 3, 2, 3, 2, 3, 2, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 3, 3, 4, 2, 3, 3, 2, 3, 3, 2, 3, 2],
        'line_prefixes': ['EW'],
        'line_color': (66, 148, 84),
        'train_capacity': 1920,
        'seat_capacity': 264
    },
    'EWL-CGL': {
        'station_codes': ['CG2', 'CG1/DT35', 'EW4', 'EW5', 'EW6', 'EW7', 'EW8/CC9', 'EW9', 'EW10', 'EW11', 'EW12/DT14', 'NS25/EW13', 'EW14/NS26', 'EW15', 'EW16/NE3/TE17', 'EW17', 'EW18', 'EW19', 'EW20', 'EW21/CC22', 'EW22', 'EW23', 'EW24/NS1', 'EW25', 'EW26', 'EW27', 'EW28', 'EW29', 'EW30', 'EW31', 'EW32', 'EW33'],
        'travel_times': [4, 3, 3, 3, 2, 3, 2, 3, 2, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 3, 3, 4, 2, 3, 3, 2, 3, 3, 2, 3, 2],
        'line_prefixes': ['EW', 'CG'],
        'line_color': (66, 148, 84),
        'train_capacity': 1920,
        'seat_capacity': 264
    },
    'NEL': {
        'station_codes': ['NE1/CC29', 'EW16/NE3/TE17', 'NE4/DT19', 'NE5', 'NS24/NE6/CC1', 'NE7/DT12', 'NE8', 'NE9', 'NE10', 'NE11', 'NE12/CC13', 'NE13', 'NE14', 'NE15', 'NE16/STC', 'NE17/PTC'],
        'travel_times': [3, 2, 2, 2, 2, 2, 3, 3, 1, 2, 3, 2, 2, 2, 3],
        'line_prefixes': ['NE'],
        'line_color': (133, 69, 149),
        'train_capacity': 1920,
        'seat_capacity': 268
    },
    'CCL': {
        'station_codes': ['NS24/NE6/CC1', 'CC2', 'CC3', 'CC4/DT15', 'CC5', 'CC6', 'CC7', 'CC8', 'EW8/CC9', 'CC10/DT26', 'CC11', 'CC12', 'NE12/CC13', 'CC14', 'NS17/CC15', 'CC16', 'CC17/TE9', 'CC19/DT9', 'CC20', 'CC21', 'EW21/CC22', 'CC23', 'CC24', 'CC25', 'CC26', 'CC27', 'CC28', 'NE1/CC29'],
        'travel_times': [3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        'line_prefixes': ['CC'],
        'line_color': (236, 161, 68),
        'train_capacity': 931,
        'seat_capacity': 146
    },
    'CCL-CEL': {
        'station_codes': ['CE1/DT16', 'NS27/CE2/TE20', 'CC4/DT15', 'CC5', 'CC6', 'CC7', 'CC8', 'EW8/CC9', 'CC10/DT26', 'CC11', 'CC12', 'NE12/CC13', 'CC14', 'NS17/CC15', 'CC16', 'CC17/TE9', 'CC19/DT9', 'CC20', 'CC21', 'EW21/CC22', 'CC23', 'CC24', 'CC25', 'CC26', 'CC27', 'CC28', 'NE1/CC29'],
        'travel_times': [2, 6, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        'line_prefixes': ['CE', 'CC'],
        'line_color': (236, 161, 68),
        'train_capacity': 931,
        'seat_capacity': 146
    },
    'TEL': {
        'station_codes': ['TE1', 'NS9/TE2', 'TE3', 'TE4', 'TE5', 'TE6', 'TE7', 'TE8', 'CC17/TE9', 'DT10/TE11', 'TE12', 'TE13', 'TE14/NS22', 'TE15', 'TE16', 'EW16/NE3/TE17', 'TE18', 'TE19', 'NS27/CE2/TE20', 'TE22'],
        'travel_times': [3, 3, 4, 4, 2, 2, 3, 3, 4, 3, 2, 2, 3, 1, 3, 1, 2, 2, 3],
        'line_prefixes': ['TE'],
        'line_color': (148, 94, 49),
        'train_capacity': 1280,
        'seat_capacity': 156
    },
    'DTL': {
        'station_codes': ['BP6/DT1', 'DT2', 'DT3', 'DT5', 'DT6', 'DT7', 'DT8', 'CC19/DT9', 'DT10/TE11', 'NS21/DT11', 'NE7/DT12', 'DT13', 'EW12/DT14', 'CC4/DT15', 'CE1/DT16', 'DT17', 'DT18', 'NE4/DT19', 'DT20', 'DT21', 'DT22', 'DT23', 'DT24', 'DT25', 'CC10/DT26', 'DT27', 'DT28', 'DT29', 'DT30', 'DT31', 'EW2/DT32', 'DT33', 'DT34', 'CG1/DT35'],
        'travel_times': [2, 1, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 3, 1, 2, 2, 2, 3, 1, 2, 2, 2, 2, 3, 2, 2, 3, 2],
        'line_prefixes': ['DT'],
        'line_color': (38, 91, 163),
        'train_capacity': 931,
        'seat_capacity': 130
    },
    'SELRT': {
        'station_codes': ['NE16/STC', 'SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'NE16/STC'],
        'travel_times': [1, 1, 1, 1, 1, 1],
        'line_prefixes': ['ST', 'SE'],
        'line_color': (117, 132, 116),
        'train_capacity': 105,
        'seat_capacity': 14
    },
    'SWLRT': {
        'station_codes': ['NE16/STC', 'SW1', 'SW2', 'SW3', 'SW4', 'SW5', 'SW6', 'SW7', 'SW8', 'NE16/STC'],
        'travel_times': [1, 1, 1, 1, 1, 1, 1, 1, 1],
        'line_prefixes': ['ST', 'SW'],
        'line_color': (117, 132, 116),
        'train_capacity': 105,
        'seat_capacity': 14
    },
    'PELRT': {
        'station_codes': ['NE17/PTC', 'PE1', 'PE2', 'PE3', 'PE4', 'PE5', 'PE6', 'PE7', 'NE17/PTC'],
        'travel_times': [1, 1, 1, 1, 1, 1, 1, 1],
        'line_prefixes': ['PT', 'PE'],
        'line_color': (117, 132, 116),
        'train_capacity': 105,
        'seat_capacity': 14
    },
    'PWLRT': {
        'station_codes': ['NE17/PTC', 'PW1', 'PW3', 'PW4', 'PW5', 'PW6', 'PW7', 'NE17/PTC'],
        'travel_times': [1, 1, 1, 1, 1, 1, 1],
        'line_prefixes': ['PT', 'PW'],
        'line_color': (117, 132, 116),
        'train_capacity': 105,
        'seat_capacity': 14
    },
    'BPLRT': {
        'station_codes': ['NS4/BP1', 'BP2', 'BP3', 'BP4', 'BP5', 'BP6/DT1', 'BP7', 'BP8', 'BP9', 'BP10', 'BP11', 'BP12', 'BP13', 'BP6/DT1', 'BP5', 'BP4', 'BP3', 'BP2', 'NS4/BP1'],
        'travel_times': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'line_prefixes': ['BP'],
        'line_color': (117, 132, 116),
        'train_capacity': 105,
        'seat_capacity': 16
    }
}

prefix_colors = {
    prefix: data['line_color']
    for line_code, data in all_lines.items()
    for prefix in data['line_prefixes']
}

station_set = set(sum([data['station_codes'] for data in all_lines.values()], []))

with open('network_graph.pkl', 'rb') as f:
    network_graph = pickle.load(f)

counts_df = pd.read_csv('counts_df.csv')


def get_shortest_path(start_station, end_station):
    start_station = [start_station]if type(start_station) is str else start_station
    end_station = [end_station]if type(end_station) is str else end_station

    shortest_path = None
    for start, end in product(start_station, end_station):
        path = nx.shortest_path(network_graph, start, end)
        if shortest_path is None or len(path) < len(shortest_path):
            shortest_path = path
    
    return shortest_path

def generate_network_graph():
    print("Generating Network Graph...")
    interchange_transfer_time = 8
    network_graph = nx.Graph()
    for line_code, station_data in all_lines.items():
        station_codes = extract_same_line_codes(station_data['station_codes'], station_data['line_prefixes'])
        travel_times = station_data['travel_times']

        for i in range(len(station_codes)-1):
            network_graph.add_edge(station_codes[i], station_codes[i+1], time=travel_times[i], train_capacity=station_data['train_capacity'])

            if '/' in station_data['station_codes'][i]:
                sub_codes = station_data['station_codes'][i].split('/')
                for u, v in combinations(sub_codes, 2):
                    network_graph.add_edge(u, v, time=interchange_transfer_time, train_capacity=station_data['train_capacity'])

    # Add reverse edges
    for u, v in network_graph.edges:
        network_graph.add_edge(v, u, **network_graph.edges[(u, v)])
        
    len(network_graph.nodes)

    with open('network_graph.pkl', 'wb') as f:
        pickle.dump(network_graph, f)


def generate_path_demand_factors(network_graph):
    print("Generating Path Demand Factors...")
    path_demand_factors = {s1: {s2: None for s2 in station_set if s1 != s2} for s1 in station_set}
    weight_func = lambda path: nx.path_weight(network_graph, path, 'time')

    for station1, station2 in combinations(station_set, 2):
        origin_codes = station1.split('/')
        destination_codes = station2.split('/')

        candidate_paths = set()
        for origin, destination in product(origin_codes, destination_codes):
            k_shortest_paths = set([tuple(l) for l in islice(nx.shortest_simple_paths(network_graph, origin, destination, 'time'), 5)])
            candidate_paths = candidate_paths.union(k_shortest_paths)

        candidate_paths = sorted(candidate_paths, key=weight_func)
        final_paths = [candidate_paths[0]]
        for i in range(1, len(candidate_paths)):
            if any([set(l).issubset(set(candidate_paths[i])) for l in final_paths]):
                continue
            else:
                final_paths.append(candidate_paths[i])

        final_paths = [x for x in final_paths if weight_func(x) <= weight_func(final_paths[0]) + 15][:3]

        total_demand = [weight_func(final_paths[-1]) - weight_func(x) + 1 for x in final_paths]
        path_demand_factors[station1][station2] = [(x, total_demand[i] / sum(total_demand)) for i, x in enumerate(final_paths)]
        path_demand_factors[station2][station1] = [(x[::-1], total_demand[i] / sum(total_demand)) for i, x in enumerate(final_paths)]
    
    return path_demand_factors

def generate_counts_df(raw_df_filename):
    print("Generating Counts...")
    raw_df = pd.read_csv(raw_df_filename)
    station_name_df = pd.read_csv("Train Station Codes and Chinese Names.csv", usecols=[0, 1], names=['STATION_CODE', 'STATION_NAME'])

    generate_network_graph()
    path_demand_factors = generate_path_demand_factors(network_graph)

    sections = set()
    for start, end in set(network_graph.edges):
        sections.add((start, end))
        sections.add((end, start))

    capacity_df = pd.DataFrame.from_records([(start, end, network_graph[start][end]['train_capacity']) for start, end in sections], columns=['START', 'END', 'TRAIN_CAPACITY'])
    path_df = pd.DataFrame.from_records([(start, end, path[i], path[i+1], demand_factor) for start in path_demand_factors for end in path_demand_factors[start] for path, demand_factor in path_demand_factors[start][end] for i in range(len(path)-1)], columns=['ORIGIN_PT_CODE', 'DESTINATION_PT_CODE', 'START', 'END', "DEMAND_FACTOR"])

    counts_df = pd.merge(path_df, raw_df, on=['ORIGIN_PT_CODE', 'DESTINATION_PT_CODE'], how='left')
    counts_df['COUNT'] = counts_df['DEMAND_FACTOR'] * counts_df['TOTAL_TRIPS']
    counts_df = counts_df.drop(columns=['DEMAND_FACTOR'])

    counts_df = counts_df.groupby(['DAY_TYPE', 'TIME_PER_HOUR', 'START', 'END']).sum().reset_index()

    counts_df = counts_df.merge(capacity_df[['START', 'END', 'TRAIN_CAPACITY']], on=['START', 'END'], how='left')
    counts_df['TOTAL_CAPACITY'] = counts_df['TRAIN_CAPACITY'] * np.where(counts_df['DAY_TYPE'] == 'WEEKDAY', num_weekdays * 60 / np.where(counts_df['TIME_PER_HOUR'].isin(weekday_peak_hours), weekday_peak_freq, weekday_nonpeak_freq), num_weekends_holidays * 60 / np.where(counts_df['TIME_PER_HOUR'].isin(weekend_peak_hours), weekend_peak_freq, weekend_nonpeak_freq))

    counts_df['CROWDEDNESS'] = np.round((counts_df['COUNT'] / counts_df['TOTAL_CAPACITY']) * 100)

    counts_df = counts_df.drop(['TOTAL_CAPACITY', 'TRAIN_CAPACITY'], axis='columns')

    counts_df = counts_df.merge(station_name_df, how='left', left_on='START', right_on='STATION_CODE').drop(columns=['STATION_CODE']).rename({'STATION_NAME': 'START_NAME'}, axis='columns')
    counts_df = counts_df.merge(station_name_df, how='left', left_on='END', right_on='STATION_CODE').drop(columns=['STATION_CODE']).rename({'STATION_NAME': 'END_NAME'}, axis='columns')

    counts_df.to_csv("counts_df.csv", index=False)


def get_data(station_codes, hours, day_type, col='CROWDEDNESS'):
    data_df = counts_df[
        counts_df['START'].isin(station_codes) &
        counts_df['END'].isin(station_codes) &
        counts_df['DAY_TYPE'].str.contains(day_type)
    ]

    forward_sections = [(station_codes[i], station_codes[i+1]) for i in range(len(station_codes) - 1)]
    forward_df = data_df.set_index(['TIME_PER_HOUR', 'START', 'END', 'START_NAME', 'END_NAME'])[col]
    forward_df = forward_df.unstack('TIME_PER_HOUR')[hours]
    forward_df = forward_df.join(pd.DataFrame(index=pd.MultiIndex.from_tuples(forward_sections, names=['START', 'END'])), how='right')

    backward_sections = [(station_codes[::-1][i], station_codes[::-1][i+1]) for i in range(len(station_codes) - 1)]
    backward_df = data_df.set_index(['TIME_PER_HOUR', 'START', 'END', 'START_NAME', 'END_NAME'])[col]
    backward_df = backward_df.unstack('TIME_PER_HOUR')[hours]
    backward_df = backward_df.join(pd.DataFrame(index=pd.MultiIndex.from_tuples(backward_sections, names=['START', 'END'])), how='right')

    return forward_df, backward_df

def extract_same_line_codes(station_codes, line_codes):
    if type(line_codes) is not list:
        line_codes = [line_codes]
    return [sub_code for code in station_codes for sub_code in code.split('/') if sub_code[:2] in line_codes]

if __name__ == '__main__':
    generate_counts_df("origin_destination_train_202305.csv")