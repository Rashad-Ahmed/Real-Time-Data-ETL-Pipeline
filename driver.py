import configparser
from imp import reload
from businesssearch import BusinessSearch
from queries import create_business_schema, create_business_table, insert_business_table
from databasedriver import DatabaseDriver
import argparse
import sys
reload(sys)
sys.setdefaultencoding('utf8')

config = configparser.ConfigParser()
config.read("config.cfg")

parser = argparse.ArgumentParser(
        description="A Example yelp business finder based on parameters such as term, location, price, ")

api_key = config['KEYS']['API_KEY']
headers = {'Authorization': 'Bearer %s' % api_key}

def main():
    args = parser.parse_args()
    # Pricing levels to filter the search result with: 1 = $, 2 = $$, 3 = $$$, 4 = $$$$.
    b = BusinessSearch(term=args.term, location=args.location, price=args.price)
    db = DatabaseDriver()
    db.setup()

    queries = [insert_business_table.format(str(result['id']),str(result['name']),str(result['image_url']),str(result['url']),str(result['review_count']),str(result['categories']),str(result['rating']),str(result['latitude']),str(result['longitude']),str(result['price']),str(result['location']),str(result['display_phone'])) for result in b.get_results()]
    query_to_execute = "BEGIN; \n" + '\n'.join(queries) + "\nCOMMIT;"
    db.execute_query(query_to_execute)

if __name__ == "__main__":
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument("-t", "--term",  metavar='', required=True,
                          help="Search term, for example \"food\" or \"restaurants\". The term may also be business names, such as \"Starbucks.\".")
    required.add_argument("-l", "--location",  metavar='', required=True,
                          help="This string indicates the geographic area to be used when searching for businesses. ")
    optional.add_argument("-p", "--price", type=int, metavar='', required=False, default=1,
                          help="Pricing levels to filter the search result with: 1 = $, 2 = $$, 3 = $$$, 4 = $$$$.")

    main()