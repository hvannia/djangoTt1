from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404  #see also get_list_or_404() 
from django.urls import reverse 
from django.views import generic

#from django.template import loader
from .models import Question, Choice


layout_url= 'polls/layout.html'

class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_question_list'
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name= 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name='polls/results.html'


def vote(request, question_id):
    question= get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message':"You didn't select a choice",
            'layout_url':layout_url
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


'''

def index(request):
    latest_question_list= Question.objects.order_by('-pub_date')[:5]
    #template=loader.get_template('polls/index.html')
    context={
        'latest_question_list': latest_question_list,
        'layout_url':layout_url
    }
    return render(request,'polls/index.html',context)
            #HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request, 'polls/detail.html',{'question':question, 'layout_url':layout_url})



def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request,'polls/results.html',{
        'question':question,
        'layout_url':layout_url
    })
'''