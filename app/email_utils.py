import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_employer_id_email(to_email, employer_id):
    sender_email = os.getenv("APP_EMAIL")
    sender_password = os.getenv("APP_PASSWORD")
    
    if not sender_email or not sender_password:
        print("Email credentials not found in environment variables.")
        return False
        
    subject = "Your Unique NEXORA Employer ID"
    
    # HTML formatted email to match "our website name and our website design formmat"
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
          <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #6C5CF5; margin: 0;">NEXORA</h1>
            <p style="color: #888; font-size: 14px; margin-top: 5px;">Your Career Starts Here</p>
          </div>
          <div style="padding: 20px; background-color: #f9f9f9; border-radius: 6px; border-left: 4px solid #6C5CF5;">
            <h2 style="color: #333; margin-top: 0;">Welcome to Nexora Employers!</h2>
            <p style="color: #555; line-height: 1.5;">Thank you for registering. To complete your verification, please use the following unique Employer ID:</p>
            <div style="text-align: center; margin: 30px 0;">
              <span style="display: inline-block; padding: 15px 25px; background-color: #6C5CF5; color: #ffffff; font-size: 24px; font-weight: bold; border-radius: 8px; letter-spacing: 2px;">
                {employer_id}
              </span>
            </div>
            <p style="color: #555; line-height: 1.5;">Please enter this ID on the registration page to verify your email address.</p>
          </div>
          <div style="margin-top: 30px; text-align: center; color: #aaa; font-size: 12px;">
            <p>&copy; 2026 NEXORA. All rights reserved.</p>
          </div>
        </div>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = f"NEXORA <{sender_email}>"
    msg['To'] = to_email
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_password_reset_email(to_email, reset_link):
    sender_email = os.getenv("APP_EMAIL")
    sender_password = os.getenv("APP_PASSWORD")
    
    if not sender_email or not sender_password:
        print("Email credentials not found in environment variables.")
        return False
        
    subject = "Reset Your NEXORA Password"
    
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
          <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #6C5CF5; margin: 0;">NEXORA</h1>
            <p style="color: #888; font-size: 14px; margin-top: 5px;">Your Career Starts Here</p>
          </div>
          <div style="padding: 20px; background-color: #f9f9f9; border-radius: 6px; border-left: 4px solid #6C5CF5;">
            <h2 style="color: #333; margin-top: 0;">Password Reset Request</h2>
            <p style="color: #555; line-height: 1.5;">We received a request to reset your password for your NEXORA account. Click the button below to choose a new password:</p>
            <div style="text-align: center; margin: 30px 0;">
              <a href="{reset_link}" style="display: inline-block; padding: 14px 28px; background-color: #6C5CF5; color: #ffffff; font-size: 16px; font-weight: bold; text-decoration: none; border-radius: 8px;">
                Reset Password
              </a>
            </div>
            <p style="color: #777; font-size: 13px; line-height: 1.5;">If the button above does not work, copy and paste this link into your browser:<br>
            <a href="{reset_link}" style="color: #6C5CF5; word-break: break-all;">{reset_link}</a></p>
            <p style="color: #888; font-size: 12px; margin-top: 20px;">If you did not request a password reset, you can safely ignore this email.</p>
          </div>
          <div style="margin-top: 30px; text-align: center; color: #aaa; font-size: 12px;">
            <p>&copy; 2026 NEXORA. All rights reserved.</p>
          </div>
        </div>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = f"NEXORA <{sender_email}>"
    msg['To'] = to_email
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send password reset email: {e}")
        return False

