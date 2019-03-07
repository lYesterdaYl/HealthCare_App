import random

class estimation:
    def __init__(self,input_dict):
        self.input = input_dict

    def estimate(self):
        average = self.input["average_score"]
        score   = self.input["score"]
        prefer = self.input["prefer"]
        if prefer == "":
            prefer = "music" if random.random()>0.5 else "video"
        result = 0.3*average+0.7*score
        if result<=1.5:
            return ("A",prefer)
        elif result<=2.5:
            return ("B",prefer)
        elif result<=3.5:
            return ("C",prefer)
        else:
            return ("D",prefer)
