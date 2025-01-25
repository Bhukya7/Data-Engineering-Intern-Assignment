## Overview
The Log Analyzer Tool is a command-line application that processes server log files. It extracts key information from logs, filters them based on user-defined criteria, and generates a summary report in CSV format. The tool also integrates with MongoDB and provides a REST API for accessing log data.

## Features
- *Command-Line Interface*: Analyze logs using various command-line arguments.
- *Log Parsing*: Extracts timestamp, log level, user ID, and message from log entries.
- *Filtering*: Filter logs by severity level and timestamps.
- *Summarization*: Generate summaries including time duration, log counts by category, and the most active user.
- *Database Integration*: Insert parsed logs into a MongoDB collection.
- *REST API*: Fetch logs via a FastAPI-based REST API.
- *User Interface*: A simple UI built with Streamlit to interact with the API.

## Activate the virtual environment:
- *Windows*:
  
  myenv\Scripts\activate
  
- *macOS/Linux*:
  
  source myenv/bin/activate
  

## Install the required packages:
## Usage

### Running the Command-Line Tool

To analyze logs using the command-line tool, run:
### Starting the REST API

To start the FastAPI application, run:

### Running the Streamlit UI

To run the Streamlit user interface, execute:

## MongoDB Integration

Make sure to set your MongoDB connection URI in api.py. Replace 'your_mongodb_uri' with your actual MongoDB connection string.

## Deployment

For deployment instructions, consider using platforms like Heroku or Vercel. Follow their documentation for deploying Python applications.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by various open-source projects and tutorials on Python logging and data processing.

Conclusion
This README.md file provides a comprehensive overview of your Log Analyzer project, including installation instructions, usage examples, and feature descriptions. It will help users understand how to set up and use your tool effectively
