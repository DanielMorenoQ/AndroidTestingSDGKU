package com.example.androidtestingsdgku

import org.junit.Test
import org.junit.Assert.assertEquals;

class LoginValidatorTests {

    @Test fun emptyEmail() {
        assertEquals(LoginValidator.LoginError.EMPTY_EMAIL, LoginValidator.validate("", "daniel"))
    }

    @Test fun invalidEmail() {
        assertEquals(LoginValidator.LoginError.INVALID_EMAIL, LoginValidator.validate("daniel", "daniel"))
    }

    @Test fun shortPassword() {
        assertEquals(LoginValidator.LoginError.SHORT_PASSWORD, LoginValidator.validate("daniel@example.com", "daniel"))
    }

    @Test fun validEmailAndPassword() {
        assertEquals(null, LoginValidator.validate("daniel@example.com", "daniel123"))
    }
}