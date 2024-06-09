import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email(subject, message, to_email):
    # Define your email settings
    from_email = "afabri24@gmail.com"
    password = "hedf axiw aqat yfdu"
    image_path = "public/prueba.png"

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the HTML message
    html_message = MIMEText(message, 'html')
    msg.attach(html_message)

    # Attach the image
    with open(image_path, 'rb') as file:
        img = MIMEImage(file.read())
        img.add_header('Content-ID', '<image1>')  # Use '<image1>' as the image ID
        msg.attach(img)

    # Add the footer with the image
    footer = MIMEText('<footer><img src="cid:image1"></footer>', 'html')
    msg.attach(footer)

    try:
        # Send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use the correct SMTP server and port for your email provider
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        return False
    

