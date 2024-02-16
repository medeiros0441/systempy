from django.shortcuts import render, get_object_or_404, redirect
from ..models.sessao import SessaoUsuario
from django.http import JsonResponse
from django.utils import timezone

def sessao_usuario_list(request):
    sessoes = SessaoUsuario.objects.all()
    return render(request, 'sessao_usuario_list.html', {'sessoes': sessoes})

def sessao_usuario_detail(request, pk):
    sessao = get_object_or_404(SessaoUsuario, pk=pk)
    return render(request, 'sessao_usuario_detail.html', {'sessao': sessao})


def sessao_usuario_delete(request, pk):
    sessao = get_object_or_404(SessaoUsuario, pk=pk)
    if request.method == 'POST':
        sessao.delete()
        return redirect('sessao_usuario_list')
    return render(request, 'sessao_usuario_confirm_delete.html', {'sessao': sessao})

import json

def atualizar_sessao_usuario(request,status):
    try:
        if request.method == 'POST':
            id_usuario = request.session.get("id_usuario")
            if id_usuario:
                data = json.loads(request.body)
                pagina_atual = data.get('pagina_atual')
                endereco_ip = data.get('endereco_ip')
                

                sessao_usuario, created = SessaoUsuario.objects.get_or_create(usuario=id_usuario)
                # Atualiza informações da sessão
                sessao_usuario.pagina_atual = pagina_atual
                sessao_usuario.ip_sessao = endereco_ip         
                sessao_usuario.ip_sessao =  status
                sessao_usuario.update = timezone.now()

                sessao_usuario.save()
                return JsonResponse({'success': True, 'message': 'Sessão do usuário atualizada com sucesso'})
    except SessaoUsuario.DoesNotExist:


        pass
    return JsonResponse({'success': False, 'message': 'Sessão do usuário não encontrada'}, status=404)

def status_on(request):
    return atualizar_sessao_usuario(request,True)

def status_off(request):
    return atualizar_sessao_usuario(request,False)
# Retorna informações da sessão de um usuário específico como JSON
def get_sessao_usuario(request, user_id):
    try:
        sessao_usuario = SessaoUsuario.objects.filter(usuario_id=user_id).first()
        if sessao_usuario:
            data = {
                'id_sessao': sessao_usuario.id_sessao,
                'ip_sessao': sessao_usuario.ip_sessao,
                'descricao': sessao_usuario.descricao,
                'pagina_atual': sessao_usuario.pagina_atual,
                'time_iniciou': sessao_usuario.time_iniciou.strftime('%Y-%m-%d %H:%M:%S'),
                'time_finalizou': sessao_usuario.time_finalizou.strftime('%Y-%m-%d %H:%M:%S'),
                'status': sessao_usuario.status,
                'insert': sessao_usuario.insert.strftime('%Y-%m-%d %H:%M:%S'),
                'update': sessao_usuario.update.strftime('%Y-%m-%d %H:%M:%S') if sessao_usuario.update else None
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'message': 'Sessao do usuario nao encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Atualiza informações da sessão de um usuário específico
def atualizar_sessao_usuario(request, user_id):
    try:
        sessao_usuario = SessaoUsuario.objects.filter(usuario_id=user_id).first()
        if sessao_usuario:
            # Atualiza informações da sessão, você pode modificar isso de acordo com suas necessidades
            sessao_usuario.descricao = request.POST.get('descricao', sessao_usuario.descricao)
            sessao_usuario.pagina_atual = request.POST.get('pagina_atual', sessao_usuario.pagina_atual)
            sessao_usuario.status = request.POST.get('status', sessao_usuario.status)
            sessao_usuario.save()
            return JsonResponse({'message': 'Sessao do usuario atualizada com sucesso'})
        else:
            return JsonResponse({'message': 'Sessao do usuario nao encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)