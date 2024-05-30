from db import Region


class ListRegions:
    def run(self):
        for i, region in enumerate(Region.list_regions()):
            if i == 0:
                print("\t".join(region.data.keys()))
            print("\t".join(str(s) for s in region.data.values()))


if __name__ == "__main__":
    ListRegions().run()
