import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

class WasteDataAnalyzer:
    def __init__(self, csv_path='sample_data.csv'):
        self.df = pd.read_csv(csv_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        
    def get_zone_summary(self, zone):
        """Get summary statistics for a specific zone"""
        zone_data = self.df[self.df['Area'] == zone]
        return {
            'total_waste': zone_data['Waste_kg'].sum(),
            'avg_waste': zone_data['Waste_kg'].mean(),
            'avg_biodegradable': zone_data['Biodegradable_percent'].mean(),
            'avg_non_biodegradable': zone_data['Non_Biodegradable_percent'].mean()
        }
    
    def get_all_zones(self):
        """Get list of all zones"""
        return self.df['Area'].unique().tolist()
    
    def get_trend_data(self, zone=None):
        """Get trend data for visualization"""
        if zone:
            data = self.df[self.df['Area'] == zone]
        else:
            data = self.df.groupby('Date')['Waste_kg'].sum().reset_index()
        return data
    
    def predict_future_waste(self, zone, days=7):
        """Predict future waste generation using linear regression"""
        zone_data = self.df[self.df['Area'] == zone].copy()
        zone_data['day_num'] = (zone_data['Date'] - zone_data['Date'].min()).dt.days
        
        X = zone_data['day_num'].values.reshape(-1, 1)
        y = zone_data['Waste_kg'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        last_day = zone_data['day_num'].max()
        future_days = np.array([last_day + i for i in range(1, days + 1)]).reshape(-1, 1)
        predictions = model.predict(future_days)
        
        last_date = zone_data['Date'].max()
        future_dates = [last_date + timedelta(days=i) for i in range(1, days + 1)]
        
        return list(zip(future_dates, predictions))
    
    def get_waste_distribution(self, zone):
        """Get biodegradable vs non-biodegradable distribution"""
        zone_data = self.df[self.df['Area'] == zone]
        avg_bio = zone_data['Biodegradable_percent'].mean()
        avg_non_bio = zone_data['Non_Biodegradable_percent'].mean()
        return {'Biodegradable': avg_bio, 'Non-Biodegradable': avg_non_bio}
