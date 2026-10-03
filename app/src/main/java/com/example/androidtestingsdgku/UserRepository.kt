package com.example.androidtestingsdgku


// Allows for dependency injection of the user repository, making it easier to test the LoginService in isolation.
interface UserRepository {
    fun passwordFor(email: String): String?
}