import sqlite3

conn = None


class DBO:
    DB_FILE = "../data/countries.db"

    def __init__(self):
        global conn

        if conn is None:
            conn = sqlite3.connect(self.DB_FILE)
        self.cursor = conn.cursor()

        self.data = None


class Region(DBO):
    def create(self, name):
        insert_query = "INSERT INTO region (name) VALUES (?)"
        self.cursor.execute(insert_query, (name,))
        conn.commit()

    def get_by_name(self, name):
        select_query = "SElECT id, name FROM region WHERE name=?"
        self.cursor.execute(select_query, (name,))
        region_data = self.cursor.fetchone()
        if not region_data:
            return False
        headers = [header[0] for header in self.cursor.description]
        self.data = {k: v for k, v in zip(headers, region_data)}
        return True

    def get_or_create_by_name(self, name):
        self.get_by_name(name)
        if not self.data:
            self.create(name)
        self.get_by_name(name)

    @classmethod
    def list_regions(cls):
        dbo = DBO()
        select_statement = """
            SELECT r.name as name, count(*) as number_countries, SUM(c.population) as total_population
                FROM country c
                JOIN region r ON c.region_id = r.id
                GROUP BY region_id;
            """
        dbo.cursor.execute((select_statement))
        headers = [header[0] for header in dbo.cursor.description]

        for row in dbo.cursor.fetchall():
            obj = cls()
            obj.data = {k: v for k, v in zip(headers, row)}
            yield obj


class Country(DBO):
    def insert(self, name, alpha2Code, alpha3Code, population, region_id, topLevelDomain, capital):
        insert_query = (
            "INSERT INTO country (name, alpha2Code, alpha3Code, population, "
            "topLevelDomain, capital, region_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
        )
        self.cursor.execute(
            insert_query, (name, alpha2Code, alpha3Code, population, region_id, topLevelDomain, capital)
        )
        conn.commit()
        self.get_by_name(name)

    def get_by_name(self, name):
        select_query = "SElECT * FROM country WHERE name=?"
        self.cursor.execute(select_query, (name,))
        region_data = self.cursor.fetchone()
        if not region_data:
            return False
        headers = [header[0] for header in self.cursor.description]
        self.data = {k: v for k, v in zip(headers, region_data)}
        return True

    @classmethod
    def list_all(cls):
        dbo = DBO()
        select_statement = """
            SELECT c.name AS country_name, c.alpha2Code, c.alpha3Code,
                    c.population, c.topLevelDomain, c.capital, r.name AS region_name
                FROM country c
                JOIN region r ON c.region_id = r.id;
            """
        # dbo.cursor.execute("PRAGMA table_info(country)")
        dbo.cursor.execute((select_statement))
        headers = [header[0] for header in dbo.cursor.description]

        for row in dbo.cursor.fetchall():
            obj = cls()
            obj.data = {k: v for k, v in zip(headers, row)}
            yield obj
