# PulsePoint

PulsePoint is a web application built with Django for blood donation management. It allows individuals to track their blood donations, schedule future donations, and volunteer at accredited facilities.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [Docker](https://www.docker.com/) installed on your machine.

### Installing

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/pulsepoint.git
    ```

2. Navigate to the project directory:

    ```bash
    cd pulsepoint
    ```

3. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

4. Access the application at [http://localhost:8000/](http://localhost:8000/).

## Project Structure

The project follows a standard Django structure, with additional features for blood donation management.

- `accounts`: Contains user authentication and role-related functionality.
- `pulsepoint`: Django project settings and configuration.
- `Extras`: Additional documentation and notes.

## Configuration

- The PostgreSQL database is configured in the `docker-compose.yml` file.
- Django settings can be adjusted in the `pulsepoint/settings.py` file.
- Other configurations can be found in various files throughout the project.

## Contributing

If you'd like to contribute to PulsePoint, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make your changes and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thank you to the Django and Docker communities for providing excellent tools for web development and containerization.
- Special thanks to [contributors](https://github.com/yourusername/pulsepoint/graphs/contributors) who have participated in this project.

