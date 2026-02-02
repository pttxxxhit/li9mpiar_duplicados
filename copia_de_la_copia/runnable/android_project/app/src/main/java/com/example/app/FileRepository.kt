package com.example.app

import android.content.Context
import android.net.Uri
import androidx.documentfile.provider.DocumentFile
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class FileRepository(private val context: Context) {
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
            }
        }

        traverse(root)
        return@withContext out
    }

    suspend fun deleteFile(uri: Uri): Boolean = withContext(Dispatchers.IO) {
        try {
            val doc = DocumentFile.fromSingleUri(context, uri)
            if (doc != null) return@withContext doc.delete()
            else {
                val rows = context.contentResolver.delete(uri, null, null)
                return@withContext (rows > 0)
            }
        } catch (e: Exception) {
            return@withContext false
        }
    }

    suspend fun refreshFiles(): List<Uri> = withContext(Dispatchers.IO) {
        val t = lastTreeUri ?: return@withContext emptyList()
        return@withContext listFiles(t)
    }
}
