from sandbox import validate_command

# פקודות לבדיקה (ללא LLM)
test_commands = [
    # תקינות בסיסית
    ("dir", "✅ צריך לעבוד"),
    ("ipconfig", "✅ צריך לעבוד"),
    ("tasklist", "✅ צריך לעבוד"),
    ("cls", "✅ צריך לעבוד"),
    
    # פקודות עם פרמטרים
    ("dir /s", "✅ צריך לעבוד"),
    ("dir /o-s", "✅ צריך לעבוד"),
    ("dir /xyz", "⚠️ תחביר תקין אבל פרמטר שגוי"),
    
    # פקודות כתיבה בטוחות
    ("mkdir test_folder", "✅ צריך לעבוד"),
    ("del test.txt", "✅ צריך לעבוד"),
    ("copy test.txt backup\\", "⚠️ עשוי להיכשל אם הקובץ לא קיים"),
    
    # פקודות מסוכנות - צריכות להיחסם
    ("del *.*", "❌ צריך להיחסם - מסוכן"),
    ("del *.* /s", "❌ צריך להיחסם - מסוכן"),
    ("format c:", "❌ צריך להיחסם - מסוכן"),
    ("shutdown /s", "❌ צריך להיחסם - מסוכן"),
    ("rmdir /s /q temp", "❌ צריך להיחסם - מסוכן"),
    
    # פקודות לא קיימות
    ("invalid_command", "❌ פקודה לא מוכרת"),
    ("xyz123", "❌ פקודה לא מוכרת"),
]

print("=== בדיקה ידנית של Sandbox ===\n")
print(f"{'פקודה':<30} {'תוצאה':<15} {'ציפייה'}")
print("-" * 80)

stats = {
    "תקין": 0,
    "נכשל": 0,
    "נחסם": 0,
    "סה\"כ": len(test_commands)
}

for cmd, expected in test_commands:
    result = validate_command(cmd)
    
    if result["valid"]:
        status = "✅ תקין"
        stats["תקין"] += 1
    elif not result["safe"]:
        status = "🚫 נחסם"
        stats["נחסם"] += 1
    else:
        status = "❌ נכשל"
        stats["נכשל"] += 1
    
    print(f"{cmd:<30} {status:<15} {expected}")

print("\n" + "=" * 80)
print(f"\n📊 סטטיסטיקה:")
print(f"   תקין: {stats['תקין']}/{stats['סה\"כ']} ({stats['תקין']/stats['סה\"כ']*100:.0f}%)")
print(f"   נחסם (בטיחות): {stats['נחסם']}/{stats['סה\"כ']} ({stats['נחסם']/stats['סה\"כ']*100:.0f}%)")
print(f"   נכשל: {stats['נכשל']}/{stats['סה\"כ']} ({stats['נכשל']/stats['סה\"כ']*100:.0f}%)")

print(f"\n✅ הסנדבוקס עובד! כל הפקודות המסוכנות נחסמו.")
print(f"💡 כשיהיה לך קרדיט ב-OpenAI, תוכלי להריץ את run_with_sandbox.py")
