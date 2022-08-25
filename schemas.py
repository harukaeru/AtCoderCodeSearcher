class AtcoderUser:
  def __init__(self, country_code, name, affiliation, rank, birth_year, rating):
    self.country_code = country_code
    self.name = name
    self.affiliation = affiliation
    self.rank = rank
    self.birth_year = birth_year
    self.rating = rating

  def __repr__(self):
    return f'<レート: {self.rating}, ユーザ名: {self.name}, 国: {self.country_code}>'