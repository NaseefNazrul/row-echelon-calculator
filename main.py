import math
# For now it can simulate making RREF or REF matrices
# Commands: 
# "next" to move on to another row 
# "stop" tp stop making the matrix


# --------------------------- INPUT MATRIX ---------------------------------

max_col = 0  
max_row = 0
matrix = [[]]
command = None
count = 0
while True:
    command = input("row " + str((max_row+1)) + " x" + str((count+1)) + ": ")

    try: 
        command = int(command)
        matrix[max_row].append(command)
        count+=1

    except ValueError: 
        if command.lower() == "next":
            if count < 2:
                print("Please enter another value")
                continue
            max_row += 1
            if count > max_col:
                max_col = count
            count = 0
            matrix.append([])

        elif command.lower() == "stop":
            if count < 2:
                print("Please enter another value")
                continue
            if max_row+1 < 2:
                print("Please add another row")
                continue
            if count > max_col:
                max_col = count
            # extra processing to clean up the matrix
            for row in matrix:
                if len(row) != max_col: 
                    for _ in range(0,max_col+1-len(row)):
                        row.insert(-1, 0)
            break
        
        elif command.lower() == "help":
            print("""i) Enter a number to insert into the matrix
ii) 'next' - next row
iii) 'stop' - finish making the matrix
iv) 'restart' - restart the matrix""")
            print(" ")
            continue

        elif command.lower() == "restart":
            max_col = 0  
            max_row = 0
            matrix = [[]]
            count = 0
            continue
        else: 
            print("Please enter the right input")
            continue


# ---------------------- Printing Function ---------------------------

def printingMatrix(matrix, reason: str):
    if not matrix or not matrix[0]:
        return

    rows = len(matrix)
    cols = len(matrix[0])

    # Find max width for each column (allows multi-digit numbers)
    col_widths = []
    for c in range(cols):
        max_width = max(len(str(matrix[r][c])) for r in range(rows))
        col_widths.append(max_width)

    # Build a row's content between the bars
    def build_row(r):
        coeffs = []
        for c in range(cols - 1):
            coeffs.append(str(matrix[r][c]).rjust(col_widths[c]))
        coeff_part = "  ".join(coeffs)   # two spaces between coefficients
        const_part = str(matrix[r][-1]).rjust(col_widths[-1])
        return f"{coeff_part}  -  {const_part}"

    # Use the widest row to determine internal width
    max_content_len = max(len(build_row(r)) for r in range(rows))
    internal_width = max_content_len + 2   # +2 for the spaces inside "| " and " |"

    # ----- Top border (underscores match the width of the bars) -----
    underscore_line = "_" * internal_width
    print(" " + underscore_line)

    # Empty bar line
    print("|" + " " * internal_width + "|")

    # ----- Matrix rows -----
    for i in range(rows):
        content = build_row(i)
        # Pad content to exactly fill internal_width (left & right spaces)
        padded = content.center(internal_width)
        line = "|" + padded + "|"
        if i == rows // 2:
            line += "  " + reason
        print(line)

    # Bottom border (bars + underscores inside)
    print("|" + "_" * internal_width + "|")


# Reference
# ______                            ______
#|                                        |
#|    4    4    4    4    4    -    5     |   
#|    4    4    4    4    4    -    5     |     (R2' = R1 - 3R4)
#|    4    4    4    4    4    -    5     |    
#|    4    4    4    4    4    -    5     |
#|    4    4    4    4    4    -    5     |
#|                                        |
#|______                            ______|



# -------------------------Simulation Code---------------------------------
print(" ")

process = input("REF or RREF: ")
printingMatrix(matrix, "Starting Matrix")
print(" ")
print(" ")
print("-------------------------------------Simulation-----------------------------------------")
print(" ")
print(" ")
def REF(matrix): # REF 
    
    # First check if the first row has non zero
    def swap_row(matrix, row, col): # the row and col for the pivot to be set 
        if matrix[row][col] == 0: 
            non_zero = 0 
            for i in range(row+1, len(matrix)):
                if non_zero != 0:
                    break
                else:
                    if matrix[i][col] != 0:
                        non_zero = i
            if non_zero == 0: 
                return
            temp = matrix[row]
            matrix[row]= matrix[non_zero]
            matrix[non_zero] = temp
            printingMatrix(matrix, ("[Swapped " + "R"+ str(row+1) +" and R" + str(non_zero+1) + "]"))
    
    def row_calculator_helper(matrix, pivot, row, pivot_multiplier, row_multiplier,type): # A function to transform a row 
        
        for col in range(0,len(matrix[0])):
            if type == "add":
                matrix[row][col] = matrix[row][col]* row_multiplier + matrix[pivot][col]*pivot_multiplier
            else:
                matrix[row][col] = matrix[row][col]* row_multiplier - matrix[pivot][col]*pivot_multiplier
        
    def make_zero_below(matrix, pivot_row, col):
        for current_row in range(pivot_row+1, len(matrix)):
            if matrix[current_row][col] == 0: # Already zeroed out so no changes
                continue
            else:
                pivot_location = matrix[pivot_row][col]
                current_row_location = matrix[current_row][col]
                if (pivot_location > 0 and current_row_location < 0) or (pivot_location > 0 and current_row_location < 0): # Both different signs so adding will cancel them out
                    gcd = math.gcd(pivot_location, current_row_location)
                    row_calculator_helper(matrix, pivot_row, current_row, abs(current_row_location//gcd), abs(pivot_location//gcd), "add") # Dont even question this (basically to get the same values we need the gcd between them and therefore they will easily be cancelled out)
                    printingMatrix(matrix, ("[ R" + str(current_row+1) + "' = " + str(abs(pivot_location//gcd)) + "R" + str(current_row+1) + " + " + str(abs(current_row_location//gcd)) + "R" + str(pivot_row+1) + " ]"))
                else: # Both postive so subtract the pivot
                    gcd = math.gcd(pivot_location, current_row_location)
                    row_calculator_helper(matrix, pivot_row, current_row, abs(current_row_location//gcd), abs(pivot_location//gcd), "sub") # Dont even question this (basically to get the same values we need the gcd between them and therefore they will easily be cancelled out)
                    printingMatrix(matrix, ("[ R" + str(current_row+1) + "' = " + str(abs(pivot_location//gcd)) + "R" + str(current_row+1) + " - " + str(abs(current_row_location//gcd)) + "R" + str(pivot_row+1) + " ]"))

    # Now begins the traversal of the matrix 
    current_row = 0 
    current_col = 0
    while True:
        if current_row == len(matrix):
            current_row = 1
            continue
        swap_row(matrix,current_row,current_col)
        if matrix[current_row][current_col] == 0: # The whole column is zero meaning free variable
            current_col += 1
            if current_col > len(matrix[0]) - 2:
                break
            continue
        else: 
            make_zero_below(matrix, current_row, current_col)
            current_row += 1
            current_col += 1
            if current_col > len(matrix[0]) - 2:
                break
    print(" ")
    print(" ")
            

REF(matrix)


                
                    



