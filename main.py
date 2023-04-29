import oracledb
import getpass

if __name__ == "__main__":
    url = input("DB URL: ")
    username = input("Username: ")
    userpwd = getpass.getpass()
    serviceName = input("Service Name: ")

    params = oracledb.ConnectParams(host=url, port=1521, service_name=serviceName)
    connection = oracledb.connect(user=username, password=userpwd,params=params)
    


    