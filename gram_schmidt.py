import numpy as np

# Function to read vectors from a file (.txt format)

def read_vectors_from_file(file_path):
    vectors = []  # An empty list is initialised to store the vectors from the file  
    try: 
        # Reading code from the file, read after with allows file to close after 
        with open(file_path, "r") as file: 
            for line in file:
                # Check if the line is not empty 
                if line.strip():
                    # Convert the line into a list of floats
                    try:
                        vectors.append([float(component) for component in line.strip().split(',') if component.strip()])
                    except ValueError:
                        # Print a warning if some components can't be converted to numbers
                        print(f"Warning: Couldn't convert the line to numbers -> {line.strip()}")
                else:
                    # Skip empty lines
                    print("Found an empty line, skipping it.")
        return np.array(vectors)  # Return the list of vectors as a NumPy array
    except FileNotFoundError:
        # Handle the case where the file does not exist
        print("Error: The file was not found. Please check the file path.")
        return np.array([])  # Return an empty array if the file was not found
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return np.array([])  # Return an empty array in case of unexpected errors

 # Function to perform Gaussian elimination 

def perform_gaussian_elimination(matrix):
    # Determine the matrix dimensions.
    num_rows, num_cols = matrix.shape 

    # Gaussian elimination process.
    for matrix_row in range(num_rows):
        pivot_found = False  # Initial assumption: no pivot found

        # Search for pivot in the current row
        for pivot_column in range(matrix_row, num_cols):
            if matrix[matrix_row, pivot_column] != 0:
                pivot_found = True  # Pivot located
                # Normalise the pivot row by dividing it by the pivot value
                matrix[matrix_row] /= matrix[matrix_row, pivot_column] 
                # Eliminate values below the pivot
                for row_below_pivot in range(matrix_row + 1, num_rows):
                    matrix[row_below_pivot] -= matrix[row_below_pivot, pivot_column] * matrix[matrix_row] 
                break  # Move to the next row after processing the first pivot.

        if not pivot_found:
            return False  # Linear dependence detected.

    return True  # Matrix is in reduced echelon form; vectors are independent.

def check_linear_independence(vectors):
    # Perform Gaussian elimination on a copy to preserve original vectors.
    if perform_gaussian_elimination(vectors.copy()):
        print("The set of vectors is Linearly Independent.")
        return True
    else:
        print("The set of vectors is Linearly Dependent.")
        return False


# Function to apply the Gram-Schmidt process to a set of vectors

def gram_schmidt(vectors):
    orthogonal_vectors = []  # Initialise an empty list for orthogonal vectors
    print("Starting the Gram-Schmidt process...")
    for vector in vectors:
        # Orthogonalise the vector against all previously found orthogonal vectors
        for orthogonal_vector in orthogonal_vectors:
            vector -= np.dot(vector, orthogonal_vector) / np.dot(orthogonal_vector, orthogonal_vector) * orthogonal_vector
        orthogonal_vectors.append(vector)  # Add the orthogonalised vector to the list
    return np.array(orthogonal_vectors)  # Return the list of orthogonal vectors as a NumPy array

# Function to normalise a set of vectors

def normalise_vectors(orthogonal_vectors):
    normalised_vectors = []  # This will store the normalised vectors
    for vector in orthogonal_vectors:  # For loop goes through each vector in the list
        norm = 0  # Start with zero norm
        for component in vector:  # Calculate the norm of the vector
            norm += component**2  # Sum the squares of the components
        norm = norm**0.5  # Take the square root of the sum

        # Now, create a new vector for the normalised vector components
        normalised_vector = []
        for component in vector:  # Divide each component by the norm
            normalised_vector.append(component / norm)

        # Add the normalised vector to the list of normalised vectors
        normalised_vectors.append(normalised_vector)

    return normalised_vectors

file_path = input("Enter the path to your file with vectors: ")  # Prompt the user to enter the file path
vectors = read_vectors_from_file(file_path)  # Read vectors from the provided file

# Proceed only if vectors were successfully read from the file
if vectors.size > 0:
    print("Vectors read from the file:", vectors)
    # Check if the vectors are linearly independent before proceeding
    if check_linear_independence(vectors):
        orthogonal_vectors = gram_schmidt(vectors)  # Apply the Gram-Schmidt process

        # Ask the user if they want to normalise the orthogonal vectors
        user_input = input("Do you want to normalise the orthogonal vectors? (yes/no): ").lower()
         # User chose to normalise the orthogonal vectors
        if user_input == 'yes':
            orthonormal_vectors = normalise_vectors(orthogonal_vectors)  # Normalise the vectors
            print("Normalised vectors:")
            for vector in orthonormal_vectors:
                 # Iterate through each orthonormal vector and print it
                print(vector)
        elif user_input == 'no':
             # User chose not to normalise the vectors, so print the orthogonal vectors as is
            print("Orthogonal vectors:")
            for vector in orthogonal_vectors:
                # Iterate through each orthogonal vector and print it
                print(vector)
        else:
            # User input was not recognised (not 'yes' or 'no'), prompt for valid input
            print("Invalid input. Please type 'yes' or 'no'.")
# This else relates to the initial check if vectors were successfully read
else:
    # No vectors were found in the file, print statement in terminal
    print("No vectors were read from the file.")







