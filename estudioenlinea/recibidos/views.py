from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from .forms import MisComprobantesRecibidos_Form
from .scripts import extrae, mis_comprobantes_recibidos
from django.contrib import messages
# Create your views here.


@staff_member_required
def MisComprobantesRecibidosView(request):
    tabla=None
    excel = None
    if request.method == 'POST':
        form = MisComprobantesRecibidos_Form(request.POST, request.FILES)      
        
        if form.is_valid():
            if request.FILES['file'].name.endswith('xlsx'):
                excel = request.FILES['file']

                try:
                    data = extrae(excel)
                    if 'Denominación_Receptor' in data.columns:
                        raise ValueError('emitido en recibido')
                    tabla = data.to_dict('records')
                    request.session['tabla'] = tabla
                except:
                    mensaje = "Hubo un problema con el archivo."
                    messages.info(request,mensaje)
                    return render(request, 'recibidos/recibidos_upload.html', {'form': form})

                contribuyente = request.POST.get('contribuyente')
                request.session['contribuyente'] = contribuyente
                mensaje = "Archivo Cargado exitosamente"
                messages.info(request,mensaje)
                return redirect('recibidos_succes')
   
    form = MisComprobantesRecibidos_Form()
    return render(request, 'recibidos/recibidos_upload.html', {'form': form})

@staff_member_required
def recibidos_succes(request):
    tabla = None
    if request.method == "POST":
        if request.POST.get("Answer") == "si":
            tabla = request.session['tabla']
            contribuyente = request.session['contribuyente']
            listaRecibidos = mis_comprobantes_recibidos(tabla,contribuyente)
            n = 0
            for comp in listaRecibidos:
                    comp.save()
                    n = n + 1
            messages.info(request,f"Se agregaron exitosamente {n} comprobantes")
            #borra variables de sesión al terminar
            if 'tabla' in request.session:
                del request.session['tabla']

            if 'contribuyente' in request.session:
                del request.session['contribuyente']

            return render(request, 'recibidos/recibidos_succes.html', {})

        if request.POST.get("Answer") == "no":
            return redirect('recibidos')
            
    return render(request, 'recibidos/recibidos_succes.html', {})