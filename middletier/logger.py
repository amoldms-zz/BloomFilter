

# Debug logging method
# ToDo: Enable logging to specified destination as console, text file, database, or telemetry system.
def log(string, destination='console'):
    if destination == 'console':
        print(string)