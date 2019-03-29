import pandas as pd
import csv


def line_origin(file_path, to_path):
    df = pd.read_excel(file_path, sheet_name=None, ignore_index=True, header=1)
    cdf = pd.concat(df.values())
    #print(cdf)
    # making boolean series for a team name
    filter1 = cdf["אופי התחנה"].astype(str) == "מוצא"
    cdf.where(filter1, inplace=True)
    cdf["station"] = cdf["תאור תחנה"].astype(str) + "," + cdf["מספר תחנה"].astype(str)
    cdf["line"] = cdf["תאור קו נוסעים"].astype(str) + "," + cdf["קו נוסעים"].astype(str)
    new_set = set(zip(cdf['station'], cdf['line']))
    print(new_set)
    with open(to_path + '\\line_cache.csv', 'w', encoding='utf-8') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(new_set)



def read_excel(file_path, to_path):
    df = pd.read_excel(file_path, sheetname=None, ignore_index=True)
    cdf = pd.concat(df.values())
    cdf["date_and_train_num"] = cdf["תאריך נסיעת רכבת"].astype(str) + "," + cdf["מספר רכבת"].astype(str)
    cdf["line_and_station"] = cdf["קו נוסעים"].astype(str) + "," + cdf["מספר תחנה"].astype(str)

    # making boolean series for a team name
    filter = cdf["אופי התחנה"] == "מוצא"

    # filtering data
    cdf.where(filter, inplace=True)

    new_dic = dict(cdf['date_and_train_num'], cdf['line_and_station'])
    print(cdf)
    print(new_dic)
    csv_file = to_path + "\\csv_file.csv"
    try:
        with open('dict.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in new_dic.items():
                writer.writerow([key, value])
    except IOError:
        print("I/O error")



#Desktop
if __name__ == '__main__':
    line_origin("D:\\Programming\\CivilHack\\OpenTrainUI\\2018_12.xls", "D:\\Programming\\CivilHack\\OpenTrainUI")