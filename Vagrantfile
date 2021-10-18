Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/bionic64"
    config.ssh.forward_agent = true
    config.ssh.forward_x11 = true
    config.ssh.insert_key = 'true'

    config.vm.provision "shell", inline: <<~SHELL
     add-apt-repository ppa:git-core/ppa -y
     sudo apt-get update
     sudo apt-get install -y git vim curl
     sudo apt-get install mininet -y
     sudo PYTHON=python3 mininet/util/install.sh -n
     sudo apt-get install -y uthash-dev
     sudo apt-get install -y libev-dev
     sudo apt-get install python-pip -y
     pip install pathlib
     git clone git://github.com/mininet/mininet
     mininet/util/install.sh -fw
     sudo apt-get install nasm -y
     sudo apt-get install libssl-dev -y
     sudo apt remove --purge --auto-remove cmake
     wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | sudo tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null
     sudo apt-add-repository "deb https://apt.kitware.com/ubuntu/ $(lsb_release -cs) main"
     sudo apt update
     sudo apt install cmake
     echo 'curl https://sh.rustup.rs -sSf | sh -s -- -y;' | su vagrant
     git clone --recursive https://github.com/cloudflare/quiche
     git clone https://github.com/bytebeamio/rumqtt
   SHELL
  end