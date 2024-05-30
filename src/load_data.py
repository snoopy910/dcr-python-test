import json
import requests

from db import Country, Region


class LoadData:
    # DATA_FILE = "../data/countries.json"
    DATA_ENDPOINT = "https://storage.googleapis.com/dcr-django-test/countries.json"

    def __init__(self):
        # Cache of regions
        self.regions = {}

    def get_raw_data(self):
        try:
            # data = None
            # with open(self.DATA_FILE, encoding="utf8") as f:
            #     data = json.load(f)
            response = requests.get(self.DATA_ENDPOINT)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return []

    def add_country(self, data):
        region_name = data.get("region", "Unknown")
        region_id = self.get_region_id(region_name)

        country = Country()
        found = country.get_by_name(data["name"])
        top_level_domains = ', '.join(data["topLevelDomain"]) if data["topLevelDomain"] else None
        if found:
            return
        country.insert(
            data["name"],
            data["alpha2Code"],
            data["alpha3Code"],
            data["population"],
            top_level_domains,
            data["capital"],
            region_id,
        )
        print(country.data)

    def get_region_id(self, region_name):
        if region_name not in self.regions:
            region = Region()
            region.get_or_create_by_name(region_name)
            self.regions[region.data["name"]] = region.data["id"]
        return self.regions[region_name]

    def run(self):
        data = self.get_raw_data()
        for row in data:
            self.add_country(row)


if __name__ == "__main__":
    LoadData().run()
