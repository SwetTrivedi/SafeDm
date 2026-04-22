package com.safedm

import org.json.JSONObject
import java.net.URL

object ApiClient {

    fun analyze(msg: String, sender: String): String {
        return try {
            val url = URL("http://YOUR_IP:8000/analyze")

            val conn = url.openConnection()
            conn.doOutput = true
            conn.setRequestProperty("Content-Type", "application/json")

            val json = JSONObject()
            json.put("msg", msg)
            json.put("sender", sender)

            conn.outputStream.write(json.toString().toByteArray())

            val response = conn.inputStream.bufferedReader().readText()
            val obj = JSONObject(response)

            obj.getString("action")

        } catch (e: Exception) {
            "allow"
        }
    }
}