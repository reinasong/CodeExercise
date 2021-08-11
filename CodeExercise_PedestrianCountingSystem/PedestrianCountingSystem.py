import sys
import pandas as pd

def convertStringToNumber(s):
    if isinstance(s, int):
        return s

    if isinstance(s, str):
        return int(s.replace(',', ''))

    raise exception()
        


def main():
    OUTPUT_FOLDER = "./output/"
    SOURCE_DATA_FOLDER = './source_data/'
    try:
        df = pd.read_csv(f'{SOURCE_DATA_FOLDER}/Pedestrian_Counting_System_-_Monthly__counts_per_hour_.csv')

        # convert Hourly_Counts column into integer data type (remove ,)
        df['Hourly_Counts_N'] = df['Hourly_Counts'].apply(convertStringToNumber)


        # top 10 (most pedestrians) locations by day
        df_daily = df[['Year', 'Month', 'Mdate', 'Sensor_Name', 'Hourly_Counts_N']].groupby(by=['Year', 'Month', 'Mdate', 'Sensor_Name']).sum().reset_index()
        df_daily.rename(columns={'Hourly_Counts_N': 'Count'}, inplace=True)
        df_daily = df_daily.set_index(['Sensor_Name']).groupby(by=['Year', 'Month', 'Mdate'])['Count'].nlargest(10, keep='all').reset_index()
        
        # add rank
        df_daily['Rank'] = df_daily.groupby(by=['Year', 'Month', 'Mdate'])['Count'].rank(method='min', ascending=False)

        # save output into a file
        df_daily.to_csv(f'{OUTPUT_FOLDER}/Top10LocationsByDay.csv', index=False)

        # top 10 (most pedestrians) locations by month
        df_monthly = df[['Year', 'Month', 'Sensor_Name', 'Hourly_Counts_N']].groupby(by=['Year', 'Month','Sensor_Name']).sum().reset_index()
        df_monthly.rename(columns={'Hourly_Counts_N': 'Count'}, inplace=True)
        df_monthly = df_monthly.set_index(['Sensor_Name']).groupby(by=['Year', 'Month'])['Count'].nlargest(10, keep='all').reset_index()
        
        # add rank
        df_monthly['Rank'] = df_monthly.groupby(by=['Year', 'Month'])['Count'].rank(method='min', ascending=False)
        
        # save output into a file
        df_monthly.to_csv(f'{OUTPUT_FOLDER}/Top10LocationsByMonth.csv', index=False)

    except:
        ex_type, ex_value, ex_traceback = sys.exc_info()

        print(ex_value)

if __name__ == '__main__':
    main()





