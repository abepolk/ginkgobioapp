from django.shortcuts import render
from django.views.generic.edit import CreateView
from dna_protein_align.models import DnaSeq
from dna_protein_align.forms import IndexForm
from dna_protein_align.align import align

# Create your views here.


def index(request):

    def serialize_seq_list(seq_list):
        return ','.join(seq_list)

    def deserialize_seq_list(seq_str):
        if not seq_str:
            return ''
        return seq_str.split(',')

    previous_searches = deserialize_seq_list(request.session.get('previous_searches', ''))

    result = ''

    if request.method == 'POST':
        form = IndexForm(request.POST)

        if form.is_valid(): # Check this makes sense, i.e. is_valid refers to something that does something useful
            cleaned_seq = form.clean_seq()
            previous_searches.append(cleaned_seq)
            request.session['previous_searches'] = serialize_seq_list(previous_searches)

            result = align(cleaned_seq)
            # Should do something with HttpResponseDirect ? No because there is only one page
    else:
        form = IndexForm()

    # seq = form.cleaned_data['seq']

    context = {
        'form' : form,
        'previous_searches' : previous_searches,
        'result' : result
    }

    return render(request, 'template    .html', context=context)
    
'''
class indexForm(CreateView):

    model = DnaSeq

    fields = '__all__' \
             '''