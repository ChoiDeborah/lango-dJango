from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Sentence
from .models import Pos
from .models import Dependency
from .forms import SentenceEditForm
from .forms import PosTable
from .forms import DependencyTable


def sentence_edit(request, sid):
    sentence = get_object_or_404(Sentence, pk=sid)
    if request.method == 'POST':
        sform = SentenceEditForm(request.POST, instance=sentence)
        pos_table = PosTable(Pos.objects.filter(sentence=sentence))
        dependency_table = DependencyTable(Dependency.objects.filter(sentence=sentence))
        if sform.is_valid():
            sentence = sform.save(commit=False)
            sentence.save()
    else:
        sform = SentenceEditForm(instance=sentence)
        pos_table = PosTable(Pos.objects.filter(sentence=sentence))
        dependency_table = DependencyTable(Dependency.objects.filter(sentence=sentence))
    return render(request,
                  'lango_content/post_sentence.html',
                  {'form': sform, 'pos_table': pos_table, 'dependency_table': dependency_table})


