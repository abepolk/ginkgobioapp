from django.shortcuts import render
from dna_protein_align.forms import IndexForm
from dna_protein_align.align import Aligner # Change name of align.py
from django.core.exceptions import ValidationError
import json

def index(request):

    # The list of previous searches is held in an array. Each entry is a previous search, with elements
    # elem[0] the sequence, elem[1] the protein name, and elem[2] the protein location (index)

    '''
    # This is covered by json.dumps now
    def serialize_seq_list(seq_data):
        if seq_data:
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
    '''

    previous_searches = json.loads(request.session.get('previous_searches', '[]'))

    # Lower-cased boolean for JS
    is_post = 'false'
    result_found = 'false'
    protein_name = 'null'
    protein_index = 'null'
    validation_throws = 'false'


    if request.method == 'POST':
        print('vt')
        print(validation_throws)
        is_post = 'true'
        form = IndexForm(request.POST)
        print(form.is_valid())
        if form.is_valid(): # Check this makes sense, i.e. is_valid refers to something that does something useful
            try:
                cleaned_seq = form.clean_seq()
            except ValidationError as e:
                validation_throws = 'true'
            if form.clean_remove_search_history():
                previous_searches = []
            aligner = Aligner()
            result = aligner.find_seq(cleaned_seq)
            if result:
                result_found = 'true'
                protein_name = result[0]
                protein_index = result[1]
                previous_searches.append([cleaned_seq, protein_name, str(protein_index)])
            request.session['previous_searches'] = json.dumps(previous_searches)
    else:
        form = IndexForm()

    context = {
        'form' : form,
        'validation_throws' : validation_throws,
        'previous_searches' : json.dumps(previous_searches),
        'is_post' : is_post,
        'result_found' : result_found,
        'protein_name' : protein_name,
        'protein_index' : protein_index
    }
    return render(request, 'template.html', context=context)