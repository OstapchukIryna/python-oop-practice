# Inventory Item

A demonstration of operator overloading in Python: designing a class with
meaningful arithmetic, comparison, and representation semantics.

## What it is

`InventoryItem` represents a named item with an integer quantity — the
kind of value object you'd find in an inventory or warehouse system.
The focus is not on the domain itself, but on **how to design dunder
methods that behave predictably and idiomatically**.

## Supported operations

| Operator     | Behavior                                                             |
|--------------|----------------------------------------------------------------------|
| `a + b`      | Same-name items → new item with summed quantity. Different names → `ValueError`. |
| `a - b`      | Same-name items → new item with subtracted quantity. Negative result → `ValueError`. |
| `a * n`      | Non-negative int → scales quantity. Rejects `bool`, `float`, other types. |
| `a == b`     | True if both name and quantity match. Comparing to non-item → False. |
| `a < b`, `a > b`, `a <= b`, `a >= b` | Same-name items compared by quantity. Different names → `ValueError`. |
| `repr(a)`    | Returns a valid Python expression that reconstructs the object.      |

## Design decisions

**Same-name constraint on arithmetic.** Adding an apple to a banana has no
meaningful result, so the class refuses rather than silently coercing.

**Strict integer multiplication.** Multiplying quantity by a float would
silently truncate, which is a common source of bugs. The class rejects
floats explicitly. `bool` is also rejected, since it's a subclass of `int`
in Python but `item * True` has no useful meaning.

**Unhashable by design.** Because `quantity` is mutable, allowing the
class to be hashed would break `set`/`dict` semantics — an item could
"disappear" from a set after its quantity is changed. `__hash__` is
explicitly set to `None`.

**`NotImplemented` for foreign types.** Operators with non-`InventoryItem`
operands return `NotImplemented` rather than raising, so Python can try
the reflected operation on the other object before giving up with a
`TypeError`.

**`@total_ordering` for comparisons.** Only `__eq__` and `__lt__` are
implemented directly; `<=`, `>`, `>=` are generated automatically by
`functools.total_ordering`.

## Usage

```python
from inventory_item.inventory_item import InventoryItem

apples = InventoryItem("apple", 10)
more_apples = InventoryItem("apple", 5)

apples + more_apples          # InventoryItem(name='apple', quantity=15)
apples * 3                    # InventoryItem(name='apple', quantity=30)
apples > more_apples          # True
apples == InventoryItem("apple", 10)   # True
```

## Tests

Run from the project root:

    python3 -m unittest inventory_item.tests.test_inventory_item -v

Around 30 tests covering: construction, all arithmetic operators, all
comparison operators, edge cases (zero, negative, bool, float, foreign
types), and hashability.