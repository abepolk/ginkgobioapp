from django.shortcuts import render
from dna_protein_align.forms import IndexForm
from dna_protein_align.align import Aligner # Change name of align.py

def index(request):

    # The list of previous searches is held in an array. Each entry is a previous search, with elements
    # elem[0] the sequence, elem[1] the protein name, and elem[2] the protein location (index)
    def serialize_seq_list(seq_data):
        if seq_data:
            print(seq_data)
            return ','.join([x for y in seq_data for x in y])
        else:
            return None

    # See comment for serialization method
    def deserialize_seq_list(data_string):
        if not data_string:
            return []
        flat_list = data_string.split(',')
        array = []
        for i in range(0, len(flat_list), 3):
            # There is guaranteed divisible by 3 num elems in flat_list
            array.append([flat_list[i], flat_list[i+1], flat_list[i+2]])
        return array

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
                previous_searches.append([cleaned_seq, protein_name, str(protein_index)])
            request.session['previous_searches'] = serialize_seq_list(previous_searches)
    else:
        form = IndexForm()

    # seq = form.cleaned_data['seq']

    context = {
        'form':form,
        'previous_searches' : previous_searches,
        'is_post':is_post,
        'result_found':result_found,
        'protein_name':protein_name,
        'protein_index':protein_index
    }

    return render(request, 'template.html', context=context)