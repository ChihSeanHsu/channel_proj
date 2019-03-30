from django.shortcuts import render, HttpResponse
from django.views.generic import View

# Create your views here.


class ChatRoom(View):
    template_name = 'chat/index.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            f'<script>alert(\'Please enter home page to type your name.\'); window.location = \'http://{request.get_host()}/\';</script>'
        )

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'name': request.POST.get('name', 'NoName')
        })
