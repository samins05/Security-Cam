# Security-Cam
Security camera that uses grayscale images and haar cascade and LBF classifiers to detect if person on the camera that is detected is in the database. This program uses a local database and user must run MYSQL and Apache on XAMPP Host to run the program successfully
- User will add people they know to a database and train the program by taking pictures of whoever they want to add
- Anyone that appears on the camera that isn't in the database will be flagged UNKNOWN. **This will then send an alert to the program for the user to be notified(this will be added soon)**
