package com.example.app

import android.app.Application
import android.net.Uri
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.launch

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val repo = FileRepository(application.applicationContext)

    private val _files = MutableStateFlow<List<Uri>>(emptyList())
    val files: StateFlow<List<Uri>> = _files.asStateFlow()

    private val _selected = MutableStateFlow<Set<Uri>>(emptySet())
    val selected: StateFlow<Set<Uri>> = _selected.asStateFlow()

    private val _preview = MutableStateFlow<Uri?>(null)
    val preview: StateFlow<Uri?> = _preview.asStateFlow()

    private val _events = MutableSharedFlow<String>()
    val events = _events.asSharedFlow()

    fun onFolderSelected(treeUri: Uri) {
        viewModelScope.launch {
            val list = repo.listFiles(treeUri)
            _files.value = list
            _selected.value = emptySet()
            _preview.value = null
        }
    }

    fun toggleSelect(file: Uri) {
        val m = _selected.value.toMutableSet()
        if (m.contains(file)) m.remove(file) else m.add(file)
        _selected.value = m
        _preview.value = if (_selected.value.size == 1) _selected.value.first() else _preview.value
    }

    fun deleteSelected() {
        viewModelScope.launch {
            val toDelete = _selected.value.toList()
            var ok = 0
            var fail = 0
            for (u in toDelete) {
                val r = repo.deleteFile(u)
                if (r) ok++ else fail++
            }
            _files.value = repo.refreshFiles()
            _selected.value = emptySet()
            _preview.value = null
            _events.emit("Eliminados: $ok, Fallidos: $fail")
        }
    }
}
