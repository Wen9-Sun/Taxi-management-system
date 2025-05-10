#2.The highest part I have attempted is HD level (especially iv,vi,vii)
#3.My code is problem-free and meets all requirements.
# Read through the program requirements.
# Build a taxi system for booking trips, calculating fares, displaying receipts, etc.
# Required data to be collected: customer name, customer type, departure place, destination, rates, services and various charges, etc.
# Create classes for required attributes separately for calling information.
# Create appropriate get and set methods
# Create exception to handle different errors
# Create a class to store data for reading, searching and displaying the required file content.
# Create the final operating system class and load the data operation program respectively.
# Use a dictionary to store customer orders.
# Store name, location, rate, service, reservation and other data in the list
# Adjust all data accepted according to the type of the original file and write it to the file
# Write command line arguments
# Test code, handle unexpected input, debug errors, and improve code and UI.
# Added final comments.
# Challenge: preliminary overall planning, large-scale programming, data structure selection, testing, debugging.

# Custom exceptions for specific error scenarios.
class DataFileNotFoundError(Exception):
    def __init__(self, filename):
        super().__init__(f"Error: {filename} not found. Please make sure the data files exist.")
        self.filename = filename
class InvalidNameError(Exception):
    pass
class InvalidLocationError(Exception):
    pass
class InvalidRateTypeError(Exception):
    pass
class InvalidDistanceError(Exception):
    pass
class InvalidServiceAnswer(Exception):
    pass
class InvalidRateError(Exception):
    pass
class NotEnterpriseCustomerError(Exception):
    pass
class InvalidRateListError(Exception):
    pass

class Customer:
    def __init__(self,customer_id,name):
        self.customer_id=customer_id
        self.name=name
    #get method
    def get_customer_id(self):
        return self.customer_id
    def get_name(self):
        return self.name
    #Placeholder method, find subclasses based on customer type
    def get_discount(self):
        pass
    def display_info(self):
        pass
# Inherit the parent class customer
class BasicCustomer(Customer):
    discount_rate=0.10 # Default discount rate
    type="B" # Default rate type
    # Using super() to call the parent class's constructor
    def __init__(self,customer_id,name):
        super().__init__(customer_id,name)
    # Calculate discount, if the customer is first time, the discount is 0
    def get_discount(self,distance_fee,first_time=False):
        if first_time:
            return 0
        return self.discount_rate * distance_fee
     # Display basic customer-specific information.
    def display_info(self):
        print(f'Customer ID: {self.customer_id}')
        print(f'Customer Name: {self.name}')
        print(f'Discount Rate: {self.discount_rate * 100}%')
    # Static method allows setting the discount rate for all Basic customers.
    @staticmethod
    def set_discount_rate(new_rate):
        BasicCustomer.discount_rate = new_rate
# Inherit the parent class customer
class EnterpriseCustomer(Customer):
    threshold=100 # Default threshold 
    type="E" # Default rate type
    def __init__(self,customer_id,name,discount_rate1):
        super().__init__(customer_id,name)
        self.discount_rate1 = discount_rate1
        self.discount_rate2 = discount_rate1+0.05 # Default the second rate is always 5% more than the first rate.
    # Calculate enterprise-specific discount
    def get_discount(self,distance_fee,first_time=False):
        if distance_fee < self.threshold:# Amount above which a different discount rate is applied.
            return self.discount_rate1*distance_fee
        else:
            return self.discount_rate2*distance_fee
    # Display enterprise customer-specific information.
    def display_info(self):
        print(f'Customer ID: {self.customer_id}')
        print(f'Customer Name: {self.name}')
        print(f'Discount Rate: (Threshold < {self.threshold}$): {self.discount_rate1*100}%')
        print(f'Discount Rate: (Threshold >= {self.threshold}$): {self.discount_rate2*100}%')
        print(f'Threshold:${self.threshold}')
    # Allows setting the discount rates dynamically.
    def set_discount_rates(self,rate1,rate2=None):
        self.discount_rate1 = rate1
        self.discount_rate2 = rate2 if rate2 else rate1+0.05
    # setting the threshold.    
    @staticmethod
    def set_threshold(new_threshold):
        EnterpriseCustomer.threshold=new_threshold
# Represents a location entity.
class Location:
    def __init__(self,location_id,name):
        self.location_id=location_id
        self.name=name
    # Display location-specific information.
    def display_info(self):
        print(f'Location ID: {self.location_id}')
        print(f'Location Name: {self.name}')
# Represents a rate entity
class Rate:
    def __init__(self,rate_id,name,price_per_km):
        self.rate_id=rate_id
        self.name=name
        self.price_per_km=price_per_km
    # Display rate-specific information.
    def display_info(self):
        print(f'Rate ID: {self.rate_id}')
        print(f'Rate type: {self.name}')
        print(f'Price per km: ${self.price_per_km}')
# Define the Booking class to represent bookings
class Booking:
    def __init__(self,customer,departure,destinations,distances,rate):
        self.customer = customer #Customer object
        self.departure = departure # Departure location
        self.destinations = destinations # destination list
        self.distances = distances # List of distances for each journey
        self.rate = rate # Rate object
    #calculate all the fee
    def compute_cost(self,first_time=False):
        total_distance = sum(self.distances)
        distance_fee = total_distance * self.rate.price_per_km
        discount=self.customer.get_discount(distance_fee,first_time=first_time)
        basic_fee=self.calculate_basic_fee()
        total_cost=basic_fee+distance_fee-discount
        return distance_fee,basic_fee,discount,total_cost
    def calculate_basic_fee(self):
        # Return the fixed base fee
        return 4.2
# Define the Service class to represent the service
class Service:
    def __init__(self, service_id, name, price):
        self.service_id = service_id
        self.name = name
        self.price = price

    def display_info(self):
        print(f'Service ID: {self.service_id}')
        print(f'Service Name: {self.name}')
        print(f'Price: ${self.price:.2f}')
# Define the Package class, which is a subclass of Service and is used to represent service packages
class Package(Service):
    def __init__(self, service_id, name, components):
        super().__init__(service_id, name, 0)# Call the initialization method of the parent class
        self.components = components# List of services included in the service package
        self.calculate_price()
    def calculate_price(self):
        # Calculate the price as 80% of the total price of its components
        self.price = sum(component.price for component in self.components) * 0.8
    def display_info(self):
        super().display_info()# Call the display information method of the parent class
        print("Components:")
        for component in self.components:
            print(f'  - {component.name} (${component.price:.2f})')
# Store and manage customer, location, rate ,service and booking records
class Records:
    def __init__(self):
        self.customers=[]
        self.locations=[]
        self.rates=[]
        self.services = []
        self.bookings=[]
    def read_customers(self,filename):
        #Read customer information from file
        try:
            with open(filename,'r') as file:
                lines = file.readlines()
                for line in lines:
                    # Parse the data in the file
                    data = line.strip().split(',')
                    customer_id = int(data[0])
                    name = data[1].strip()
                    customer_type = data[2].strip()
                    discount_rate = float(data[3])
                    #Create corresponding customer objects based on customer type
                    if customer_type == 'B':
                        customer = BasicCustomer(customer_id, name.strip())
                        BasicCustomer.discount_rate=discount_rate
                    elif customer_type == 'E':
                        threshold = float(data[4])
                        customer = EnterpriseCustomer(customer_id, name.strip(), discount_rate)
                    else:
                        print(f"Unknown customer type: {customer_type}")
                        continue
                    self.customers.append(customer)#Add customer to list
        except FileNotFoundError:
            raise DataFileNotFoundError(filename)
    def read_locations(self, filename):
        # Read location data from the specified file and add it to the locations list
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    location_id, name = line.strip().split(',')
                    location = Location(location_id, name.strip())
                    self.locations.append(location)
        except FileNotFoundError:
            raise DataFileNotFoundError(filename)
    def read_rates(self, filename):
        # Read rate data from the specified file and add it to the rates list
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    rate_id, name, price_per_km = line.strip().split(',')
                    rate = Rate(rate_id, name, float(price_per_km))
                    self.rates.append(rate)
        except FileNotFoundError:
            raise DataFileNotFoundError(filename)
    def read_services(self, filename):
        # Read service and service package information from the file
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                # Read the information of a single service
                for line in lines:
                    # If a line containing 'P' is found, break out of the loop
                    if 'P' in line.split(',')[0]:
                        break
                    service_id, name, price = line.strip().split(',')
                    service = Service(service_id, name.strip(), float(price))
                    self.services.append(service)
                # Read service pack information
                for line in lines[len(self.services):]:
                    data = line.strip().split(',')
                    service_id, name, *component_ids = data
                    components = [self.find_service(id_) for id_ in component_ids]
                    package = Package(service_id, name.strip(), components)
                    self.services.append(package)
        except FileNotFoundError:
            raise DataFileNotFoundError(filename)
    def read_bookings(self, filename="bookings.txt"):
    #Reads booking data from a file and stores it in a list.
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                        # Split each line into separate fields
                        data = line.strip().split(',')
                        # Extract customer information
                        customer_id_or_name = data[0]
                        customer = self.find_customer(customer_id_or_name)
                        # Extract departure location information
                        departure_id_or_name = data[1]
                        departure = self.find_location(departure_id_or_name)
                        # Extract destination and distance data
                        destinations_data = data[2:-6:2]  # Extract every second element starting from index 2
                        distances_data = data[3:-6:2]  # Extract every second element starting from index 3
                        # Convert ID or name to actual objects
                        destinations = [self.find_location(dest_id_or_name) for dest_id_or_name in destinations_data]
                        distances = [float(dist) for dist in distances_data]
                        # Extract rate information
                        rate_id_or_name = data[-6]
                        rate = self.find_rate(rate_id_or_name)
                        # Extract service information
                        service_id_or_name = data[-5]
                        service = self.find_service(service_id_or_name) if service_id_or_name else None
                        # Extract fees and total cost
                        basic_fee = float(data[-4])
                        distance_fee = float(data[-3])
                        discount = float(data[-2])
                        total_cost = float(data[-1])
                        # Store all booking information in a dictionary
                        booking = {"customer": customer,
                                    "departure": departure,
                                    "destinations": destinations,
                                    "distances": distances,
                                    "rate": rate,
                                    "service": service,
                                    "basic_fee": basic_fee,
                                    "distance_fee": distance_fee,
                                    "discount": discount,
                                    "total_cost": total_cost}
                        # Append the booking dictionary to the bookings list
                        self.bookings.append(booking)

        except FileNotFoundError:
             # Raise a custom error if file is not found
            raise DataFileNotFoundError(filename)
    def find_customer(self, search_value):
        # Find a customer by ID or name
        for customer in self.customers:
            if customer.get_name().lower() == search_value.lower() or str(customer.get_customer_id()) == str(search_value):
                return customer
        return None
    def find_location(self, search_value):
        # Find a location by ID or name
        for location in self.locations:
            if location.location_id.strip().lower() == search_value.strip().lower() or location.name.strip().lower() == search_value.strip().lower():
                return location
        return None
    def find_rate(self, search_value):
        # Find a rate by ID or name
        for rate in self.rates:
            if rate.rate_id.strip().lower() == search_value.strip().lower() or rate.name.strip().lower() == search_value.strip().lower():
                return rate
        return None
    def find_service(self, search_value):
        # Find a service by ID or name
        for service in self.services:
            if service.service_id.strip().lower() == search_value.strip().lower() or service.name.strip().lower() == search_value.strip().lower():
                return service
        return None
    def list_customers(self):
        #Display information about all customers.
        for customer in self.customers:
            customer.display_info()
            
    def list_locations(self):
        # Display information about all locations
        for location in self.locations:
            location.display_info()
    def list_rates(self):
        # Display information about all rate types
        for rate in self.rates:
            rate.display_info()
    def list_services(self):
        # Display information about all services
        for service in self.services:
            service.display_info()
#Handle the operation of taxi management system
class Operations:
    #Set paths and recording objects for various files
    def __init__(self,records,customer_file, location_file, rate_file, service_file, booking_file=None):
        self.records=records
        self.customer_file = customer_file
        self.location_file = location_file
        self.rate_file = rate_file
        self.service_file = service_file
        # If the path to the booking file is provided, use it, otherwise default to "bookings.txt"
        self.booking_file = booking_file if booking_file else "bookings.txt"
        self.load_data()
    #load data
    def load_data(self):
        try:
            # Read data from each file
            self.records.read_customers(self.customer_file)
            self.records.read_locations(self.location_file)
            self.records.read_rates(self.rate_file)
            self.records.read_services(self.service_file)
            # If a booking file exists, also read data from it
            if self.booking_file:
                self.records.read_bookings(self.booking_file)
            print("Data loaded successfully.")#Confirm loaded successfully
            self.display_menu()
        # If the file does not exist, catch the error and exit the program
        except FileNotFoundError as e:
            print(e)
            exit(1)
    #Show taxi management system menu
    def display_menu(self):
        while True:# Loop until user chooses to exit
            print("\nTaxi Management System Menu: ")
            print("\n"+"#"*60)
            print("You can choose from the following options:")
            print("1: Book a Trip")
            print("2: Display Existing Customers")
            print("3: Display Existing Locations")
            print("4: Display Existing Rate Types")
            print("5: Display Existing Services")
            print("6: Add New Locations")
            print("7: Adjust Discount Rate for Basic Customers")
            print("8: Adjust Discount Rate for Enterprise Customers")
            print("9: Add/update rate types and prices")
            print("10: Display all bookings")
            print("11: Display the most popular customer")
            print("12: Display a customer booking history")
            print("13: Exit the Program")
            print("#"*60)
            option= input("Choose one option: ")
            if option == "1":
                self.book_trip()
            elif option == "2":
                self.records.list_customers()
            elif option == "3":
                self.records.list_locations()
            elif option == "4":
                self.records.list_rates()
            elif option == "5":
                self.records.list_services()
            elif option == "6":
                self.add_new_locations()
            elif option == "7":
                self.adjust_discount_basic_customers()
            elif option == "8":
                self.adjust_discount_enterprise_customer()
            elif option == "9":
                self.add_update_rate()
            elif option == "10":
                self.display_all_bookings()
            elif option == "11":
                self.display_popular_customer()
            elif option == "12":
                self.display_customer_history()
            elif option == "13":
                self.exit_program()
                break
            else:
                # If the selection is invalid, prompt the user to choose again
                print("Invalid option. Please choose a valid option.")
    def book_trip(self):
        # Get customer information
        while True:
            try:
                customer_input = input("Please Enter customer name or ID: \n").strip()
                customer = self.records.find_customer(customer_input)
                # Verify customer ID
                if customer_input.isdigit():
                    if not customer:
                        raise InvalidNameError("Invalid input. Please enter a valid customer ID.")
                    else:
                        break
                # Verify customer name
                elif customer_input.isalpha():    
                    break        
                else:
                    raise InvalidNameError("Invalid input. Please enter a valid customer name or ID.")
            except InvalidNameError as e:
                    print(e)
        # Get starting point
        while True:
            try:
                departure_input = input("Please Enter departure location (ID or name): \n").strip()
                if self.records.find_location(departure_input):
                    departure_name = self.records.find_location(departure_input).name
                    break
                else:
                    raise InvalidLocationError("Invalid departure location.")
            except InvalidLocationError as e:
                print(e)
        destinations = []
        distances = []
        # Get destination information
        while True:
            try:
                destination_input = input("Please Enter destination location (ID or name): \n").strip()
                if self.records.find_location(destination_input):
                    destination_name = self.records.find_location(destination_input).name
                    if destination_name == departure_name or destination_name in destinations:
                        raise InvalidLocationError("Destination should be different from departure and other destinations.")                  
                    destinations.append(destination_name)
                    # Get the distance between destination and departure point
                    while True:
                        try:
                            distance = float(input("Please Enter the distance(in km): \n"))
                            if distance <= 0:
                                raise InvalidDistanceError("Distance must be a positive number.")
                            distances.append(distance)
                            break
                        except (InvalidDistanceError, ValueError) as e:
                            if isinstance(e, ValueError):
                                print("Please enter a valid number.\n")
                            else:
                                print(e)
                    # The user decides whether to add other destinations
                    another_destination=input("Do you want to add another destination?(y/n): \n")
                    while another_destination.lower() not in ['y','n']:
                        another_destination=input("Invalid input. Do you want to add another destination?(y/n): ")
                    if another_destination.lower() =='n':
                        break
                else:
                    raise InvalidLocationError("Invalid destination location.")
            except InvalidLocationError as e:
                print(e)
        # Get rate type
        while True:
            try:
                rate_input = input("Please Enter rate type (ID or name): \n").strip()
                if self.records.find_rate(rate_input):
                    rate=self.records.find_rate(rate_input)
                    break
                else:
                    raise InvalidRateTypeError(f"Rate type '{rate_input}' not found.")
            except InvalidRateTypeError as e:
                print(e)
        service_fee=0
        selected_service=None
        #Ask if you need additional services or packages
        while True:
            try:
                answer = input("Do you want to order extra service/package? (y/n): \n").lower()
                if answer not in ['y', 'n']:
                    raise InvalidServiceAnswer("Please answer with y or n.")
            
                if answer == 'y':
                    while True:
                        service_input = input("Please enter the name of the service/package you want to order: \n").strip()
                        selected_service = self.records.find_service(service_input)
                        if selected_service:
                            service_fee = selected_service.price
                            break
                        else:
                            print("Invalid service name. Try again.")
                break
            except InvalidServiceAnswer as e:
                print(e)
        
        # Determine whether the customer is an existing customer or a new customer
        customer=self.records.find_customer(customer_input)     
        if customer:
            if isinstance(customer, BasicCustomer):
                print(f"\nWelcome back, {customer.get_name()}! You are a Basic customer.")
            else:
                print(f"\nWelcome back, {customer.get_name()}! You are an Enterprise customer.")
            first_time=False
        else:
            print(f"\nWelcome, {customer_input}! You are a new customer.")
            customer = self.add_new_customer(customer_input)
            first_time=True
        # calculate cost
        booking = Booking(customer, departure_name, destinations, distances, rate)
        distance_fee, basic_fee, discount, total_cost = booking.compute_cost(first_time=first_time)
        total_cost += service_fee
        # Create travel records and add them to the system
        departure_obj = self.records.find_location(departure_name)
        destinations_objs = [self.records.find_location(dest_name) for dest_name in destinations]
        #Create a subscription dictionary
        booking = {"customer": customer if customer else customer_input,
        "departure": departure_obj,
        "destinations": destinations_objs,
        "distances": distances,
        "rate": rate,
        "service": selected_service if selected_service else None,  # Store service or None if no service is selected
        "basic_fee": basic_fee,
        "distance_fee": distance_fee,
        "discount": discount,
        "total_cost": total_cost}

        # Add booking to self.bookings
        self.records.bookings.append(booking)
        # Print booking receipt
        print("Taxi Receipt".center(57))
        print("-"*57)
        print(f'{"Name:":<26}{customer.get_name()}')
        print(f'{"Departure:":<26}{departure_name}')
        for de,di in zip(destinations,distances):
            print(f'{"Destination:":<26}{de}')
            print(f'{"Distance:":<26}{di}{"(km)"}')
        print(f'{"Rate:":<26}{rate.price_per_km:.2f}{"(AUD per km)"}')
        print(f'{"Total Distance:":<26}{sum(distances):.2f}{"(km)"}')
        print("-" * 57)
        print(f'{"Basic fee:":<26}{basic_fee:.2f}{"(AUD)"}')
        print(f'{"Distance fee:":<26}{distance_fee:.2f}{"(AUD)"}')
        print(f'{"Discount:":<26}{discount:.2f}{"(AUD)"}')
        print("-" * 57)
        if selected_service:
            print(f'{"Service:":<26}{selected_service.name}')
            print(f'{"Service Fee:":<26}{service_fee:.2f}{"(AUD)"}')
            print("-" * 57)
        print(f'{"Total cost:":<26}{total_cost:.2f}{"(AUD)"}')
        
    def add_new_customer(self, customer_name):
        max_id = max([int(c.get_customer_id()) for c in self.records.customers], default=0)
        new_customer_id = str(max_id + 1)
        # Create a new basic customer
        new_customer = BasicCustomer(new_customer_id, customer_name)
        # Add the new customer to the records
        self.records.customers.append(new_customer)
        return new_customer
    def add_new_locations(self):
        input_locations=input("Please enter the new locations (comma-separated): \n").split(',')
        new_locations=[location.strip() for location in input_locations]
        existing_location_names = [existing_location.name.lower() for existing_location in self.records.locations]
        existing_location_ids = [existing_location.location_id for existing_location in self.records.locations]
        
        for location in new_locations:
            new_location_id = "L"+ str(len(self.records.locations) + 1)
            # Check if location is already an existing name or ID
            if location.lower() in existing_location_names or location in existing_location_ids:
                print(f"{location.capitalize()} is an existing location, so it will not do anything.\n")
            elif new_location_id in existing_location_ids:
                print(f"{new_location_id} is an existing location ID, so a new ID will be generated.")
                num = len(self.records.locations) + 1
                while "L" + str(num) in existing_location_ids:
                    num += 1
                new_location_id = "L" + str(num)
                new_location_obj = Location(str(new_location_id), location.capitalize())
                self.records.locations.append(new_location_obj)
                print(f"{location.capitalize()} added to the locations with ID {new_location_id} successfully!\n")
            else:    
                # Assuming location IDs are just numeric and incremental
                new_location_obj = Location(str(new_location_id), location.capitalize())
                self.records.locations.append(new_location_obj)
                print(f"{location.capitalize()} added to the locations successfully!\n")

    def adjust_discount_basic_customers(self):
        while True:
            try:
                # Get new discount rate from user
                new_rate = float(input("Enter new discount rate for Basic customers (e.g., 0.1 for 10%): \n"))
                #Validate the discount rate
                if 0 < new_rate < 1:
                    # Set the new discount rate
                    BasicCustomer.set_discount_rate(new_rate)
                    print(f"Updated discount rate to {new_rate * 100}% for Basic customers.\n")
                    break
                else:
                    raise InvalidRateError("Invalid rate. Please enter a value between 0 and 1.")
            except (InvalidRateError, ValueError) as e:
                # Need to enter a number
                if isinstance(e, ValueError):
                    print("Please enter a valid number.\n")
                else:
                    print(e)

    def adjust_discount_enterprise_customer(self):
        while True:
            customer_input = input("Enter Enterprise customer name or ID: \n")
            customer = self.records.find_customer(customer_input)
            try:
                # Check if the entered customer is an Enterprise customer
                if customer and isinstance(customer, EnterpriseCustomer):
                    while True:
                        try:
                            # Get new discount rate from user
                            new_rate1 = float(input("Enter new first discount rate for the Enterprise customer (e.g., 0.2 for 20%): \n"))
                            if 0 < new_rate1 < 1:
                                # Set the new discount rate for the customer
                                customer.set_discount_rates(new_rate1)
                                print(f"Updated first discount rate to {new_rate1 * 100}% for {customer.get_name()}.\n")
                                break
                            else:
                                raise ValueError("Invalid rate. Please enter a value between 0 and 1.")
                        except ValueError as e:
                            # Need to enter a number
                            if isinstance(e, ValueError):
                                print("Please enter a valid number.\n")
                    break
                else:
                    raise NotEnterpriseCustomerError("Invalid customer or the customer is not an Enterprise customer. Please try again.")
            except NotEnterpriseCustomerError as e:
                print(e)
    def add_update_rate(self):
        while True:
            print("Do you want to add new or update existing rate types\n")
            # Get rate types and prices from user
            rate_types_input = input("Please enter rate types separated by commas (e.g., metropolitan, deluxe, premium): \n").strip()
            rate_types = [rate.strip().lower() for rate in rate_types_input.split(",")]

            prices_input = input("Please enter prices for the rate types separated by commas (e.g., 2.0, 2.5, 2.2): \n").strip()
            try:
                prices = [float(price.strip()) for price in prices_input.split(",")]
                # Validate number of rates matches number of prices
                if len(rate_types) != len(prices):
                    raise InvalidRateListError("Number of rate types doesn't match the number of prices.")
                # Validate positive prices
                for price in prices:
                    if price <= 0:
                        raise InvalidRateError("Price should be a positive value.")

            except (ValueError, InvalidRateListError, InvalidRateError) as e:
                if isinstance(e, ValueError):
                    print("Please enter a valid number.")
                else:
                    print(e)
                continue
            # Process each entered rate type
            for rate_type, price in zip(rate_types, prices):
                existing_rate = self.records.find_rate(rate_type)

                if existing_rate:
                    # Update the existing rate
                    existing_rate.price_per_km = price
                    print(f"Rate {existing_rate.name} updated successfully to {price} AUD per km.\n")
                else:
                    # Add a new rate
                    new_rate_id = "R"+str(len(self.records.rates) + 1)  # Assuming rate IDs are incremental numbers
                    new_rate = Rate(new_rate_id, rate_type, price)
                    self.records.rates.append(new_rate)
                    print(f"New rate {rate_type} added successfully at {price} AUD per km.\n")
            break
        
    def display_all_bookings(self):
        # Check if there are no bookings
        if not self.records.bookings:
            print("No bookings have been made.")
            return
        #Display a header for the bookings and all detailed information
        print("\nAll Bookings:\n" + "-" * 40)
        for idx, booking in enumerate(self.records.bookings, start=1):
            print(f"Booking {idx}:".center(40, '-'))
            print(f"Customer: {booking['customer'].get_name()}")
            
            # Convert Location object to its name
            print(f"Departure: {booking['departure'].name}")
            
            # Convert list of Location objects to their names
            destinations_names = [destination.name for destination in booking['destinations']]
            print(f"Destinations: {', '.join(destinations_names)}")
            
            print(f"Distances: {', '.join(map(str, booking['distances']))} (km)")
            print(f"Rate: {booking['rate'].name} ({booking['rate'].price_per_km} AUD per km)")
            if booking.get('service'):
                print(f"Service: {booking['service'].name} ({booking['service'].price} AUD)")
            print(f"Basic fee: {booking['basic_fee']:.2f} (AUD)")
            print(f"Distance fee: {booking['distance_fee']:.2f} (AUD)")
            print(f"Discount: {booking['discount']:.2f} (AUD)")
            print(f"Total cost: {booking['total_cost']:.2f} (AUD)")
    
    def display_popular_customer(self):
        # A dictionary to store the total money spent by each customer
        customer_spending = {}

        # Traverse through the bookings to populate the dictionary
        for booking in self.records.bookings:
            customer_name = booking['customer'].get_name()
            # Ensure the 'total_cost' key exists and is of type float
            total_cost = float(booking.get('total_cost', 0))
            customer_spending[customer_name] = customer_spending.get(customer_name, 0) + total_cost

        # Find the customer who has spent the most
        if not customer_spending:
            print("No bookings have been made yet.")
            return
        # Identify the customer who has spent the most
        popular_customer_name = max(customer_spending, key=customer_spending.get)
        popular_customer_spending = customer_spending[popular_customer_name]

        print(f"The customer who has spent the most is: {popular_customer_name}")
        print(f"Total amount spent: ${popular_customer_spending:.2f}")

    def display_customer_history(self):
        while True:
            try:
                customer_input = input("Enter the customer name or ID to see booking history: \n").strip()
                customer = self.records.find_customer(customer_input)
                # Validate the customer input
                if customer_input.isdigit():
                    if not customer:
                        raise InvalidNameError("Invalid input. Please enter a valid customer ID.")
                    else:
                        break
                elif customer_input.isalpha():    
                    break        
                else:
                    raise InvalidNameError("Invalid input. Please enter a valid customer name or ID.")
            except InvalidNameError as e:
                print(e)

        # If customer is not found
        if not customer:
            print(f"No customer found with the name or ID: {customer_input}")
            return

        # Display customer booking history
        print(f'{"This is the booking history of "}{customer.name}{"."}')

        booking_count=0
        bookings_data = []
        # Gather booking details for the selected customer
        for booking in self.records.bookings:
            if booking["customer"] == customer:
                booking_count += 1
                booking_info = {}
                booking_info["Departure"] = booking['departure'].name
                booking_info["Destination"] = ', '.join([dest.name for dest in booking['destinations']])
                booking_info["Service"] = booking['service'].name if ('service' in booking and booking['service'] is not None) else 'N/A'
                booking_info["Total cost"] = "{:.2f}".format(booking['total_cost'])
                bookings_data.append(booking_info)

        # Prepare the header
        header = ["", *["Booking {}".format(i + 1) for i in range(booking_count)]]
        print("{:<0}".format("") + "".join("{:<20}".format(item) for item in header))

        # Prepare the rows for each info title
        info_titles = ["Departure", "Destination", "Service", "Total cost"]
        for title in info_titles:
            if title == "Service" and all([booking["Service"] == 'N/A' for booking in bookings_data]):
                continue
            row = [title]
            for booking in bookings_data:
                row.append(booking[title])
            print("".join("{:<20}".format(item) for item in row))

        if booking_count == 0:
            print("No bookings found for this customer.")
    # Save data and exit the program
    def exit_program(self):
        self.save_customers_to_file("customers.txt")
        self.save_locations_to_file("locations.txt")
        self.save_rates_to_file("rates.txt")
        self.save_bookings_to_file("bookings.txt")
        print("Data saved successfully. Exiting the program.")
        exit(0) # Exit the program
        
    def save_customers_to_file(self, filename):
        with open(filename, 'w') as file:
            for customer in self.records.customers:
                # Differentiate between customers with and without threshold attribute
                if hasattr(customer,"threshold"):
                    line = f"{customer.customer_id},{customer.name},{customer.type},{customer.discount_rate1},{customer.threshold}"
                else:
                    line = f"{customer.customer_id},{customer.name},{customer.type},{customer.discount_rate}"
                file.write(line + "\n")

    def save_locations_to_file(self, filename):
        with open(filename, 'w') as file:
            for location in self.records.locations:
                line = f"{location.location_id},{location.name}"
                file.write(line + "\n")
    def save_rates_to_file(self, filename):
        with open(filename, 'w') as file:
            for rate in self.records.rates:
                line = f"{rate.rate_id},{rate.name},{rate.price_per_km}"
                file.write(line + "\n")
    def save_bookings_to_file(self, filename):
        with open(filename, 'w') as file:
            for booking in self.records.bookings:
                dest_and_distances = []
                for dest, distance in zip(booking['destinations'], booking['distances']):
                    dest_and_distances.append(dest.name)
                    dest_and_distances.append(str(distance))
                dest_and_distances_str = ','.join(dest_and_distances)

                service_str = booking['service'].name if 'service' in booking and booking['service'] else ""

                line = f"{booking['customer'].name},{booking['departure'].name},{dest_and_distances_str},{booking['rate'].name},{service_str},{booking['basic_fee']},{booking['distance_fee']},{booking['discount']},{booking['total_cost']}"
                file.write(line + "\n")



                
import sys

if __name__ == "__main__":
    if 2 <= len(sys.argv) <= 6:
        ops = Operations(Records(), *sys.argv[1:])
    elif len(sys.argv) == 1:
        ops = Operations(Records(), "customers.txt", "locations.txt", "rates.txt", "services.txt")
    else:
        print("Usage: program_name customer_file location_file rate_file service_file [booking_file]")
        sys.exit(1)
##references
##[1]“python - How do I terminate a script?,” Stack Overflow. https://stackoverflow.com/questions/73663/how-do-i-terminate-a-script
##[2]“How to use sys.argv in Python,” GeeksforGeeks, Dec. 16, 2019. https://www.geeksforgeeks.org/how-to-use-sys-argv-in-python/
##                




