import subprocess
import tempfile
import os
import shutil
from pathlib import Path

class CMDSandbox:
    """Sandbox בטוח להרצת פקודות CMD"""
    
    # פקודות בטוחות לקריאה בלבד
    SAFE_READ_COMMANDS = [
        'dir', 'cd', 'type', 'find', 'findstr', 'tree', 'echo',
        'set', 'path', 'ver', 'vol', 'date', 'time', 'cls',
        'ipconfig', 'ping', 'tracert', 'netstat', 'hostname',
        'tasklist', 'systeminfo', 'wmic'
    ]
    
    # פקודות מסוכנות - חסומות לחלוטין
    DANGEROUS_COMMANDS = [
        'format', 'shutdown', 'restart', 'reboot', 'reg', 'regedit',
        'diskpart', 'fdisk', 'bcdedit', 'powercfg'
    ]
    
    def __init__(self):
        """יוצר sandbox זמני"""
        self.sandbox_dir = tempfile.mkdtemp(prefix="cmd_sandbox_")
        self._setup_sandbox()
    
    def _setup_sandbox(self):
        """מכין את ה-sandbox עם קבצים לדוגמה"""
        # יצירת מבנה תיקיות
        (Path(self.sandbox_dir) / "test_folder").mkdir()
        (Path(self.sandbox_dir) / "backup").mkdir()
        
        # יצירת קבצים לדוגמה
        (Path(self.sandbox_dir) / "test.txt").write_text("Hello World")
        (Path(self.sandbox_dir) / "file1.tmp").write_text("Temp file 1")
        (Path(self.sandbox_dir) / "file2.tmp").write_text("Temp file 2")
        (Path(self.sandbox_dir) / "document.doc").write_text("Document")
    
    def is_safe_command(self, command: str) -> tuple[bool, str]:
        """בודק אם פקודה בטוחה להרצה"""
        cmd_lower = command.lower().strip()
        first_word = cmd_lower.split()[0] if cmd_lower.split() else ""
        
        # בדיקה לפקודות מסוכנות
        for dangerous in self.DANGEROUS_COMMANDS:
            if dangerous in cmd_lower:
                return False, f"פקודה מסוכנת: {dangerous}"
        
        # בדיקה לתבניות מסוכנות
        dangerous_patterns = [
            'c:\\windows', 'c:\\program files', 'c:\\users',
            '*.* /s', 'del *.*', 'rmdir /s'
        ]
        for pattern in dangerous_patterns:
            if pattern in cmd_lower:
                return False, f"תבנית מסוכנת: {pattern}"
        
        # פקודות קריאה - תמיד בטוחות
        if first_word in self.SAFE_READ_COMMANDS:
            return True, "פקודת קריאה בטוחה"
        
        # פקודות כתיבה - רק ב-sandbox
        write_commands = ['copy', 'move', 'ren', 'rename', 'mkdir', 'md']
        if first_word in write_commands:
            return True, "פקודת כתיבה ב-sandbox"
        
        # del, rmdir - רק אם ספציפי ולא כולל תבניות מסוכנות
        if first_word in ['del', 'erase', 'rmdir', 'rd']:
            if '*.*' in cmd_lower or '/s' in cmd_lower:
                return False, "מחיקה כללית מסוכנת"
            return True, "מחיקה ספציפית ב-sandbox"
        
        return False, f"פקודה לא מוכרת: {first_word}"
    
    def execute(self, command: str, timeout: int = 5) -> dict:
        """מריץ פקודה ב-sandbox"""
        result = {
            "command": command,
            "safe": False,
            "executed": False,
            "exit_code": None,
            "stdout": "",
            "stderr": "",
            "error": None
        }
        
        # בדיקת בטיחות
        is_safe, reason = self.is_safe_command(command)
        result["safe"] = is_safe
        result["safety_reason"] = reason
        
        if not is_safe:
            result["error"] = f"פקודה נחסמה: {reason}"
            return result
        
        try:
            # הרצה ב-sandbox
            process = subprocess.run(
                command,
                shell=True,
                cwd=self.sandbox_dir,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='cp862'  # Windows Hebrew encoding
            )
            
            result["executed"] = True
            result["exit_code"] = process.returncode
            result["stdout"] = process.stdout
            result["stderr"] = process.stderr
            
        except subprocess.TimeoutExpired:
            result["error"] = "Timeout - הפקודה לקחה יותר מדי זמן"
        except Exception as e:
            result["error"] = f"שגיאה בהרצה: {str(e)}"
        
        return result
    
    def cleanup(self):
        """מנקה את ה-sandbox"""
        try:
            shutil.rmtree(self.sandbox_dir)
        except Exception as e:
            print(f"שגיאה בניקוי sandbox: {e}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()


def validate_command(command: str) -> dict:
    """מאמת פקודה על ידי הרצה ב-sandbox"""
    with CMDSandbox() as sandbox:
        result = sandbox.execute(command)
        
        # ניתוח התוצאה
        validation = {
            "command": command,
            "valid": False,
            "safe": result["safe"],
            "executed": result["executed"],
            "syntax_ok": False,
            "reason": ""
        }
        
        if not result["safe"]:
            validation["reason"] = result["safety_reason"]
            return validation
        
        if not result["executed"]:
            validation["reason"] = result.get("error", "לא הורץ")
            return validation
        
        # בדיקת תחביר
        if result["exit_code"] == 0:
            validation["valid"] = True
            validation["syntax_ok"] = True
            validation["reason"] = "פקודה תקינה"
        elif "not recognized" in result["stderr"].lower():
            validation["reason"] = "פקודה לא מוכרת"
        elif "syntax" in result["stderr"].lower():
            validation["reason"] = "שגיאת תחביר"
        else:
            validation["syntax_ok"] = True  # תחביר תקין אבל הפקודה נכשלה
            validation["reason"] = f"הפקודה נכשלה: {result['stderr'][:100]}"
        
        return validation


if __name__ == "__main__":
    # דוגמאות בדיקה
    test_commands = [
        "dir",
        "ipconfig",
        "del test.txt",
        "del *.*",  # מסוכן
        "format c:",  # מסוכן
        "mkdir new_folder",
        "invalid_command",
        "dir /xyz",  # תחביר שגוי
    ]
    
    print("=== בדיקת פקודות ב-Sandbox ===\n")
    
    for cmd in test_commands:
        print(f"פקודה: {cmd}")
        result = validate_command(cmd)
        
        status = "✅" if result["valid"] else "❌"
        print(f"{status} תקין: {result['valid']}")
        print(f"   בטוח: {result['safe']}")
        print(f"   סיבה: {result['reason']}")
        print()
