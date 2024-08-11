# Redefine Reckoner

Welcome to the **Redefine Reckoner** project! This Streamlit application allows users to filter and view feature availability across different checkout types and verticals.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Contributing](#contributing)
  - [Forking the Repository](#forking-the-repository)
  - [Setting Up Your Development Environment](#setting-up-your-development-environment)
  - [Making Changes](#making-changes)
  - [Submitting a Pull Request](#submitting-a-pull-request)
- [License](#license)

## Introduction

**Redefine Reckoner** is a user-friendly application built with Streamlit that helps users explore and analyze feature availability across different checkout types and verticals. Users can filter data based on checkout type, vertical name, and methods of choice, and view the filtered data with an interactive data editor.

## Features

- **Dynamic Filtering**: Filter data based on checkout type, vertical name, and payment methods.
- **Interactive Data Editor**: View and edit the filtered data with color-coded implementation statuses.
- **Persistent Changes**: Save changes made to the data for future reference.
- **Seamless Navigation**: Switch between different sections of the app with ease.

## Getting Started

Follow these instructions to set up the project on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following software installed on your system:

- **Python 3.7+**: You can download it from [python.org](https://www.python.org/downloads/).
- **Git**: You can download it from [git-scm.com](https://git-scm.com/downloads).

### Installation

1. **Clone the Repository**

   First, clone the repository to your local machine using the following command:

   ```bash
   git clone https://github.com/<yourusername>/redefine-reckoner.git
   ```

   Replace `yourusername` with your GitHub username if you've forked the repository.

2. **Navigate to the Project Directory**

   ```bash
   cd redefine-reckoner
   ```

3. **Create and Activate a Virtual Environment**

   ```bash
   python3 -m venv prodEnv
   ```

   - Activate the Virtual Enviornment

     - Windows
       ```bash
       venv\Scripts\activate
       ```
     - MacOS / Linux
       ```bash
       source venv/bin/activate
       ```

4. **Install Dependencies**

   With the virtual environment activated, install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Streamlit App**

  Run the following command to configure a SQLite Database and create a table named `features` for the application to pull data from:

   ```bin
   python3 populate_db.py
   ```

   Run the following command to start the Streamlit application:

   ```bin
   streamlit run app.py
   ```

2. **Open Your Web Browser**

   Open your web browser and navigate to `http://localhost:8501` to view the application.

## Contributing

Contributions are welcome! Follow the steps below to contribute to this project.

### Forking the Repository

1. **Fork the Repository**

   Go to the GitHub repository page and click the Fork button to create a personal copy of the repository on your GitHub account.

2. **Clone Your Forked Repository**

   Clone your forked repository to your local machine:

   ```bash
   git clone https://github.com/<yourusername>/redefine-reckoner.git
   ```

   Replace `yourusername` with your GitHub username.

### Setting Up Your Development Environment

1. **Navigate to the Project Directory**

   ```bash
   cd redefine-reckoner
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python3 -m venv venv
   ```

   - Activate the Virtual Enviornment
     - Windows
       ```bash
       venv\Scripts\activate
       ```
     - MacOS / Linux
       ```bash
       source venv/bin/activate
       ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Making Changes

1. **Create a New Branch**

   Before making changes, create a new branch to isolate your work:

   ```bash
   git checkout -b feature/your-feature-name
   ```

   Replace `your-feature-name` with a descriptive name for your feature or bug fix.

2. **Make your Changes**

   Open your text editor or IDE and make the necessary changes to the codebase.

3. **Test Your Changes**

   Ensure that your changes work as expected by running the application and testing your modifications.

### Submitting a Pull Request

1. **Commit Your Changes**

   Add and commit your changes with a descriptive commit message:

   ```bash
   git add .
   git commit -m "Add a descriptive commit message"
   ```

2. **Push Your Changes to Your Forked Repository**

   Push your changes to your forked repository on GitHub:

   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**

   Go to the original repository on GitHub and click the **_Compare & pull request_** button to submit your changes for review.
