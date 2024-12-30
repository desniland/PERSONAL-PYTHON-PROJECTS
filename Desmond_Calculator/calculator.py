"""
This module provides a basic framework for creating graphical user interfaces (GUIs) using the Tkinter library.

"""
import tkinter as tk

#Various font styles i'll use throughout the calculator application. 
LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

#Color Definitions
OFF_WHITE = "#F8FAFF"   #offwhite
WHITE = "#FFFFFF"       #White
LIGHT_BLUE = "#CCEDFF"  #Blue
LIGHT_GRAY = "#F5F5F5"  #Gray
LABEL_COLOR = "#25265E" #Paua


class Calculator:
    """
    This module defines the `Calculator` class, which is the core component of the calculator application.
    **Description:**

    The `Calculator` class is responsible for creating the graphical user interface (GUI) of the calculator application and handling user interactions.
        It manages the display, buttons, and internal logic for performing calculations.

    **Methods:**
         **__init__(self):**
        - Constructor for the `Calculator` class. It initializes the following:
            - `window`: Main application window using `tk.Tk()`.
            - `window.geometry("375x667")`: Sets the window size.
            - `window.resizable(0, 0)`: Disables window resizing.
            - `window.title("Calculator")`: Sets the window title to "Calculator".
            - `total_expression`: An empty string to store the complete expression entered by the user.
            - `current_expression`: An empty string to store the current number being entered.
            - `display_frame`: Calls the `create_display_frame` method to create the frame for the calculator display.
            - `total_label, self.label`: Calls the `create_display_labels` method to create labels for displaying the total expression and current number.
            - `digits`: A dictionary that maps digit buttons (7-0, .) to their grid positions within the button frame.
            - `operations`: A dictionary that maps operation buttons (/ , *, -, +) to their corresponding symbols.
            - `buttons_frame`: Calls the `create_buttons_frame` method to create the frame for the calculator buttons.
            - Configures button frame rows and columns for proper layout.
            - Calls methods to create digit buttons, operator buttons, and special buttons (clear, equal).
            - `bind_keys()`: Binds keyboard keys to calculator functions for alternative input.

    """


    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        '''
        This method establishes keyboard shortcuts for various calculator functions. 
        **Functionality:**

        * **<Return> Key:**
            - Binds the "Enter" key (`<Return>`) to the `evaluate()` method. 
            - This allows users to trigger the calculation by pressing the Enter key.

        * **Digit Keys (0-9, .):**
            - Binds each digit key (0-9, .) to the `add_to_expression()` method.
            - When a digit key is pressed, the corresponding digit is added to the current expression.

        * **Operator Keys (+, -, *, /):**
            - Binds each operator key (+, -, *, /) to the `append_operator()` method. 
            - When an operator key is pressed, the corresponding operator is appended to the expression.
        '''

        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        '''
        This method is responsible for creating and positioning special function buttons on the calculator's button frame.
         * **Calls Helper Methods:**
             - `create_clear_button()`: Creates the "Clear" button.
             - `create_equals_button()`: Creates the "=" button.
             - `create_square_button()`: Creates the "x²" button (for calculating the square of a number).
             - `create_sqrt_button()`: Creates the "√" button (for calculating the square root of a number).

        '''

        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        '''
        This method creates and configures the labels used to display the calculator's expressions.
           **Functionality:**
        1. Creates Total Expression Label
        2. Creates Current Expression Label
        3. Returns Labels
        '''
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        '''
        This creates and configures the frame that will hold the calculator's display elements (labels for total expression and current expression).
         **Functionality:**
        1.Creates a frame
        2.packs the frame
        3.Returns the frame
        '''
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        '''
        This method handles the addition of digits or decimal points to the current expression being entered by the user.

        **Parameters:**

        @value: The digit or decimal point to be added to the expression (e.g., '7', '0', '.').

        **Functionality:**

        1.Concatenate Value.
        2. Update Display.
  
        '''
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        '''
        This method creates and positions the digit buttons (0-9, .) on the calculator's button frame.
        **Functionality:**
        1. Iterates through digits
        2. Create a button for each digit
        3. Positions Button
        '''

        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        '''
        This method handles the addition of operators (+, -, *, /) to the expression.
         **Parameters**
        @operator: The operator to be added to the expression (e.g., '+', '-', '*', '/').
         **Functionality**
        1.Append Operator to Current Expression
        2.Append Current Expression to Total Expression
        3.Clear Current Expression
        4.Update Labels
        '''

        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        '''
        This method creates and positions the operator buttons (+, -, *, /) on the calculator's button frame.
         **Functionality:**
        1.Iterate through Operators
        2.Create Button for each operator
        3.Position Button
        4.Increment Row Counter
        '''
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
