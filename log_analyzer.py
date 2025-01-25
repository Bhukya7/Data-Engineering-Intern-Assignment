import argparse
import pandas as pd
from datetime import datetime
from pymongo import MongoClient

def parse_log_line(line):
    """Parses a single log line and extracts relevant information."""
    try:
        parts = line.split(' ', 3)
        timestamp = parts[0] + ' ' + parts[1]
        log_level = parts[2]
        user_id = parts[3].split(' ')[0].split(':')[1]
        message = parts[3][len('UserID:' + user_id) + 1:]
        return timestamp, log_level, user_id, message
    except IndexError:
        print(f"Skipping malformed log line: {line}")
        return None  # Handle malformed lines gracefully

def filter_logs(logs, level=None, start_time=None, end_time=None):
    """Filters logs based on specified criteria."""
    filtered_logs = []
    for log in logs:
        if log is None:  # Skip malformed lines
            continue

        timestamp = datetime.strptime(log[0], '%Y-%m-%d %H:%M:%S')
        if level and log[1] != level:
            continue
        if start_time and timestamp < start_time:
            continue
        if end_time and timestamp > end_time:
            continue
        filtered_logs.append(log)
    return filtered_logs

def summarize_logs(logs):
    """Summarizes logs by time duration, log categories, and most active user."""
    if not logs:  # Handle empty logs
        return {"Time Duration": "N/A", "Logs by Category": {}, "Most Active User": "N/A"}
    
    start_time = logs[0][0]
    end_time = logs[-1][0]
    levels_count = {'INFO': 0, 'ERROR': 0, 'WARN': 0}
    user_activity = {}

    for log in logs:
        levels_count[log[1]] += 1
        user_activity[log[2]] = user_activity.get(log[2], 0) + 1

    most_active_user = max(user_activity, key=user_activity.get) if user_activity else "N/A" 
    
    summary = {
        "Time Duration": f"{start_time} - {end_time}",
        "Logs by Category": levels_count,
        "Most Active User": most_active_user
    }
    return summary

def insert_to_mongodb(logs, db_uri="mongodb://localhost:27017/"):
    """Inserts log data into MongoDB."""
    client = MongoClient(db_uri)
    db = client['log_database']
    collection = db['logs']
    
    # Convert timestamp to datetime object for MongoDB
    for log in logs:
        log_dict = {
            'timestamp': datetime.strptime(log[0], '%Y-%m-%d %H:%M:%S'), 
            'log_level': log[1],
            'user_id': log[2],
            'message': log[3]
        }
        collection.insert_one(log_dict)
    
    print(f"Inserted {len(logs)} logs into MongoDB.")
    client.close()

def main():
    parser = argparse.ArgumentParser(description='Log Analyzer Tool')
    parser.add_argument('--logfile', required=True, help='Path to the input log file.')
    parser.add_argument('--output', required=True, help='Path to save the generated CSV report.')
    parser.add_argument('--level', choices=['INFO', 'ERROR', 'WARN'], 
                        help='Filter logs by severity level.')
    parser.add_argument('--st_time', help='Start timestamp to filter logs (YYYY-MM-DD HH:mm:ss).')
    parser.add_argument('--end_time', help='End timestamp to filter logs (YYYY-MM-DD HH:mm:ss).')
    parser.add_argument('--summarize', action='store_true', 
                        help='Summarizes the logs and print output to console.')
    parser.add_argument('--mongodb_uri', help='MongoDB connection URI (optional).')

    args = parser.parse_args()

    try:
        with open(args.logfile, 'r') as file:
            logs = [parse_log_line(line.strip()) for line in file.readlines()]

        start_time = datetime.strptime(args.st_time, '%Y-%m-%d %H:%M:%S') if args.st_time else None
        end_time = datetime.strptime(args.end_time, '%Y-%m-%d %H:%M:%S') if args.end_time else None
        
        filtered_logs = filter_logs(logs, args.level, start_time, end_time)

        df = pd.DataFrame(filtered_logs, columns=['Timestamp', 'Log Level', 'UserID', 'Message'])
        df.to_csv(args.output, index=False)

        if args.summarize:
            summary = summarize_logs(filtered_logs)
            print("Summary:")
            for key, value in summary.items():
                print(f"{key}: {value}")

        # Insert into MongoDB if --mongodb_uri is provided
        if args.mongodb_uri:
            insert_to_mongodb(filtered_logs, args.mongodb_uri)
        else:
            # Use default URI if not provided
            insert_to_mongodb(filtered_logs) 

    except FileNotFoundError:
        print(f"Error: Log file not found at path: {args.logfile}")
    except ValueError:
        print("Error: Invalid date/time format. Please use YYYY-MM-DD HH:mm:ss.")
    except Exception as e:
        print(f"Error inserting into MongoDB: {e}")

if __name__ == "__main__":
    import sys
    log_file_path = 'C:\Users\hp\OneDrive\Desktop\Data Engineer Project\server_logs.txt'  
    sys.argv = ['script_name.py', '--logfile', log_file_path, '--output', 'output.csv', '--mongodb_uri', 'your_mongodb_uri']  
    main()
