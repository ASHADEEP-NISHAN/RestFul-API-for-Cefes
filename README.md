# RestFul API for Cafes
Here i create a RESTFUL API for different cafe data with the help of Pyhthon Flask and POSTMAN API platform.

#Key Features
Here are the key features of the cafe API you have developed:

### 1. **Random Cafe Retrieval (`/random`)**:
   - **Description**: Returns a random cafe from the database.
   - **Response Format**: JSON with details about the cafe such as name, location, seating capacity, amenities (Wi-Fi, sockets, etc.), and coffee price.

### 2. **List All Cafes (`/all`)**:
   - **Description**: Fetches and returns a list of all cafes in the database.
   - **Response Format**: JSON array containing cafe details for each cafe in the database.

### 3. **Search Cafe by Location (`/search`)**:
   - **Description**: Allows users to search for cafes based on a specific location passed as a query parameter (`loc`).
   - **Response Format**: JSON array of cafes in the specified location. If no cafe is found, an error message is returned with a `404` status code.

### 4. **Add a New Cafe (`/add`, POST)**:
   - **Description**: Enables adding a new cafe to the database via form data.
   - **Required Parameters**: Name, map URL, image URL, location, availability of sockets, Wi-Fi, toilets, whether calls can be taken, seating capacity, and coffee price.
   - **Response Format**: A success message in JSON format once the new cafe is added.

### 5. **Update Cafe's Coffee Price (`/update-price/<int:cafe_id>`, PATCH)**:
   - **Description**: Updates the coffee price of a cafe by its unique ID. The new price is passed as a query parameter (`new_price`).
   - **Response Format**: A success message in JSON format if the update is successful; otherwise, an error message if the cafe ID is not found.

### 6. **Delete Cafe (`/report-closed/<cafe_id>`, DELETE)**:
   - **Description**: Allows for the deletion of a cafe from the database by its ID, only if the correct API key (`api_key`) is provided.
   - **Security**: The `DELETE` request is protected by an API key to prevent unauthorized deletions.
   - **Response Format**: A success message if the cafe is deleted, or an error message if the cafe is not found or the API key is incorrect.

### 7. **Error Handling**:
   - For both the search and delete operations, if no matching cafe is found, the API returns a `404` error with an appropriate error message.
   - In case of unauthorized access for deletion, a `403` error is returned.

This API is designed for basic CRUD operations on cafes, allowing users to interact with the database to add, search, update, and delete cafe entries efficiently.
