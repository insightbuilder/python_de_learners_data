
# Python code to split a text file into a list of tasks

# Read the contents of the file
with open('file.txt', 'r') as file:
    file_contents = file.read()

# Split the file contents into a list of tasks
tasks_list = file_contents.split('\n')

# Print the list of tasks
print(tasks_list)
