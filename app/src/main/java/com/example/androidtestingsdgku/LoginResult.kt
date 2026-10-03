package com.example.androidtestingsdgku

interface LoginResult {
    object Success : LoginResult
    object WrongCredentials : LoginResult
    data class Invalid(val error: LoginValidator.LoginError) : LoginResult
}

