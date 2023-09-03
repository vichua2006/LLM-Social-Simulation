import jsonpickle

class B:
    def __init__(self, value):
        self.value = value
    
    def __getstate__(self):
        print("B's getstate invoked")
        return self.__dict__
    
    def __setstate__(self, state):
        print("B's setstate invoked")
        self.__dict__.update(state)

class A:
    def __init__(self, x, y):
        self.x = x
        self.y = B(y)


# Create an instance of A
a = A(10, 20)

# Encode
encoded_a = jsonpickle.encode(a)
print("Encoded A:", encoded_a)

# Decode
decoded_a = jsonpickle.decode(encoded_a)
print("Decoded A:", decoded_a)