package com.example.androidtestingsdgku

import androidx.test.core.app.ActivityScenario
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.click
import androidx.test.espresso.action.ViewActions.typeText
import androidx.test.espresso.assertion.ViewAssertions.doesNotExist
import androidx.test.espresso.intent.Intents
import androidx.test.espresso.matcher.ViewMatchers.withId
import org.junit.runner.RunWith
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.After
import org.junit.Before
import org.junit.Test
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.hasErrorText
import androidx.test.espresso.matcher.ViewMatchers.isDisplayed
import com.example.androidtestingsdgku.TextInputLayoutMatchers.hasTextInputLayoutError
import org.hamcrest.CoreMatchers.not

class LoginPage {
    val emailTitle = onView(withId(R.id.emailTitle))
    val passwordTitle = onView(withId(R.id.passwordTitle))
    val emailInput = onView(withId(R.id.emailInput))
    val passwordInput = onView(withId(R.id.passwordInput))
    val loginButton = onView(withId(R.id.loginButton))
}

@RunWith(AndroidJUnit4::class)
class LoginViewTest {

    private lateinit var scenario: ActivityScenario<MainActivity>
    private val loginPage = LoginPage()

    @Before
    fun setUp() {
        Intents.init()
        scenario = ActivityScenario.launch(MainActivity::class.java)
    }

    @After
    fun tearDown() {
        scenario.close()
        Intents.release()
    }

    @Test
    fun loginScreen_showsAllComponents() {
        loginPage.emailTitle.check(matches(isDisplayed()))
        loginPage.passwordTitle.check(matches(isDisplayed()))
        loginPage.emailInput.check(matches(isDisplayed()))
        loginPage.passwordInput.check(matches(isDisplayed()))
        loginPage.loginButton.check(matches(isDisplayed()))
    }

    @Test
    fun emptyEmail_showsError() {
        loginPage.loginButton.perform(click())
        loginPage.emailTitle.check(matches(hasTextInputLayoutError("Email is required")))
    }

    @Test
    fun loginWithValidCredentials_navigatesToShop() {
        loginPage.emailInput.perform(typeText("tom@example.com"))
        loginPage.passwordInput.perform(typeText("password123"))
        loginPage.loginButton.perform(click())
        loginPage.emailTitle.check(doesNotExist())
    }
}