from django.db import connection
import os
import sys

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblindbox.settings')

# 导入Django
try:
    import django
    django.setup()
except Exception as e:
    print(f"设置Django环境失败: {e}")
    sys.exit(1)

# 检查数据库表列表
print("数据库表列表:")
tables = connection.introspection.table_names()
for table in tables:
    print(f"- {table}")

# 检查用户表结构
print("\n检查用户表结构:")
try:
    with connection.cursor() as cursor:
        cursor.execute('PRAGMA table_info(accounts_customuser);')
        user_table_info = cursor.fetchall()
        for row in user_table_info:
            print(row)
except Exception as e:
    print(f"获取用户表结构失败: {e}")

# 检查盲盒表结构
print("\n检查盲盒表结构:")
try:
    with connection.cursor() as cursor:
        cursor.execute('PRAGMA table_info(blindbox_blindbox);')
        blindbox_table_info = cursor.fetchall()
        for row in blindbox_table_info:
            print(row)
except Exception as e:
    print(f"获取盲盒表结构失败: {e}")

# 检查外键约束
print("\n检查盲盒表的外键约束:")
try:
    with connection.cursor() as cursor:
        cursor.execute('PRAGMA foreign_key_list(blindbox_blindbox);')
        foreign_keys = cursor.fetchall()
        for row in foreign_keys:
            print(row)
except Exception as e:
    print(f"获取外键约束失败: {e}")

# 检查用户记录
print("\n检查用户记录:")
try:
    from accounts.models import CustomUser
    users = CustomUser.objects.all()
    print(f"总用户数: {users.count()}")
    for user in users:
        print(f"用户ID: {user.id}, 用户名: {user.username}, 密码: {user.password}")
except Exception as e:
    print(f"获取用户记录失败: {e}")

# 检查盲盒表中的记录
print("\n检查盲盒记录:")
try:
    from blindbox.models import BlindBox
    boxes = BlindBox.objects.all()
    print(f"总盲盒数: {boxes.count()}")
    for box in boxes:
        print(f"盲盒ID: {box.id}, 用户ID: {box.user_id}, 内容: {box.content}")
except Exception as e:
    print(f"获取盲盒记录失败: {e}")
