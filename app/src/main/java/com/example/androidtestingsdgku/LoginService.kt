package com.example.androidtestingsdgku

// Tightly coupled LoginService with UserStore, making it hard to test in isolation.
class LoginService(private val store: UserRepository = UserStore()) {
    fun login(email: String, password: String): LoginResult {

        LoginValidator.validate(email, password)?.let {
            return LoginResult.Invalid(it)
        }

        return if (store.passwordFor(email.trim()) == password) {
            LoginResult.Success
        } else {
            LoginResult.WrongCredentials
        }
    }
}