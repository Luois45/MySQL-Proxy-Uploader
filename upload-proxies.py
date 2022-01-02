import json
import mysql.connector

with open('config.json', 'r') as configFile:
    config = json.load(configFile)

cnx = mysql.connector.connect(user=config['mysql']['username'],
                              password=config['mysql']['password'],
                              host=config['mysql']['ip'],
                              port=config['mysql']['port'],
                              database=config['mysql']['database'])
print(f"MySQL: Logged in as {cnx.user}")
cursor = cnx.cursor()


def executeSQL(command):
    cursor.execute(command)
    cnx.commit()


def searchSQL(command):
    # cursor.execute(f"SELECT * FROM items WHERE name = ''")
    # productinfo = cart_cursor.fetchall()[0]
    cursor.execute(command)
    return cursor.fetchall()


executeSQL(
    'CREATE TABLE IF NOT EXISTS `proxies` (`id` int NOT NULL AUTO_INCREMENT PRIMARY KEY, `ip` varchar(256) DEFAULT NULL, `port` MEDIUMINT DEFAULT NULL, `username` varchar(256) DEFAULT NULL, `password` varchar(256) DEFAULT NULL, `inuse` BOOLEAN DEFAULT False) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4'
)

with open(config['proxy']['file'], 'r') as proxiesFile:
    for proxy in proxiesFile:
        proxyList = proxy.replace('\n', '').split(':')
        proxyIP = proxyList[0]
        proxyPort = proxyList[1]
        proxyUsername = proxyList[2]
        proxyPassword = proxyList[3]
        if searchSQL(
                f"SELECT * FROM proxies WHERE ip = '{proxyIP}' AND port = '{proxyPort}' AND username = '{proxyUsername}' AND password = '{proxyPassword}'"
        ) == []:
            executeSQL(
                f"INSERT INTO proxies (ip, port, username, password) VALUES ('{proxyIP}', '{proxyPort}', '{proxyUsername}', '{proxyPassword}');"
            )
print('Uploaded proxies to MySQL database')

cnx.close()
