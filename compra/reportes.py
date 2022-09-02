from django.shortcuts import render
from .models import ComprasEnc, ComprasDet
from django.utils import timezone, dateformat

def imprimir_factura_compra(request,id):
    template_name="compra/reporte/imprimir_compra.html"

    enc = ComprasEnc.objects.get(id=id)
    det = ComprasDet.objects.filter(compra__id=id)

    context={
        'request':request,
        'enc':enc,
        'detalle':det
    }

    return render(request,template_name,context)



def imprimir_factura_compra_todas(request):
    template_name="compra/reporte/imprimir_compra_todas.html"

    enc = ComprasEnc.objects.all()
    today = dateformat.format(timezone.now(), 'd-m-Y')


    context={
        'request':request,
        'enc':enc,
        'hoy':today
    }

    return render(request,template_name,context)
# def reporte_compras(request):
#     today = dateformat.format(timezone.now(), 'd-m-Y')

#     compras = ComprasEnc.objects.all()
    
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="report.pdf"'
#     buff = BytesIO()
#     doc = SimpleDocTemplate(buff,pagesize=letter)
#     Story = []
    
#     h1 = PS(name = 'Heading1',fontSize = 25,leading = 16,alignment=TA_CENTER,fontName="Times-Roman")
#     h2 = PS(name = 'Heading1',fontSize = 14, leading = 14,fontName="Times-Roman")
#     h3 = PS(name='parrafos_normales',fontSize=12,fontName="Times-Roman",alignment=TA_JUSTIFY)
#     h4 = PS(name='parrafos_centrados',fontSize=12,fontName="Times-Roman",alignment=TA_CENTER)
#     h5 = PS(name='parrafos_derechos',fontSize=12,fontName="Times-Roman",alignment=TA_RIGHT)
    
#     texto = 'COMERCIALIZADORA REMETAL, C.A'
#     Story.append(Paragraph(texto, h5))
#     Story.append(Spacer(1, 12))
#     texto =  "Servicio de Reciclaje de Metales Ferrosos, No Ferrosos, Plasticos y Carton"
#     Story.append(Paragraph(texto, h5))
#     texto =  f"Reporte de Compras General al dia {today}"
#     Story.append(Paragraph(texto, h5)) 
#     Story.append(Spacer(1, 12))
#     for item in compras:
#         texto =  f"Compra de Materiales, No de Facturacion {item.no_factura}"
#         Story.append(Paragraph(texto, h3))
#         Story.append(Spacer(1, 12)) 
#         headings = ('Id', 'Proveedor', 'Fecha Compra', 'Total')
#         todascategorias = [(item.id, item.proveedor, item.fecha_compra, item.total)]   
#         t = Table([headings] + todascategorias)  
#         t.setStyle(TableStyle(  
#             [  
#             ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),  
#             ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),  
#             ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)  
#             ]  
#         ))  
#         Story.append(t)
#         Story.append(Spacer(1, 12))

#     doc.build(Story)
#     pdf = buff.getvalue()
#     response.write(pdf)
#     buff.close()
#     return response



