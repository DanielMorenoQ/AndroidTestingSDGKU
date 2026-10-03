package com.example.androidtestingsdgku

import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.tooling.preview.Preview

object  ToggleButtonTag {
    const val TAG = "ToggleButton"
}

@Composable
fun ToggleButton() {
    var label by remember { mutableStateOf("Tap me") } // State to hold the button label, lives through the lifecycle of the composable function and will be reset when the composable function is recomposed.
    Button(
        onClick = {
            label = if (label == "Tap me") "Tapped" else "Tap me"
        },
        modifier = Modifier.testTag(ToggleButtonTag.TAG)
    ) {
        Text(text = label)
    }
}

@Preview
@Composable
fun ToggleButtonPreview() {
    ToggleButton()
}