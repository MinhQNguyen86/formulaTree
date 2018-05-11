"""
# Copyright Minh Nguyen, 2018
# Copyright Nick Cheng, 2016, 2018
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2018
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file. If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment.

# Add your functions here.


def build_tree(formula):
    '''(str) -> FormulaTree
    If the str <formula> meets the criteria
    of being a valid formula, create and return
    the FormulaTree representation of the string.
    Otherwise returns None.
    REQ: formula is not empty
    >>> build_tree('x')
    Leaf('x')
    '''
    # Check if formula is valid
    if is_valid(formula):
        # Base case when length of list is one
        if len(formula) == 1:
            tree = Leaf(formula)
        # Second base case is special case of the NotTree
        elif formula[0] == '-':
            # Recursively create the rest of the formula '--(..)'
            if formula[1] == '-':
                tree = NotTree(build_tree(formula[1:]))
            # Create the NotTree for the rest of the bracket '-(..)'
            elif formula[1] == '(':
                tree = NotTree(build_tree(formula[1:formula.index(')')+1]))
            # Create the NotTree only for the variable
            elif formula[1].islower():
                tree = NotTree(build_tree(formula[1]))
        else:
            # Get the root and the index of the root
            (r, index) = find_root(formula)
            # Build the 'And' and/or 'Or' trees respectively
            if r == '*':
                tree = AndTree(build_tree(formula[1:index]), build_tree(
                    formula[index+1:len(formula)-1]))
            elif r == '+':
                tree = OrTree(build_tree(formula[1:index]), build_tree(
                    formula[index+1:len(formula)-1]))
    else:
        tree = None

    return tree


def find_root(formula):
    '''(str) -> str
    Used to find the root when formula is valid and contains
    either '+' or '*'
    '''
    for i in range(len(formula)):
        if formula[i] == '+' or formula[i] == '*':
            if is_valid(formula[1:i]) and is_valid(
                    formula[i+1:len(formula)-1]):
                return formula[i], i


def is_valid(formula):
    '''(str) -> bool
    Given a formula string, return a boolean
    value to determine if it's a valid formula
    adhering to the requirements shown on
    a2.pdf
    >>> is_valid('-x')
    True
    '''
    stack = []
    numsym = 0  # Number of * and +
    numbrac = 0  # Number of ( brackets
    numbrac2 = 0  # Number of ) brackets
    numvar = 0  # Number of letters
    val = True
    # Checks the base case where length
    # of the string is zero or if the
    # string contains a space
    if len(formula) == 0 or ' ' in formula:
        val = False
    # if the length is 1 and it's not a letter
    elif len(formula) == 1 and not formula.islower():
        val = False
    # if length is 2 and doesn't contain '-'
    elif len(formula) == 2 and '-' not in formula:
        val = False
    else:
        # Loop through the string to check if
        # brackets are balanced
        for i in range(len(formula)):
            if formula[i] == '(':
                # If formula contains empty brackets '()'
                if formula[i+1] == ')':
                    val = False
                stack.append(formula[i])
                numbrac += 1
            elif formula[i] == ')':
                if len(stack) > 0:
                    popped = stack.pop()
                numbrac2 += 1
            elif formula[i] == '+' or formula[i] == '*':
                # Check if the values before and after
                # '+' and '*' are valid
                if (not formula[i-1].islower() and formula[i-1] != ')') or (
                        not formula[i+1].islower() and (
                                formula[i+1] != '(' and formula[i+1] != '-')):
                    val = False
                numsym += 1
            elif formula[i].islower():
                numvar += 1
                # Makes sure OutofBounds Error doesn't occur
                if (i > 0 and i < len(formula)-1):
                    # '(x)' is invalid
                    if formula[i-1] == '(' and formula[i+1] == ')':
                        val = False
                    # Makes sure the values before and after
                    # the varible is valid
                    # ('*', '+', '-' comes before)
                    # ('*', '+', comes after)
                    elif formula[i-1] != '*' and (
                            formula[i-1] != '+' and formula[i-1] != '-'):
                        if (formula[i+1] != '*' and formula[i+1] != '+'):
                            val = False

    # If the parentheses are not balanced
    if len(stack) != 0 or numbrac2 != numbrac:
        val = False

    # If there are no variables
    if numvar == 0:
        val = False

    # Check if the number of '(' brackets
    # equals the number of * and + symbols
    # and if the variables is one less than the
    # number of + and * symbols
    if numbrac != numsym or numvar-1 != numsym:
        val = False

    return val


def draw_formula_tree(root):
    '''(FormulaTree) -> str
    Given a FormulaTree, draw the string representation
    of the tree as shown on pg. 2 of a2.pdf, and return
    that string
    REQ: symbols are either '+', '-', '*' or .islower()
    REQ: root is a valid binary FormulaTree
    >>> draw_formula_tree(NotTree(Leaf('x')))
    '- x'
    '''
    return draw_helper(root)


def draw_helper(root, d=1):
    '''(FormulaTree, int) -> str
    Returns the string that draws out the FormulaTree
    'd' holds the current recursion depth in order to
    find out how many spaces is needed for each line
    '''
    # Initiate empty tree
    tree = ''
    # Base case is if the node is a leaf
    if isinstance(root, Leaf):
        tree += root.get_symbol()
    # Else draw the tree for '-', '*', and '+'
    elif isinstance(root, NotTree):
        tree += '- ' + draw_helper(root.get_children()[0], d=d+1)
    elif isinstance(root, AndTree):
        tree += '* ' + draw_helper(root.get_children()[1], d=d+1) + '\n'
        tree += '  '*d + draw_helper(
            root.get_children()[0], d=d+1)
    elif isinstance(root, OrTree):
        tree += '+ ' + draw_helper(root.get_children()[1], d=d+1) + '\n'
        tree += '  '*d + draw_helper(root.get_children()[0], d=d+1)
    return tree


def evaluate(root, var, values):
    '''(FormulaTree, str, str) -> bool
    Given the formula represented as a FormulaTree,
    a string of the variables in the formula, and the
    values each variable represents, return the boolean
    expression that is the result of replacing the variables
    in the FormulaTree with their corresponding values.
    REQ: values are either '1' or '0'
    REQ: len(variables) == len(values)
    REQ: var contains the variables in the FormulaTree
    REQ: root is a valid FormulaTree
    >>> evaluate(Leaf('x'), 'x', '1')
    True
    '''
    # If the root is just one variable, the formula
    # evaluates to values
    if isinstance(root, Leaf):
        # Get the symbol of the Leaf, then
        # find its index in the string var
        sym = root.get_symbol()
        i = var.index(sym)
        val = bool(int(values[i]))
    else:
        # Recursive case; check whether the root is a
        # NOT, AND, OR function
        if isinstance(root, NotTree):
            val = not evaluate(root.get_children()[0], var, values)
        elif isinstance(root, AndTree):
            val = evaluate(root.get_children()[0], var, values
                           ) and evaluate(root.get_children()[1], var, values)
        elif isinstance(root, OrTree):
            val = evaluate(root.get_children()[0], var, values
                           ) or evaluate(root.get_children()[1], var, values)
    return val


def play2win(root, turns, var, values):
    '''(FormulaTree, str, str, str) -> int
    The game configuration is given as the parameters:
    where root is the root of the FormulaTree,
    turns is a string representing the order of the
    players' turn, var representing the variables
    that each player can set values to, and values
    being the values that have been set for each
    variable. Given this, returns the best move that
    the next player can make in order to have the best
    chance of winning.
    If the next move is irrelevant then 1 is returned if player
    E is up, and 0 is returned if it is player A's turn.
    REQ: (root, turns, variables, values) must be a valid
    game configuration
    REQ: len(turns) > len(values)
    >>> play2win(OrTree(Leaf('x'), Leaf('y')), 'EA', 'xy', '')
    1
    '''
    win = -1
    # root, turns, var, values
    # (x*y), 'EA', 'xy', '0'
    # Base case, root is a Leaf
    if isinstance(root, Leaf):
        # If the current player is E, return 1
        # Else the current player is A, return 0
        if turns[0] == 'E':
            win = 1
        else:
            win = 0
    else:
        if len(turns) > len(values):
            # Find the Player we want to win (A or E)
            first = turns[len(values)]
            # plays 0
            a = play2win(root, turns, var, values+'0')
            # plays 1
            b = play2win(root, turns, var, values+'1')

            if first == 'E':
                if a:
                    win = 0
                elif b:
                    win = 1
                else:
                    # If choice makes no difference, choose 1
                    win = 1
            elif first == 'A':
                if not a:
                    win = 0
                elif not b:
                    win = 1
                else:
                    # If choice makes no difference, choose 0
                    win = 0
        else:
            # Evaluate the Truth value
            win = evaluate(root, var, values)
    return win
