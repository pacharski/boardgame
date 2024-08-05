class Token():
    def __init__(self, name, color, image=None, location=None):
        self.name = name
        self.color = color
        self.image = image
        self.location = location
        
    def __str__(self):
        form = "Token {}: {}/{} at {}"
        return form.format(self.name, self.color, self.image, self.location)
        

if __name__ == '__main__':
    t1 = Token("G-er", "green", location=0)
    t2 = Token("B-er", "blue",  location=23)
    t3 = Token("R-er", "red",   location=100)
    t4 = Token("R-er", "red",   location=212)
    t5 = Token("W-er", "white", location=256)

    tokens = [t1, t2, t3, t4, t5]
    for token in tokens:
        print(token)
