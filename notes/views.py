# notes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import NoteForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm, RegistrationForm
from .models import Note, Document
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

#password reset
def password_reset(request):
    return render(request, 'login.html', {'form': form})

#Register
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

#LOGIN
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))  # Redirect to home after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@csrf_exempt
def auto_save_note(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')
        title = data.get('title')
        hashtags = data.get('hashtags')

        # Assuming you are editing an existing note
        # You might need to pass the note ID to identify which note to update
        note_id = request.session.get('note_id')
        if note_id:
            document = Document.objects.get(id=note_id)
            document.processed_content = content
            document.title = title
            document.hashtags = hashtags
            document.save()
            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'}, status=400)

@login_required
def home(request):
    query = request.GET.get('q', '')
    if query:
        documents = Document.objects.filter(user=request.user, hashtags__icontains=query)
    else:
        documents = Document.objects.filter(user=request.user)  # Filter to only user's documents

    notes = Note.objects.filter(user=request.user)  # Filter to only user's notes
    context = {
        'documents': documents,
        'notes': notes,
    }
    return render(request, 'home.html', context)


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully.')
        return redirect('home')
    return render(request, 'notes/confirm_delete.html', {'object': note})

@login_required
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document deleted successfully.')
        return redirect('home')
    return render(request, 'notes/confirm_delete.html', {'object': document})

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_detail', note_id=note.id)
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})

@login_required
def note_detail(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})

@login_required
def edit_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_detail', note_id=note.id)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form, 'note': note})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm
from .models import Document
from langchain.document_loaders import YoutubeLoader, PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import OpenAIEmbeddings
from langchain import OpenAI

@login_required
def edit_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentForm(instance=document)
    # Set the note ID in session
    request.session['note_id'] = pk

    return render(request, 'notes/document_form.html', {'form': form, 'document': document})


@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if document.user != request.user:
        return redirect('home')  # Replace 'some_error_page_or_homepage' with your actual URL name

    return render(request, 'notes/document_detail.html', {'document': document})


@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)  # Do not save immediately
            document.user = request.user  # Set the user field
            document.save()  # Now save the document
            process_document(document)
            messages.success(request, 'Document uploaded successfully!')
            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentForm()
    return render(request, 'notes/upload.html', {'form': form})


def process_document(document):
    if document.youtube_url:
        loader = YoutubeLoader.from_youtube_url(document.youtube_url, add_video_info=False)
        documents = loader.load()
    elif document.file:
        print("uploading doc")
        loader = PyPDFLoader(document.file.path)
        documents = loader.load()
    else:
        return
    openai_api_key = "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"
    index = VectorstoreIndexCreator(embedding=OpenAIEmbeddings(api_key=openai_api_key)).from_loaders([loader])
    query = "what are the key biological concepts in the content. Also include the key biological learning points and the learning outcomes. Do not miss any biological concepts and learning points out"
    llm = OpenAI(api_key=openai_api_key, temperature=0)
    output = index.query(query, llm=llm)
    query = f"""
        You are a educator, with the content given, {output} contains all the items that you must explain to a university student in great detail
        Do not generate any additional content that is not included in the content. Explain everything

        An example of the format is:
        Concept 1: Holiday Model
            Summary of concept 1 (if applicable, if not applicable do not write it out)
            The Holliday model proposes that recombination occurs through the formation of a four-stranded structure called a Holliday junction.
            Examples/code/math (if applicable, if not applicable do not write it out)
            For example...
            Explnation of concept 1 (if applicable, if not applicable do not write it out)
            Mechanism of concept 1 (if applicable, if not applicable do not write it out)
            (a) Two homologous DNA molecules line up (e.g., two nonsister chromatids line up during meiosis).
            (b) Cuts in one strand of both DNAs.
            (c) The cut strands cross and join homologous strands, forming the Holliday structure (or Holliday junction).
            (d) Heteroduplex region is formed by branch migration.
            (e) Resolution of the Holliday structure. Figure (e) is a different view of the Holliday junction than Figure (d). DNA strands may be cut along either the vertical line or horizontal line.
            (f) The vertical cut will result in crossover between f-f' and F-F' regions. The heteroduplex region will eventually be corrected by mismatch repair.
            (g) The horizontal cut does not lead to crossover after mismatch repair. However, it could cause gene conversion
        Concept 2: Double Strand Break model (DSB)
            Summary of concept 2 (if applicable, if not applicable do not write it out)
            The steps of DSB include:
            - Double strand break- Strand resection- D-loop formation- GAP repair- Branch migration- Resolution
            Exampls/code/math (if applicable, if not applicable do not write it out)
            Explnation of concept 2 (if applicable, if not applicable do not write it out)
            Mechanism of concept 2 (if applicable, if not applicable do not write it out)
            Step 1. Doublestrand break formation
            Step 2. Resection
            Step 3. First strand invasion 
            Step 4. Formation of a double Holliday junction and Branch migration
            Step 5. Alternative resolution
        ...

        Be clear and concise in your notes generation of biological concepts. Include any steps, information, summary, flows, mechanism and formulas from the content
        Generate all the concepts in the content.
        Generate as many concepts as possible.
        
        Important!: Output all in a HTML format that can be interpreted by Quill

        """
    llm = OpenAI(api_key=openai_api_key ,temperature=0, max_tokens = -1) # Initialize an OpenAI LLM
    final = index.query(query, llm=llm) # Pass the LLM to the query method
    
    document.processed_content = final
    document.save()

