from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import os
from groq import Groq
from church.models import SpiritualGuidance  # ADD THIS LINE ONLY

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

@login_required(login_url='/login/')
def chatbot_view(request):
    return render(request, 'chatbot/chatbot.html')

@login_required(login_url='/login/')
def chatbot_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({'reply': 'Please type a message. 🙏'})

        # ADD THIS BLOCK — search dataset first
        dataset_reply = search_dataset(user_message)
        if dataset_reply:
            return JsonResponse({'reply': dataset_reply})

        if not GROQ_API_KEY:
            return JsonResponse({'reply': get_fallback_response(user_message)})

        try:
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are FaithConnect AI - a warm, knowledgeable and compassionate "
                            "Christian spiritual guidance assistant for a church platform in Kenya "
                            "called FaithConnect, built by a Zetech University student.\n\n"
                            "You have access to the complete King James Version Bible with all "
                            "31,102 verses across 66 books from Genesis to Revelation.\n\n"
                            "Your role:\n"
                            "- Provide Biblical guidance and accurate scripture references\n"
                            "- Support church members with compassion and wisdom\n"
                            "- Always include at least one relevant Bible verse\n"
                            "- Keep responses warm, encouraging and concise\n"
                            "- Use a pastoral tone like a trusted pastor\n"
                            "- Be sensitive to the Kenyan church context\n\n"
                            "Always end with an encouraging word or follow-up question."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            reply = response.choices[0].message.content

        except Exception:
            reply = get_fallback_response(user_message)

        return JsonResponse({'reply': reply})

    return JsonResponse({'error': 'Invalid request'}, status=400)


# ADD THIS NEW FUNCTION — searches your dataset
def search_dataset(message):
    message_lower = message.lower()
    try:
        guidance_list = SpiritualGuidance.objects.all()
        for item in guidance_list:
            question_words = item.question.lower().split()
            matches = sum(1 for word in question_words if word in message_lower and len(word) > 3)
            if matches >= 2:
                return f"{item.answer}\n\n📖 Reference: {item.verse_reference}"
    except Exception:
        pass
    return None


# KEEP THIS FUNCTION — fallback responses
def get_fallback_response(message):
    message = message.lower()
    if any(w in message for w in ['hello', 'hi', 'hey', 'jambo']):
        return "Peace be with you! 🙏 Welcome to FaithConnect. How can I support you spiritually today?"
    if any(w in message for w in ['pray', 'prayer']):
        return "🙏 Prayer is our direct line to God!\n\n'Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.' - Philippians 4:6"
    if any(w in message for w in ['hope', 'future']):
        return "✨ God has wonderful plans for you!\n\n'For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you.' - Jeremiah 29:11"
    if any(w in message for w in ['strength', 'tired', 'weak']):
        return "💪 God is your strength!\n\n'I can do all this through him who gives me strength.' - Philippians 4:13"
    if any(w in message for w in ['peace', 'anxiety', 'worry', 'stress']):
        return "🕊 God's peace is available to you!\n\n'Cast all your anxiety on him because he cares for you.' - 1 Peter 5:7"
    if any(w in message for w in ['love', 'god loves']):
        return "❤️ God loves you unconditionally!\n\n'For God so loved the world that He gave His one and only Son.' - John 3:16"
    if any(w in message for w in ['forgive', 'sin', 'guilty']):
        return "🙏 God's forgiveness is complete!\n\n'If we confess our sins, he is faithful and just and will forgive us.' - 1 John 1:9"
    if any(w in message for w in ['faith', 'believe', 'trust']):
        return "✝ Faith is the foundation!\n\n'Now faith is confidence in what we hope for.' - Hebrews 11:1"
    if any(w in message for w in ['sad', 'depressed', 'lonely', 'broken']):
        return "💙 God is close to the brokenhearted!\n\n'The Lord is close to the brokenhearted.' - Psalm 34:18"
    return "🙏 God is always with you.\n\n'The Lord himself goes before you and will be with you.' - Deuteronomy 31:8\n\nHow else can I support you spiritually today?"