import os
import sys

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

from django.db import connection

def fix_foreign_key():
    """修复盲盒表的外键约束，将其从auth_user改为accounts_customuser"""
    print("开始修复外键约束...")
    
    try:
        with connection.cursor() as cursor:
            # 首先检查表是否存在
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]
            print(f"数据库中的表: {table_names}")
            
            # 1. 处理BlindBox表
            if 'blindbox_blindbox' in table_names:
                print("找到blindbox_blindbox表，开始修复...")
                
                # 重命名现有表
                print("重命名现有表...")
                cursor.execute("ALTER TABLE blindbox_blindbox RENAME TO blindbox_blindbox_old;")
                
                # 创建新表，带有正确的外键约束
                print("创建新表，带有正确的外键约束...")
                cursor.execute("""
                    CREATE TABLE blindbox_blindbox (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        created_at DATETIME NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES accounts_customuser(id) ON DELETE CASCADE
                    );
                """)
                
                # 检查旧表是否有数据并复制
                cursor.execute("SELECT COUNT(*) FROM blindbox_blindbox_old;")
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"发现{count}条数据，开始复制...")
                    cursor.execute("""
                        INSERT INTO blindbox_blindbox (id, content, created_at, user_id)
                        SELECT id, content, created_at, user_id FROM blindbox_blindbox_old;
                    """)
                else:
                    print("旧表中没有数据，跳过复制步骤。")
                
                # 删除旧表
                print("删除旧表...")
                cursor.execute("DROP TABLE IF EXISTS blindbox_blindbox_old;")
            else:
                # 如果表不存在，直接创建新表
                print("blindbox_blindbox表不存在，直接创建新表...")
                cursor.execute("""
                    CREATE TABLE blindbox_blindbox (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        created_at DATETIME NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES accounts_customuser(id) ON DELETE CASCADE
                    );
                """)
            
            # 2. 处理Message表
            if 'blindbox_message' in table_names:
                print("找到blindbox_message表，开始修复...")
                
                # 重命名现有表
                cursor.execute("ALTER TABLE blindbox_message RENAME TO blindbox_message_old;")
                
                # 创建新表，带有正确的外键约束
                cursor.execute("""
                    CREATE TABLE blindbox_message (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        created_at DATETIME NOT NULL,
                        sender_id INTEGER NOT NULL,
                        receiver_id INTEGER NOT NULL,
                        blindbox_id INTEGER NOT NULL,
                        FOREIGN KEY (sender_id) REFERENCES accounts_customuser(id) ON DELETE CASCADE,
                        FOREIGN KEY (receiver_id) REFERENCES accounts_customuser(id) ON DELETE CASCADE,
                        FOREIGN KEY (blindbox_id) REFERENCES blindbox_blindbox(id) ON DELETE CASCADE
                    );
                """)
                
                # 检查旧表是否有数据并复制
                cursor.execute("SELECT COUNT(*) FROM blindbox_message_old;")
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"发现{count}条Message数据，开始复制...")
                    cursor.execute("""
                        INSERT INTO blindbox_message (id, content, created_at, sender_id, receiver_id, blindbox_id)
                        SELECT id, content, created_at, sender_id, receiver_id, blindbox_id FROM blindbox_message_old;
                    """)
                else:
                    print("Message表中没有数据，跳过复制步骤。")
                
                # 删除旧表
                cursor.execute("DROP TABLE IF EXISTS blindbox_message_old;")
            else:
                # 如果表不存在，直接创建新表
                print("blindbox_message表不存在，直接创建新表...")
                cursor.execute("""
                    CREATE TABLE blindbox_message (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        created_at DATETIME NOT NULL,
                        sender_id INTEGER NOT NULL,
                        receiver_id INTEGER NOT NULL,
                        blindbox_id INTEGER NOT NULL,
                        FOREIGN KEY (sender_id) REFERENCES accounts_customuser(id) ON DELETE CASCADE,
                        FOREIGN KEY (receiver_id) REFERENCES accounts_customuser(id) ON DELETE CASCADE,
                        FOREIGN KEY (blindbox_id) REFERENCES blindbox_blindbox(id) ON DELETE CASCADE
                    );
                """)
            
            print("外键约束修复完成！")
            
            # 验证修复结果
            print("\n验证修复结果:")
            if 'blindbox_blindbox' in table_names:
                cursor.execute("PRAGMA foreign_key_list(blindbox_blindbox);")
                new_foreign_keys = cursor.fetchall()
                print("BlindBox表外键约束:")
                for row in new_foreign_keys:
                    print(row)
            
            if 'blindbox_message' in table_names:
                cursor.execute("PRAGMA foreign_key_list(blindbox_message);")
                new_foreign_keys_message = cursor.fetchall()
                print("Message表外键约束:")
                for row in new_foreign_keys_message:
                    print(row)
                
    except Exception as e:
        print(f"修复外键约束失败: {e}")
        # 如果出错，尝试恢复旧表
        try:
            with connection.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS blindbox_blindbox;")
                cursor.execute("ALTER TABLE blindbox_blindbox_old RENAME TO blindbox_blindbox;")
                cursor.execute("DROP TABLE IF EXISTS blindbox_message;")
                cursor.execute("ALTER TABLE blindbox_message_old RENAME TO blindbox_message;")
            print("已恢复原始表结构。")
        except:
            print("恢复表结构失败。")

if __name__ == "__main__":
    fix_foreign_key()
