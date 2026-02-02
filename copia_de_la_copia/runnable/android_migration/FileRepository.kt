package com.example.app

import android.content.Context
import android.net.Uri
import androidx.documentfile.provider.DocumentFile
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * FileRepository: implementación básica basada en SAF (Storage Access Framework).
 * - listFiles(treeUri): lista recursiva de archivos bajo el árbol seleccionado
 * - deleteFile(uri): elimina el documento usando DocumentFile
 * - refreshFiles(): re-lista usando el último treeUri
 *
 * Notas:
 * - Requiere que la app haya solicitado y guardado permisos persistentes para treeUri
 *   usando contentResolver.takePersistableUriPermission(uri, flags)
 * - Esta es una implementación sencilla; para producción conviene añadir manejo de excepciones
 *   detallado y reportes de errores al ViewModel.
 */
class FileRepository(private val context: Context) {

    // Último treeUri seleccionado por el usuario
    private var lastTreeUri: Uri? = null

    suspend fun listFiles(treeUri: Uri): List<Uri> = withContext(Dispatchers.IO) {
        lastTreeUri = treeUri
        val root = DocumentFile.fromTreeUri(context, treeUri)
        if (root == null || !root.canRead()) return@withContext emptyList()

        val out = mutableListOf<Uri>()

        fun traverse(folder: DocumentFile) {
            try {
                val children = folder.listFiles()
                for (child in children) {
                    if (child.isDirectory) traverse(child)
                    else if (child.isFile) out.add(child.uri)
                }
            } catch (e: Exception) {
                // ignorar errores de acceso a archivos individuales
            }
        }

        traverse(root)
        return@withContext out
    }

    suspend fun deleteFile(uri: Uri): Boolean = withContext(Dispatchers.IO) {
        try {
            val doc = DocumentFile.fromSingleUri(context, uri)
            if (doc != null) {
                return@withContext doc.delete()
            } else {
                // fallback: intentar eliminar vía ContentResolver
                val rows = context.contentResolver.delete(uri, null, null)
                return@withContext (rows > 0)
            }
        } catch (e: Exception) {
            return@withContext false
        }
    }

    // Re-listar usando el último treeUri seleccionado (si existe)
    suspend fun refreshFiles(): List<Uri> = withContext(Dispatchers.IO) {
        val t = lastTreeUri ?: return@withContext emptyList()
        return@withContext listFiles(t)
    }
}
