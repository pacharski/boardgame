from token import Token

class TokenView():
    def __init__(self, token)
        self.token = token
        
    def __str__(self):
        form = "TokenView: {}"
        return form.format(self.token)   


if __name__ == '__main__':      
    t1 = Token("G-er", "green", "square") 
    t2 = Token("B-er", "blue", "circle") 
    t3 = Token("R-er", "red", "triangle")  
    t4 = Token("R-er", "red", "triangle")   
    t5 = Token("W-er", "white", "star")

    # Display token on a tkinter canvas
    tokens = [t1, t2, t3, t4, t5]
    for token in tokens:
        print(token)
