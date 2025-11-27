from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlindBoxForm, MessageForm
from .models import BlindBox, Message  # 确保你需要导入 Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def blindbox(request):
    if request.method == 'POST':
        form = BlindBoxForm(data=request.POST)
        if form.is_valid():
            try:
                # 确保用户对象是完整的并检查其有效性
                user_id = request.user.id
                username = request.user.username
                
                # 从数据库重新获取用户对象，确保它存在于数据库中
                from accounts.models import CustomUser
                try:
                    user = CustomUser.objects.get(id=user_id)
                except CustomUser.DoesNotExist:
                    form.add_error(None, f'用户不存在: 用户ID {user_id} 不存在于数据库中')
                    return render(request, 'blindbox.html', {'form': form, 'blind_boxes': []})
                
                # 创建盲盒实例并设置用户外键
                blindbox_instance = form.save(commit=False)
                # 直接使用user_id而不是对象引用，减少关联错误可能性
                blindbox_instance.user_id = user.id
                
                # 保存到数据库
                blindbox_instance.save()
                
                return redirect('blindbox:all_blindboxes')
            except Exception as e:
                # 添加详细的错误信息，包括异常类型
                error_msg = f'保存失败: {type(e).__name__}: {str(e)}'
                user_info = f'用户ID: {user_id}, 用户名: {username}'
                print(f'错误详情: {error_msg}')
                print(f'用户信息: {user_info}')
                form.add_error(None, error_msg)
                form.add_error(None, user_info)
    else:
        form = BlindBoxForm()

    # 使用异常处理获取用户盲盒，避免潜在错误
    try:
        blind_boxes = BlindBox.objects.filter(user=request.user)
    except Exception as e:
        print(f'获取盲盒失败: {str(e)}')
        blind_boxes = []

    return render(request, 'blindbox.html', {
        'form': form,
        'blind_boxes': blind_boxes,
    })

@login_required
def blindbox_detail(request, box_id):
    try:
        box = get_object_or_404(BlindBox, id=box_id)
        
        if request.method == 'POST':
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                try:
                    # 确保所有外键关系有效
                    if request.user.is_authenticated and box is not None and box.user is not None:
                        message_instance = message_form.save(commit=False)
                        message_instance.sender = request.user
                        message_instance.receiver = box.user
                        message_instance.blindbox = box
                        message_instance.save()
                        return redirect('blindbox:blindbox_detail', box_id=box.id)
                    else:
                        message_form.add_error(None, '用户认证或盲盒信息无效')
                except Exception as e:
                    # 捕获并显示详细的错误信息
                    message_form.add_error(None, f'发送消息失败: {str(e)}')
        else:
            message_form = MessageForm()
        
        return render(request, 'blindbox_detail.html', {
            'box': box,
            'message_form': message_form,
        })
    except Exception as e:
        # 处理盲盒不存在的情况
        return render(request, 'blindbox_detail.html', {
            'error': f'加载盲盒失败: {str(e)}',
            'box': None,
            'message_form': None
        })

@login_required
def all_blindboxes(request):
    """显示所有用户的盲盒"""
    # 获取所有盲盒，但排除当前用户自己的盲盒
    blind_boxes = BlindBox.objects.exclude(user=request.user).order_by('-created_at')
    
    return render(request, 'all_blindboxes.html', {
        'blind_boxes': blind_boxes,
    })

