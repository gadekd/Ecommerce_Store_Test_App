# Ecommerce_Store_Test_App
This project is created to simulate simple ecommerce website. The main focus of this project is to create some kind of item creator for users to enable persolnalizing orders.

<h1>How to install the project</h1>
<ol type="1">
    <li>Select the code editor of your choice (I use Visual Studio Code)</li>
    <li>Copy the repository to your new catalogue - use `git clone link_to_repository` command</li>
    <li>Create virtual environment - use `python -m venv .` command (after `.` you can enter name of your venv; leave empty for default name)</li>
    <li>Ensure that you are on the master branch</li>
    <li>Install required dependencies (Django)</li>
    <li>Make migrations using `python manage.py makemigrations` and `python manage.py migrate` commands</li>
    <li>Change branch to the new one</li>
</ol>

<h1>Structure of the application</h1>

Due to some erros during creating structure of this application, it is recommended to create virtual environment within the <strong>django_ecom_app</strong> catalogue and running the server within the next catalogue - <strong>app_ecommerce</strong>.

<h1>How to open the project in web browser</h1>

After creation of virtual environment, accessing it and installing all necessary packages, you are ready to run server and start working with the Simple Shop™.

To run server, you have to be in the right catalogue. You have to get to the `app_ecommerce` catalogue, so that your path would look like this:

*\<path_to_your_main_catalogue>\Ecommerce_Store_Test\django_ecom_app\app_ecommerce*

Finally you can apply django command to run the server, which is `python manage.py runserver`. And *BOOM!* you are now at the main page of the Simple Shop™.
