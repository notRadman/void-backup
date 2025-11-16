#!/bin/bash
# system-backup.sh - Complete system and configuration backup
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_ROOT="$HOME/backups"
BACKUP_DIR="$BACKUP_ROOT/$DATE"
MAX_BACKUPS=5

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "=== System Backup ==="
echo "Directory: $BACKUP_DIR"
echo ""

# 1. Installed packages list
echo "1/6 - Saving package list..."
xbps-query -l > "$BACKUP_DIR/packages.txt"

# 2. Enabled services
echo "2/6 - Saving enabled services..."
ls -1 /var/service/ > "$BACKUP_DIR/services.txt"

# 3. Copy /etc (system configuration)
echo "3/6 - Copying /etc..."
sudo tar -czf "$BACKUP_DIR/etc.tar.gz" \
    /etc \
    2>/dev/null

# 4. Copy /usr/local (dwm, st, manually installed programs)
echo "4/6 - Copying /usr/local..."
sudo tar -czf "$BACKUP_DIR/usr-local.tar.gz" \
    /usr/local/bin \
    /usr/local/share \
    2>/dev/null

# 5. Personal configuration files only (dotfiles)
echo "5/6 - Copying personal configuration..."
cd "$HOME"
tar -czf "$BACKUP_DIR/dotfiles.tar.gz" \
    .config \
    .xinitrc \
    .Xresources \
    .bashrc \
    .bash_profile \
    .tmux.conf \
    2>/dev/null

# 6. System information
echo "6/6 - Saving system information..."
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
    echo "=== Installed Packages Count ==="
    xbps-query -l | wc -l
    echo ""
    echo "=== Enabled Services ==="
    ls -1 /var/service/
} > "$BACKUP_DIR/system-info.txt"

# Fix permissions
sudo chown -R $USER:$USER "$BACKUP_DIR"

# Delete old backups (keep only 5 most recent)
echo ""
echo "7/7 - Cleaning old backups..."
BACKUP_COUNT=$(ls -1d "$BACKUP_ROOT"/*/ 2>/dev/null | wc -l)

if [ "$BACKUP_COUNT" -gt "$MAX_BACKUPS" ]; then
    BACKUPS_TO_DELETE=$((BACKUP_COUNT - MAX_BACKUPS))
    echo "Found $BACKUP_COUNT backups, removing oldest $BACKUPS_TO_DELETE..."
    
    ls -1td "$BACKUP_ROOT"/*/ | tail -n "$BACKUPS_TO_DELETE" | while read OLD_BACKUP; do
        echo "  Deleting: $(basename "$OLD_BACKUP")"
        rm -rf "$OLD_BACKUP"
    done
else
    echo "Only $BACKUP_COUNT backups found, no cleanup needed."
fi

# Results
echo ""
echo "✓✓✓ Backup Complete! ✓✓✓"
echo ""
echo "Directory: $BACKUP_DIR"
echo ""
echo "Files:"
ls -lh "$BACKUP_DIR"
echo ""
echo "Total Size:"
du -sh "$BACKUP_DIR"
echo ""
echo "=== All Backups (newest first) ==="
ls -1t "$BACKUP_ROOT"
