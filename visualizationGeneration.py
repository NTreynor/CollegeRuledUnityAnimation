import csv
import matplotlib.pyplot as plt
import numpy as np

def display_dot_plot_from_csv(csv_filename):
    data = []

    # Read the data from the CSV file
    with open(csv_filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append([int(value) for value in row])

    if not data:
        print("The CSV file is empty or does not contain valid data.")
        return

    # Create a dot plot
    plt.figure(figsize=(10, 5))  # Adjust the figure size as needed
    plt.plot(np.arange(len(data[0])), data[0], 'bo', label='Data')  # Plot the first line of data as blue dots

    # Customize the plot if needed (e.g., set labels, titles, etc.)
    plt.xlabel('Data Point Index')
    plt.ylabel('Values')
    plt.title('Dot Plot of Data')

    # Show the plot
    plt.legend()
    plt.grid()
    plt.show()

# Specify the CSV file containing lines of 15 integers
csv_filename = 'dramaValues.csv'

# Call the function to display the dot plot
display_dot_plot_from_csv(csv_filename)

def showcase_means_from_csv(csv_filename):
    x_values = []
    y_values = []

    # Read the data from the CSV file
    with open(csv_filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) == 2:
                x, y = map(float, row)
                x_values.append(x)
                y_values.append(y)

    if not x_values or not y_values:
        print("The CSV file is empty or does not contain valid data.")
        return

    # Calculate the mean of the y-values
    y_mean = sum(y_values) / len(y_values)

    # Create a bar chart to showcase the mean
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.bar(x_values, y_values, label='Y Values', alpha=0.6)
    plt.axhline(y=y_mean, color='red', linestyle='--', label=f'Mean Y Value: {y_mean:.2f}')

    # Customize the plot
    plt.xlabel('X Values')
    plt.ylabel('Y Values')
    plt.title('Means of Y Values')
    plt.legend()

    # Show the plot
    plt.grid()
    plt.show()

# Specify the CSV file containing X and Y values
csv_filename = 'alpha+visitedStatesCorrectedSimple.csv'

# Call the function to showcase the means
showcase_means_from_csv(csv_filename)




