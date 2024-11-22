# import firebase_admin
# from firebase_admin import credentials, db
# from telegram import Update
# from telegram.ext import Application, CommandHandler, ContextTypes

# # Replace with your bot token and Firebase database URL
# TOKEN = '7909977759:AAEh2zT1R5CBp8jL0tTWqCdKPQwxe6A22tI'
# FIREBASE_DATABASE_URL = 'https://medical-chatbot-99edb-default-rtdb.firebaseio.com/'

# # Initialize Firebase Admin SDK
# cred = credentials.Certificate("C:\\Users\\anshu\\Downloads\\telegram bot\\.vscode\\medical-chatbot-99edb-firebase-adminsdk-6c4om-4dc57ca86c.json")
# firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_DATABASE_URL})


# # Firebase database reference for appointments
# appointments_ref = db.reference('appointments')

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text('Hello! I am your medical chatbot. Use /book to book an appointment, /delete to delete an appointment, or /view to view all appointments.')

# async def book(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if len(context.args) != 2:
#         await update.message.reply_text('Usage: /book <date> <time>\nExample: /book 2023-10-10 10:00')
#         return

#     date = context.args[0]
#     time = context.args[1]
#     appointment_id = f"{date}_{time}"
    
#     # Check if appointment already exists
#     if appointments_ref.child(appointment_id).get():
#         await update.message.reply_text(f'Appointment for {date} at {time} already exists.')
#         return

#     # Confirm booking
#     await update.message.reply_text(f'Are you sure you want to book an appointment for {date} at {time}? Reply with "yes" to confirm.')

#     # Wait for user confirmation
#     response = await context.bot.wait_for_message(user_id=update.effective_user.id, timeout=30)

#     if response and response.text.lower() == 'yes':
#         # Save appointment to Firebase
#         appointments_ref.child(appointment_id).set({
#             'user_id': update.effective_user.id,
#             'date': date,
#             'time': time
#         })
#         await update.message.reply_text(f'Appointment booked for {date} at {time}.')
#     else:
#         await update.message.reply_text('Booking canceled.')

# async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if len(context.args) != 2:
#         await update.message.reply_text('Usage: /delete <date> <time>\nExample: /delete 2023-10-10 10:00')
#         return

#     date = context.args[0]
#     time = context.args[1]
#     appointment_id = f"{date}_{time}"
    
#     # Check if appointment exists
#     if not appointments_ref.child(appointment_id).get():
#         await update.message.reply_text(f'No appointment found for {date} at {time}.')
#         return

#     # Confirm deletion
#     await update.message.reply_text(f'Are you sure you want to delete the appointment for {date} at {time}? Reply with "yes" to confirm.')

#     # Wait for user confirmation
#     response = await context.bot.wait_for_message(user_id=update.effective_user.id, timeout=30)

#     if response and response.text.lower() == 'yes':
#         # Delete appointment from Firebase
#         appointments_ref.child(appointment_id).delete()
#         await update.message.reply_text(f'Appointment for {date} at {time} has been deleted.')
#     else:
#         await update.message.reply_text('Deletion canceled.')

# async def view(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     appointments = appointments_ref.get()

#     if not appointments:
#         await update.message.reply_text('No appointments found.')
#         return

#     appointments_text = "Here are all booked appointments:\n"
#     for appointment_id, data in appointments.items():
#         appointments_text += f"Date: {data['date']}, Time: {data['time']}\n"
    
#     await update.message.reply_text(appointments_text)

# def main():
#     application = Application.builder().token(TOKEN).build()

#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CommandHandler("book", book))
#     application.add_handler(CommandHandler("delete", delete))
#     application.add_handler(CommandHandler("view", view))

#     print("Bot is starting...")
#     application.run_polling()

# if __name__ == '__main__':
#     try:
#         main()
#     except Exception as e:
#         print(f"An error occurred: {e}")


import firebase_admin
from firebase_admin import credentials, db
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Replace with your bot token and Firebase database URL
TOKEN = '7909977759:AAEh2zT1R5CBp8jL0tTWqCdKPQwxe6A22tI'

FIREBASE_DATABASE_URL = 'https://medical-chatbot-99edb-default-rtdb.firebaseio.com/'

# Initialize Firebase Admin SDK
cred = credentials.Certificate("C:\\Users\\anshu\\Downloads\\telegram bot\\.vscode\\medical-chatbot-99edb-firebase-adminsdk-6c4om-4dc57ca86c.json")
firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_DATABASE_URL})

# Firebase database references
appointments_ref = db.reference('appointments')
pending_appointments_ref = db.reference('pending_appointments')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Hello! I am your medical chatbot. Use /book to book an appointment, /delete to delete an appointment, or /view to view all appointments.'
    )

async def book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text('Usage: /book <date> <time>\nExample: /book 2023-10-10 10:00')
        return

    date = context.args[0]
    time = context.args[1]
    appointment_id = f"{date}_{time}"

    # Check if appointment already exists
    if appointments_ref.child(appointment_id).get():
        await update.message.reply_text(f'Appointment for {date} at {time} already exists.')
        return

    # Save pending appointment for confirmation
    pending_appointments_ref.child(update.effective_user.id).set({
        'date': date,
        'time': time
    })

    await update.message.reply_text(
        f'Are you sure you want to book an appointment for {date} at {time}? Type /confirm to confirm or /cancel to cancel.'
    )

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pending_appointment = pending_appointments_ref.child(update.effective_user.id).get()

    if not pending_appointment:
        await update.message.reply_text('No pending appointment to confirm.')
        return

    date = pending_appointment['date']
    time = pending_appointment['time']
    appointment_id = f"{date}_{time}"

    # Save appointment to Firebase
    appointments_ref.child(appointment_id).set({
        'user_id': update.effective_user.id,
        'date': date,
        'time': time
    })

    # Remove pending appointment
    pending_appointments_ref.child(update.effective_user.id).delete()

    await update.message.reply_text(f'Appointment booked for {date} at {time}.')

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not pending_appointments_ref.child(update.effective_user.id).get():
        await update.message.reply_text('No pending appointment to cancel.')
        return

    # Remove pending appointment
    pending_appointments_ref.child(update.effective_user.id).delete()
    await update.message.reply_text('Appointment booking canceled.')

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text('Usage: /delete <date> <time>\nExample: /delete 2023-10-10 10:00')
        return

    date = context.args[0]
    time = context.args[1]
    appointment_id = f"{date}_{time}"

    if not appointments_ref.child(appointment_id).get():
        await update.message.reply_text(f'No appointment found for {date} at {time}.')
        return

    appointments_ref.child(appointment_id).delete()
    await update.message.reply_text(f'Appointment for {date} at {time} has been deleted.')

async def view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    appointments = appointments_ref.get()

    if not appointments:
        await update.message.reply_text('No appointments found.')
        return

    appointments_text = "Here are all booked appointments:\n"
    for appointment_id, data in appointments.items():
        appointments_text += f"Date: {data['date']}, Time: {data['time']}\n"

    await update.message.reply_text(appointments_text)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("book", book))
    application.add_handler(CommandHandler("confirm", confirm))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(CommandHandler("view", view))

    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
