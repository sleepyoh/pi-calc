import decimal
import time
import os

def calculate_pi_gauss_legendre(digits):
    """
    Calculates Pi to the specified number of decimal digits using the Gauss-Legendre algorithm.
    This algorithm has quadratic convergence, meaning the number of correct digits
    roughly doubles with each iteration, making it very efficient for high precision.
    """
    # Set precision for decimal calculations.
    # We add a buffer for intermediate calculations to ensure accuracy.
    # A common rule of thumb is to add a few extra digits (e.g., 5-10)
    # beyond the target 'digits' for the context precision.
    decimal.getcontext().prec = digits + 10

    # Initialize the variables for the Gauss-Legendre algorithm
    a = decimal.Decimal(1)
    b = decimal.Decimal(1) / decimal.Decimal(2).sqrt() # 1 / sqrt(2)
    t = decimal.Decimal(1) / decimal.Decimal(4)       # 1/4
    p = decimal.Decimal(1)                            # Initial p

    # Determine the number of iterations needed.
    # For quadratic convergence, log2(digits) iterations are roughly needed.
    # We add a small buffer here too.
    # For 1,000,000 digits, log2(1,000,000) is approx 19.9, so ~20 iterations.
    # Let's run a few more to be safe, e.g., 25-30 iterations for 1M digits.
    # The loop will naturally stop when 'a' and 'b' are close enough,
    # but a fixed number of iterations is also common for high precision.
    # For this implementation, we'll iterate until 'a' and 'b' are very close.

    # We need to define a stopping condition based on the difference between a and b
    # becoming sufficiently small to guarantee 'digits' precision.
    # The difference 'a-b' should be smaller than 10^(-digits).
    # We'll use a slightly more generous threshold for safety.
    threshold = decimal.Decimal(1) / (10**(digits + 2)) # e.g., 1e-100002 for 100K digits

    iteration_count = 0
    while True:
        iteration_count += 1
        a_next = (a + b) / 2
        b_next = (a * b).sqrt()
        t_next = t - p * (a - a_next)**2
        p_next = 2 * p

        # Update variables for the next iteration
        a = a_next
        b = b_next
        t = t_next
        p = p_next

        # Check stopping condition: if a and b are close enough
        if abs(a - b).compare(threshold) < 0:
            break
        
        # Safety break to prevent infinite loops in case of unexpected convergence issues
        # For 100,000 digits, ~17 iterations are expected (log2(100,000) approx 16.6).
        # Setting a safety limit of 25-30 iterations should be more than sufficient.
        if iteration_count > 25: 
            print(f"Warning: Reached max iterations ({iteration_count}) without full convergence. Result might be less precise.")
            break

    # Final approximation of Pi
    pi = (a + b)**2 / (4 * t)

    # Convert the result to a string and return only the requested number of digits.
    # We slice to `digits + 2` to include "3." and then the 'digits' number of decimal places.
    return str(pi)[:digits + 2]

if __name__ == "__main__":
    num_digits = 100_000 # Set the desired number of digits (100 thousand)

    print(f"Calculating Pi to {num_digits} digits using Gauss-Legendre algorithm...")
    start_time = time.time() # Record start time

    pi_digits = calculate_pi_gauss_legendre(num_digits) # Perform the calculation

    end_time = time.time() # Record end time
    
    # Print the first 100 digits (including "3.") and the total calculation time
    print(f"Pi (first 100 digits): {pi_digits[:102]}")
    print(f"Calculation took {end_time - start_time:.2f} seconds.")

