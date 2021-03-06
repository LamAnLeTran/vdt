from app import mysql, session
from blockchain import Block, Blockchain

class InvalidTransactionException(Exception): pass
class InsufficientFundsException(Exception): pass
#<-------------------------->
class Table():
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = "(%s)" %",".join(args)
        self.columnsList = args

        #if table does not already exist, create it.
        if isnewtable(table_name):
            create_data = ""
            for column in self.columnsList:
                create_data += "%s varchar(100)," %column

            cur = mysql.connection.cursor() #create the table
            cur.execute("CREATE TABLE %s(%s)" %(self.table, create_data[:len(create_data)-1]))
            cur.close()
    
    # sql execute
    #get all the values from the table
    def getall(self):
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s" %self.table)
        data = cur.fetchall(); return data

    #get one value from the table based on a column's data
    #EXAMPLE using blockchain: ...getone("hash","00003f73gh93...")
    def getone(self, search, value):
        data = {}; cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s WHERE %s = \"%s\"" %(self.table, search, value))
        if result > 0: data = cur.fetchone()
        cur.close(); return data

    #delete a value from the table based on column's data
    def deleteone(self, search, value):
        cur = mysql.connection.cursor()
        cur.execute("DELETE from %s where %s = \"%s\"" %(self.table, search, value))
        mysql.connection.commit(); cur.close()

    #delete all values from the table.
    def deleteall(self):
        self.drop() #remove table and recreate
        self.__init__(self.table, *self.columnsList)

    #remove table from mysql
    def drop(self):
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE %s" %self.table)
        cur.close()

    #insert values into the table
    def insert(self, *args):
        data = ""
        for arg in args: #convert data into string mysql format
            data += "\"%s\"," %(arg)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO %s%s VALUES(%s)" %(self.table, self.columns, data[:len(data)-1]))
        mysql.connection.commit()
        cur.close()
    
    #<------------>

#execute mysql code from python
def sql_raw(execution):
    cur = mysql.connection.cursor()
    cur.execute(execution)
    mysql.connection.commit()
    cur.close()

#check if table already exists
def isnewtable(tableName):
    cur = mysql.connection.cursor()

    try: #attempt to get data from table
        result = cur.execute("SELECT * from %s" %tableName)
        cur.close()
    except:
        return True
    else:
        return False

#check if user already exists
def isnewuser(username):
    #access the users table and get all values from column "username"
    users = Table("users", "name", "email", "username", "password")
    data = users.getall()
    usernames = [user.get('username') for user in data]

    return False if username in usernames else True


def send_money(sender, receipient, amount):
    try: amount =float(amount)
    except ValueError:
        raise InvalidTransactionException("Invalid Transaction.")
    if amount > get_balance(sender) and sender !="BANK":
        raise InsufficientFundsException("Insufficient Funds.")
    elif sender == receipient or amount<=0.00:
        raise InvalidTransactionException("Invalid Transaction.")
    elif isnewuser(receipient):
        raise InvalidTransactionException("User does not exist.")

    blockchain = get_blockchain()
    number = len(blockchain.chain) + 1
    data = "%s-->%s-->%s" %(sender,receipient,amount)
    blockchain.mine(Block(number,data=data))
    sync_blockchain(blockchain)


def get_balance(username):
    balance = 0.00
    blockchain = get_blockchain()
    for block in blockchain.chain:
        data = block.data.split("-->")
        if username == data[0]:
            balance -= float(data[2])
        if username == data[1]:
            balance += float(data[2])
    return balance

def get_user_block(username):
    blockchain_sql = Table("blockchain", "number", "hash", "previous", "data", "nonce")
    user_blockchain = Blockchain()
    for b in blockchain_sql.getall():
        data = b.get('data').split("-->")
        if username == data[0]:
            user_blockchain.add(Block(int(b.get('number')), b.get('previous'), b.get('data'), b.get('nonce')))
        if username == data[1]:
            user_blockchain.add(Block(int(b.get('number')), b.get('previous'), b.get('data'), b.get('nonce')))
    return user_blockchain

# get block from table
def get_blockchain():
    blockchain = Blockchain()
    blockchain_sql = Table("blockchain", "number", "hash", "previous", "data", "nonce")
    for b in blockchain_sql.getall():
        blockchain.add(Block(int(b.get('number')), b.get('previous'), b.get('data'), b.get('nonce')))

    return blockchain
    

# insert block to db
def sync_blockchain(blockchain):
    blockchain_sql = Table("blockchain", "number", "hash", "previous", "data", "nonce")
    blockchain_sql.deleteall()

    for block in blockchain.chain:
        blockchain_sql.insert(str(block.number), block.hash(), block.previous_hash, block.data, block.nonce)

# test blockchain insert, delete
def test_blockchain():
    # blockchain = Blockchain()
    # database = ["hello world", "wat's up", "hello", "bye"]

    # num=0
    # for data in database:
    #     num+=1
    #     blockchain.mine(Block(number=num,data=data))
    # sync_blockchain(blockchain)
    blockchain_sql = Table("blockchain", "number", "hash", "previous", "data", "nonce")
    blockchain_sql.deleteall()