import pandas as pd
import requests
import json

class Zamg_Data:
    def __init__(self, start, end, station = 5904) -> None:
        self.start = start
        self.end = end
        self.station = station
        self.data = None

    def prepare_parameters(self):
        '''prepares standard parameters: joins list of strings'''
        parameters = ['t','tmax','tmin','nied','vv','vvmax']
        return ','.join(parameters)

    def create_url(self):
        parameters = self.prepare_parameters()
        return f'https://dataset.api.hub.zamg.ac.at/v1/station/historical/klima-v1-1d?parameters={parameters}&start={self.start}T00:00&end={self.end}T00:00&station_ids={self.station}'

    def get_json_data(self):
        url = self.create_url()
        return json.loads(requests.get(url).content)

    def get_dataframe(self):
        data_for_dataframe = {
            'date':[],
            't':[],
            'tmax' : [],
            'tmin' : [],
            'nied' : [],
            'vv' : [],
            'vvmax' : []
        }

        data_json = self.get_json_data()
        data_for_dataframe['date'] = data_json['timestamps']

        for key, value in data_json['features'][0]['properties']['parameters'].items():
            data_for_dataframe[key] = value['data']
        self.data = pd.DataFrame(data = data_for_dataframe)
        self.data['date'] = pd.to_datetime(self.data['date']).dt.date
        self.data = self.data.set_index('date')

    @staticmethod
    def repair_rain(col):
        col[col <0] = 0
        return col

    def fill_nan_or_report(self):
        if (self.data.isnull().sum()>0.1*self.data.shape[0]).any():
            raise ValueError("too many NaNs in at least one columns")
        else: 
            self.data.fillna(method='ffill')

    def zamg_data(self):
        self.get_dataframe()
        self.fill_nan_or_report()
        self.data['nied'] = self.repair_rain(self.data['nied'])
        return self.data