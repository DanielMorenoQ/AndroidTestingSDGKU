package com.example.androidtestingsdgku

object LoginValidator {

    enum class LoginError { EMPTY_EMAIL, INVALID_EMAIL, SHORT_PASSWORD }
    private val emailRegex = Regex("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$")

    fun validate(email: String, password: String): LoginError? {
        return when {
            email.isBlank() -> LoginError.EMPTY_EMAIL
            !emailRegex.matches(email.trim()) -> LoginError.INVALID_EMAIL
            password.length < 8 -> LoginError.SHORT_PASSWORD
            else -> null
        }
    }
}