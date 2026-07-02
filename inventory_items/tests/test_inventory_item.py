"""Tests for the InventoryItem class."""

import unittest

from inventory_items.inventory_item import InventoryItem


class TestInventoryItemConstruction(unittest.TestCase):
    """Basic construction and representation."""

    def test_stores_name_and_quantity(self):
        item = InventoryItem("apple", 10)
        self.assertEqual(item.name, "apple")
        self.assertEqual(item.quantity, 10)

    def test_repr_is_reconstructible(self):
        item = InventoryItem("apple", 10)
        self.assertEqual(
            repr(item), "InventoryItem(name='apple', quantity=10)")


class TestInventoryItemAddition(unittest.TestCase):
    """Behavior of the + operator."""

    def test_add_same_name_sums_quantity(self):
        result = InventoryItem("apple", 10) + InventoryItem("apple", 5)
        self.assertEqual(result, InventoryItem("apple", 15))

    def test_add_returns_new_instance(self):
        a = InventoryItem("apple", 10)
        b = InventoryItem("apple", 5)
        result = a + b
        self.assertIsNot(result, a)
        self.assertIsNot(result, b)
        self.assertEqual(a.quantity, 10)  # originals unchanged
        self.assertEqual(b.quantity, 5)

    def test_add_different_names_raises(self):
        with self.assertRaises(ValueError):
            InventoryItem("apple", 10) + InventoryItem("banana", 5)

    def test_add_non_item_returns_not_implemented(self):
        # Python converts NotImplemented into a TypeError at the operator level.
        with self.assertRaises(TypeError):
            InventoryItem("apple", 10) + 5


class TestInventoryItemSubtraction(unittest.TestCase):
    """Behavior of the - operator."""

    def test_sub_same_name_subtracts_quantity(self):
        result = InventoryItem("apple", 10) - InventoryItem("apple", 3)
        self.assertEqual(result, InventoryItem("apple", 7))

    def test_sub_to_zero(self):
        result = InventoryItem("apple", 5) - InventoryItem("apple", 5)
        self.assertEqual(result.quantity, 0)

    def test_sub_negative_result_raises(self):
        with self.assertRaises(ValueError):
            InventoryItem("apple", 3) - InventoryItem("apple", 10)

    def test_sub_different_names_raises(self):
        with self.assertRaises(ValueError):
            InventoryItem("apple", 10) - InventoryItem("banana", 5)

    def test_sub_non_item_returns_not_implemented(self):
        with self.assertRaises(TypeError):
            InventoryItem("apple", 10) - 5


class TestInventoryItemMultiplication(unittest.TestCase):
    """Behavior of the * operator."""

    def test_mul_by_positive_int(self):
        result = InventoryItem("apple", 10) * 3
        self.assertEqual(result, InventoryItem("apple", 30))

    def test_mul_by_zero(self):
        result = InventoryItem("apple", 10) * 0
        self.assertEqual(result.quantity, 0)

    def test_mul_by_negative_raises(self):
        with self.assertRaises(ValueError):
            InventoryItem("apple", 10) * -1

    def test_mul_by_bool_returns_not_implemented(self):
        # bool is a subclass of int, but multiplying by True/False makes no sense here.
        with self.assertRaises(TypeError):
            InventoryItem("apple", 10) * True

    def test_mul_by_float_returns_not_implemented(self):
        with self.assertRaises(TypeError):
            InventoryItem("apple", 10) * 1.5

    def test_mul_by_string_returns_not_implemented(self):
        with self.assertRaises(TypeError):
            InventoryItem("apple", 10) * "3"


class TestInventoryItemEquality(unittest.TestCase):
    """Behavior of == and !=."""

    def test_equal_when_name_and_quantity_match(self):
        self.assertEqual(InventoryItem("apple", 10),
                         InventoryItem("apple", 10))

    def test_not_equal_when_names_differ(self):
        self.assertNotEqual(InventoryItem("apple", 10),
                            InventoryItem("banana", 10))

    def test_not_equal_when_quantities_differ(self):
        self.assertNotEqual(InventoryItem("apple", 10),
                            InventoryItem("apple", 5))

    def test_not_equal_to_other_types(self):
        item = InventoryItem("apple", 10)
        self.assertNotEqual(item, "apple")
        self.assertNotEqual(item, 10)
        self.assertNotEqual(item, None)


class TestInventoryItemOrdering(unittest.TestCase):
    """Behavior of <, >, <=, >= (via total_ordering)."""

    def test_less_than_same_name(self):
        self.assertLess(InventoryItem("apple", 3), InventoryItem("apple", 10))

    def test_greater_than_same_name(self):
        self.assertGreater(InventoryItem("apple", 10),
                           InventoryItem("apple", 3))

    def test_less_or_equal_generated_by_total_ordering(self):
        self.assertLessEqual(InventoryItem("apple", 5),
                             InventoryItem("apple", 5))
        self.assertLessEqual(InventoryItem("apple", 3),
                             InventoryItem("apple", 5))

    def test_greater_or_equal_generated_by_total_ordering(self):
        self.assertGreaterEqual(InventoryItem(
            "apple", 5), InventoryItem("apple", 5))
        self.assertGreaterEqual(InventoryItem(
            "apple", 10), InventoryItem("apple", 5))

    def test_compare_different_names_raises(self):
        with self.assertRaises(ValueError):
            _ = InventoryItem("apple", 10) < InventoryItem("banana", 5)

    def test_compare_with_non_item_returns_not_implemented(self):
        with self.assertRaises(TypeError):
            _ = InventoryItem("apple", 10) < 5


class TestInventoryItemHashability(unittest.TestCase):
    """The class is intentionally unhashable."""

    def test_cannot_be_used_in_set(self):
        with self.assertRaises(TypeError):
            {InventoryItem("apple", 10)}

    def test_cannot_be_used_as_dict_key(self):
        with self.assertRaises(TypeError):
            {InventoryItem("apple", 10): "value"}


if __name__ == "__main__":
    unittest.main()
