#!/usr/bin/env python3
"""
Config Backup Tool - Backup configs with versioning + latest for-git folder
"""
import os
import shutil
from datetime import datetime
from pathlib import Path

MAX_BACKUPS = 5  # Maximum number of backups to keep per program

def get_config_items():
    """Get all folders and files in .config"""
    config_path = Path.home() / ".config"
    
    if not config_path.exists():
        print("❌ .config directory not found!")
        return []
    
    items = []
    try:
        for item in sorted(config_path.iterdir()):
            items.append(item.name)
    except PermissionError:
        print("❌ No permission to access .config")
        return []
    
    return items

def display_items(items):
    """Display numbered list"""
    print("\n" + "="*60)
    print("📁 Contents of ~/.config:")
    print("="*60)
    
    for idx, item in enumerate(items, 1):
        config_path = Path.home() / ".config" / item
        item_type = "📁" if config_path.is_dir() else "📄"
        print(f"{idx:3d}. {item_type} {item}")
    
    print("="*60)

def get_user_selection(max_num):
    """Get user selection"""
    print("\n💡 Enter numbers of items to backup")
    print("   Example: 1,3,5 or 1 3 5")
    print("   Type 'all' to backup everything")
    print("   Type 'h' to show backup history")
    print("   Type 'q' to quit")
    
    while True:
        user_input = input("\n👉 Your choice: ").strip()
        
        if user_input.lower() == 'q':
            return None
        
        if user_input.lower() == 'h':
            return 'h'
        
        if user_input.lower() == 'all':
            return list(range(1, max_num + 1))
        
        try:
            # Convert input to numbers (comma or space separated)
            numbers = []
            parts = user_input.replace(',', ' ').split()
            
            for part in parts:
                num = int(part)
                if 1 <= num <= max_num:
                    numbers.append(num)
                else:
                    print(f"⚠️  Number {num} is out of range!")
            
            if numbers:
                return numbers
            else:
                print("❌ Please enter at least one valid number!")
        
        except ValueError:
            print("❌ Please enter valid numbers only!")

def cleanup_old_backups(program_folder):
    """Keep only the 5 most recent backups"""
    if not program_folder.exists():
        return
    
    # Get all backup folders sorted by name (timestamp)
    backups = sorted(
        [d for d in program_folder.iterdir() if d.is_dir()],
        reverse=True  # Newest first
    )
    
    # If more than MAX_BACKUPS, delete the oldest ones
    if len(backups) > MAX_BACKUPS:
        backups_to_delete = backups[MAX_BACKUPS:]
        
        for old_backup in backups_to_delete:
            try:
                shutil.rmtree(old_backup)
                print(f"   🗑️  Deleted old backup: {old_backup.name}")
            except Exception as e:
                print(f"   ⚠️  Failed to delete {old_backup.name}: {e}")

def update_for_git(item_name, source_path):
    """Update the for-git folder with latest version"""
    dotfiles_path = Path.home() / "dotfiles"
    for_git_path = dotfiles_path / "for-git"
    for_git_path.mkdir(exist_ok=True)
    
    destination = for_git_path / item_name
    
    # Remove old version if exists
    if destination.exists():
        if destination.is_dir():
            shutil.rmtree(destination)
        else:
            destination.unlink()
    
    # Copy new version
    try:
        if source_path.is_dir():
            shutil.copytree(source_path, destination, symlinks=True)
        else:
            shutil.copy2(source_path, destination)
        
        print(f"   🔄 Updated for-git/{item_name}")
        return True
    except Exception as e:
        print(f"   ⚠️  Failed to update for-git: {e}")
        return False

def backup_items(items, selected_indices):
    """Backup selected items"""
    config_path = Path.home() / ".config"
    dotfiles_path = Path.home() / "dotfiles"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create dotfiles folder if not exists
    dotfiles_path.mkdir(exist_ok=True)
    
    print(f"\n⏰ Timestamp: {timestamp}")
    print("="*60)
    
    success_count = 0
    fail_count = 0
    
    for idx in selected_indices:
        item_name = items[idx - 1]  # -1 because list starts at 0
        source = config_path / item_name
        
        # Create program folder
        program_folder = dotfiles_path / item_name
        program_folder.mkdir(exist_ok=True)
        
        # Create timestamp folder
        backup_folder = program_folder / timestamp
        destination = backup_folder / item_name
        
        print(f"\n📦 Backing up: {item_name}")
        print(f"   From: {source}")
        print(f"   To: {destination}")
        
        try:
            if source.is_dir():
                shutil.copytree(source, destination, symlinks=True)
                print("   ✅ Backup successful!")
            elif source.is_file():
                backup_folder.mkdir(exist_ok=True)
                shutil.copy2(source, destination)
                print("   ✅ Backup successful!")
            else:
                print("   ⚠️  Item not found!")
                fail_count += 1
                continue
            
            success_count += 1
            
            # Update for-git folder
            update_for_git(item_name, source)
            
            # Cleanup old backups (keep only 5 most recent)
            cleanup_old_backups(program_folder)
            
        except PermissionError:
            print("   ❌ No permission to backup!")
            fail_count += 1
        except Exception as e:
            print(f"   ❌ Error: {e}")
            fail_count += 1
    
    # Final result
    print("\n" + "="*60)
    print("📊 Results:")
    print(f"   ✅ Success: {success_count}")
    print(f"   ❌ Failed: {fail_count}")
    print("="*60)
    
    if success_count > 0:
        print(f"\n💾 Saved to: {dotfiles_path}")
        print(f"🕐 Timestamp: {timestamp}")
        print(f"🔄 Latest versions in: {dotfiles_path}/for-git/")
        print(f"♻️  Keeping only {MAX_BACKUPS} most recent backups per program")
        print(f"\n💡 Tip: You can 'git init' inside for-git/ and push to GitHub!")

def show_backup_history():
    """Show backup history"""
    dotfiles_path = Path.home() / "dotfiles"
    
    if not dotfiles_path.exists():
        print("\n📁 No backups yet!")
        return
    
    print("\n" + "="*60)
    print("📚 Existing Backups:")
    print("="*60)
    
    for program_folder in sorted(dotfiles_path.iterdir()):
        if program_folder.is_dir() and program_folder.name != "for-git":
            backups = sorted(program_folder.iterdir(), reverse=True)
            if backups:
                print(f"\n📁 {program_folder.name}:")
                for backup in backups[:5]:  # Show last 5 only
                    size = sum(f.stat().st_size for f in backup.rglob('*') if f.is_file())
                    size_mb = size / (1024 * 1024)
                    print(f"   🕐 {backup.name} ({size_mb:.2f} MB)")
    
    # Show for-git status
    for_git_path = dotfiles_path / "for-git"
    if for_git_path.exists():
        print(f"\n🔄 for-git/ folder:")
        for item in sorted(for_git_path.iterdir()):
            size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
            size_mb = size / (1024 * 1024)
            item_type = "📁" if item.is_dir() else "📄"
            print(f"   {item_type} {item.name} ({size_mb:.2f} MB)")
    
    print("="*60)

def main():
    """Main function"""
    print("="*60)
    print("🔧 Config Backup Tool")
    print("="*60)
    
    # Get .config contents
    items = get_config_items()
    
    if not items:
        return
    
    while True:
        # Display items
        display_items(items)
        
        # Get user selection
        selected = get_user_selection(len(items))
        
        if selected is None:
            print("\n👋 Goodbye!")
            break
        
        if selected == 'h':
            show_backup_history()
            continue
        
        # Backup
        backup_items(items, selected)
        
        # Continue?
        print("\n" + "="*60)
        choice = input("Backup more items? (y/n): ").strip().lower()
        if choice != 'y':
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
