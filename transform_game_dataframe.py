import pandas as pd
import numpy as np
import os

def transform_game_dataframe(dataframe):

    def define_location(height, width, x_min, y_min):
    
        location = ""
    
        # Define horizontal position
        if x_min <= width * (1/3):
            horizontal = "left"
        elif x_min <= width * (2/3):
            horizontal = "center"
        else:
            horizontal = "right"
        
        # Define vertical position
        if y_min <= height * (1/3):
            vertical = "upper"
        elif y_min <= height * (2/3):
            vertical = "middle"
        else:
            vertical = "lower"
        
        # Combine vertical and horizontal positions
        location = f"{vertical} {horizontal}"
        
        return location

    
    dataframe['seat_location'] = dataframe.apply(lambda row: define_location(row['img_height'], row['img_width'], row['x_min'], row['y_min']), axis=1)

    dataframe['distance_to_center'] = dataframe.apply(lambda row: np.sqrt((row['x_min'] - row['img_width'] / 2) ** 2 + (row['y_min'] - row['img_height'] / 2) ** 2), axis=1)

    # Clean price column
    dataframe['price'] = dataframe['price'].str.extract('(\d+)')  # Extract only digits
    dataframe['price'] = dataframe['price'].astype(float)  # Convert to float first if decimals are present
    dataframe['price'] = dataframe['price'].fillna(0).astype(int)

    dataframe['deal_score'] = dataframe['distance_to_center']*dataframe['price'] # Smaller is better

    return dataframe