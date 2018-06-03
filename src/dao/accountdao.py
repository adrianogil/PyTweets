
class AccountDAO:
    DEFAULT_Account = 'In Cash'

    def __init__(self, conn, cursor, entityFactory):
        self.conn = conn
        self.cursor = cursor
        self.entityFactory = entityFactory
        self.noCategory = None

    def createTables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Accounts (
                id_account INTEGER,
                account_name TEXT,
                twitter_handle TEXT,
                bio TEXT,
                followers INTEGER,
                following INTEGER,
                total_tweets INTEGER,
                is_following_me INTEGER,
                iam_following INTEGER,
                PRIMARY KEY (id_account)
            )
        ''')
        # print('No Category with id: ' + str(self.noCategory.id))

    def save(self, account):
        sql_query_save = "INSERT INTO Accounts " + \
                            "(account_name, twitter_handle, bio, followers, following, " +\
                            " total_tweets, is_following_me, iam_following)" + \
                        " VALUES (:account_name, :twitter_handle, :bio, :followers, :following," +\
                            " :total_tweets, :is_following_me, :iam_following)"
        save_data = account.get_data()
        self.cursor.execute(sql_query_save, save_data)
        self.conn.commit()

    def createAccount(self, row):
        account = self.entityFactory.createAccount()

        account.id = int(row[0])
        account.bio = row[3]
        account.name = row[1]
        account.twitter_handle = row[2]
        account.followers = int(row[4])
        account.following = int(row[5])
        account.iam_following = row[8]
        account.total_tweets = int(row[6])


    def getAccount(self, twitter_handle):
        # print('DEBUG: categoryDAO - trying to get category from name: ' + name)
        sql_query_get = "SELECT * from Accounts WHERE twitter_handle LIKE ?"
        sql_data = (twitter_handle,)
        self.cursor.execute(sql_query_get, sql_data)
        row = self.cursor.fetchone()
        if row is None:
            return None
        
        return createAccount(row)

    def getAll(self):
        sql_query_get = "SELECT * from Accounts ORDER BY id_account"
        self.cursor.execute(sql_query_get)
        account_list = []
        for row in self.cursor:
            account = self.entityFactory.createAccount(str(row[1]))
            account.id = int(row[0])

            account_list.append(account)

        return account_list

    def getAccountFromId(self, id):
        sql_query_get = "SELECT * from Accounts WHERE id_account LIKE ?"
        sql_data = (id,)
        self.cursor.execute(sql_query_get, sql_data)
        row = self.cursor.fetchone()
        if row is None:
            return None
        account = self.entityFactory.createAccount(str(row[1]))
        account.id = int(row[0])

        return account

    def update(self, account):
        sql_query_update = "UPDATE Accounts SET account_name = ? WHERE id_account = ?"
        update_data = (account.name, account.id)
        self.cursor.execute(sql_query_update, update_data)
        self.conn.commit()

    def delete(self, account):
        sql_query_delete = "DELETE FROM Accounts WHERE id_account = ?"
        delete_data = (account.id,)
        self.cursor.execute(sql_query_delete, delete_data)
        self.conn.commit()

