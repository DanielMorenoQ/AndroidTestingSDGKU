package com.example.androidtestingsdgku

import android.content.Intent
import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.google.android.material.button.MaterialButton
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout

class MainActivity : AppCompatActivity() {
    val loginService: LoginService = LoginService()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val inputEmail = findViewById<TextInputEditText>(R.id.emailInput)
        val inputPassword = findViewById<TextInputEditText>(R.id.passwordInput)

        val titleEmail = findViewById<TextInputLayout>(R.id.emailTitle)
        val titlePassword = findViewById<TextInputLayout>(R.id.passwordTitle)

        val loginButton = findViewById<MaterialButton>(R.id.loginButton)

        // For testing purposes, we can skip the login and go directly to the shop
        goToShop()

        loginButton.setOnClickListener {
            titleEmail.error = null
            titlePassword.error = null

            val email = inputEmail.text.toString()
            val password = inputPassword.text.toString()

            loginService.login(email, password).let { result ->
                when (result) {
                    is LoginResult.Success -> goToShop()
                    is LoginResult.WrongCredentials -> {
                        titleEmail.error = "Wrong credentials"
                        titlePassword.error = "Wrong credentials"
                    }
                    is LoginResult.Invalid -> {
                        when (result.error) {
                            LoginValidator.LoginError.EMPTY_EMAIL -> titleEmail.error = "Email is required"
                            LoginValidator.LoginError.INVALID_EMAIL -> titleEmail.error = "Email is invalid"
                            LoginValidator.LoginError.SHORT_PASSWORD -> titlePassword.error = "Password must be at least 8 characters"
                        }
                    }
                }
            }
        }
    }

    fun goToShop() {
        startActivity(Intent(this, ShopActivity::class.java))
    }
}