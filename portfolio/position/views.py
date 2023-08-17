from django.shortcuts import render, redirect

from portfolio.position.forms import AddPositionForm


def add_position(request):
    if request.method == 'GET':
        form = AddPositionForm()
    else:
        form = AddPositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {
        'form': form,
    }
    return render(request, 'add-position.html', context)
