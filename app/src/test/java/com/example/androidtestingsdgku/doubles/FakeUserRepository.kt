package com.example.androidtestingsdgku.doubles

import com.example.androidtestingsdgku.UserRepository

class FakeUserRepository : UserRepository {
    private val users = mutableMapOf<String, String>()

    fun withUser(email: String, password: String) = apply {
        users[email] = password
    }

    override fun passwordFor(email: String): String? {
        return users[email]
    }
}