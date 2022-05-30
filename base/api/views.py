from django.http import JsonResponse

def getRoutes(request): #This is a view that shows all routes/URLs in the API
    routes = [
        'GET /api', #Home Page
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return JsonResponse(routes, safe=False) #safe means we can use more than python dictonaries in this JSON response
