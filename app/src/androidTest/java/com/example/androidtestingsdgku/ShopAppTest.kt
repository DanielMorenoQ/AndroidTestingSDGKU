package com.example.androidtestingsdgku

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.assertTextEquals
import androidx.compose.ui.test.hasTestTag
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollToNode
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class ShopAppTest {
    @get:Rule
    val composeRule = createAndroidComposeRule<ShopActivity>()

    @Test
    fun shoppingCartShowsAllElements() {
        composeRule.onNodeWithTag("shop_title").assertIsDisplayed()
        composeRule.onNodeWithTag("cart_item_count", useUnmergedTree = true)
            .assertTextEquals("Cart (0)")

        composeRule.onNodeWithTag("go_to_cart_button").performClick()

        composeRule.onNodeWithTag("cart_title").assertIsDisplayed()
        composeRule.onNodeWithTag("empty_cart").assertIsDisplayed()
    }

    @Test
    fun shopStartsWithEmptyCart() {
        composeRule.onNodeWithTag("shop_title").assertIsDisplayed()
        composeRule.onNodeWithTag("cart_item_count", useUnmergedTree = true)
            .assertTextEquals("Cart (0)")

        composeRule.onNodeWithTag("go_to_cart_button").performClick()

        composeRule.onNodeWithTag("cart_title").assertIsDisplayed()
        composeRule.onNodeWithTag("empty_cart").assertIsDisplayed()
    }

    @Test
    fun addingProductTwice_preservesQuantityAcrossNavigation() {
        composeRule.onNodeWithTag("product_list")
            .performScrollToNode(hasTestTag("add_1"))
        composeRule.onNodeWithTag("add_1").performClick()
        composeRule.onNodeWithTag("add_1").performClick()
        composeRule.onNodeWithTag("cart_item_count", useUnmergedTree = true)
            .assertTextEquals("Cart (2)")

        composeRule.onNodeWithTag("go_to_cart_button").performClick()

        composeRule.onNodeWithTag("cart_title").assertIsDisplayed()
        composeRule.onNodeWithTag("quantity_1").assertTextEquals("Quantity: 2")

        composeRule.onNodeWithTag("back_to_shop_button").performClick()

        composeRule.onNodeWithTag("shop_title").assertIsDisplayed()
        composeRule.onNodeWithTag("cart_item_count", useUnmergedTree = true)
            .assertTextEquals("Cart (2)")
        composeRule.onNodeWithTag("go_to_cart_button").performClick()
        composeRule.onNodeWithTag("quantity_1").assertTextEquals("Quantity: 2")
    }
}