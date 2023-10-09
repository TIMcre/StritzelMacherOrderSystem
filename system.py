import sys



strizel_sorts = {
  1 : "Zimt und Zucker"
  2 : "Oreo"
  
}
def get_input():
  
def convert_to_stritzel(number):
  try:
    stritzel = stritzel_sorts[number]
  except ValueError:
    sys.exit("value error")

  return strizel

def add_order():

def remove_order():

def add_history():

def main():
  get_input()
  strizel = convert_to_strizel(input)
  add_order(strizel)
  # if 2nd input true remove_order and add to history


if __name__ == "__main__":
  main()
  
