# myapp/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from mydjango_project.myapp.domain.commands import CreateBookmarkCommand
from mydjango_project.myapp.service_layer import message_bus
from mydjango_project.myapp.domain import ListBookmarksQuery


@csrf_exempt  
@require_http_methods(["POST"])
def create_bookmark(request):
    # Extract data from request to create a command
    data = request.POST
    command = CreateBookmarkCommand(
        title=data.get('title'),
        url=data.get('url'),
        notes=data.get('notes')
    )
    
    # The message bus will handle the command
    message_bus.handle(command)
    
    return JsonResponse({'status': 'success', 'message': 'Bookmark created'})

@require_http_methods(["POST"])
def update_bookmark(request, bookmark_id):
    # Extract data from request to create a command
    data = request.POST
    command = CreateBookmarkCommand(
        id=bookmark_id,
        title=data.get('title'),
        url=data.get('url'),
        notes=data.get('notes')
    )
    
    # The message bus will handle the command
    message_bus.handle(command)
    
    return JsonResponse({'status': 'success', 'message': 'Bookmark updated'})

@require_http_methods(["GET"])
def list_bookmarks(request):
    # Create a query
    query = ListBookmarksQuery()
    
    # The message bus will handle the query
    bookmarks = message_bus.handle(query)
    
    # Convert bookmarks to a JSON-compatible format
    bookmarks_data = [{'id': b.id, 'title': b.title, 'url': b.url, 'notes': b.notes} for b in bookmarks]
    
    return JsonResponse({'bookmarks': bookmarks_data})
