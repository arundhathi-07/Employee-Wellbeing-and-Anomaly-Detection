import plyer

def send_notification(title, message):
    plyer.notification.notify(title=title, message=message, timeout=5)
