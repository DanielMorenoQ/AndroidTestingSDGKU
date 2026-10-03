# Course Script — XML Views, Espresso & TDD

**Project:** `AndroidTestingSDGKU`
**Package:** `com.example.androidtestingsdgku`
**Modules used:** XML Views (ConstraintLayout + Material), Espresso (instrumented + Robolectric), JUnit4.

> Pending item from last session: *test an XML View with Espresso*.
> This script closes that gap and then transitions into a full TDD exercise (Shopping Cart).

---

## Agenda

| # | Topic | Type | Est. |
|---|-------|------|------|
| 1 | Creating an XML Login View | Live coding | 20 min |
| 2 | Navigation on successful login | Live coding | 15 min |
| 3 | Testing the View with Espresso | Live coding + lab | 30 min |
| 4 | The Shop screen (items list) | Live coding | 20 min |
| 5 | Checkout — Shopping Cart via TDD | Lab (red/green/refactor) | 45 min |

---

## Prerequisites check (2 min, do before class)

```bash
./gradlew :app:testDebugUnitTest --tests "com.example.androidtestingsdgku.LoginValidatorTests"
```

Everything green? Good — we already have `LoginValidator` with unit tests. Today we put a **UI** on top of it.

Talking point: *"We have logic tested. We do NOT have the view tested. That's today's first goal."*

---

# 1. Creating an XML Login View

### 1.1 Say this

> "We're using XML Views, not Compose, because Espresso is the classic View-testing tool and most legacy Android code you'll touch in the industry is XML."

### 1.2 Add strings

`app/src/main/res/values/strings.xml`

```xml
<resources>
    <string name="app_name">AndroidTestingSDGKU</string>

    <string name="login_title">Sign in</string>
    <string name="hint_email">Email</string>
    <string name="hint_password">Password</string>
    <string name="action_login">Login</string>

    <string name="error_empty_email">Email is required</string>
    <string name="error_invalid_email">Email format is invalid</string>
    <string name="error_short_password">Password must be at least 8 characters</string>
</resources>
```

### 1.3 Replace the layout

`app/src/main/res/layout/activity_main.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="24dp"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/titleLogin"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/login_title"
        android:textSize="28sp"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginTop="64dp" />

    <com.google.android.material.textfield.TextInputLayout
        android:id="@+id/tilEmail"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:hint="@string/hint_email"
        android:layout_marginTop="32dp"
        app:layout_constraintTop_toBottomOf="@id/titleLogin"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent">

        <com.google.android.material.textfield.TextInputEditText
            android:id="@+id/inputEmail"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:inputType="textEmailAddress"
            android:imeOptions="actionNext" />
    </com.google.android.material.textfield.TextInputLayout>

    <com.google.android.material.textfield.TextInputLayout
        android:id="@+id/tilPassword"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:hint="@string/hint_password"
        android:layout_marginTop="16dp"
        app:endIconMode="password_toggle"
        app:layout_constraintTop_toBottomOf="@id/tilEmail"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent">

        <com.google.android.material.textfield.TextInputEditText
            android:id="@+id/inputPassword"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:inputType="textPassword"
            android:imeOptions="actionDone" />
    </com.google.android.material.textfield.TextInputLayout>

    <com.google.android.material.button.MaterialButton
        android:id="@+id/buttonLogin"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:text="@string/action_login"
        android:layout_marginTop="24dp"
        app:layout_constraintTop_toBottomOf="@id/tilPassword"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
```

### 1.4 Teaching notes

- **Every testable widget needs an `android:id`.** Espresso's primary matcher is `withId()`. No id → no test.
- `TextInputLayout` owns the **error**, `TextInputEditText` owns the **text**. This matters in step 3: we assert errors on `tilEmail`, not on `inputEmail`.
- Ask the class: *"Where would you put the validation logic?"* → Answer: not in the Activity. In `LoginValidator`, which is already unit-tested.

---

# 2. Add navigation to the next view when login and pass are correct

### 2.1 Say this

> "The Activity's only job is: read input → ask the validator → either show an error or navigate. That's it. That's what we assert with Espresso."

### 2.2 Map errors to strings

`app/src/main/java/com/example/androidtestingsdgku/MainActivity.kt`

```kotlin
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

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val bars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(bars.left, bars.top, bars.right, bars.bottom)
            insets
        }

        val tilEmail: TextInputLayout = findViewById(R.id.tilEmail)
        val tilPassword: TextInputLayout = findViewById(R.id.tilPassword)
        val inputEmail: TextInputEditText = findViewById(R.id.inputEmail)
        val inputPassword: TextInputEditText = findViewById(R.id.inputPassword)
        val buttonLogin: MaterialButton = findViewById(R.id.buttonLogin)

        buttonLogin.setOnClickListener {
            tilEmail.error = null
            tilPassword.error = null

            val email = inputEmail.text?.toString().orEmpty()
            val password = inputPassword.text?.toString().orEmpty()

            when (LoginValidator.validate(email, password)) {
                LoginValidator.LoginError.EMPTY_EMAIL ->
                    tilEmail.error = getString(R.string.error_empty_email)

                LoginValidator.LoginError.INVALID_EMAIL ->
                    tilEmail.error = getString(R.string.error_invalid_email)

                LoginValidator.LoginError.SHORT_PASSWORD ->
                    tilPassword.error = getString(R.string.error_short_password)

                null -> goToShop()
            }
        }
    }

    private fun goToShop() {
        startActivity(Intent(this, ShopActivity::class.java))
    }
}
```

### 2.3 Create the destination (stub for now)

`app/src/main/java/com/example/androidtestingsdgku/ShopActivity.kt`

```kotlin
package com.example.androidtestingsdgku

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class ShopActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_shop)
    }
}
```

Register it in `AndroidManifest.xml`, inside `<application>`:

```xml
<activity android:name=".ShopActivity" />
```

> **Gotcha to call out:** forgetting the manifest entry throws `ActivityNotFoundException` at click time — and Espresso will catch it for you. Demo it on purpose if time allows.

### 2.4 Discussion (3 min)

> "Why an `Intent` and not Navigation Component? Because for testing we only care about the *observable outcome*: an Intent was fired. Espresso-Intents can assert that without ever launching the second screen."

---

# 3. Do testing on the View with Espresso

### 3.1 Dependencies

Add to `gradle/libs.versions.toml` under `[libraries]`:

```toml
androidx-espresso-intents = { group = "androidx.test.espresso", name = "espresso-intents", version.ref = "espressoCore" }
androidx-espresso-contrib = { group = "androidx.test.espresso", name = "espresso-contrib", version.ref = "espressoCore" }
androidx-test-core = { group = "androidx.test", name = "core", version = "1.7.0" }
```

Add to `app/build.gradle.kts`:

```kotlin
androidTestImplementation(libs.androidx.espresso.intents)
androidTestImplementation(libs.androidx.espresso.contrib)
androidTestImplementation(libs.androidx.test.core)

testImplementation(libs.androidx.espresso.intents)
testImplementation(libs.androidx.test.core)
```

Turn off animations on the test device (emulator → Developer options → Window/Transition/Animator scale = off). Explain: **Espresso's idling breaks with animations on.**

### 3.2 The Espresso mental model — write on the board

```
onView( MATCHER )        →  find the view
      .perform( ACTION ) →  do something to it
      .check( ASSERTION )→  verify something about it
```

| Matchers | Actions | Assertions |
|---|---|---|
| `withId()`, `withText()`, `withHint()` | `click()`, `typeText()`, `replaceText()`, `closeSoftKeyboard()`, `scrollTo()` | `matches(isDisplayed())`, `matches(withText(...))`, `doesNotExist()` |

Key point: **Espresso synchronizes with the UI thread automatically.** No `Thread.sleep()`. Ever.

### 3.3 Custom matcher for TextInputLayout errors

Espresso has no built-in error matcher for `TextInputLayout`. Write one — great teaching moment.

`app/src/androidTest/java/com/example/androidtestingsdgku/TextInputLayoutMatchers.kt`

```kotlin
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
```

### 3.4 The test class

`app/src/androidTest/java/com/example/androidtestingsdgku/LoginViewTest.kt`

```kotlin
package com.example.androidtestingsdgku

import androidx.test.core.app.ActivityScenario
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.click
import androidx.test.espresso.action.ViewActions.closeSoftKeyboard
import androidx.test.espresso.action.ViewActions.replaceText
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.intent.Intents
import androidx.test.espresso.intent.matcher.IntentMatchers.hasComponent
import androidx.test.espresso.matcher.ViewMatchers.isDisplayed
import androidx.test.espresso.matcher.ViewMatchers.withId
import androidx.test.espresso.matcher.ViewMatchers.withText
import androidx.test.ext.junit.runners.AndroidJUnit4
import com.example.androidtestingsdgku.TextInputLayoutMatchers.hasNoTextInputLayoutError
import com.example.androidtestingsdgku.TextInputLayoutMatchers.hasTextInputLayoutError
import org.junit.After
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class LoginViewTest {

    private lateinit var scenario: ActivityScenario<MainActivity>

    @Before
    fun setUp() {
        Intents.init()
        scenario = ActivityScenario.launch(MainActivity::class.java)
    }

    @After
    fun tearDown() {
        scenario.close()
        Intents.release()
    }

    // --- Rendering -------------------------------------------------------

    @Test
    fun loginScreen_showsAllWidgets() {
        onView(withId(R.id.titleLogin)).check(matches(isDisplayed()))
        onView(withId(R.id.inputEmail)).check(matches(isDisplayed()))
        onView(withId(R.id.inputPassword)).check(matches(isDisplayed()))
        onView(withId(R.id.buttonLogin))
            .check(matches(isDisplayed()))
            .check(matches(withText("Login")))
    }

    // --- Validation errors ----------------------------------------------

    @Test
    fun emptyEmail_showsEmptyEmailError() {
        onView(withId(R.id.buttonLogin)).perform(click())

        onView(withId(R.id.tilEmail))
            .check(matches(hasTextInputLayoutError("Email is required")))
    }

    @Test
    fun malformedEmail_showsInvalidEmailError() {
        onView(withId(R.id.inputEmail)).perform(replaceText("daniel"), closeSoftKeyboard())
        onView(withId(R.id.inputPassword)).perform(replaceText("password123"), closeSoftKeyboard())

        onView(withId(R.id.buttonLogin)).perform(click())

        onView(withId(R.id.tilEmail))
            .check(matches(hasTextInputLayoutError("Email format is invalid")))
    }

    @Test
    fun shortPassword_showsShortPasswordError() {
        onView(withId(R.id.inputEmail)).perform(replaceText("daniel@example.com"), closeSoftKeyboard())
        onView(withId(R.id.inputPassword)).perform(replaceText("123"), closeSoftKeyboard())

        onView(withId(R.id.buttonLogin)).perform(click())

        onView(withId(R.id.tilPassword))
            .check(matches(hasTextInputLayoutError("Password must be at least 8 characters")))
        onView(withId(R.id.tilEmail)).check(matches(hasNoTextInputLayoutError()))
    }

    // --- Navigation ------------------------------------------------------

    @Test
    fun validCredentials_navigatesToShop() {
        onView(withId(R.id.inputEmail)).perform(replaceText("daniel@example.com"), closeSoftKeyboard())
        onView(withId(R.id.inputPassword)).perform(replaceText("password123"), closeSoftKeyboard())

        onView(withId(R.id.buttonLogin)).perform(click())

        Intents.intended(hasComponent(ShopActivity::class.java.name))
    }

    @Test
    fun invalidCredentials_doesNotNavigate() {
        onView(withId(R.id.inputEmail)).perform(replaceText("daniel"), closeSoftKeyboard())
        onView(withId(R.id.inputPassword)).perform(replaceText("123"), closeSoftKeyboard())

        onView(withId(R.id.buttonLogin)).perform(click())

        Intents.assertNoUnverifiedIntents()
    }
}
```

### 3.5 Run it

```bash
./gradlew :app:connectedDebugAndroidTest \
  --tests "com.example.androidtestingsdgku.LoginViewTest"
```

HTML report: `app/build/reports/androidTests/connected/debug/index.html`

### 3.6 Bonus — the same test without an emulator (Robolectric)

We already have Robolectric configured (`ToggleButtonRoboTests.kt`, `isIncludeAndroidResources = true`). Espresso APIs work under Robolectric for Views:

`app/src/test/java/com/example/androidtestingsdgku/LoginViewRoboTest.kt`

```kotlin
package com.example.androidtestingsdgku

import androidx.test.core.app.ActivityScenario
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.click
import androidx.test.espresso.action.ViewActions.replaceText
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.isDisplayed
import androidx.test.espresso.matcher.ViewMatchers.withId
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner

@RunWith(RobolectricTestRunner::class)
class LoginViewRoboTest {

    @Test
    fun loginButton_isVisible() {
        ActivityScenario.launch(MainActivity::class.java).use {
            onView(withId(R.id.buttonLogin)).check(matches(isDisplayed()))
        }
    }

    @Test
    fun emptyEmail_showsError() {
        ActivityScenario.launch(MainActivity::class.java).use {
            onView(withId(R.id.inputPassword)).perform(replaceText("password123"))
            onView(withId(R.id.buttonLogin)).perform(click())
            // assert via the activity itself
            it.onActivity { activity ->
                val til = activity.findViewById<com.google.android.material.textfield.TextInputLayout>(R.id.tilEmail)
                assert(til.error == "Email is required")
            }
        }
    }
}
```

```bash
./gradlew :app:testDebugUnitTest --tests "*LoginViewRoboTest"
```

Discussion: *emulator tests = highest fidelity, slowest. Robolectric = fast, JVM, good enough for 80% of View assertions.*

### 3.7 Student lab (10 min)

1. Add a "Forgot password?" `TextView` with id `linkForgotPassword`; assert it is displayed.
2. Assert that after a failed attempt, typing a valid email and clicking again **clears** the email error.
3. Assert the password field is masked (`inputType=textPassword`) — write a custom matcher.

---

# 4. Next screen is a shop with a few items

### 4.1 Domain models

`app/src/main/java/com/example/androidtestingsdgku/shop/Product.kt`

```kotlin
package com.example.androidtestingsdgku.shop

data class Product(
    val id: String,
    val name: String,
    val price: Double
)

object Catalog {
    val items = listOf(
        Product("p1", "Keyboard", 80.0),
        Product("p2", "Mouse", 45.0),
        Product("p3", "Monitor", 180.0),
        Product("p4", "Headset", 120.0),
        Product("p5", "Webcam", 60.0)
    )
}
```

### 4.2 Layouts

`app/src/main/res/layout/activity_shop.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/shopRoot"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:id="@+id/titleShop"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Shop"
        android:textSize="24sp" />

    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/listProducts"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1" />

    <TextView
        android:id="@+id/textSubtotal"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:textSize="20sp"
        android:text="Subtotal: $0.00" />

    <com.google.android.material.button.MaterialButton
        android:id="@+id/buttonCheckout"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Checkout" />
</LinearLayout>
```

`app/src/main/res/layout/item_product.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="horizontal"
    android:gravity="center_vertical"
    android:padding="12dp">

    <TextView
        android:id="@+id/textProductName"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_weight="1" />

    <TextView
        android:id="@+id/textProductPrice"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:paddingEnd="12dp" />

    <com.google.android.material.button.MaterialButton
        android:id="@+id/buttonAdd"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Add" />
</LinearLayout>
```

Add RecyclerView to the catalog + `app/build.gradle.kts`:

```toml
androidx-recyclerview = { group = "androidx.recyclerview", name = "recyclerview", version = "1.4.0" }
```
```kotlin
implementation(libs.androidx.recyclerview)
```

### 4.3 Adapter + Activity (thin — logic lives in the cart)

```kotlin
package com.example.androidtestingsdgku.shop

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.androidtestingsdgku.R

class ProductAdapter(
    private val products: List<Product>,
    private val onAdd: (Product) -> Unit
) : RecyclerView.Adapter<ProductAdapter.VH>() {

    class VH(view: View) : RecyclerView.ViewHolder(view) {
        val name: TextView = view.findViewById(R.id.textProductName)
        val price: TextView = view.findViewById(R.id.textProductPrice)
        val add: View = view.findViewById(R.id.buttonAdd)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) = VH(
        LayoutInflater.from(parent.context).inflate(R.layout.item_product, parent, false)
    )

    override fun getItemCount() = products.size

    override fun onBindViewHolder(holder: VH, position: Int) {
        val product = products[position]
        holder.name.text = product.name
        holder.price.text = "$%.2f".format(product.price)
        holder.add.setOnClickListener { onAdd(product) }
    }
}
```

```kotlin
class ShopActivity : AppCompatActivity() {

    private val cart = ShoppingCart()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_shop)

        val subtotal = findViewById<TextView>(R.id.textSubtotal)
        val list = findViewById<RecyclerView>(R.id.listProducts)

        list.layoutManager = LinearLayoutManager(this)
        list.adapter = ProductAdapter(Catalog.items) { product ->
            cart.add(product)
            subtotal.text = "Subtotal: $%.2f".format(cart.subtotal())
        }
    }
}
```

> **Say this:** "Notice the Activity has zero math in it. All the money logic is in `ShoppingCart`. That's the class we're about to build — test first."

---

# 5. Checkout — Shopping Cart with TDD

### 5.1 The requirements (read them out loud, verbatim)

```
/**
 * 1. Create a Shopping Cart
 *  * if the shopping cart is empty return 0
 * 2. I want to be able to add items to my shopping cart
 * 3. I want to be able to remove items from my shopping cart
 * 4. I should be able to calculate the subtotal of my shopping cart
 *    calculate the subtotal of all items
 *    apply a discount of 10% if subtotal is Greater than 200 and 20% if is Greater than 300
 */
```

### 5.2 The TDD loop — board diagram

```
   ┌──────────┐
   │   RED    │  write a failing test (it must fail for the RIGHT reason)
   └────┬─────┘
        ▼
   ┌──────────┐
   │  GREEN   │  simplest code that passes — even if it's "cheating"
   └────┬─────┘
        ▼
   ┌──────────┐
   │ REFACTOR │  clean up. Tests stay green.
   └────┬─────┘
        └──► repeat
```

Three rules (Uncle Bob):
1. No production code until you have a failing test.
2. No more test than is sufficient to fail.
3. No more production code than is sufficient to pass.

### 5.3 Clarify the ambiguity FIRST (5 min discussion)

Before writing a line, ask the class:

- *"Greater than 200" — is 200.00 exactly discounted?* → No. Strictly greater.
- *Is the discount tiered or a single bracket?* → Single bracket: `>300` → 20%, else `>200` → 10%, else 0%.
- *Does removing an item that isn't there throw, or no-op?* → We decide: **no-op**.
- *Duplicate items?* → We allow them; same product can be added twice.

> **Teaching point:** TDD forces the conversation about requirements *before* the code exists. This is the real value.

---

### Step 0 — RED: empty cart returns 0

`app/src/test/java/com/example/androidtestingsdgku/shop/ShoppingCartTest.kt`

```kotlin
package com.example.androidtestingsdgku.shop

import org.junit.Assert.assertEquals
import org.junit.Test

class ShoppingCartTest {

    private val delta = 0.001

    @Test
    fun `empty cart subtotal is zero`() {
        val cart = ShoppingCart()
        assertEquals(0.0, cart.subtotal(), delta)
    }
}
```

Run → **it does not compile.** Say: *"In TDD, a compile error IS a red test. Our first failure."*

### Step 0 — GREEN

```kotlin
package com.example.androidtestingsdgku.shop

class ShoppingCart {
    fun subtotal(): Double = 0.0
}
```

Green. Yes, it's hardcoded. **That is correct TDD.** Don't let students jump ahead.

---

### Step 1 — RED: add items

```kotlin
@Test
fun `adding one item makes cart size one`() {
    val cart = ShoppingCart()
    cart.add(Product("p1", "Keyboard", 80.0))
    assertEquals(1, cart.itemCount())
}

@Test
fun `adding the same product twice keeps both`() {
    val cart = ShoppingCart()
    val mouse = Product("p2", "Mouse", 45.0)
    cart.add(mouse)
    cart.add(mouse)
    assertEquals(2, cart.itemCount())
}
```

### Step 1 — GREEN

```kotlin
class ShoppingCart {
    private val items = mutableListOf<Product>()

    fun add(product: Product) { items += product }

    fun itemCount(): Int = items.size

    fun subtotal(): Double = 0.0
}
```

---

### Step 2 — RED: remove items

```kotlin
@Test
fun `removing an item decreases the count`() {
    val cart = ShoppingCart()
    val mouse = Product("p2", "Mouse", 45.0)
    cart.add(mouse)
    cart.remove(mouse)
    assertEquals(0, cart.itemCount())
}

@Test
fun `removing removes only one instance`() {
    val cart = ShoppingCart()
    val mouse = Product("p2", "Mouse", 45.0)
    cart.add(mouse)
    cart.add(mouse)
    cart.remove(mouse)
    assertEquals(1, cart.itemCount())
}

@Test
fun `removing an item that is not in the cart does nothing`() {
    val cart = ShoppingCart()
    cart.add(Product("p1", "Keyboard", 80.0))
    cart.remove(Product("p9", "Ghost", 10.0))
    assertEquals(1, cart.itemCount())
}
```

### Step 2 — GREEN

```kotlin
fun remove(product: Product) { items.remove(product) }
```

> `MutableList.remove` removes the *first* match and returns `false` if absent — both tests pass for free. Point out that the test documented the decision.

---

### Step 3 — RED: subtotal with no discount

```kotlin
@Test
fun `subtotal adds up all item prices`() {
    val cart = ShoppingCart()
    cart.add(Product("p1", "Keyboard", 80.0))
    cart.add(Product("p2", "Mouse", 45.0))
    assertEquals(125.0, cart.subtotal(), delta)
}
```

### Step 3 — GREEN

```kotlin
fun subtotal(): Double = items.sumOf { it.price }
```

The hardcoded `0.0` is gone — and the *empty cart returns 0* test still passes, because `sumOf` on an empty list is `0.0`. **Regression safety demonstrated live.**

---

### Step 4 — RED: the discount rules (boundaries!)

```kotlin
@Test
fun `no discount when subtotal is exactly 200`() {
    val cart = cartWorth(200.0)
    assertEquals(200.0, cart.subtotal(), delta)
}

@Test
fun `ten percent discount when subtotal is greater than 200`() {
    val cart = cartWorth(250.0)
    assertEquals(225.0, cart.subtotal(), delta)   // 250 - 10%
}

@Test
fun `ten percent discount when subtotal is exactly 300`() {
    val cart = cartWorth(300.0)
    assertEquals(270.0, cart.subtotal(), delta)   // 300 - 10%
}

@Test
fun `twenty percent discount when subtotal is greater than 300`() {
    val cart = cartWorth(400.0)
    assertEquals(320.0, cart.subtotal(), delta)   // 400 - 20%
}

@Test
fun `discount is recalculated after removing an item`() {
    val cart = ShoppingCart()
    val monitor = Product("p3", "Monitor", 180.0)
    cart.add(monitor)
    cart.add(Product("p4", "Headset", 120.0))     // 300 -> 270
    cart.remove(monitor)                          // 120 -> no discount
    assertEquals(120.0, cart.subtotal(), delta)
}

private fun cartWorth(amount: Double) = ShoppingCart().apply {
    add(Product("x", "Bundle", amount))
}
```

> **Emphasize:** boundary tests at 200 and 300 are where bugs live. `>` vs `>=` is the single most common off-by-one in business rules.

### Step 4 — GREEN

```kotlin
package com.example.androidtestingsdgku.shop

class ShoppingCart {

    private val items = mutableListOf<Product>()

    fun add(product: Product) { items += product }

    fun remove(product: Product) { items.remove(product) }

    fun itemCount(): Int = items.size

    fun items(): List<Product> = items.toList()

    fun clear() = items.clear()

    fun subtotal(): Double {
        val raw = items.sumOf { it.price }
        return raw - (raw * discountRate(raw))
    }

    private fun discountRate(raw: Double): Double = when {
        raw > 300 -> 0.20
        raw > 200 -> 0.10
        else -> 0.0
    }
}
```

### Step 4 — REFACTOR

Now that we're green, clean it up and make the rules explicit:

```kotlin
class ShoppingCart {

    private val items = mutableListOf<Product>()

    fun add(product: Product) { items += product }
    fun remove(product: Product) { items.remove(product) }
    fun itemCount(): Int = items.size
    fun items(): List<Product> = items.toList()
    fun clear() = items.clear()

    /** Sum of item prices, before any discount. */
    fun rawTotal(): Double = items.sumOf { it.price }

    /** Discount fraction applied to [rawTotal], per the checkout rules. */
    fun discountRate(): Double = when {
        rawTotal() > TIER_2_THRESHOLD -> TIER_2_RATE
        rawTotal() > TIER_1_THRESHOLD -> TIER_1_RATE
        else -> 0.0
    }

    /** Final amount the customer pays. */
    fun subtotal(): Double = rawTotal() * (1 - discountRate())

    companion object {
        const val TIER_1_THRESHOLD = 200.0
        const val TIER_1_RATE = 0.10
        const val TIER_2_THRESHOLD = 300.0
        const val TIER_2_RATE = 0.20
    }
}
```

Run all tests → still green. **That is the payoff of TDD: fearless refactoring.**

```bash
./gradlew :app:testDebugUnitTest --tests "*ShoppingCartTest"
```

---

### 5.4 Close the loop — Espresso test for the checkout screen

Bring it back to where the session started: UI test over TDD'd logic.

`app/src/androidTest/java/com/example/androidtestingsdgku/ShopViewTest.kt`

```kotlin
package com.example.androidtestingsdgku

import androidx.test.core.app.ActivityScenario
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.contrib.RecyclerViewActions.actionOnItemAtPosition
import androidx.test.espresso.matcher.ViewMatchers.withId
import androidx.test.espresso.matcher.ViewMatchers.withText
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.recyclerview.widget.RecyclerView
import com.example.androidtestingsdgku.shop.ShopActivity
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class ShopViewTest {

    @Test
    fun subtotalStartsAtZero() {
        ActivityScenario.launch(ShopActivity::class.java).use {
            onView(withId(R.id.textSubtotal)).check(matches(withText("Subtotal: $0.00")))
        }
    }

    @Test
    fun addingMonitorAndHeadset_appliesTenPercentDiscount() {
        ActivityScenario.launch(ShopActivity::class.java).use {
            // Monitor 180 + Headset 120 = 300 -> 10% -> 270
            onView(withId(R.id.listProducts))
                .perform(actionOnItemAtPosition<RecyclerView.ViewHolder>(2, clickChildWithId(R.id.buttonAdd)))
            onView(withId(R.id.listProducts))
                .perform(actionOnItemAtPosition<RecyclerView.ViewHolder>(3, clickChildWithId(R.id.buttonAdd)))

            onView(withId(R.id.textSubtotal)).check(matches(withText("Subtotal: $270.00")))
        }
    }
}
```

`clickChildWithId` is a small custom `ViewAction` — leave it as the final lab exercise:

```kotlin
fun clickChildWithId(id: Int) = object : ViewAction {
    override fun getConstraints() = null
    override fun getDescription() = "Click child view with id $id"
    override fun perform(uiController: UiController, view: View) {
        view.findViewById<View>(id).performClick()
    }
}
```

---

## Wrap-up — 5 min

| Layer | Tool | Speed | What it proves |
|---|---|---|---|
| Pure logic (`ShoppingCart`, `LoginValidator`) | JUnit | ms | The rules are right |
| View, JVM | Robolectric + Espresso | ~1 s | The screen wires up |
| View, device | Espresso instrumented | ~10 s | It really works |

**Key takeaways to repeat:**
1. Give every widget an `id` — it's your test API.
2. Keep Activities dumb; push logic into testable classes.
3. Test boundaries (200 and 300), not just happy paths.
4. RED → GREEN → REFACTOR. Never skip red — a test you never saw fail proves nothing.

## Homework

1. Add `Cart` quantity support (`add(product, qty)`) using TDD — test first, commit the red test separately so I can see it.
2. Write an Espresso test asserting the cart resets after checkout.
3. Add a `CheckoutActivity` showing raw total, discount, and final subtotal; test it with Robolectric.

## Commands cheat sheet

```bash
# unit tests (fast, JVM, includes Robolectric)
./gradlew :app:testDebugUnitTest

# one class
./gradlew :app:testDebugUnitTest --tests "*ShoppingCartTest"

# instrumented Espresso tests (needs emulator/device)
./gradlew :app:connectedDebugAndroidTest

# reports
open app/build/reports/tests/testDebugUnitTest/index.html
open app/build/reports/androidTests/connected/debug/index.html
```
