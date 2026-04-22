package com.safedm

import android.app.NotificationManager
import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification
import kotlinx.coroutines.*

class MyNotificationListener : NotificationListenerService() {

    override fun onNotificationPosted(sbn: StatusBarNotification) {

        val pkg = sbn.packageName

        if (pkg.contains("instagram") || pkg.contains("facebook")) {

            val text = sbn.notification.extras
                .getCharSequence("android.text")?.toString()

            val sender = sbn.notification.extras
                .getCharSequence("android.title")?.toString()

            if (text != null && sender != null) {

                GlobalScope.launch {

                    val action = ApiClient.analyze(text, sender)

                    when (action) {
                        "block" -> cancelNotification(sbn.key)
                        "warn" -> {
                            cancelNotification(sbn.key)
                            showWarning(sender)
                        }
                    }
                }
            }
        }
    }

    private fun showWarning(sender: String) {
        val manager = getSystemService(NOTIFICATION_SERVICE) as NotificationManager

        val notification = android.app.Notification.Builder(this)
            .setContentTitle("⚠️ Filtered Message")
            .setContentText("Message from $sender hidden")
            .setSmallIcon(android.R.drawable.ic_dialog_alert)
            .build()

        manager.notify(1, notification)
    }
}