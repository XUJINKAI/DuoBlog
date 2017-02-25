from django.shortcuts import render

# Create your views here.

def note_view(request):
	return render(request, 'note/index.html')