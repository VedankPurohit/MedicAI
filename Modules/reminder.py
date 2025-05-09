# import threading
# import time
# from datetime import datetime
# import smtplib

# def SendMail(msg: str, Time: str):
#     MY_EMAIL = "use.onlyme1a@gmail.com"
#     PASSWORD = "vlfmvghaqjoecfiv"  # this is only for hackathon

#     def send_email():
#         try:
#             with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
#                 connection.starttls()  # Secure the connection
#                 connection.login(user=MY_EMAIL, password=PASSWORD)
#                 connection.sendmail(
#                     from_addr=MY_EMAIL,
#                     to_addrs="vedankpurohit@gmail.com",
#                     msg=msg
#                 )
#                 print("Email sent successfully!")
#         except Exception as e:
#             print(f"Failed to send email: {e}")

#     def wait_until(target_time, action):
#         """
#         Wait until the target_time (in "HH:MM" format) and then perform the action.
        
#         Args:
#         - target_time (str): The target time in "HH:MM" format (24-hour).
#         - action (function): The function to execute when the time is reached.
#         """
#         def time_checker():
#             current_time = datetime.now().strftime("%H:%M")
#             while True:
#                 if current_time == target_time:
#                     print("DOne")
#                     action()  # Perform the action
#                     break  # Exit the loop after performing the action
#                 time.sleep(10)  # Sleep for 10 seconds to avoid tight looping

#         # Run the time checker in a separate thread
#         thread = threading.Thread(target=time_checker)
#         thread.daemon = True  # Daemon thread will exit when the main program exits
#         thread.start()

#     # Start the waiting thread with the target time and the email sending function
#     wait_until(Time, send_email)

#     # Your main program can continue running without interruption
#     print(f"Waiting for the specified time ({Time}) to send the email...")

# SendMail("Hii", "8:46")


# import time
# from datetime import datetime

# def schedule_message(target_time: str, msg: str):
#     # Convert target_time from string to a datetime object
#     target_time = datetime.strptime(target_time, "%H:%M").time()
    
#     # Infinite loop to keep checking the current time
#     while True:
#         now = datetime.now().time()
#         if now >= target_time:
#             print(msg)
#             break
#         # Sleep for 1 minute to reduce CPU usage
#         time.sleep(60)

# # Example usage:
# schedule_message("8:49", "It's time to shine!")


import time
import threading
from datetime import datetime

def schedule_message(target_time: str, msg: str):
    def run_at_time():
        # Convert target_time from string to a datetime object
        target_time_obj = datetime.strptime(target_time, "%H:%M").time()
        
        # Infinite loop to keep checking the current time
        while True:
            now = datetime.now().time()
            if now >= target_time_obj:
                print(msg)
                break
            # Sleep for 1 minute to reduce CPU usage
            time.sleep(60)
    
    # Create a new thread to run the scheduling function
    scheduling_thread = threading.Thread(target=run_at_time)
    scheduling_thread.start()

# Example usage:
schedule_message("9:13", "It's time to shine!")

# Main program can continue running here
print("The program is still running!")
