class Token():
    cShapes = ["circle", "triangle", "square", "pentagon", "hexagon",
               "star"]
    
    def __init__(self, name, color=None, shape="circle", size=None, image=None):
        self.name = name
        self.color = color
        self.shape = shape
        self.size = size
        self.image = image
        
    def __str__(self):
        form = "Token: {} Shape={}-{}-{} Image={}"
        return form.format(self.name, self.color, self.shape, 
                           "auto" if self.size == None else self.size,
                           self.image)
        

if __name__ == '__main__':
    t1 = Token("G-er", "green", "square") 
    t2 = Token("B-er", "blue", "circle") 
    t3 = Token("R-er", "red", "triangle")  
    t4 = Token("R-er", "red", "triangle")   
    t5 = Token("W-er", "white", "star")

    tokens = [t1, t2, t3, t4, t5]
    for token in tokens:
        print(token)
