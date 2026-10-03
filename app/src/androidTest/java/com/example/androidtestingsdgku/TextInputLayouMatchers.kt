package com.example.androidtestingsdgku

import android.view.View
import com.google.android.material.textfield.TextInputLayout
import org.hamcrest.Description
import org.hamcrest.Matcher
import org.hamcrest.TypeSafeMatcher

object TextInputLayoutMatchers {

    fun hasTextInputLayoutError(expected: String): Matcher<View> =
        object : TypeSafeMatcher<View>() {

            override fun describeTo(description: Description) {
                description.appendText("TextInputLayout with error: $expected")
            }

            override fun matchesSafely(view: View): Boolean {
                if (view !is TextInputLayout) return false
                return view.error?.toString() == expected
            }
        }

    fun hasNoTextInputLayoutError(): Matcher<View> =
        object : TypeSafeMatcher<View>() {
            override fun describeTo(description: Description) {
                description.appendText("TextInputLayout with no error")
            }

            override fun matchesSafely(view: View): Boolean =
                view is TextInputLayout && view.error.isNullOrEmpty()
        }
}

