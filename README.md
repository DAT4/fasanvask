# APP for a small commutity to organize and book laundry times.

## The Backend
The backend is build in python with the framework Django, here the models are created
### The resident model
This model is inherited from the default UserModel in Django, and changed so that the PrimaryKey and the username is the RoomNumber of the resident. 
FirstName and LastName is also added to the model, and username and email is removed. Now the ResidentModel can be used for logging in to the system.
### The WashTime model
This model is very simple but also very central, it has the attributes:
* start_date
* end_date
* resident

Start and end dates are of the type datetime and __TODO:__ should be handled in blocks of one hour where the blocks are unique, so that multiple residents won't overlap their wash_times. 

#### Resident 
this attribute is a foreign key for the washtime, and when a resident is deleted then all the washTimes for that resident will be deleted as well. 
