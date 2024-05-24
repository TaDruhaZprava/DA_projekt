import pandas as pd

with open('data/03_weather.csv', mode='r', encoding='Windows 1252') as file: # nepouzivam encodig utf-8, protoze data jsou stazena v jinem.
    text = file.read()
    splited = text.split(",\n")
    weather = "\n".join(splited[3:])

with open('data/weather.csv', mode='w', encoding='utf-8') as output_file:
    print(weather, file=output_file)
    
# Changing the time to type datetime as in all the other tables
weather = pd.read_csv('data/weather.csv')
weather["time"] = pd.to_datetime(weather["time"], errors='coerce')
weather.to_csv('data/weather_datetime.csv')
 
# Rename the column and change decimal point in strings to decimal comma so that the CSV is easy to upload to Azure SQL 
weather = weather.rename(columns={"time": "DateTime"})
columns_to_replace = ['temperature_2m (°C)', 'dew_point_2m (°C)', 'apparent_temperature (°C)', 
                      'precipitation (mm)', 'rain (mm)', 'snowfall (cm)','snow_depth (m)', 
                      'pressure_msl (hPa)', 'surface_pressure (hPa)', 'wind_speed_10m (km/h)', 
                      'wind_speed_100m (km/h)',
                      'wind_gusts_10m (km/h)', 'sunshine_duration (s)', 'direct_normal_irradiance (W/m?)', 
                      'terrestrial_radiation (W/m?)']

weather[columns_to_replace] = weather[columns_to_replace].astype(str).apply(lambda col: col.map(lambda x: x.replace('.', ',')))

weather.to_csv('data/weather_sql.csv', index=False)