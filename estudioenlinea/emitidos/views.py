from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from .forms import MisComprobantesEmitidos_Form
from .scripts import extrae, mis_comprobantes_emitidos
from django.contrib import messages
# Create your views here.


@staff_member_required
def MisComprobantesEmitidosView(request):
    tabla=None
    excel = None
    if request.method == 'POST':
        form = MisComprobantesEmitidos_Form(request.POST, request.FILES)      
        
        if form.is_valid():
            if request.FILES['file'].name.endswith('xlsx'):
                excel = request.FILES['file']

                try:
                    data = extrae(excel)
                    if 'Denominación_Emisor' in data.columns:
                        raise ValueError('recibido en emitido')
                    tabla = data.to_dict('records')
                    request.session['tabla'] = tabla
                except:
                    mensaje = "Hubo un problema con el archivo."
                    messages.info(request,mensaje)
                    return render(request, 'emitidos/emitidos_upload.html', {'form': form})

                contribuyente = request.POST.get('contribuyente')
                request.session['contribuyente'] = contribuyente
                mensaje = "Archivo Cargado exitosamente"
                messages.info(request,mensaje)
                return redirect('emitidos_succes')
   
    form = MisComprobantesEmitidos_Form()
    return render(request, 'emitidos/emitidos_upload.html', {'form': form})

@staff_member_required
def emitidos_succes(request):
    tabla = None
    if request.method == "POST":
        if request.POST.get("Answer") == "si":
            tabla = request.session['tabla']
            contribuyente = request.session['contribuyente']
            listaEmitidos = mis_comprobantes_emitidos(tabla,contribuyente)
            n = len(listaEmitidos)
            for comp in listaEmitidos:
                comp.save()
            messages.info(request,f"Se agregaron exitosamente {n} comprobantes")
            #borra variables de sesión al terminar
            if 'tabla' in request.session:
                del request.session['tabla']

            if 'contribuyente' in request.session:
                del request.session['contribuyente']

            return render(request, 'emitidos/emitidos_succes.html', {})

        if request.POST.get("Answer") == "no":
            return redirect('emitidos')
    return render(request, 'emitidos/emitidos_succes.html', {})