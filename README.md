## formulaTree
A FormulaTree ADT

## About
A tree that represents a boolean expression.

`+ == OR`

`- == NOT`

`* == AND`

`a b c .. x y z == boolean values`


`E.g. "(x+y)" is an OR expression. Plugging True into the parameters 'x' and 'y' will give a resultant value of True`

Brackets must open and close a valid expression. Brackets are not used for the NOT operator. There is one set of brackets for each operator.

**Not Valid Expressions:**

`"-(x)" - Redundant use of brackets => "-x"`

`"-((x+y))" - Redundant use of brackets => "-(x+y)"`

`"(-x)" - Brackets are not used for NOT operator => "-x"`

`"(a+b+c)" - One set of bracket per operator => "((a+b)+c)"`

`"(a+b)*-c" - Missing a set of brackets => "((a+b)*-c)"`

## Methods
The following methods are in the formula_game_functions class.

**build_tree** - `Creates a FormulaTree given the string representation of the boolean expression`

```
>>> build_tree("-(x+y)")
>>> NotTree(OrTree(Leaf('x'), Leaf('y')))
```
**find_root** - `Finds the root/base of the tree given a valid string formula`

**is_valid** - `Checks if a string formula is a valid expression`

**draw_formula_tree** - `Draws a sideway view of the expression given a FormulaTree root`

```
>>> print(draw_formula_tree(NotTree(OrTree(Leaf('x'), Leaf('y')))))
>>> - + y
       x
```
**evaluate** - `Evaluates the boolean expression given the FormulaTree, string representation of all the parameters, and boolean values (1/0)`

```
>>> evaluate(AndTree(OrTree(Leaf('a'), Leaf('b')), NotTree(Leaf('c'))), 'abc', '101')
>>> False
```

**play2win** - `Given the FormulaTree, string representation of player's turn (Player E/A), string representation of parameters, and played boolean values, returns the optimal choice that the current player should play in order to win. E = 1, A = 0 to win.`

```
>>> play2win(OrTree(Leaf('x'), Leaf('y')), 'EA', 'xy', '')
>>> 1
```
Player E goes first, and since the FormulaTree is a simple OR Tree, player E must play 1 in order to win the game.
