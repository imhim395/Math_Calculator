import math
import json
import os
from collections import Counter
from datetime import datetime
from typing import List, Tuple, Optional, Any
import re


# ========== Configuration & Utilities ==========

class CalculatorConfig:
    """Configuration settings for the calculator."""
    HISTORY_FILE = "calculator_history.json"
    MAX_HISTORY = 100
    DECIMAL_PLACES = 10
    ENABLE_COLORS = True


class InputValidator:
    """Utility class for input validation."""

    @staticmethod
    def get_float(prompt: str, allow_negative: bool = True) -> float:
        """Safely get a float input with validation."""
        while True:
            try:
                value = float(input(prompt))
                if not allow_negative and value < 0:
                    print("Please enter a non-negative number.")
                    continue
                return value
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def get_int(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
        """Safely get an integer input with validation."""
        while True:
            try:
                value = int(input(prompt))
                if min_val is not None and value < min_val:
                    print(f"Please enter a number >= {min_val}.")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Please enter a number <= {max_val}.")
                    continue
                return value
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    @staticmethod
    def get_numbers(prompt: str = "Enter numbers separated by spaces: ") -> List[float]:
        """Safely get a list of numbers."""
        while True:
            try:
                numbers = input(prompt)
                nums = [float(x) for x in numbers.split()]
                if not nums:
                    print("Please enter at least one number.")
                    continue
                return nums
            except ValueError:
                print("Invalid input. Please enter valid numbers separated by spaces.")

    @staticmethod
    def get_choice(prompt: str, valid_choices: List[str]) -> str:
        """Get a choice from valid options."""
        while True:
            choice = input(prompt).strip().lower()
            if choice in [c.lower() for c in valid_choices]:
                return choice
            print(f"Invalid choice. Please enter one of: {', '.join(valid_choices)}")


class CalculationHistory:
    """Manages calculation history."""

    def __init__(self):
        self.history: List[dict] = []
        self.load_history()

    def add(self, operation: str, inputs: dict, result: Any):
        """Add a calculation to history."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "inputs": inputs,
            "result": str(result)
        }
        self.history.append(entry)
        if len(self.history) > CalculatorConfig.MAX_HISTORY:
            self.history.pop(0)
        self.save_history()

    def display_recent(self, n: int = 10):
        """Display recent calculations."""
        if not self.history:
            print("\nNo calculation history.")
            return

        print(f"\n{'=' * 60}")
        print(f"   Recent Calculations (showing last {min(n, len(self.history))})")
        print('=' * 60)

        for i, entry in enumerate(self.history[-n:], 1):
            print(f"\n{i}. {entry['operation']}")
            print(f"   Inputs: {entry['inputs']}")
            print(f"   Result: {entry['result']}")
            print(f"   Time: {entry['timestamp']}")

        print('=' * 60)

    def clear(self):
        """Clear calculation history."""
        self.history = []
        self.save_history()
        print("History cleared.")

    def save_history(self):
        """Save history to file."""
        try:
            with open(CalculatorConfig.HISTORY_FILE, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception:
            pass  # Silently fail if can't save

    def load_history(self):
        """Load history from file."""
        try:
            if os.path.exists(CalculatorConfig.HISTORY_FILE):
                with open(CalculatorConfig.HISTORY_FILE, 'r') as f:
                    self.history = json.load(f)
        except Exception:
            self.history = []


# Global history instance
history = CalculationHistory()


def format_result(value: Any) -> str:
    """Format result for display."""
    if isinstance(value, (int, float)):
        if abs(value) < 1e-10:
            return "0"
        if isinstance(value, float) and (value == float('inf') or value == float('-inf') or math.isnan(value)):
            return str(value)
        # Format to reasonable decimal places
        formatted = f"{value:.{CalculatorConfig.DECIMAL_PLACES}f}".rstrip('0').rstrip('.')
        return formatted
    return str(value)


# ========== Enhanced Calculation Functions ==========

def addition_calculator():
    """Add multiple numbers."""
    nums = InputValidator.get_numbers()
    result = sum(nums)
    print(f"\n{'=' * 40}")
    print(f"Sum: {format_result(result)}")
    print('=' * 40)
    history.add("Addition", {"numbers": nums}, result)


def subtraction_calculator():
    """Subtract multiple numbers sequentially."""
    nums = InputValidator.get_numbers()
    total = nums[0]
    for n in nums[1:]:
        total -= n
    print(f"\n{'=' * 40}")
    print(f"Difference: {format_result(total)}")
    print('=' * 40)
    history.add("Subtraction", {"numbers": nums}, total)


def multiplication_calculator():
    """Multiply multiple numbers."""
    nums = InputValidator.get_numbers()
    total = 1
    for n in nums:
        total *= n
    print(f"\n{'=' * 40}")
    print(f"Product: {format_result(total)}")
    print('=' * 40)
    history.add("Multiplication", {"numbers": nums}, total)


def division_calculator():
    """Divide multiple numbers sequentially."""
    nums = InputValidator.get_numbers()
    if len(nums) < 2:
        print("Error: Need at least 2 numbers for division.")
        return

    total = nums[0]
    try:
        for n in nums[1:]:
            if n == 0:
                print("Error: Division by zero!")
                return
            total /= n
        print(f"\n{'=' * 40}")
        print(f"Quotient: {format_result(total)}")
        print('=' * 40)
        history.add("Division", {"numbers": nums}, total)
    except ZeroDivisionError:
        print("Error: Division by zero!")


def average_calculator():
    """Calculate the mean of numbers."""
    nums = InputValidator.get_numbers()
    result = sum(nums) / len(nums)
    print(f"\n{'=' * 40}")
    print(f"Average: {format_result(result)}")
    print(f"Count: {len(nums)}")
    print('=' * 40)
    history.add("Average", {"numbers": nums}, result)


def percent_calculator():
    """Perform various percentage calculations."""
    print("\n1. a% of b")
    print("2. a is what % of b")
    print("3. Increase b by a%")
    print("4. Decrease b by a%")
    ch = InputValidator.get_choice("Choice: ", ["1", "2", "3", "4"])

    if ch == "1":
        a = InputValidator.get_float("Percent: ")
        b = InputValidator.get_float("Number: ")
        result = (a / 100) * b
        print(f"\n{'=' * 40}")
        print(f"{a}% of {b} = {format_result(result)}")
        print('=' * 40)
        history.add("Percent (a% of b)", {"percent": a, "number": b}, result)
    elif ch == "2":
        a = InputValidator.get_float("Part: ")
        b = InputValidator.get_float("Whole: ")
        if b == 0:
            print("Error: Whole cannot be zero.")
            return
        result = (a / b) * 100
        print(f"\n{'=' * 40}")
        print(f"{a} is {format_result(result)}% of {b}")
        print('=' * 40)
        history.add("Percent (a is what % of b)", {"part": a, "whole": b}, result)
    elif ch == "3":
        a = InputValidator.get_float("Percent: ")
        b = InputValidator.get_float("Number: ")
        result = b * (1 + a / 100)
        print(f"\n{'=' * 40}")
        print(f"Increase {b} by {a}% = {format_result(result)}")
        print('=' * 40)
        history.add("Percent (Increase)", {"percent": a, "number": b}, result)
    elif ch == "4":
        a = InputValidator.get_float("Percent: ")
        b = InputValidator.get_float("Number: ")
        result = b * (1 - a / 100)
        print(f"\n{'=' * 40}")
        print(f"Decrease {b} by {a}% = {format_result(result)}")
        print('=' * 40)
        history.add("Percent (Decrease)", {"percent": a, "number": b}, result)


def exponent_calculator():
    """Calculate base raised to an exponent."""
    base = InputValidator.get_float("Base: ")
    exp = InputValidator.get_float("Exponent: ")
    try:
        result = base ** exp
        print(f"\n{'=' * 40}")
        print(f"{base}^{exp} = {format_result(result)}")
        print('=' * 40)
        history.add("Exponent", {"base": base, "exponent": exp}, result)
    except OverflowError:
        print("Error: Result too large!")
    except ValueError as e:
        print(f"Error: {e}")


def squareroot_calculator():
    """Calculate square root of a number."""
    number = InputValidator.get_float("Number: ", allow_negative=False)
    result = math.sqrt(number)
    print(f"\n{'=' * 40}")
    print(f"√{number} = {format_result(result)}")
    print('=' * 40)
    history.add("Square Root", {"number": number}, result)


def logarithm_calculator():
    """Calculate logarithm with various bases."""
    n = InputValidator.get_float("Number: ", allow_negative=False)
    if n <= 0:
        print("Error: Number must be positive.")
        return

    base = input("Base (10 for log, e for ln, or number): ").lower().strip()
    try:
        if base == "10":
            result = math.log10(n)
            print(f"\n{'=' * 40}")
            print(f"log₁₀({n}) = {format_result(result)}")
            print('=' * 40)
            history.add("Logarithm (base 10)", {"number": n}, result)
        elif base == "e":
            result = math.log(n)
            print(f"\n{'=' * 40}")
            print(f"ln({n}) = {format_result(result)}")
            print('=' * 40)
            history.add("Natural Logarithm", {"number": n}, result)
        else:
            base_val = float(base)
            if base_val <= 0 or base_val == 1:
                print("Error: Base must be positive and not equal to 1.")
                return
            result = math.log(n, base_val)
            print(f"\n{'=' * 40}")
            print(f"log_{base_val}({n}) = {format_result(result)}")
            print('=' * 40)
            history.add("Logarithm", {"number": n, "base": base_val}, result)
    except ValueError as e:
        print(f"Error: {e}")


def quadratic_solver():
    """Solve quadratic equation ax² + bx + c = 0."""
    a = InputValidator.get_float("a: ")
    if a == 0:
        print("Error: 'a' cannot be zero for a quadratic equation.")
        return

    b = InputValidator.get_float("b: ")
    c = InputValidator.get_float("c: ")

    discriminant = b ** 2 - 4 * a * c

    print(f"\n{'=' * 40}")
    print(f"Equation: {a}x² + {b}x + {c} = 0")
    print(f"Discriminant: {format_result(discriminant)}")

    if discriminant < 0:
        real_part = -b / (2 * a)
        imag_part = math.sqrt(-discriminant) / (2 * a)
        print(f"Complex solutions:")
        print(f"  x₁ = {format_result(real_part)} + {format_result(imag_part)}i")
        print(f"  x₂ = {format_result(real_part)} - {format_result(imag_part)}i")
        history.add("Quadratic (Complex)", {"a": a, "b": b, "c": c}, f"Complex roots")
    elif discriminant == 0:
        result = -b / (2 * a)
        print(f"One solution (repeated root): {format_result(result)}")
        history.add("Quadratic", {"a": a, "b": b, "c": c}, result)
    else:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        print(f"Solutions:")
        print(f"  x₁ = {format_result(x1)}")
        print(f"  x₂ = {format_result(x2)}")
        history.add("Quadratic", {"a": a, "b": b, "c": c}, [x1, x2])
    print('=' * 40)


def factor_quadratic():
    """Factor quadratic expression."""
    print("Factor quadratic: ax² + bx + c")
    a = InputValidator.get_int("a: ")
    b = InputValidator.get_int("b: ")
    c = InputValidator.get_int("c: ")

    if a == 0:
        print("Error: 'a' cannot be zero.")
        return

    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        print("Cannot factor over real numbers")
        return

    sqrt_d = int(math.sqrt(discriminant))
    if sqrt_d * sqrt_d != discriminant:
        print("Cannot factor nicely over integers")
        return

    r1 = (-b + sqrt_d) // (2 * a)
    r2 = (-b - sqrt_d) // (2 * a)
    print(f"\n{'=' * 40}")
    print(f"Factored form: {a}(x-{r1})(x-{r2})")
    print('=' * 40)
    history.add("Factor Quadratic", {"a": a, "b": b, "c": c}, f"{a}(x-{r1})(x-{r2})")


def system_of_equations():
    """Solve 2x2 system of linear equations."""
    print("Solve ax + by = c and dx + ey = f")
    a = InputValidator.get_float("a: ")
    b = InputValidator.get_float("b: ")
    c = InputValidator.get_float("c: ")
    d = InputValidator.get_float("d: ")
    e = InputValidator.get_float("e: ")
    f = InputValidator.get_float("f: ")

    det = a * e - b * d
    print(f"\n{'=' * 40}")
    if abs(det) < 1e-10:
        print("No unique solution (determinant is zero)")
    else:
        x = (c * e - b * f) / det
        y = (a * f - c * d) / det
        print(f"x = {format_result(x)}")
        print(f"y = {format_result(y)}")
        history.add("System of Equations", {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f}, {"x": x, "y": y})
    print('=' * 40)


def slope_intercept_solver():
    """Solve y = mx + b for x or y."""
    m = InputValidator.get_float("Slope m: ")
    b = InputValidator.get_float("Intercept b: ")
    choice = InputValidator.get_choice("Solve for y or x? (y/x): ", ["y", "x"])

    print(f"\n{'=' * 40}")
    if choice == "y":
        x = InputValidator.get_float("x = ")
        result = m * x + b
        print(f"y = {format_result(result)}")
        history.add("Slope-Intercept (solve for y)", {"m": m, "b": b, "x": x}, result)
    elif choice == "x":
        y = InputValidator.get_float("y = ")
        if abs(m) < 1e-10:
            print("No solution or infinite solutions (slope is zero)")
        else:
            result = (y - b) / m
            print(f"x = {format_result(result)}")
            history.add("Slope-Intercept (solve for x)", {"m": m, "b": b, "y": y}, result)
    print('=' * 40)


def slope_2points():
    """Calculate slope between two points."""
    x1 = InputValidator.get_float("x1: ")
    y1 = InputValidator.get_float("y1: ")
    x2 = InputValidator.get_float("x2: ")
    y2 = InputValidator.get_float("y2: ")

    print(f"\n{'=' * 40}")
    if abs(x1 - x2) < 1e-10:
        print("Undefined slope (vertical line)")
    else:
        result = (y2 - y1) / (x2 - x1)
        print(f"Slope: {format_result(result)}")
        history.add("Slope (2 points)", {"x1": x1, "y1": y1, "x2": x2, "y2": y2}, result)
    print('=' * 40)


def area_calculator():
    """Calculate area of a rectangle."""
    l = InputValidator.get_float("Length: ", allow_negative=False)
    w = InputValidator.get_float("Width: ", allow_negative=False)
    result = l * w
    print(f"\n{'=' * 40}")
    print(f"Area: {format_result(result)}")
    print('=' * 40)
    history.add("Rectangle Area", {"length": l, "width": w}, result)


def perimeter_calculator():
    """Calculate perimeter of a polygon."""
    nums = InputValidator.get_numbers("Enter sides separated by spaces: ")
    result = sum(nums)
    print(f"\n{'=' * 40}")
    print(f"Perimeter: {format_result(result)}")
    print('=' * 40)
    history.add("Perimeter", {"sides": nums}, result)


def trianglearea_calculator():
    """Calculate triangle area using Heron's formula."""
    a = InputValidator.get_float("Side 1: ", allow_negative=False)
    b = InputValidator.get_float("Side 2: ", allow_negative=False)
    c = InputValidator.get_float("Side 3: ", allow_negative=False)

    # Check triangle inequality
    if a + b <= c or a + c <= b or b + c <= a:
        print("Error: These sides do not form a valid triangle.")
        return

    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    print(f"\n{'=' * 40}")
    print(f"Triangle area: {format_result(area)}")
    print('=' * 40)
    history.add("Triangle Area", {"side1": a, "side2": b, "side3": c}, area)


def circlearea_calculator():
    """Calculate area of a circle."""
    radius = InputValidator.get_float("Radius: ", allow_negative=False)
    result = math.pi * radius ** 2
    print(f"\n{'=' * 40}")
    print(f"Circle area: {format_result(result)}")
    print('=' * 40)
    history.add("Circle Area", {"radius": radius}, result)


def circumference_calculator():
    """Calculate circumference of a circle."""
    r = InputValidator.get_float("Radius: ", allow_negative=False)
    result = 2 * math.pi * r
    print(f"\n{'=' * 40}")
    print(f"Circumference: {format_result(result)}")
    print('=' * 40)
    history.add("Circumference", {"radius": r}, result)


def polygon_area_calculator():
    """Calculate area of a regular polygon."""
    n = InputValidator.get_int("Number of sides: ", min_val=3)
    s = InputValidator.get_float("Side length: ", allow_negative=False)
    area = (n * s ** 2) / (4 * math.tan(math.pi / n))
    print(f"\n{'=' * 40}")
    print(f"Polygon area: {format_result(area)}")
    print('=' * 40)
    history.add("Polygon Area", {"sides": n, "side_length": s}, area)


def surface_area_of_cube():
    """Calculate surface area of a cube."""
    a = InputValidator.get_float("Edge length of cube: ", allow_negative=False)
    result = 6 * a ** 2
    print(f"\n{'=' * 40}")
    print(f"Surface area of cube: {format_result(result)}")
    print('=' * 40)
    history.add("Cube Surface Area", {"edge": a}, result)


def prism_surface_area():
    """Calculate surface area of a rectangular prism."""
    l = InputValidator.get_float("Length: ", allow_negative=False)
    w = InputValidator.get_float("Width: ", allow_negative=False)
    h = InputValidator.get_float("Height: ", allow_negative=False)
    result = 2 * (l * w + w * h + h * l)
    print(f"\n{'=' * 40}")
    print(f"Surface area: {format_result(result)}")
    print('=' * 40)
    history.add("Prism Surface Area", {"length": l, "width": w, "height": h}, result)


def cylinder_volume():
    """Calculate volume of a cylinder."""
    r = InputValidator.get_float("Radius: ", allow_negative=False)
    h = InputValidator.get_float("Height: ", allow_negative=False)
    result = math.pi * r * r * h
    print(f"\n{'=' * 40}")
    print(f"Volume: {format_result(result)}")
    print('=' * 40)
    history.add("Cylinder Volume", {"radius": r, "height": h}, result)


def cone_volume():
    """Calculate volume of a cone."""
    r = InputValidator.get_float("Radius: ", allow_negative=False)
    h = InputValidator.get_float("Height: ", allow_negative=False)
    result = (1 / 3) * math.pi * r * r * h
    print(f"\n{'=' * 40}")
    print(f"Volume: {format_result(result)}")
    print('=' * 40)
    history.add("Cone Volume", {"radius": r, "height": h}, result)


def sphere_volume_calculator():
    """Calculate volume of a sphere."""
    r = InputValidator.get_float("Radius: ", allow_negative=False)
    result = 4 / 3 * math.pi * r ** 3
    print(f"\n{'=' * 40}")
    print(f"Sphere volume: {format_result(result)}")
    print('=' * 40)
    history.add("Sphere Volume", {"radius": r}, result)


def distance_formula():
    """Calculate distance between two points."""
    x1 = InputValidator.get_float("x1: ")
    y1 = InputValidator.get_float("y1: ")
    x2 = InputValidator.get_float("x2: ")
    y2 = InputValidator.get_float("y2: ")
    result = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    print(f"\n{'=' * 40}")
    print(f"Distance: {format_result(result)}")
    print('=' * 40)
    history.add("Distance", {"x1": x1, "y1": y1, "x2": x2, "y2": y2}, result)


def pythagoras():
    """Calculate hypotenuse using Pythagorean theorem."""
    a = InputValidator.get_float("Side 1: ", allow_negative=False)
    b = InputValidator.get_float("Side 2: ", allow_negative=False)
    result = math.sqrt(a ** 2 + b ** 2)
    print(f"\n{'=' * 40}")
    print(f"Hypotenuse: {format_result(result)}")
    print('=' * 40)
    history.add("Pythagoras", {"side1": a, "side2": b}, result)


def angle_converter():
    """Convert between degrees and radians."""
    ch = InputValidator.get_choice("1. Deg → Rad, 2. Rad → Deg: ", ["1", "2"])
    print(f"\n{'=' * 40}")
    if ch == "1":
        deg = InputValidator.get_float("Degrees: ")
        result = math.radians(deg)
        print(f"Radians: {format_result(result)}")
        history.add("Angle Converter (Deg→Rad)", {"degrees": deg}, result)
    else:
        rad = InputValidator.get_float("Radians: ")
        result = math.degrees(rad)
        print(f"Degrees: {format_result(result)}")
        history.add("Angle Converter (Rad→Deg)", {"radians": rad}, result)
    print('=' * 40)


def median_calculator():
    """Calculate median of a dataset."""
    nums = InputValidator.get_numbers()
    sorted_nums = sorted(nums)
    n = len(sorted_nums)
    if n % 2 == 1:
        result = sorted_nums[n // 2]
    else:
        result = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2
    print(f"\n{'=' * 40}")
    print(f"Median: {format_result(result)}")
    print('=' * 40)
    history.add("Median", {"numbers": nums}, result)


def mode_calculator():
    """Calculate mode(s) of a dataset."""
    nums = InputValidator.get_numbers()
    count = Counter(nums)
    max_count = max(count.values())
    modes = [k for k, v in count.items() if v == max_count]
    print(f"\n{'=' * 40}")
    print(f"Mode(s): {modes}")
    print(f"Frequency: {max_count}")
    print('=' * 40)
    history.add("Mode", {"numbers": nums}, modes)


def range_calculator():
    """Calculate range of a dataset."""
    nums = InputValidator.get_numbers()
    result = max(nums) - min(nums)
    print(f"\n{'=' * 40}")
    print(f"Range: {format_result(result)}")
    print(f"Min: {format_result(min(nums))}, Max: {format_result(max(nums))}")
    print('=' * 40)
    history.add("Range", {"numbers": nums}, result)


def quartiles():
    """Calculate quartiles of a dataset."""
    nums = sorted(InputValidator.get_numbers())
    n = len(nums)
    if n == 0:
        print("Error: No numbers provided.")
        return

    q2 = nums[n // 2] if n % 2 else (nums[n // 2] + nums[n // 2 - 1]) / 2
    mid = n // 2
    lower = nums[:mid]
    upper = nums[mid + 1:] if n % 2 else nums[mid:]

    def med(arr):
        if not arr:
            return None
        n_arr = len(arr)
        return arr[n_arr // 2] if n_arr % 2 else (arr[n_arr // 2] + arr[n_arr // 2 - 1]) / 2

    q1 = med(lower)
    q3 = med(upper)

    print(f"\n{'=' * 40}")
    print(f"Q1: {format_result(q1)}")
    print(f"Q2 (median): {format_result(q2)}")
    print(f"Q3: {format_result(q3)}")
    if q1 is not None and q3 is not None:
        iqr = q3 - q1
        print(f"IQR: {format_result(iqr)}")
    print('=' * 40)
    history.add("Quartiles", {"numbers": nums}, {"Q1": q1, "Q2": q2, "Q3": q3})


def std_variance_calculator():
    """Calculate variance and standard deviation."""
    nums = InputValidator.get_numbers()
    if len(nums) < 2:
        print("Error: Need at least 2 numbers for standard deviation.")
        return

    mean = sum(nums) / len(nums)
    variance = sum((x - mean) ** 2 for x in nums) / len(nums)
    std = math.sqrt(variance)

    # Sample standard deviation
    sample_variance = sum((x - mean) ** 2 for x in nums) / (len(nums) - 1)
    sample_std = math.sqrt(sample_variance)

    print(f"\n{'=' * 40}")
    print(f"Mean: {format_result(mean)}")
    print(f"Population Variance: {format_result(variance)}")
    print(f"Population Std Dev: {format_result(std)}")
    print(f"Sample Variance: {format_result(sample_variance)}")
    print(f"Sample Std Dev: {format_result(sample_std)}")
    print('=' * 40)
    history.add("Std Dev/Variance", {"numbers": nums}, {"mean": mean, "variance": variance, "std": std})


def prime_checker():
    """Check if a number is prime."""
    n = InputValidator.get_int("Number: ", min_val=0)
    if n < 2:
        print("\nNot prime")
        return

    is_prime = True
    if n == 2:
        is_prime = True
    elif n % 2 == 0:
        is_prime = False
    else:
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                is_prime = False
                break

    print(f"\n{'=' * 40}")
    print("Prime" if is_prime else "Not prime")
    if not is_prime and n > 1:

        def prime_check(n):
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    print(f"Divisible by: {i} and {n // i}")
                    break

            print('=' * 40)
            history.add("Prime Check", {"number": n}, is_prime)


def gcd_lcm():
    """Calculate GCD and LCM of two numbers."""
    a = InputValidator.get_int("Number 1: ")
    b = InputValidator.get_int("Number 2: ")
    gcd = math.gcd(a, b)
    lcm = abs(a * b) // gcd if gcd != 0 else 0
    print(f"\n{'=' * 40}")
    print(f"GCD: {gcd}")
    print(f"LCM: {lcm}")
    print('=' * 40)
    history.add("GCD/LCM", {"a": a, "b": b}, {"gcd": gcd, "lcm": lcm})


def factorial_calculator():
    """Calculate factorial of a number."""
    n = InputValidator.get_int("Number: ", min_val=0, max_val=170)  # math.factorial limit
    if n < 0:
        print("No factorial for negative numbers!")
        return

    try:
        result = math.factorial(n)
        print(f"\n{'=' * 40}")
        print(f"{n}! = {result}")
        print('=' * 40)
        history.add("Factorial", {"number": n}, result)
    except OverflowError:
        print("Error: Result too large!")


def fibonacci_sequence():
    """Generate Fibonacci sequence."""
    n = InputValidator.get_int("Number of terms: ", min_val=1, max_val=1000)
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    result = seq[:n]
    print(f"\n{'=' * 40}")
    print(f"Fibonacci sequence ({n} terms):")
    print(result)
    if n > 1:
        print(f"Last term: {result[-1]}")
    print('=' * 40)
    history.add("Fibonacci", {"terms": n}, result)


def roman_converter():
    """Convert decimal number to Roman numerals."""
    num = InputValidator.get_int("Number to convert to Roman: ", min_val=1, max_val=3999)
    original_num = num
    vals = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    res = ""
    for i, v in enumerate(vals):
        while num >= v:
            res += syms[i]
            num -= v
    print(f"\n{'=' * 40}")
    print(f"{original_num} in Roman numerals: {res}")
    print('=' * 40)
    history.add("Roman Numerals", {"number": original_num}, res)


def simplify_fraction():
    """Simplify a fraction to lowest terms."""
    num = InputValidator.get_int("Numerator: ")
    den = InputValidator.get_int("Denominator: ")
    if den == 0:
        print("Error: Denominator cannot be zero.")
        return

    g = math.gcd(num, den)
    simplified_num = num // g
    simplified_den = den // g

    print(f"\n{'=' * 40}")
    print(f"Simplified: {simplified_num}/{simplified_den}")
    if simplified_den < 0:
        print(f"Or: {-simplified_num}/{-simplified_den}")
    print('=' * 40)
    history.add("Simplify Fraction", {"numerator": num, "denominator": den}, f"{simplified_num}/{simplified_den}")


def simplify_radical():
    """Simplify a square root radical."""
    n = InputValidator.get_int("Number: ", min_val=0)
    if n < 0:
        print("Error: Cannot simplify negative number.")
        return

    largest_sq = 1
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % (i * i) == 0:
            largest_sq = i * i
    outside = int(math.sqrt(largest_sq))
    inside = n // largest_sq

    print(f"\n{'=' * 40}")
    if inside == 1:
        print(f"Simplified: {outside}")
    elif outside == 1:
        print(f"Simplified: √{inside}")
    else:
        print(f"Simplified: {outside}√{inside}")
    print('=' * 40)
    history.add("Simplify Radical", {"number": n}, f"{outside}√{inside}")


def sequences():
    """Calculate arithmetic or geometric sequence."""
    print("\n1. Arithmetic\n2. Geometric")
    ch = InputValidator.get_choice("Choice: ", ["1", "2"])

    print(f"\n{'=' * 40}")
    if ch == "1":
        a = InputValidator.get_float("a₁ (first term): ")
        d = InputValidator.get_float("d (common difference): ")
        n = InputValidator.get_int("n (term number): ", min_val=1)
        nth_term = a + (n - 1) * d
        sum_n = n / 2 * (2 * a + (n - 1) * d)
        print(f"nth term = {format_result(nth_term)}")
        print(f"Sum of first n terms = {format_result(sum_n)}")
        history.add("Arithmetic Sequence", {"a1": a, "d": d, "n": n}, {"nth_term": nth_term, "sum": sum_n})
    else:
        a = InputValidator.get_float("a₁ (first term): ")
        r = InputValidator.get_float("r (common ratio): ")
        if abs(r) == 1:
            print("Warning: Sum formula may not apply for |r| = 1")
        n = InputValidator.get_int("n (term number): ", min_val=1)
        nth_term = a * r ** (n - 1)
        if abs(r) != 1:
            sum_n = a * (1 - r ** n) / (1 - r)
        else:
            sum_n = a * n
        print(f"nth term = {format_result(nth_term)}")
        print(f"Sum of first n terms = {format_result(sum_n)}")
        history.add("Geometric Sequence", {"a1": a, "r": r, "n": n}, {"nth_term": nth_term, "sum": sum_n})
    print('=' * 40)


def unit_converter():
    """Convert between common units."""
    print("\n1. Length: Meters ↔ Feet ↔ Inches ↔ Kilometers ↔ Miles")
    print("2. Temperature: Celsius ↔ Fahrenheit ↔ Kelvin")
    print("3. Weight: Kg ↔ Lb ↔ Oz")
    print("4. Volume: Liters ↔ Gallons ↔ Cubic Meters")
    ch = InputValidator.get_choice("Choice: ", ["1", "2", "3", "4"])

    print(f"\n{'=' * 40}")
    if ch == "1":
        print("1. Meters to Feet")
        print("2. Feet to Meters")
        print("3. Meters to Inches")
        print("4. Inches to Meters")
        print("5. Kilometers to Miles")
        print("6. Miles to Kilometers")
        sub_ch = InputValidator.get_choice("Choice: ", ["1", "2", "3", "4", "5", "6"])
        val = InputValidator.get_float("Value: ", allow_negative=False)

        conversions = {
            "1": (val * 3.28084, "feet"),
            "2": (val / 3.28084, "meters"),
            "3": (val * 39.3701, "inches"),
            "4": (val / 39.3701, "meters"),
            "5": (val * 0.621371, "miles"),
            "6": (val / 0.621371, "kilometers")
        }
        result, unit = conversions[sub_ch]
        print(f"Result: {format_result(result)} {unit}")
        history.add("Unit Converter (Length)", {"choice": sub_ch, "value": val}, result)
    elif ch == "2":
        print("1. Celsius to Fahrenheit")
        print("2. Fahrenheit to Celsius")
        print("3. Celsius to Kelvin")
        print("4. Kelvin to Celsius")
        sub_ch = InputValidator.get_choice("Choice: ", ["1", "2", "3", "4"])
        val = InputValidator.get_float("Value: ")

        conversions = {
            "1": (val * 9 / 5 + 32, "°F"),
            "2": ((val - 32) * 5 / 9, "°C"),
            "3": (val + 273.15, "K"),
            "4": (val - 273.15, "°C")
        }
        result, unit = conversions[sub_ch]
        print(f"Result: {format_result(result)} {unit}")
        history.add("Unit Converter (Temperature)", {"choice": sub_ch, "value": val}, result)
    elif ch == "3":
        print("1. Kg to Lb")
        print("2. Lb to Kg")
        print("3. Kg to Oz")
        print("4. Oz to Kg")
        sub_ch = InputValidator.get_choice("Choice: ", ["1", "2", "3", "4"])
        val = InputValidator.get_float("Value: ", allow_negative=False)

        conversions = {
            "1": (val * 2.20462, "lbs"),
            "2": (val / 2.20462, "kg"),
            "3": (val * 35.274, "oz"),
            "4": (val / 35.274, "kg")
        }
        result, unit = conversions[sub_ch]
        print(f"Result: {format_result(result)} {unit}")
        history.add("Unit Converter (Weight)", {"choice": sub_ch, "value": val}, result)
    elif ch == "4":
        print("1. Liters to Gallons")
        print("2. Gallons to Liters")
        print("3. Liters to Cubic Meters")
        print("4. Cubic Meters to Liters")
        sub_ch = InputValidator.get_choice("Choice: ", ["1", "2", "3", "4"])
        val = InputValidator.get_float("Value: ", allow_negative=False)

        conversions = {
            "1": (val * 0.264172, "gallons"),
            "2": (val / 0.264172, "liters"),
            "3": (val / 1000, "m³"),
            "4": (val * 1000, "liters")
        }
        result, unit = conversions[sub_ch]
        print(f"Result: {format_result(result)} {unit}")
        history.add("Unit Converter (Volume)", {"choice": sub_ch, "value": val}, result)
    print('=' * 40)


def random_generator():
    """Generate random numbers."""
    import random
    print("\n1. Random integer")
    print("2. Random float 0-1")
    print("3. Roll dice")
    print("4. Random from list")
    ch = InputValidator.get_choice("Choice: ", ["1", "2", "3", "4"])

    print(f"\n{'=' * 40}")
    if ch == "1":
        a = InputValidator.get_int("Min: ")
        b = InputValidator.get_int("Max: ")
        if a > b:
            a, b = b, a
        result = random.randint(a, b)
        print(f"Result: {result}")
        history.add("Random Integer", {"min": a, "max": b}, result)
    elif ch == "2":
        result = random.random()
        print(f"Result: {format_result(result)}")
        history.add("Random Float", {}, result)
    elif ch == "3":
        sides = InputValidator.get_int("Dice sides: ", min_val=2)
        result = random.randint(1, sides)
        print(f"Result: {result}")
        history.add("Dice Roll", {"sides": sides}, result)
    else:
        items = input("Enter items separated by commas: ").split(',')
        items = [item.strip() for item in items]
        if items:
            result = random.choice(items)
            print(f"Result: {result}")
            history.add("Random from List", {"items": items}, result)
    print('=' * 40)


def base_converter():
    """Convert between number bases."""
    print("\n1. Dec → Bin")
    print("2. Bin → Dec")
    print("3. Dec → Hex")
    print("4. Hex → Dec")
    print("5. Dec → Oct")
    print("6. Oct → Dec")
    ch = InputValidator.get_choice("Choice: ", ["1", "2", "3", "4", "5", "6"])

    print(f"\n{'=' * 40}")
    if ch == "1":
        n = InputValidator.get_int("Decimal: ", min_val=0)
        result = bin(n)[2:]
        print(f"Binary: {result}")
        history.add("Base Converter (Dec→Bin)", {"decimal": n}, result)
    elif ch == "2":
        b = input("Binary: ").strip()
        try:
            result = int(b, 2)
            print(f"Decimal: {result}")
            history.add("Base Converter (Bin→Dec)", {"binary": b}, result)
        except ValueError:
            print("Error: Invalid binary number.")
    elif ch == "3":
        n = InputValidator.get_int("Decimal: ", min_val=0)
        result = hex(n)[2:].upper()
        print(f"Hexadecimal: {result}")
        history.add("Base Converter (Dec→Hex)", {"decimal": n}, result)
    elif ch == "4":
        h = input("Hexadecimal: ").strip()
        try:
            result = int(h, 16)
            print(f"Decimal: {result}")
            history.add("Base Converter (Hex→Dec)", {"hex": h}, result)
        except ValueError:
            print("Error: Invalid hexadecimal number.")
    elif ch == "5":
        n = InputValidator.get_int("Decimal: ", min_val=0)
        result = oct(n)[2:]
        print(f"Octal: {result}")
        history.add("Base Converter (Dec→Oct)", {"decimal": n}, result)
    else:
        o = input("Octal: ").strip()
        try:
            result = int(o, 8)
            print(f"Decimal: {result}")
            history.add("Base Converter (Oct→Dec)", {"octal": o}, result)
        except ValueError:
            print("Error: Invalid octal number.")
    print('=' * 40)


def determinant_2x2():
    """Calculate determinant of 2x2 matrix."""
    print("Enter matrix [[a, b], [c, d]]:")
    a = InputValidator.get_float("a: ")
    b = InputValidator.get_float("b: ")
    c = InputValidator.get_float("c: ")
    d = InputValidator.get_float("d: ")
    result = a * d - b * c
    print(f"\n{'=' * 40}")
    print(f"Matrix: [[{a}, {b}], [{c}, {d}]]")
    print(f"Determinant: {format_result(result)}")
    print('=' * 40)
    history.add("Determinant 2x2", {"a": a, "b": b, "c": c, "d": d}, result)


def determinant_3x3():
    """Calculate determinant of 3x3 matrix."""
    m = []
    print("Enter 3 rows of 3 numbers each:")
    for i in range(3):
        row = InputValidator.get_numbers(f"Row {i + 1}: ")
        if len(row) != 3:
            print("Error: Each row must have exactly 3 numbers.")
            return
        m.append(row)

    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

    print(f"\n{'=' * 40}")
    print("Matrix:")
    for row in m:
        print(f"  {row}")
    print(f"Determinant: {format_result(det)}")
    print('=' * 40)
    history.add("Determinant 3x3", {"matrix": m}, det)


def volume_calculator():
    """Calculate volume of a rectangular prism."""
    l = InputValidator.get_float("Length: ", allow_negative=False)
    w = InputValidator.get_float("Width: ", allow_negative=False)
    h = InputValidator.get_float("Height: ", allow_negative=False)
    result = l * w * h
    print(f"\n{'=' * 40}")
    print(f"Volume: {format_result(result)}")
    print('=' * 40)
    history.add("Volume (Prism)", {"length": l, "width": w, "height": h}, result)


def trapezoid_area():
    """Calculate area of a trapezoid."""
    a = InputValidator.get_float("Base 1: ", allow_negative=False)
    b = InputValidator.get_float("Base 2: ", allow_negative=False)
    h = InputValidator.get_float("Height: ", allow_negative=False)
    result = (a + b) / 2 * h
    print(f"\n{'=' * 40}")
    print(f"Area: {format_result(result)}")
    print('=' * 40)
    history.add("Trapezoid Area", {"base1": a, "base2": b, "height": h}, result)


def parallelogram_area():
    """Calculate area of a parallelogram."""
    b = InputValidator.get_float("Base: ", allow_negative=False)
    h = InputValidator.get_float("Height: ", allow_negative=False)
    result = b * h
    print(f"\n{'=' * 40}")
    print(f"Area: {format_result(result)}")
    print('=' * 40)
    history.add("Parallelogram Area", {"base": b, "height": h}, result)


def ellipse_area():
    """Calculate area of an ellipse."""
    a = InputValidator.get_float("Semi-major radius: ", allow_negative=False)
    b = InputValidator.get_float("Semi-minor radius: ", allow_negative=False)
    result = math.pi * a * b
    print(f"\n{'=' * 40}")
    print(f"Area: {format_result(result)}")
    print('=' * 40)
    history.add("Ellipse Area", {"semi_major": a, "semi_minor": b}, result)


def trig_calculator():
    """Calculate trigonometric functions."""
    print("\nAvailable functions: sin, cos, tan, sec, csc, cot")
    print("Inverse: arcsin, arccos, arctan")
    choice = input("Choose function: ").lower().strip()

    valid_choices = ["sin", "cos", "tan", "sec", "csc", "cot", "arcsin", "arccos", "arctan"]
    if choice not in valid_choices:
        print("Invalid choice.")
        return

    print(f"\n{'=' * 40}")
    if "arc" in choice:
        val = InputValidator.get_float("Value: ")
        if choice == "arcsin":
            if abs(val) > 1:
                print("Error: Value must be between -1 and 1.")
                return
            result = math.degrees(math.asin(val))
            print(f"arcsin({val}) = {format_result(result)}°")
            history.add("Trig (arcsin)", {"value": val}, result)
        elif choice == "arccos":
            if abs(val) > 1:
                print("Error: Value must be between -1 and 1.")
                return
            result = math.degrees(math.acos(val))
            print(f"arccos({val}) = {format_result(result)}°")
            history.add("Trig (arccos)", {"value": val}, result)
        elif choice == "arctan":
            result = math.degrees(math.atan(val))
            print(f"arctan({val}) = {format_result(result)}°")
            history.add("Trig (arctan)", {"value": val}, result)
    else:
        val = InputValidator.get_float("Angle in degrees: ")
        rad = math.radians(val)
        if choice == "sin":
            result = math.sin(rad)
            print(f"sin({val}°) = {format_result(result)}")
            history.add("Trig (sin)", {"angle": val}, result)
        elif choice == "cos":
            result = math.cos(rad)
            print(f"cos({val}°) = {format_result(result)}")
            history.add("Trig (cos)", {"angle": val}, result)
        elif choice == "tan":
            result = math.tan(rad)
            print(f"tan({val}°) = {format_result(result)}")
            history.add("Trig (tan)", {"angle": val}, result)
        elif choice == "sec":
            result = 1 / math.cos(rad)
            print(f"sec({val}°) = {format_result(result)}")
            history.add("Trig (sec)", {"angle": val}, result)
        elif choice == "csc":
            result = 1 / math.sin(rad)
            print(f"csc({val}°) = {format_result(result)}")
            history.add("Trig (csc)", {"angle": val}, result)
        elif choice == "cot":
            result = 1 / math.tan(rad)
            print(f"cot({val}°) = {format_result(result)}")
            history.add("Trig (cot)", {"angle": val}, result)
    print('=' * 40)


def expression_calculator():
    """Evaluate a mathematical expression safely."""
    expr = input("Enter expression (use ** for power, sqrt() for square root): ").strip()

    if not expr:
        print("Error: Empty expression.")
        return

    # Safer evaluation using a restricted namespace
    try:
        # Replace common math functions
        expr = expr.replace("^", "**")

        # Create safe namespace
        safe_dict = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "sqrt": math.sqrt,
            "pi": math.pi,
            "e": math.e,
            "sin": lambda x: math.sin(math.radians(x)) if isinstance(x, (int, float)) else math.sin(x),
            "cos": lambda x: math.cos(math.radians(x)) if isinstance(x, (int, float)) else math.cos(x),
            "tan": lambda x: math.tan(math.radians(x)) if isinstance(x, (int, float)) else math.tan(x),
            "log": math.log,
            "log10": math.log10,
            "ln": math.log,
            "exp": math.exp,
            "pow": pow,
            "floor": math.floor,
            "ceil": math.ceil,
        }

        # Evaluate
        result = eval(expr, safe_dict)

        print(f"\n{'=' * 40}")
        print(f"{expr} = {format_result(result)}")
        print('=' * 40)
        history.add("Expression Calculator", {"expression": expr}, result)

    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure to use valid Python syntax and supported functions.")
def complex_number_calculator():
    """Perform operations on complex numbers."""
    print("\n1. Add complex numbers")
    print("2. Subtract complex numbers")
    print("3. Multiply complex numbers")
    print("4. Divide complex numbers")
    print("5. Power of complex number")
    print("6. Convert to polar form")
    ch = InputValidator.get_choice("Choice: ", ["1", "2", "3", "4", "5", "6"])

    print(f"\n{'=' * 40}")
    if ch in ["1", "2", "3", "4"]:
        print("First complex number (a + bi):")
        a1 = InputValidator.get_float("Real part (a): ")
        b1 = InputValidator.get_float("Imaginary part (b): ")
        z1 = complex(a1, b1)

        print("Second complex number (c + di):")
        a2 = InputValidator.get_float("Real part (c): ")
        b2 = InputValidator.get_float("Imaginary part (d): ")
        z2 = complex(a2, b2)

        if ch == "1":
            result = z1 + z2
            op = "+"
        elif ch == "2":
            result = z1 - z2
            op = "-"
        elif ch == "3":
            result = z1 * z2
            op = "×"
        else:
            if z2 == 0:
                print("Error: Division by zero.")
                return
            result = z1 / z2
            op = "÷"

        print(f"({z1}) {op} ({z2}) = {result}")
        print(f"Real: {format_result(result.real)}, Imaginary: {format_result(result.imag)}")
        print(f"Magnitude: {format_result(abs(result))}")
        history.add("Complex Number Operation", {"z1": str(z1), "z2": str(z2), "operation": op}, str(result))
    elif ch == "5":
        a = InputValidator.get_float("Real part: ")
        b = InputValidator.get_float("Imaginary part: ")
        z = complex(a, b)
        n = InputValidator.get_int("Power: ")
        result = z ** n
        print(f"({z})^{n} = {result}")
        print(f"Real: {format_result(result.real)}, Imaginary: {format_result(result.imag)}")
        history.add("Complex Power", {"z": str(z), "power": n}, str(result))
    else:
        a = InputValidator.get_float("Real part: ")
        b = InputValidator.get_float("Imaginary part: ")
        z = complex(a, b)
        r = abs(z)
        theta = math.degrees(math.atan2(b, a))
        print(f"Complex: {z}")
        print(f"Polar form: {format_result(r)}∠{format_result(theta)}°")
        print(f"Or: {format_result(r)}(cos({format_result(theta)}°) + i·sin({format_result(theta)}°))")
        history.add("Complex to Polar", {"z": str(z)}, {"r": r, "theta": theta})
    print('=' * 40)


def matrix_operations():
    """Perform matrix operations."""
    print("\n1. Add matrices")
    print("2. Multiply matrices")
    print("3. Scalar multiplication")
    print("4. Transpose matrix")
    ch = InputValidator.get_choice("Choice: ", ["1", "2", "3", "4"])

    def get_matrix(name: str, rows: int, cols: int) -> List[List[float]]:
        """Get matrix input from user."""
        print(f"\nEnter {name} ({rows}x{cols}):")
        matrix = []
        for i in range(rows):
            row = InputValidator.get_numbers(f"Row {i + 1}: ")
            if len(row) != cols:
                raise ValueError(f"Row {i + 1} must have {cols} elements")
            matrix.append(row)
        return matrix

    print(f"\n{'=' * 40}")
    try:
        if ch == "1":
            rows = InputValidator.get_int("Number of rows: ", min_val=1, max_val=10)
            cols = InputValidator.get_int("Number of columns: ", min_val=1, max_val=10)
            m1 = get_matrix("Matrix 1", rows, cols)
            m2 = get_matrix("Matrix 2", rows, cols)
            result = [[m1[i][j] + m2[i][j] for j in range(cols)] for i in range(rows)]
            print("Result:")
            for row in result:
                print(f"  {row}")
            history.add("Matrix Addition", {"m1": m1, "m2": m2}, result)
        elif ch == "2":
            rows1 = InputValidator.get_int("Rows of matrix 1: ", min_val=1, max_val=10)
            cols1 = InputValidator.get_int("Columns of matrix 1: ", min_val=1, max_val=10)
            rows2 = cols1
            cols2 = InputValidator.get_int("Columns of matrix 2: ", min_val=1, max_val=10)
            m1 = get_matrix("Matrix 1", rows1, cols1)
            m2 = get_matrix("Matrix 2", rows2, cols2)
            result = [[sum(m1[i][k] * m2[k][j] for k in range(cols1)) for j in range(cols2)] for i in range(rows1)]
            print("Result:")
            for row in result:
                print(f"  {row}")
            history.add("Matrix Multiplication", {"m1": m1, "m2": m2}, result)
        elif ch == "3":
            rows = InputValidator.get_int("Number of rows: ", min_val=1, max_val=10)
            cols = InputValidator.get_int("Number of columns: ", min_val=1, max_val=10)
            m = get_matrix("Matrix", rows, cols)
            scalar = InputValidator.get_float("Scalar: ")
            result = [[scalar * m[i][j] for j in range(cols)] for i in range(rows)]
            print("Result:")
            for row in result:
                print(f"  {row}")
            history.add("Scalar Multiplication", {"matrix": m, "scalar": scalar}, result)
        else:
            rows = InputValidator.get_int("Number of rows: ", min_val=1, max_val=10)
            cols = InputValidator.get_int("Number of columns: ", min_val=1, max_val=10)
            m = get_matrix("Matrix", rows, cols)
            result = [[m[j][i] for j in range(rows)] for i in range(cols)]
            print("Transpose:")
            for row in result:
                print(f"  {row}")
            history.add("Matrix Transpose", {"matrix": m}, result)
    except ValueError as e:
        print(f"Error: {e}")
    print('=' * 40)


def combinations_permutations():
    """Calculate combinations and permutations."""
    print("\n1. Permutations (nPr)")
    print("2. Combinations (nCr)")
    ch = InputValidator.get_choice("Choice: ", ["1", "2"])

    n = InputValidator.get_int("n: ", min_val=0)
    r = InputValidator.get_int("r: ", min_val=0, max_val=n)

    print(f"\n{'=' * 40}")
    if ch == "1":
        if n < r:
            print("Error: n must be >= r")
            return
        result = math.factorial(n) // math.factorial(n - r)
        print(f"P({n},{r}) = {result}")
        history.add("Permutations", {"n": n, "r": r}, result)
    else:
        if n < r:
            print("Error: n must be >= r")
            return
        result = math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
        print(f"C({n},{r}) = {result}")
        history.add("Combinations", {"n": n, "r": r}, result)
    print('=' * 40)


def binomial_theorem():
    """Expand binomial using binomial theorem."""
    print("Expand (a + b)^n")
    a = InputValidator.get_float("a: ")
    b = InputValidator.get_float("b: ")
    n = InputValidator.get_int("n: ", min_val=0, max_val=20)

    print(f"\n{'=' * 40}")
    print(f"Expansion of ({a} + {b})^{n}:")
    terms = []
    for k in range(n + 1):
        coeff = math.factorial(n) // (math.factorial(k) * math.factorial(n - k))
        term_val = coeff * (a ** (n - k)) * (b ** k)
        if k == 0:
            term_str = f"{format_result(term_val)}"
        else:
            term_str = f"{'+' if term_val >= 0 else ''}{format_result(term_val)}"
        terms.append(term_str)
    print(" + ".join(terms))
    result = sum(float(t.replace('+', '')) for t in terms)
    print(f"\nSum: {format_result(result)}")
    print('=' * 40)
    history.add("Binomial Theorem", {"a": a, "b": b, "n": n}, result)


# ========== Search Function ==========

def search_calculators(calculators_dict, calculator_names):
    """Search for calculators by keyword."""
    keyword = input("\nEnter search keyword (or press Enter to see all): ").strip().lower()

    if not keyword:
        return None  # Show all

    matches = []
    for key, name in calculator_names.items():
        if keyword in name.lower():
            matches.append((key, name))

    if not matches:
        print(f"\nNo calculators found matching '{keyword}'")
        input("Press Enter to continue...")
        return "no_match"

    print(f"\n{'=' * 60}")
    print(f"   Search Results for '{keyword}'")
    print('=' * 60)
    for key, name in matches:
        print(f"{key}. {name}")
    print("\n0. Back to main menu")
    print('=' * 60)

    choice = input("\nEnter choice: ").strip()
    if choice == "0":
        return "back"
    elif choice in [k for k, _ in matches]:
        return choice
    else:
        print("Invalid choice")
        input("Press Enter to continue...")
        return "invalid"


# ========== Main Menu ==========

def display_menu():
    """Display the main calculator menu."""
    print("\n" + "=" * 60)
    print("          Welcome To The Math Function Calculator     ")
    print("=" * 60)
    print("   Type 'S' to Search | 'H' for History | '0' to Exit")
    print("=" * 60)

    print("\n📊 ARITHMETIC OPERATIONS:")
    print("   1-Add, 2-Subtract, 3-Multiply, 4-Divide, 5-Average, 6-Percent")
    print("   52-Expression Calculator")

    print("\n🔢 ALGEBRA:")
    print("   7-Exponent, 8-Square Root, 9-Logarithm, 10-Quadratic, 11-Factor Quad")
    print("   12-System 2x2, 13-Slope-Intercept, 14-Slope (2pts)")
    print("   53-Complex Numbers, 54-Matrix Operations, 55-Binomial Theorem")

    print("\n📐 GEOMETRY:")
    print("   15-Rectangle Area, 16-Perimeter, 17-Triangle Area, 18-Circle Area")
    print("   19-Circumference, 20-Polygon Area, 21-Cube SA, 22-Prism SA")
    print("   23-Cylinder Vol, 24-Cone Vol, 25-Sphere Vol, 26-Distance, 27-Pythagoras")
    print("   28-Angle Converter, 48-Trapezoid, 49-Parallelogram, 50-Ellipse")

    print("\n📈 STATISTICS:")
    print("   29-Median, 30-Mode, 31-Range, 32-Quartiles, 33-Std Dev/Variance")

    print("\n🔍 NUMBER THEORY:")
    print("   34-Prime Check, 35-GCD/LCM, 36-Factorial, 37-Fibonacci, 38-Roman Numerals")
    print("   56-Combinations/Permutations")

    print("\n🔧 OTHER:")
    print("   39-Simplify Fraction, 40-Simplify Radical, 41-Sequences, 42-Unit Converter")
    print("   43-Random Generator, 44-Base Converter, 45-Det 2x2, 46-Det 3x3")
    print("   47-Volume (Prism), 51-Trig")

    print("\n" + "=" * 60)
    print("   0. Exit")
    print("=" * 60)


def show_history_menu():
    """Display history management menu."""
    print("\n" + "=" * 60)
    print("   CALCULATION HISTORY")
    print("=" * 60)
    print("1. View recent calculations")
    print("2. Clear history")
    print("0. Back to main menu")
    print("=" * 60)

    choice = input("Enter choice: ").strip()
    if choice == "1":
        n = InputValidator.get_int("How many to show? (default 10): ", min_val=1, max_val=100)
        history.display_recent(n)
        input("\nPress Enter to continue...")
    elif choice == "2":
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        if confirm == "yes":
            history.clear()
        input("\nPress Enter to continue...")


def main():
    """Main program loop."""
    calculators = {
        "1": addition_calculator,
        "2": subtraction_calculator,
        "3": multiplication_calculator,
        "4": division_calculator,
        "5": average_calculator,
        "6": percent_calculator,
        "52": expression_calculator,
        "7": exponent_calculator,
        "8": squareroot_calculator,
        "9": logarithm_calculator,
        "10": quadratic_solver,
        "11": factor_quadratic,
        "12": system_of_equations,
        "13": slope_intercept_solver,
        "14": slope_2points,
        "15": area_calculator,
        "16": perimeter_calculator,
        "17": trianglearea_calculator,
        "18": circlearea_calculator,
        "19": circumference_calculator,
        "20": polygon_area_calculator,
        "21": surface_area_of_cube,
        "22": prism_surface_area,
        "23": cylinder_volume,
        "24": cone_volume,
        "25": sphere_volume_calculator,
        "26": distance_formula,
        "27": pythagoras,
        "28": angle_converter,
        "29": median_calculator,
        "30": mode_calculator,
        "31": range_calculator,
        "32": quartiles,
        "33": std_variance_calculator,
        "34": prime_checker,
        "35": gcd_lcm,
        "36": factorial_calculator,
        "37": fibonacci_sequence,
        "38": roman_converter,
        "39": simplify_fraction,
        "40": simplify_radical,
        "41": sequences,
        "42": unit_converter,
        "43": random_generator,
        "44": base_converter,
        "45": determinant_2x2,
        "46": determinant_3x3,
        "47": volume_calculator,
        "48": trapezoid_area,
        "49": parallelogram_area,
        "50": ellipse_area,
        "51": trig_calculator,
        "53": complex_number_calculator,
        "54": matrix_operations,
        "55": binomial_theorem,
        "56": combinations_permutations,
    }

    calculator_names = {k: v.__name__.replace("_", " ").title() for k, v in calculators.items()}
    while True:
        display_menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "0":
            print("\nThank you for using the Advanced Calculator!")
            print("Exiting program...")
            break

        if choice.lower() == "s":
            result = search_calculators(calculators, calculator_names)
            if result in (None, "back", "no_match", "invalid"):
                continue
            choice = result

        if choice.lower() == "h":
            show_history_menu()
            continue

        if choice in calculators:
            try:
                calculators[choice]()
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
            except Exception as e:
                print(f"\n{'=' * 40}")
                print(f"An error occurred: {e}")
                print("Please check your inputs and try again.")
                print('=' * 40)
            input("\nPress Enter to return to menu...")
        else:
            print("\nInvalid choice, try again.")
            input("Press Enter...")


if __name__ == "__main__":
    main()
