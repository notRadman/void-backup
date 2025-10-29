#!/bin/bash
# system-backup.sh - نسخ احتياطي للنظام والإعدادات

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_ROOT="$HOME/backups"
BACKUP_DIR="$BACKUP_ROOT/$DATE"

# إنشاء المجلد
mkdir -p "$BACKUP_DIR"

echo "=== نسخ احتياطي للنظام ==="
echo "المجلد: $BACKUP_DIR"
echo ""

# 1. قائمة الحزم المثبتة
echo "1/6 - حفظ قائمة الحزم..."
xbps-query -l > "$BACKUP_DIR/packages.txt"

# 2. الخدمات المفعلة
echo "2/6 - حفظ الخدمات المفعلة..."
ls -1 /var/service/ > "$BACKUP_DIR/services.txt"

# 3. نسخ /etc (إعدادات النظام)
echo "3/6 - نسخ /etc..."
sudo tar -czf "$BACKUP_DIR/etc.tar.gz" \
    /etc \
    2>/dev/null

# 4. نسخ /usr/local (dwm, st, برامج مثبتة يدوياً)
echo "4/6 - نسخ /usr/local..."
sudo tar -czf "$BACKUP_DIR/usr-local.tar.gz" \
    /usr/local/bin \
    /usr/local/share \
    2>/dev/null

# 5. الإعدادات الشخصية فقط (dotfiles)
echo "5/6 - نسخ الإعدادات الشخصية..."
cd "$HOME"
tar -czf "$BACKUP_DIR/dotfiles.tar.gz" \
    .config \
    .xinitrc \
    .Xresources \
    .bashrc \
    .bash_profile \
    .tmux.conf \
    2>/dev/null

# 6. معلومات النظام
echo "6/6 - حفظ معلومات النظام..."
{
    echo "=== Void Linux System Backup ==="
    echo "Date: $(date)"
    echo "User: $USER"
    echo ""
    echo "=== Kernel ==="
    uname -a
    echo ""
    echo "=== Partitions ==="
    lsblk -f
    echo ""
    echo "=== fstab ==="
    cat /etc/fstab
    echo ""
    echo "=== عدد الحزم المثبتة ==="
    xbps-query -l | wc -l
    echo ""
    echo "=== الخدمات المفعلة ==="
    ls -1 /var/service/
} > "$BACKUP_DIR/system-info.txt"

# تغيير صلاحيات المجلد
sudo chown -R $USER:$USER "$BACKUP_DIR"

# النتيجة
echo ""
echo "✓✓✓ انتهى النسخ الاحتياطي! ✓✓✓"
echo ""
echo "المجلد: $BACKUP_DIR"
echo ""
echo "الملفات:"
ls -lh "$BACKUP_DIR"
echo ""
echo "الحجم الإجمالي:"
du -sh "$BACKUP_DIR"
echo ""
echo "=== كل النسخ الاحتياطية ==="
ls -1 "$BACKUP_ROOT"
```
