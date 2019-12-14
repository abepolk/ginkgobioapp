from django.shortcuts import render
from dna_protein_align.forms import IndexForm
from dna_protein_align.align import Aligner # Change name of align.py
from django.http import JsonResponse
import json

def index(request):

    # The list of previous searches is held in an array. Each entry is a previous search, with elements
    # elem[0] the sequence, elem[1] the protein name, and elem[2] the protein location (index)

    searches = json.loads(request.session.get('searches', '[]'))

    if request.method == 'POST':
        # Initialize vars, lower-cased boolean and null for JS
        result_found = 'false'
        validation_throws = 'false'
        validation_error_message = ''
        # I don't know if if using json.loads here and not using json.POST counts as a hack
        form = IndexForm(json.loads(request.body))
        if form.is_valid():
            # Django docs say this has been cleaned using both clean() and clean_seq() in forms
            cleaned_seq = form.cleaned_data['seq']
            if form.clean_remove_search_history():
                searches = []
            aligner = Aligner()
            result = aligner.find_seq(cleaned_seq)
            if result:
                result_found = 'true'
                searches.append([cleaned_seq, result[0], str(result[1])])
            request.session['searches'] = json.dumps(searches)
        else:
            validation_throws = 'true'
            # There should be no more than one error, and it should be about valid chars
            validation_error_message = list(form.errors.as_data().values())[0][0].message
        return JsonResponse({
            'validation_throws' : validation_throws,
            'validation_error_message' : validation_error_message,
            'searches' : searches,
            'result_found' : result_found,
        })
    else:
        form = IndexForm()

    context = {
        'form' : form,
        'searches' : json.dumps(searches)
    }
    return render(request, 'template.html', context=context)