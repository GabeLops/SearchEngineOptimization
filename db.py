import mysql.connector
from env import env

user = env['user']
password = env['password']

def create_db():
  mydb = mysql.connector.connect(
    host="localhost",
    user=user,
    passwd=password
  )

  mycursor = mydb.cursor()
  mycursor.execute("CREATE DATABASE search_index")


def create_table():
  mydb = mysql.connector.connect(
    host="localhost",
    user=user,
    passwd=password,
    database="search_index"
  )

  mycursor = mydb.cursor()

  mycursor.execute("CREATE TABLE search_index (token VARCHAR(8000), frequency INT, \
    document_id VARCHAR(255), tf_idf FLOAT)")

def insert_indices(doc_list):
  mydb = mysql.connector.connect(
    host="localhost",
    user=user,
    passwd=password,
    database="search_index",
    use_unicode=True
  )

  mycursor = mydb.cursor()
  mycursor.execute('SET autocommit = 0');
  mycursor.execute('SET NAMES utf8mb4')
  mycursor.execute("SET CHARACTER SET utf8mb4")
  mycursor.execute("SET character_set_connection=utf8mb4")
  mycursor.execute('ALTER TABLE search_index MODIFY COLUMN token VARCHAR(8000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;')
  mydb.commit()
  for doc in doc_list:
    data = list(doc.values())[0]
    document_id = list(doc.keys())[0]
    print('Inserting into db')
    # print(document_id)
    for word, val  in data.items():
      frequency = val['count']
      tf_idf = val['tf_idf']
      print(frequency, tf_idf)
      sql = "INSERT INTO search_index (token, frequency, document_id, tf_idf) VALUES (%s, %s, %s, %s)"
      val = (word, frequency, document_id, tf_idf)
      try:
        mycursor.execute(sql, val)
      except mysql.connector.errors.DatabaseError as err:
        print("Something went wrong: {}".format(err))

  mydb.commit()
  mydb.close()

def search(query):
  mydb = mysql.connector.connect(
    host="localhost",
    user=user,
    passwd=password,
    database="search_index",
    use_unicode=True,
    auth_plugin='mysql_native_password'
  )

  filterList = [ x.strip() for x in query.split(" ") if x.strip() ]
  mycursor = mydb.cursor()
  statement = "SELECT * FROM search_index WHERE token IN ({0}) order by tf_idf desc, frequency desc;".format(
    ', '.join(['%s'] * len(filterList)))
  mycursor.execute(statement, filterList)
  result = mycursor.fetchall()
  mydb.close()
  return result

#create_db()