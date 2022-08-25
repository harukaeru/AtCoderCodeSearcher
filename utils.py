from bs4 import BeautifulSoup

def get_text(text):
  if not text:
    return text

  print('text', text)
  soup = BeautifulSoup(text)
  return soup.get_text()