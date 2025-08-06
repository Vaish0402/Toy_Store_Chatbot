import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from .models import ChatMessage
import google.generativeai as genai


# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

# Get API key from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("Loaded GEMINI_API_KEY:", GEMINI_API_KEY)

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Max number of messages to keep in DB
MAX_MESSAGES = 20


def chatbot_view(request):
    if request.method == "POST":
        user_msg = request.POST.get("message", "").strip()

        if not user_msg:
            return JsonResponse({"response": "⚠️ Please enter a message."})

        # Clear command: wipe chat history
        if user_msg.lower() == "clear":
            ChatMessage.objects.all().delete()
            return JsonResponse({"response": "🧹 Chat history cleared."})

        try:
            # Save user message
            ChatMessage.objects.create(role="user", message=user_msg)

            # Generate bot response
            response = model.generate_content(user_msg)
            bot_response = response.text.strip()

            # Save bot response
            ChatMessage.objects.create(role="bot", message=bot_response)

            # Keep only the most recent MAX_MESSAGES
            total_messages = ChatMessage.objects.count()
            if total_messages > MAX_MESSAGES:
                to_delete = total_messages - MAX_MESSAGES
                ChatMessage.objects.order_by("timestamp")[:to_delete].delete()

        except Exception as e:
            bot_response = f"⚠️ Error: {str(e)}"
            ChatMessage.objects.create(role="bot", message=bot_response)

        return JsonResponse({"response": bot_response})

    # GET: Show chat history (latest at bottom)
    history = ChatMessage.objects.all().order_by("timestamp")  # Oldest first
    return render(request, "chatbot/chat.html", {"history": history})


@csrf_exempt
def upload_file(request):
    if request.method == "POST" and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        print("Received file:", uploaded_file.name)
        # Optional: Save file or process here
        return JsonResponse({'message': '📎 File received!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
