from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from base.chatbot.rag_handler import RAGHandler
from dashboard.models import Event
import json
import time


rag_handler = RAGHandler()


@csrf_exempt
def chat(request):
    print("Récupération de la réponse")
    start_time = time.time()

    if rag_handler.vector_store is None:
        events = Event.objects.all()
        rag_handler.create_vector_store(events)

    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get("query")
        chat_history = data.get("chat_history", [])

        response = rag_handler.get_response(query, chat_history)

        end_time = time.time()
        total_time = int((end_time - start_time)/60)

        print("Récupération de la réponse terminée")
        print(f"Temps total de récupération : {total_time} minutes")
        return JsonResponse({"response": response})