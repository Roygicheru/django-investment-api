**Investment Account API**
This project is a Django Rest Framework (DRF) API for managing investment accounts. It allows multiple users to belong to an investment account and enables users to have different levels of access to each account.


**Features**
User Permissions: Users can have multiple investment accounts with different access levels (view, crud, post).

Investment Account Management: Users can create, retrieve, update, and delete investment accounts based on their permissions.

Transaction Management: Users can view and create transactions for investment accounts they have access to.

Admin Endpoint: An admin endpoint is available to retrieve all transactions for a specific user, along with the total balance and date range filtering.




**Implementation Steps**

Set up the Django project and installed the necessary dependencies, including Django Rest Framework.

Created the InvestmentAccount, InvestmentAccountUser, and Transaction models to represent the database structure for investment accounts, user-account associations, and transactions.

Defined the serializers (InvestmentAccountSerializer and TransactionSerializer) to serialize and deserialize the model instances for API communication.

Implemented the views and viewsets (InvestmentAccountViewSet, TransactionViewSet, and UserTransactionsView) to handle API endpoints for investment accounts, transactions, and user-specific transactions.

Created custom permission classes (InvestmentAccountPermission) to handle user permissions for different access levels to investment accounts.

Defined the URL patterns in the urls.py file to map the API endpoints to the corresponding views and viewsets.

Set up token-based authentication using Django Rest Framework's built-in token authentication system.

Customized the Django admin interface to manage investment accounts, user-account associations, and transactions through the admin panel.

Wrote unit tests to validate the functionality of the API endpoints and ensure proper handling of user permissions and access levels.

Set up a GitHub Actions workflow to automatically run the unit tests on each push or pull request to the main branch.

Provided detailed instructions on how to test the API functionality using tools like cURL, Postman, or the Django Rest Framework's browsable API interface.




**Getting Started**

Clone the repository and navigate to the project directory.

Install the project dependencies using pip install -r requirements.txt.

Apply the database migrations using python manage.py migrate.

Create a superuser account using python manage.py createsuperuser.

Start the development server using python manage.py runserver.

Access the API endpoints using the provided URLs and authentication tokens.



**Testing**
This Django application has been rigorously tested using Django's built-in testing framework and Django REST Framework's APITestCase. The test suite covers various aspects of the application, focusing on user permissions, transaction creation, and data retrieval.

Key Test Areas:

User Permissions:

Tests for different permission levels (view, post, crud) on investment accounts.
Ensures users can only perform actions they're authorized for.


Transaction Operations:

Creating transactions with different user permissions.
Retrieving transactions for specific investment accounts.
Verifying correct handling of unauthorized transaction creation attempts.


Admin Functionality:

Testing the admin-only endpoint for retrieving user transactions.
Verifying date range filtering for transaction queries.


API Endpoints:

Comprehensive testing of GET, POST, and other relevant HTTP methods.
Verification of correct response status codes and data structures.


Data Integrity:

Ensuring created transactions are correctly associated with investment accounts.
Verifying accurate calculation of total balances.

To run the unit tests, use the following command:
 manage.py test api.tests
The tests cover various scenarios, including creating and retrieving transactions, testing user permissions, and verifying the admin endpoint functionality.
