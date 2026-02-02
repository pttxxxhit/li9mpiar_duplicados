package com.example.app

import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch
import android.content.Intent
import android.content.ContentResolver

class MainActivity : ComponentActivity() {
    private val vm: MainViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Launcher para seleccionar carpeta (SAF)
        val pickDirectoryLauncher = registerForActivityResult(ActivityResultContracts.OpenDocumentTree()) { uri: Uri? ->
            uri?.let {
                try {
                    // Tomar permisos persistentes para poder acceder luego
                    val takeFlags: Int = (Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
                    contentResolver.takePersistableUriPermission(it, takeFlags)
                } catch (e: Exception) {
                    // ignore
                }
                vm.onFolderSelected(it)
            }
        }

        // Launcher para solicitar permisos especiales si fuera necesario (ejemplo)
        // val manageStorageLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { /* ... */ }

        setContent {
            MaterialTheme {
                Surface {
                    // Pasamos lambdas que disparan los launchers desde la UI
                    MainScreen(
                        viewModel = vm,
                        onPickFolder = { pickDirectoryLauncher.launch(null) },
                    )
                }
            }
        }

        // Cargar estado inicial si procede
        lifecycleScope.launch {
            // vm.loadInitial() // si necesitas precarga
        }
    }
}
