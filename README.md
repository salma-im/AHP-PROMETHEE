# AHP-PROMETHEE Project

This project combines the Analytic Hierarchy Process (AHP) and PROMETHEE methods for multi-criteria decision analysis. It is implemented using Python with Flask for the backend and MySQL for data storage.

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

\\\`
ahp-promethee-project/
├── app.py
├── README.md
├── .idea/
├── static/
│   ├── images/
│   ├── script.js
│   ├── style.css
│   ├── style1.css
├── templates/
│   ├── auth/
│   ├── home/
│   ├── project/
│   ├── step1.html
│   ├── step2.html
│   ├── step3.html
│   ├── step4.html
│   ├── step5.html
│   ├── ...
├── analysis/
│   ├── ahp/
│   ├── promethee/
│   ├── ...
├── database/
│   ├── schema.sql
│   ├── ...
├── tests/
│   ├── ...
└── requirements.txt
\\\`

## Installation

### Prerequisites

- Python 3.x
- MySQL

### Steps

1. *Clone the repository:*

   \\\`bash
   git clone https://github.com/yourusername/ahp-promethee-project.git
   cd ahp-promethee-project
   \\\`

2. *Create a virtual environment and activate it:*

   \\\`bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use \venv\\Scripts\\activate\
   \\\`

3. *Install the required dependencies:*

   \\\`bash
   pip install -r requirements.txt
   \\\`

4. *Set up the database:*

   - Create a MySQL database and import the schema:

     \\\`sql
     CREATE DATABASE ahp_promethee;
     USE ahp_promethee;
     SOURCE database/schema.sql;
     \\\`

   - Update the database configuration in \app.py\ or a separate configuration file.

5. *Run the application:*

   \\\`bash
   flask run
   \\\`

## Usage

1. Open your web browser and navigate to \http://127.0.0.1:5000/\.
2. Register a new user or log in with an existing account.
3. Follow the steps to perform AHP and PROMETHEE analysis.

## Features

- *User Authentication:* Register, login, and manage user profiles.
- *AHP Analysis:* Create and manage criteria and alternatives, perform pairwise comparisons.
- *PROMETHEE Analysis:* Evaluate alternatives using the PROMETHEE method.
- *Visualization:* View results with charts and graphs.
- *Responsive Design:* Accessible on various devices.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch: \git checkout -b feature-name\.
3. Make your changes and commit them: \git commit -m 'Add some feature'\.
4. Push to the branch: \git push origin feature-name\.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
