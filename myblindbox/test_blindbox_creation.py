import os
import sys
import random

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblindbox.settings')

# 导入Django
try:
    import django
    django.setup()
except Exception as e:
    print(f"设置Django环境失败: {e}")
    sys.exit(1)

from accounts.models import CustomUser
from blindbox.models import BlindBox

def test_blindbox_creation():
    """测试盲盒创建功能，使用随机数字作为内容"""
    print("开始测试盲盒创建功能...")
    
    try:
        # 获取第一个用户
        users = CustomUser.objects.all()
        if not users:
            print("错误: 没有找到任何用户！")
            return False
        
        user = users.first()
        print(f"使用用户: {user.username} (ID: {user.id})")
        
        # 生成随机数字作为盲盒内容
        random_number = random.randint(1000, 9999)
        content = f"{random_number}"
        print(f"创建盲盒，内容: {content}")
        
        # 创建盲盒
        blindbox = BlindBox.objects.create(
            user=user,
            content=content
        )
        
        print(f"✅ 盲盒创建成功！ID: {blindbox.id}, 用户ID: {blindbox.user_id}")
        
        # 验证创建的盲盒
        created_blindbox = BlindBox.objects.get(id=blindbox.id)
        print(f"✅ 验证成功！创建的盲盒内容: {created_blindbox.content}")
        print(f"✅ 外键关系正确: user_id={created_blindbox.user_id} 指向用户 {created_blindbox.user.username}")
        
        # 显示所有盲盒
        all_blindboxes = BlindBox.objects.all()
        print(f"\n当前系统中的盲盒总数: {all_blindboxes.count()}")
        for box in all_blindboxes:
            print(f"  - 盲盒ID: {box.id}, 内容: {box.content}, 用户: {box.user.username} (ID: {box.user_id})")
        
        return True
        
    except Exception as e:
        print(f"❌ 盲盒创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_blindbox_creation()
