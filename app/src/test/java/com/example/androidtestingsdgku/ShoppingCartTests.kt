package com.example.androidtestingsdgku

import junit.framework.TestCase.assertEquals
import org.junit.Test

/**
 * 1. Create a Shopping Cart
 *  * if the shopping cart is empty return 0
 * 2. I want to be able to add items to my shopping cart
 * 3. I want to be able to remove items from my shopping cart
 * 4. I should be able to calculate the subtotal of my shopping cart
 *    calculate the subtotal of all items
 *    apply a discount of 10% if subtotal is Greater than 200 and 20% if is Greater than 300
 */

class ShoppingCartTests {

    // RED- > GREEN -> REFACTOR
    @Test
    fun emptyCartReturnsZero() {
        val cart = ShoppingCartCalculator()
        assert(cart.subtotal() == 0.0)
    }

    @Test
    fun addItemToCart() {
        val cart = ShoppingCartCalculator()
        cart.addItem(Item("Mouse", 100.0))
        assert(cart.subtotal() == 100.0)
    }

    @Test
    fun removeItemFromCart() {
        val cart = ShoppingCartCalculator()
        val item = Item("Mouse", 100.0)
        cart.addItem(item)
        cart.removeItem(item)
        assert(cart.subtotal() == 0.0)
    }

    @Test
    fun calculateSubtotalWithDiscounts() {
        val cart = ShoppingCartCalculator()
        cart.addItem(Item("Mouse", 100.0))
        cart.addItem(Item("Keyboard", 100.0))
        assert(cart.subtotal() == 200.0) // No discount applied
    }

    @Test
    fun calculateSubtotalWith10PercentDiscount() {
        val cart = ShoppingCartCalculator()
        cart.addItem(Item("Mouse", 150.0))
        cart.addItem(Item("Keyboard", 100.0))
        assert(cart.subtotal() == 225.0) // 10% discount applied
    }

    @Test
    fun calculateSubtotalWith20PercentDiscount() {
        val cart = ShoppingCartCalculator()
        cart.addItem(Item("Mouse", 200.0))
        cart.addItem(Item("Keyboard", 150.0))
        assert(cart.subtotal() == 280.0) // 20% discount applied
    }
}