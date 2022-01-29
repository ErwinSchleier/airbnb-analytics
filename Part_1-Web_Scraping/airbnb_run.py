from airbnb_parser import Parser
import time
import datetime

if __name__ == "__main__":
    # parameterize dates
    date_1 = datetime.date.today() + datetime.timedelta(days=7)
    date_2 = datetime.date.today() + datetime.timedelta(days=14)
    date_1 = date_1.strftime('%Y-%m-%d')
    date_2 = date_2.strftime('%Y-%m-%d')

    locations = {
        'Valencia_ESP': f'https://www.airbnb.com/s/Valencia/homes?query=Valencia&place_id=ChIJb7Dv8ExPYA0ROR1_HwFRo7Q&checkin=2022-03-01&checkout=2022-03-31&adults=3'
    }

    for location in locations:
        new_parser = Parser(locations[location], f'./{location}.csv')
        t0 = time.time()
        new_parser.parse()
        print(location, time.time() - t0)