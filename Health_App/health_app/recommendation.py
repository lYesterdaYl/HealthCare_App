from estimation import estimation
from cf import collaborative_filtering

class recommendation:
    def __init__(self,user_id,user_dict):
        '''
        user_id: int
        user_dict: dict = {"prefer":"music"/"video"/"",
                            "score":int(1 or 2 or 3 or 4)
                            "average_score":float(in the range of [1,4])}
        '''
        self.user_dict = user_dict
        self.item_dict = None
        self.user_id = user_id
        self.prefer = None

    def estimate(self):
        """
        returns the health state of user("A"/"B","C","D")
        """
        estimator = estimation(self.user_dict)
        state,prefer = estimator.estimate()
        self.prefer = prefer
        return state

    def recommend(self,item_dict):
        """
        Input:
            item_dict = {"music":{music_id:{user_id:rating(int,1-5)}},
                         "video":{video_id:{user_id:rating(int,1-5)}}}
        Output:
            returns the item_id(either music_id or video_id)
        """
        self.item_dict = item_dict
        ratings_dict = self.item_dict[self.prefer]
        users,items,ratings = self.parse_ratings_dict(ratings_dict)
        user_index = self.get_user_index(self.user_id,users)
        model = collaborative_filtering(ratings)
        item_index = model.recommend_item(user_index)
        item_id = items[item_index]
        return {self.prefer:item_id}

    def get_user_index(self,userid,users):
        result = 0
        for i in range(len(users)):
            if users[i] == userid:
                result = i
        return result

    def parse_ratings_dict(self,ratings_dict):
        users = []
        items = []
        ratings = []
        user_index = 0
        item_index = 0
        user_dict = dict()
        item_dict = dict()
        
        for item in ratings_dict:
            item_dict[item] = item_index
            item_index +=1
            items.append(item)
            for user in ratings_dict[item]:
                if user not in user_dict:
                    user_dict[user] = user_index
                    user_index +=1
                    users.append(user)
        for i in range(len(users)):
            ratings.append([])
            for j in range(len(items)):
                ratings[i].append(None)
        for item in ratings_dict:
            for user in ratings_dict[item]:
                ratings[user_dict[user]][item_dict[item]] = ratings_dict[item][user]
        return (users,items,ratings)
