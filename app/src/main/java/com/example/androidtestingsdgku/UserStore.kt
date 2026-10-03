package com.example.androidtestingsdgku

class UserStore : UserRepository{
    // Hardcoded user credentials for demonstration purposes
    // This is a real database in a real application, but for this example, we will use a simple map.
    val users = mapOf("tom@example.com" to "password123")
    override fun passwordFor(email: String): String? {
        return users[email]
    }
}
