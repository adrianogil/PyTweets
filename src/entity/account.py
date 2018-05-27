class Account:
    
    def __init__(self, twitter_handle='', name='', bio='', 
                        following=False, followers=False, total_tweets=0):
        self.id = -1
        self.bio = bio
        self.name = name
        self.twitter_handle = twitter_handle
        self.followers = followers
        self.following = following
        self.is_following_me = False
        self.iam_following = False
        self.total_tweets = total_tweets

    def get_data(self):
        if self.is_following_me:
            f_me = 1
        else:
            f_me = 0

        if self.iam_following:
            iam_f = 1
        else:
            iam_f = 0

        return (self.name, self.twitter_handle, self.bio, \
                self.followers, self.following, self.total_tweets, \
                f_me, iam_f)