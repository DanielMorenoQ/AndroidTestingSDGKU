package com.example.androidtestingsdgku

import com.example.androidtestingsdgku.doubles.FakeUserRepository
import io.mockk.confirmVerified
import io.mockk.every
import io.mockk.mockk
import io.mockk.verify
import org.junit.Assert.assertEquals
import org.junit.Test

class LoginServiceTestDoubles {


    // Test with a FAKE user repository to simulate the behavior of the real repository
    @Test
    fun testLoginWithValidCredentials() {
        // Arrange
        val repo = FakeUserRepository().withUser("testuser@123.com", "password123")
        val loginService = LoginService(repo)

        // Act
        val result = loginService.login("testuser@123.com", "password123")

        // Assert
        assertEquals(LoginResult.Success, result)
    }

    // Test with STUB user repository to simulate the behavior of the real repository
    @Test
    fun testWrongPasswordReturnsWrongCredentials() {

        // Arrange
        val repo = mockk<UserRepository>()
        // Stub the passwordFor method to return a specific password for a given email
        every { repo.passwordFor("testuser@123.com") } returns "password123"

        val service = LoginService(repo)

        // Act
        val result = service.login("testuser@123.com", "wrongpassword")

        // Assert
        assertEquals(LoginResult.WrongCredentials, result)
    }

    @Test
    fun invalidEmailNeverCallsRepository() {
        // Arrange
        val repo = mockk<UserRepository>()

        // Act
        LoginService(repo).login("invalid-email", "password123")

        // Assert
        // Verify that the passwordFor method was never called due to invalid email
        verify(exactly = 0) { repo.passwordFor(any()) }
        confirmVerified(repo)
    }

    @Test
    fun validAttemptLooksUpOnceWithTrimmedEmail() {
        // Arrange
        val repo = mockk<UserRepository>()
        every { repo.passwordFor("testuser@123.com") } returns "password123"

        val service = LoginService(repo)

        // Act
        service.login("  testuser@123.com ", "password123")

        // Assert
        verify(exactly = 1) { repo.passwordFor("testuser@123.com") }
        confirmVerified(repo)
    }
}

// FAKE, STUB, MOCK