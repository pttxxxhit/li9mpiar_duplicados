package com.example.app

import android.net.Uri
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Checkbox
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.Surface
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage

/**
 * MainScreen - composable principal con Coil preview
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(viewModel: MainViewModel, onPickFolder: () -> Unit) {
    val files by viewModel.files.collectAsState()
    val selected by viewModel.selected.collectAsState()
    val preview by viewModel.preview.collectAsState()

    val snackbarHostState = remember { SnackbarHostState() }

    // Escuchar eventos simples del ViewModel para mostrar snackbars
    LaunchedEffect(Unit) {
        viewModel.events.collect { msg ->
            snackbarHostState.showSnackbar(msg)
        }
    }

    Surface(modifier = Modifier.fillMaxSize()) {
        Row(modifier = Modifier.fillMaxSize().padding(16.dp)) {
            Column(modifier = Modifier.width(320.dp).fillMaxHeight(), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text(text = "Eliminar Archivos Duplicados", style = MaterialTheme.typography.headlineSmall)
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { onPickFolder() }) { Text("Seleccionar carpeta") }
                    Button(onClick = { /* viewModel.scan() */ }) { Text("Buscar duplicados") }
                }

                Spacer(modifier = Modifier.height(8.dp))
                Text(text = "Estado: listo", style = MaterialTheme.typography.bodyMedium)
                Spacer(modifier = Modifier.height(8.dp))
                Button(onClick = { viewModel.deleteSelected() }, modifier = Modifier.fillMaxWidth()) { Text("🗑️ ELIMINAR TODOS") }

                Spacer(modifier = Modifier.height(12.dp))
                Text(text = "Preview del archivo seleccionado")
                Box(modifier = Modifier.height(160.dp).fillMaxWidth(), contentAlignment = Alignment.Center) {
                    if (preview != null) {
                        AsyncImage(model = preview, contentDescription = null, modifier = Modifier.fillMaxSize())
                    } else {
                        Text(text = "Ningún archivo seleccionado")
                    }
                }

                SnackbarHost(hostState = snackbarHostState)
            }

            Spacer(modifier = Modifier.width(12.dp))

            Column(modifier = Modifier.fillMaxSize()) {
                LazyColumn(modifier = Modifier.fillMaxSize()) {
                    items(files) { f: Uri ->
                        Row(modifier = Modifier.fillMaxWidth().padding(8.dp), verticalAlignment = Alignment.CenterVertically) {
                            val checked = selected.contains(f)
                            Checkbox(checked = checked, onCheckedChange = { viewModel.toggleSelect(f) })
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(text = f.toString())
                        }
                    }
                }
            }
        }
    }
}
