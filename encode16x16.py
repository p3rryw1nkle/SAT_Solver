def calculate_dimac(input_value, row, column):

    # (17^2)*r + (17^1)*c + (17^0)*v
    # value can be from 1 to 16
    # row and column also

    
    match input_value:
        case "A":
            temp_letter_value = 10
            dimac_value = formula_calculate(row, column, temp_letter_value)
            #print(f"I found a letter! It's value is: {temp_letter_value}")

        case "B":
            temp_letter_value = 11
            dimac_value = formula_calculate(row, column, temp_letter_value)
            #print(f"I found a letter! It's value is: {temp_letter_value}")

        case "C":
            temp_letter_value = 12
            dimac_value = formula_calculate(row, column, temp_letter_value)
            #print(f"I found a letter! It's value is: {temp_letter_value}")

        case "D":
            temp_letter_value = 13
            dimac_value = formula_calculate(row, column, temp_letter_value)
            #print(f"I found a letter! It's value is: {temp_letter_value}")

        case "E":
            temp_letter_value = 14
            dimac_value = formula_calculate(row, column, temp_letter_value)
            #print(f"I found a letter! It's value is: {temp_letter_value}")

        case "F":
            temp_letter_value = 15
            dimac_value = formula_calculate(row, column, temp_letter_value)
            #print(f"I found a letter! It's value is: {temp_letter_value}")

        case "G":
            temp_letter_value = 16
            dimac_value = formula_calculate(row, column, temp_letter_value)
            #print(f"I found a letter! It's value is: {temp_letter_value}")

        case _:
            temp_number_value = int(input_value)
            dimac_value = formula_calculate(row, column, temp_number_value)
            #print(f"I found a number! It's value is: {temp_number_value}")

    return dimac_value


def formula_calculate(r,c,v):
    # Ensure the inputs r, c, v are in the range 1 to 16
    if not (1 <= r <= 16 and 1 <= c <= 16 and 1 <= v <= 16):
        raise ValueError("r, c, and v must be between 1 and 16.")

    # Apply the encoding formula: enc(r, c, v) = 17^2 * r + 17^1 * c + 17^0 * v
    encoding = 17**2 * r + 17**1 * c + 17**0 * v

    return encoding





# Open the .txt file in read mode
with open('test_sets/unencoded/one1616.txt', 'r') as file:
    # Loop through each line in the file

    counter = 1
    current_row = 1
    current_column = 1

    for line in file:
        # Strip any trailing newline or whitespace characters
        useful_variable = line.strip()
        
        # Process the line (here, we just print it for demonstration)
        print(f"Processing line: {useful_variable}")


        # Create and open a new .txt file for writing
        file_name = "encoded_16x16_"+str(counter)

        with open(file_name, 'w') as output_file:
        

            for character in line:
                print(f"Processing Character: {character}")
            
                if character == '.':
                    pass
                else:
                    current_dimac_value = calculate_dimac(character, current_row, current_column)
                    output_file.write(str(current_dimac_value) + ' 0\n')  # Write the line to the file, followed by a space, zero and a newline
                
                counter += 1
                current_column += 1
                if current_column == 17:
                    current_column = 1
                    current_row += 1

                print(f"Current row is: {current_row}")
                print(f"Current column is: {current_column}")
                print(f"COUNTER: {counter}")



        print(f"Output File '{file_name}' has been created and written successfully.")



