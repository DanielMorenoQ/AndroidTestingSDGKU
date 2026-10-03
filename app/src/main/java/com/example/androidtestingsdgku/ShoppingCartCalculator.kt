package com.example.androidtestingsdgku

class ShoppingCartCalculator {

    private val items: MutableList<Item> = mutableListOf()
    fun subtotal(): Double {
        var subtotal = 0.0
        for (item in items) {
            subtotal += item.price
        }

        if (subtotal > 300) {
            subtotal *= 0.8 // Apply 20% discount
        } else if (subtotal > 200) {
            subtotal *= 0.9 // Apply 10% discount
        }

        return subtotal
    }
    fun addItem(item: Item) {
        items.add(item)
    }

    fun removeItem(item: Item) {
        items.remove(item)
    }
}

data class Item(val name: String, val price: Double)
