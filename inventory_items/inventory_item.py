from __future__ import annotations
from functools import total_ordering


@total_ordering
class InventoryItem:
    """A named item with an integer quantity.

    Supports arithmetic and comparison operations that preserve the item's
    identity through its name:

    - Addition and subtraction require items with the same name and return
      a new item with the combined quantity. Subtraction raises ValueError
      if the result would be negative.
    - Multiplication by a non-negative integer scales the quantity.
      Rejects bool explicitly (bool is a subclass of int in Python,
      but True * item makes no semantic sense here).
    - Comparison operators (==, <, >) require items with the same name;
      comparing items with different names raises ValueError. Equality
      requires both name and quantity to match.

    The class is intentionally unhashable because quantity is mutable and
    hashing it would break dict/set semantics if the quantity later changes.

    Example:
        >>> apples = InventoryItem("apple", 10)
        >>> apples + InventoryItem("apple", 5)
        InventoryItem(name='apple', quantity=15)
        >>> apples * 3
        InventoryItem(name='apple', quantity=30)
    """

    def __init__(self, name: str, quantity: int) -> None:
        self.name = name
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"InventoryItem(name={self.name!r}, quantity={self.quantity})"

    def __add__(self, other: object) -> InventoryItem:
        """Combine two items with the same name into a new item with summed quantity."""
        if not isinstance(other, InventoryItem):
            return NotImplemented
        if self.name != other.name:
            raise ValueError(
                f"Cannot add items with different names: {self.name!r} + {other.name!r}")
        return InventoryItem(self.name, self.quantity + other.quantity)

    def __sub__(self, other: object) -> InventoryItem:
        """Combine two items with the same name into a new item with subtracted quantity."""
        if not isinstance(other, InventoryItem):
            return NotImplemented
        if self.name != other.name:
            raise ValueError(
                f"Cannot subtract items with different names: {self.name!r} + {other.name!r}")
        if self.quantity < other.quantity:
            raise ValueError("Cannot subtract more than already have.")
        return InventoryItem(self.name, self.quantity - other.quantity)

    def __mul__(self, factor: int) -> InventoryItem:
        if not isinstance(factor, int) or isinstance(factor, bool):
            return NotImplemented
        if factor < 0:
            raise ValueError(
                f"Cannot multiply quantity by negative factor: {factor}")
        return InventoryItem(self.name, self.quantity * factor)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, InventoryItem):
            return self.name == other.name and self.quantity == other.quantity
        return False

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, InventoryItem):
            return NotImplemented
        if self.name != other.name:
            raise ValueError(
                f"Cannot compare items with different names: {self.name!r} vs {other.name!r}")
        return self.quantity < other.quantity
