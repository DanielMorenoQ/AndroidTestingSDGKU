package com.example.androidtestingsdgku

import android.widget.Button
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHost
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController

data class Product(val id: String, val name: String, val price: Double)

private val products = listOf(
    Product("1", "Mouse", 10.0),
    Product("2", "Keyboard", 20.0),
    Product("3", "Monitor", 30.0),
    Product("4", "Laptop", 40.0),
    Product("5", "Headphones", 50.0),
)

@Composable
fun ShopApp() {
    val nav = rememberNavController()
    var quantities by rememberSaveable() { mutableStateOf(mutableMapOf<String, Int>()) }
    val entry by nav.currentBackStackEntryAsState()
    val inCart = entry?.destination?.route == "cart"
    val itemCount = quantities.values.sum()
    val totalPrice = products.sumOf { product -> product.price * (quantities[product.id] ?: 0) }

    Scaffold(topBar = {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            if (inCart) {
                IconButton(
                    onClick = {
                        nav.popBackStack()
                    },
                    modifier = Modifier.testTag("back_to_shop_button")
                ) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back to Shop")
                }
            }
            Text(
                text = if (inCart) "Cart" else "Shop",
                style = MaterialTheme.typography.titleLarge,
                modifier = Modifier
                    .weight(1f)
                    .testTag(
                        if (inCart) "cart_title" else "shop_title"
                    )
            )

            if (!inCart) {
                Button (
                    onClick = {
                        nav.navigate("cart") {
                            launchSingleTop = true
                        }
                    },
                    modifier = Modifier.testTag("go_to_cart_button")
                ) {
                    Text("Cart ($itemCount)", modifier = Modifier.testTag("cart_item_count"))
                }
            }
        }

    }, bottomBar = {
        if (inCart) {
            Text(
                text = "Total items: $itemCount, Total price: $${"%.2f".format(totalPrice)}",
                modifier = Modifier.padding(16.dp)
            )
        }
    }) { padding ->
        NavHost(
            navController = nav,
            startDestination = "shop",
            modifier = Modifier
                .padding(padding)
                .fillMaxWidth()
        ) {
            composable("shop") {
                LazyColumn(Modifier
                    .fillMaxSize()
                    .testTag("product_list")) {
                    items(products) { product ->
                        Column(Modifier
                            .fillMaxWidth()
                            .padding(16.dp)) {
                            Text(product.name, style = MaterialTheme.typography.titleMedium)
                            Text("$${product.price}", style = MaterialTheme.typography.bodyMedium)
                            Button(
                                onClick = {
                                    quantities = HashMap(quantities).apply {
                                        put(product.id, (get(product.id) ?: 0) + 1)
                                    }
                                },
                                modifier = Modifier
                                    .testTag("add_${product.id}")
                                    .padding(top = 8.dp)
                            ) {
                                Text("Add ${product.name}")
                            }
                        }
                        HorizontalDivider()
                    }
                }
            }
            composable("cart") {
                val selectedProducts = products.filter { quantities[it.id] ?: 0 > 0 }
                if (selectedProducts.isEmpty()) {
                    Text(
                        "Your cart is empty",
                        modifier = Modifier
                            .padding(16.dp)
                            .testTag("empty_cart")
                    )
                }
                LazyColumn(Modifier
                    .fillMaxSize()
                    .testTag("cart_list")) {
                    items(selectedProducts) { product ->
                        val quantity = quantities[product.id] ?: 0
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(product.name, style = MaterialTheme.typography.titleMedium)
                            Text(
                                "Quantity: $quantity",
                                style = MaterialTheme.typography.bodyMedium,
                                modifier = Modifier.testTag("quantity_${product.id}")
                            )
                        }
                        HorizontalDivider()
                    }
                }
            }
        }
    }

//    LazyColumn {
//        items(products) { product ->
//            Text(text = "${product.name} - $${product.price}")
//        }
//    }
}