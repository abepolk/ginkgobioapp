from django.shortcuts import render
from dna_protein_align.forms import IndexForm
from dna_protein_align.align import Aligner # Change name of align.py

def index(request):

    def serialize_seq_list(seq_data):
        print(','.join([x for y in seq_data for x in y]))
        return ','.join([x for y in seq_data for x in y])

    # This may be rotated - check
    def deserialize_seq_list(data_string):
        request.session['previous_searches'] = []
        print([x for x in data_string.split(',')])
        return [x for x in data_string.split(',')]

    # This also needs to display results, not just searches
    previous_searches = deserialize_seq_list(request.session.get('previous_searches', ''))
    is_post = False
    result_found = False
    protein_name = None
    protein_index = None

    if request.method == 'POST':
        is_post = True
        form = IndexForm(request.POST)

        if form.is_valid(): # Check this makes sense, i.e. is_valid refers to something that does something useful
            cleaned_seq = form.clean_seq()
            if form.clean_remove_search_history():
                previous_searches = []
            aligner = Aligner()
            result = aligner.find_seq(cleaned_seq)
            if result:
                result_found = True
                protein_name = result[0]
                protein_index = result[1]
            previous_searches.append([cleaned_seq, protein_name, protein_index])
            request.session['previous_searches'] = serialize_seq_list(previous_searches)
            # Should do something with HttpResponseDirect ? No because there is only one page
    else:
        form = IndexForm()

    # seq = form.cleaned_data['seq']

    context = {
        'form' : form,
        # The index needs to be fixed
        'previous_searches' : previous_searches[0:5],
        'is_post' : is_post,
        'result_found' : result_found,
        'protein_name' : protein_name,
        'protein_index' : protein_index
    }

    return render(request, 'template.html', context=context)