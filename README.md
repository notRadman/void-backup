# void-backup
Hello, here is my code of making a backup of void.
just the names of every thing and it will be downloaded
you can apply those in a freshly void like this
disc: dont worry abot arabic, it was the choose of claude, if you are worried no problem bro don't use it.

put the backup in the home or at any place and do that thx bro i am crying now

packages:
  sudo xbps-install -S $(cat packages-DATE.txt | awk '{print $2}' | cut -d- -f1)

services(close the others first):
  while read service; do
    sudo ln -s /etc/sv/$service /var/service/
  done < services-DATE.txt

/etc:
  cd /
  sudo tar -xzf path/of/backup/etc-/DATE/.tar.gz

/usr/local:
  cd /
  sudo tar -xzf path/of/backup/usr-local-/DATE/.tar.gz

dotfiles:
  cd ~
  tar -xzf path/of/backup/dotfiles-/DATE/.tar.gz

sudo reboot
