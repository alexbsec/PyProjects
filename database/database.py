class DBStructure:
    def __init__(self, nr_, nc_, db_name_=None):
        self.number_of_rows = nr_
        self.number_of_columns = nc_
        self.name = db_name_
        self.columns = self.make_list(name_="columns")
        self.rows = self.make_list(name_="rows")

    def make_list(self, name_=None):
        if name_ == "columns":
            self.columns = list()
            for i in range(self.number_of_columns):
                value = input(f'Input {i}-th index value of {name_}: ')
                self.make_content(value, name_=name_)
        elif name_ == "rows":
            self.rows = list()
            for i in range(self.number_of_rows):
                value = input(f'Input {i}-th index value of {name_}: ')
                self.make_content(value, name_=name_)

    def make_content(self, value_, name_=None):
        if name_ == "columns":
            self.columns.append(value_)
        elif name_ == "rows":
            self.rows.append(value_)






row = DBStructure(10, 10)
print(row.number_of_rows)