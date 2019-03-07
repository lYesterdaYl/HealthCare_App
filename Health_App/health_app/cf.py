import random
from math import e

class collaborative_filtering:
    def __init__(self,ratings,k=3):
        self.ratings = ratings
        self.k = k
        self.user_num = len(ratings)
        self.item_num = len(ratings[0])
        self.user_embedding = self.init_user_embedding()
        self.item_embedding = self.init_item_embedding()
        self.predictions = self.init_predictions()

    def recommend_item(self,user_index):
        self.train()
        self.predict()
        best_rating = self.predictions[user_index][0]
        item_index = 0
        for i in range(self.item_num):
            if self.predictions[user_index][i] > best_rating:
                best_rating = self.predictions[user_index][i]
                item_index = i
        return item_index
            

    def init_user_embedding(self):
        user_embedding = []
        for i in range(self.user_num):
            user_embedding.append([])
            for j in range(self.k):
                user_embedding[i].append(random.uniform(0,2))
        return user_embedding

    def init_item_embedding(self):
        item_embedding = []
        for i in range(self.k):
            item_embedding.append([])
            for j in range(self.item_num):
                item_embedding[i].append(random.uniform(0,2))
        return item_embedding

    def init_predictions(self):
        predictions = []
        for i in range(self.user_num):
            predictions.append([])
            for j in range(self.item_num):
                predictions[i].append(0)
        return predictions

    def train(self,init_step=0.01,stop_epochs=50):
        epoch = 0
        done = False
        while not done:
            stepsize = init_step*2.0/(2.0+epoch)
            epoch +=1
            for i in range(self.user_num):
                for j in range(self.item_num):
                    if self.ratings[i][j] != None:
                        r_ij = self.compute_prediction(i,j)
                        for k in range(self.k):
                            gradi_user_ik = self.compute_gradient_user_ik(r_ij,i,j,k)
                            gradi_item_kj = self.compute_gradient_item_kj(r_ij,i,j,k)
                            self.user_embedding[i][k] -= stepsize*gradi_user_ik
                            self.item_embedding[k][j] -= stepsize*gradi_item_kj
            if epoch > stop_epochs:
                done = True

    def predict(self):
        for i in range(self.user_num):
            for j in range(self.item_num):
                self.predictions[i][j] = self.compute_prediction(i,j)
                        

    def compute_prediction(self,user_index,item_index):
        result = 0
        for k in range(self.k):
            result += self.user_embedding[user_index][k] * self.item_embedding[k][item_index]
        return result

    def sigmoid(self,x):
        return 1.0/(1+e**(-x))

    def compute_gradient_user_ik(self,r_ij,i,j,k):
        sig = self.sigmoid(r_ij)
        return -10*(self.ratings[i][j]-5*sig)*sig*(1-sig)*self.item_embedding[k][j]

    def compute_gradient_item_kj(self,r_ij,i,j,k):
        sig = self.sigmoid(r_ij)
        return -10*(self.ratings[i][j]-5*sig)*sig*(1-sig)*self.user_embedding[i][k]
        
        


    

        
