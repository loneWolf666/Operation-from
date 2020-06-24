import fire

def hello(name="World"):
  return "Hello %s!" % name


class Calculator(object):
  """A simple calculator class."""

  def double(self, number):
    return 2 * number

if __name__ == '__main__':
  fire.Fire(Calculator)
# if __name__ == '__main__':
#   fire.Fire(hello)