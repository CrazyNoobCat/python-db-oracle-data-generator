import time
import oracledb
import getpass
import generate
from datetime import datetime

_connection: oracledb.Connection = None
daysAgoTimestamp = datetime.timestamp(datetime.now()) - (2 * 86399)


def _createValueString(numColoums: int, custom: list = None):
    val: str = ""
    for i in range(numColoums):
        temp = i + 1
        if custom is None:
            val += ":" + str(temp) + ", "
        elif custom[i] != None and custom[i] != '':
            if custom[i] == 'DATE':
                val += "TO_DATE(:" + str(temp) + ", 'YYYY-MM-DD'), "
            else:
                val += custom[i] + ":" + str(temp) + ", "
        else:
            val += ":" + str(temp) + ", "

    val = val.removesuffix(', ')
    return val


def _insertData(table: str, colNames: str, rows, customvalueNames=None):
    cursor = oracledb.Cursor(connection=_connection)
    cursor.prepare('insert into {} ({}) values ({})'.format(
        table, colNames, _createValueString(len(colNames.split(',')), customvalueNames)))
    cursor.statement
    cursor.executemany(None, rows, True)
    _connection.commit()
    cursor.close()
    pass


def _selectData(table: str, colNames: str):
    cursor = oracledb.Cursor(connection=_connection)
    cursor.prepare('select {} from {}'.format(colNames, table))
    cursor.execute(None, None)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def _insertAddressData(numAddressesToReturn=50) -> list:
    rows = []

    for _ in range(numAddressesToReturn):
        row = (generate.NUMBER(8, 5), generate.NUMBER(8, 5), generate.NVARCHAR2(40), generate.NVARCHAR2(50), generate.NVARCHAR2(
            20), generate.NVARCHAR2(50), generate.NVARCHAR2(50), generate.NVARCHAR2(60), generate.NVARCHAR2(20))
        rows.append(row)

    print("Address rows generated")

    _insertData(
        "addresstest", "latitude,longitude,region,country,postcode,city,suburb,street,house_number", rows)

    print("Address rows inserted")

    return rows


def _insertVehicleData(numVehicles):
    rows = []

    colours = ['white', 'white', 'green', 'purple', 'black', 'white', 'white',
               'black', 'blue',     'purple', 'yellow', 'green', 'white',
               'blue', 'blue', 'green', 'green', 'red', 'black', 'yellow',
               'white', 'blue', 'orange', 'green', 'blue', 'green', 'white',
               'red', 'yellow', 'red', 'green', 'white', 'red', 'white',
               'yellow', 'orange', 'red', 'black', 'green', 'orange', 'purple',
               'blue', 'red', 'red', 'blue', 'purple', 'yellow', 'yellow', 'red',
               'yellow']

    driveTypes = ['FWD', 'RWD', 'AWD', '4WD']

    years = [1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
             2010, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    transmissionTypes = ['Automatic', 'Manual', 'CVT',
                         'Dual Clutch', 'Auto Manual', 'Tiptronic', 'DSG', 'PDK']

    models = ['Acura', 'Alfa Romeo', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Citroen', 'Dodge', 'Ferrari', 'Fiat', 'Ford', 'Geely', 'General Motors', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Isuzu Motors', 'Jaguar Land Rover', 'Jeep', 'Kia', 'Lamborghini',
              'Land Rover', 'Lexus', 'Maserati', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mini (BMW)', 'Mitsubishi Motors', 'Nissan Motor.', 'Pagani Automobili', 'Peugeot S.A.', "Porsche AG", "Ram Trucks", "Renault S.A.", "Rolls-Royce", "Saab Automobile", "Subaru", "Suzuki Motor", "Tesla, Inc.", "Toyota Motor", "Volkswagen", "Volvo Cars"]
    vehicle_types = ['Sedan', 'Coupe', 'Convertible', 'SUV',
                     'Crossover', 'Hatchback', 'Wagon', 'Van', 'Truck']
    engine_types = ['V12', 'V10', 'V8', 'V6', 'I4', 'I6']

    for _ in range(numVehicles):
        row = (generate.NCHAR(17), generate.FROM(years), generate.FROM(colours), generate.FROM(transmissionTypes), generate.NUMBER(4, 2), generate.FROM(
            driveTypes), generate.FROM(models), generate.FROM(vehicle_types), generate.FROM(engine_types), generate.NUMBER(10, 2))
        rows.append(row)

    print("Vehicle rows generated")

    _insertData(
        "vehicletest", "vin,year,colour,transmission_type,fuel_consumption_per100km,drive_type,model,vehicle_type,engine,msrp", rows)

    print("Vehicle rows inserted")

    return rows


def _insertDealership(numToGenerate=50, originalAddresses: list = None):
    '''Requires 50 addresses to parsed in'''

    rows = []

    franchises = ['Odin Cars Rototuna', 'Odin Cars Huntington', 'Odin Cars Rototuna1', 'Odin Cars Huntington1', 'Odin Cars Rototuna12', 'Odin Cars Huntington12', 'Odin Cars Hamilton East', 'Odin Cars Hamilton CBD', 'Odin Cars Auckland', 'Odin Cars Wellington', 'Odin Cars Christchurch', 'Odin Cars Hamilton', 'Odin Cars Tauranga', 'Odin Cars Napier-Hastings', 'Odin Cars Dunedin', 'Odin Cars Palmerston North', 'Odin Cars Nelson', 'Odin Cars Rotorua', 'Odin Cars New Plymouth', 'Odin Cars Whangarei', 'Odin Cars Invercargill', 'Odin Cars Gisborne', 'Odin Cars Timaru', 'Odin Cars Blenheim', 'Odin Cars Taupo', 'Odin Cars Pukekohe East-Paerata', 'Odin Cars Masterton', 'Odin Cars Levin', 'Odin Cars Ashburton ',
                  'Odin Cars Whakatane ', 'Odin Cars Thames-Coromandel ', 'Odin Cars Kawerau ', "Odin Cars South Wairarapa ", "Odin Cars Waitomo ", "Odin Cars Kaikoura ", "Odin Cars Buller ", "Odin Cars Grey ", "Odin Cars Tasman ", "Odin Cars Stratford ", "Odin Cars Waimakariri ", "Odin Cars Central Hawke's Bay ", "Odin Cars Clutha ", "Odin Cars Gore ", "Odin Cars Mackenzie ", "Odin Cars Selwyn ", "Odin Cars Wairoa ", "Odin Cars Westland ", "Odin Cars Waitaki ", "Odin Cars Kaipara ", "Odin Cars Hauraki ", "Odin Cars Hurunui ", "Odin Cars Horowhenua ", "Odin Cars South Taranaki ", "Odin Cars Waimate "]

    addresses = originalAddresses.copy()

    for _ in range(numToGenerate):
        franchiseName = franchises.pop(generate.RANDRANGE(0, len(franchises)))
        address = addresses.pop(generate.RANDRANGE(0, len(addresses)))
        latitude = address[0]
        longitude = address[1]
        row = (franchiseName, generate.DATE(
            endDateTimestamp=daysAgoTimestamp), latitude, longitude)
        rows.append(row)

    print("Dealership rows generated")

    customValues = [None, 'DATE', None, None]

    _insertData(
        "dealershiptest", "dealership_name,dealership_start_date,dealership_latitude,dealership_longitude", rows, customValues)

    print("Dealership rows inserted")

    return rows


def _insertPeople(addresses: list) -> list:

    mostRecentDOB = datetime.timestamp(
        datetime.now()) - 662687999  # 20 years ago

    rows = []
    for _ in range(len(addresses)):
        address = addresses.pop(generate.RANDRANGE(0, len(addresses)))
        latitude = address[0]
        longitude = address[1]
        row = (generate.NUMBER(12, 0, 1000000000), generate.EMAIL(), generate.NUMBER(
            16, 0), generate.NVARCHAR2(30), generate.NVARCHAR2(30), generate.DATE(endDateTimestamp=mostRecentDOB), latitude, longitude)
        rows.append(row)

    print("People rows generated")

    customValues = [None, None, None, None, None, 'DATE', None, None]

    _insertData(
        "persontest", "phone_number,email_address,bank_account_number,lname,fname,date_of_birth,person_address_latitude,person_address_longitude", rows, customValues)

    print("People rows inserted")

    return rows


def _insertStaff(originalStaffIDs: list) -> list:
    job_positions = ["Customer Service Manager", "Customer Service Representative", "Finance Director", "Finance Manager", "General Manager", "Marketing Coordinator", "Marketing Manager", "Parts Advisor", "Parts Director", "Parts Manager", "Parts Specialist", "Sales Consultant", "Sales Director", "Sales Manager",
                     "Sales Trainer", "Service Advisor", "Service Coordinator", "Service Manager", "Service Technician", "Accountant", "Human Resources Manager", "Receptionist", "Inventory Manager", "Detailer", "Lot Attendant", "IT Manager", "IT Specialist", "IT Support Technician", "Shipment Manager", "Shipment Coordinator", "Shipment Driver"]

    rows = []

    staffIDs = originalStaffIDs.copy()

    for _ in range(len(staffIDs)):
        id = staffIDs.pop(generate.RANDRANGE(0, len(staffIDs)))[0]
        row = (id, generate.NUMBER(8, 2), generate.FROM(
            job_positions), generate.EMAIL())
        rows.append(row)

    print("Staff rows generated")

    _insertData(
        "stafftest", "staff_person_id,staff_salary,staff_position,staff_email", rows)

    print("Staff rows inserted")

    return rows


def _insertCustomers(originalCustomerIDs: list) -> list:
    rows = []

    customerIDs = originalCustomerIDs.copy()

    for _ in range(len(customerIDs)):
        id = customerIDs.pop(generate.RANDRANGE(0, len(customerIDs)))[0]
        row = [id]
        rows.append(row)

    print("Customer rows generated")

    _insertData(
        "customertest", "customer_person_id", rows)

    print("Customer rows inserted")

    return rows


def _insertEmploymentContracts(dealerships: list, originalStaffPeople: list, staffDetails: list) -> list:
    rows = []

    staffPeople = originalStaffPeople.copy()

    for _ in range(len(staffPeople)):
        person = staffPeople.pop(generate.RANDRANGE(0, len(staffPeople)))
        dob: datetime = person[6]
        # todo check this produces the correct timestamp
        timestamp = dob.timestamp()
        timestamp += 536457600  # this is 17 years
        dealership = generate.FROM(dealerships)
        dealershipStartTimestamp = time.mktime(
            time.strptime(dealership[1], "%Y-%m-%d"))

        earliestDate = None

        if timestamp < dealershipStartTimestamp:
            earliestDate = dealershipStartTimestamp
        else:
            earliestDate = timestamp

        # Ensure enndDate,Timestamp is 2 days ago
        contractStartDate = generate.DATE(earliestDate)

        endDate = ''
        if generate.RANDRANGE(0, 10) == 9:
            endDate = generate.DATE(time.mktime(
                time.strptime(contractStartDate, "%Y-%m-%d")) + 10)

        if endDate != '':
            if time.mktime(time.strptime(contractStartDate, "%Y-%m-%d")) > time.mktime(time.strptime(endDate, "%Y-%m-%d")):
                print("FAIL")

        row = (contractStartDate, person[0],
               dealership[0], dealership[1], endDate)
        rows.append(row)

    print("Employment Contract rows generated")

    customValues = ['DATE', None, None, 'DATE', 'DATE']

    _insertData(
        "employmentContractTest", "employment_contract_start_date,employee_id,dealership_name,dealership_start_date,employment_contract_end_date", rows, customValues)

    print("Employment Contract rows inserted")

    return rows


def _insertPurchaseContracts(singleSalePercentage: int, resalePercentage: int, originalDealerships: list, originalCustomerPeopl: list, originalStaffPeople: list, originalVehicles: list) -> list:
    rows = []

    # Statuses
    statuses = ['PAID', 'ON FINANCE', 'AWAITING PAYMENT', 'PAYMENT OVERDUE']

    # Ensure we are only editing a copy
    vehicles = originalVehicles.copy()

    # Pop vehicles which need to be resold (5%)?
    maxCount = int(len(vehicles) * resalePercentage)

    for _ in range(maxCount):
        vehicle = vehicles.pop(generate.RANDRANGE(0, len(vehicles)))
        vin = vehicle[0]
        numReSales = generate.RANDRANGE(2, 5)

        # We are gonna assume it can only be resold by the same dealership
        # Pick dealership
        d = generate.FROM(originalDealerships)
        dName = d[0]
        dStartDate = d[1]
        lastTimeStamp = time.mktime(time.strptime(dStartDate, "%Y-%m-%d"))

        for i in range(numReSales):
            # Generate start date
            # Ensure that an end date will exist
            pcStartDate = generate.DATE(
                startDateTimestamp=lastTimeStamp, endDateTimestamp=daysAgoTimestamp - ((1 * 86399) * (numReSales-i)))
            lastTimeStamp = time.mktime(
                time.strptime(pcStartDate, "%Y-%m-%d")) + 86399
            s = generate.FROM(originalStaffPeople)
            sID = s[0]
            c = generate.FROM(originalCustomerPeopl)
            cID = c[0]
            salePrice = generate.NUMBER(10, 2)
            status = generate.FROM(statuses)

            row = (pcStartDate, vin, dName, dStartDate,
                   cID, sID, salePrice, status)
            rows.append(row)

    # Pop vehicles to sell once (80%)?
    maxCount = int(len(vehicles) * singleSalePercentage)

    for _ in range(maxCount):
        vehicle = vehicles.pop(generate.RANDRANGE(0, len(vehicles)))
        vin = vehicle[0]

        d = generate.FROM(originalDealerships)
        dName = d[0]
        dStartDate = d[1]
        lastTimeStamp = time.mktime(time.strptime(dStartDate, "%Y-%m-%d"))
        # Generate start date
        # Ensure that an end date will exist
        pcStartDate = generate.DATE(startDateTimestamp=lastTimeStamp)
        s = generate.FROM(originalStaffPeople)
        sID = s[0]
        c = generate.FROM(originalCustomerPeopl)
        cID = c[0]
        salePrice = generate.NUMBER(10, 2)
        status = generate.FROM(statuses)

        row = (pcStartDate, vin, dName, dStartDate,
               cID, sID, salePrice, status)
        rows.append(row)

    print("Purchase Contract rows generated")

    customValues = ['DATE', None, None, 'DATE', None, None, None, None]

    _insertData(
        "purchaseContractTest", "purchase_contract_start_date,vin,dealership_name,dealership_start_date,customer_person_id,staff_person_id,sale_price,status", rows, customValues)

    print("Purchase Contract rows inserted")

    return rows


if __name__ == "__main__":
    url = input("DB URL: ")
    username = input("Username: ")
    userpwd = getpass.getpass()
    serviceName = input("Service Name: ")

    params = oracledb.ConnectParams(
        host=url, port=1521, service_name=serviceName)
    _connection = oracledb.connect(
        user=username, password=userpwd, params=params)

    addresses = _insertAddressData(300000)
    vehicles = _insertVehicleData(400000)

    dealershipAddresses = addresses[0:50]
    dealerships = _insertDealership(50,
                                    dealershipAddresses)  # 50 dealerships

    peopleAddresses = addresses[51:]
    _insertPeople(addresses=peopleAddresses)  # 499950 people

    people: list = _selectData('persontest', '*')

    staffPeople = people[0:19950]  # 19950 staff
    customerPeople = people[19951:]  # 42xxxx customers

    staffDetails = _insertStaff(staffPeople)
    _insertCustomers(customerPeople)

    employmentContracts = _insertEmploymentContracts(
        dealerships, staffPeople, staffDetails)
    # purchaseContracts = _insertPurchaseContracts(
    #    dealerships, customerPeople, staffPeople, vehicles)

    pcs = _insertPurchaseContracts(
        0.60, 0.02, dealerships, customerPeople, staffPeople, vehicles)

    _connection.close()

