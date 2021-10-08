Vagrant.configure("2") do |config|
    config.vm.box = "generic/ubuntu1804"
    config.ssh.forward_agent = true
    config.ssh.forward_x11 = true

    config.vm.provision "shell", inline: <<~SHELL
     add-apt-repository ppa:git-core/ppa -y
     sudo apt-get update
     sudo apt-get install -y git vim curl
     sudo apt-get install mininet -y
     git clone git://github.com/mininet/mininet
     mininet/util/install.sh -fw
     sudo apt-get install python3.7 -y
     sudo apt-get install vim git nasm -y
     sudo apt-get install cmake libssl-dev -y
     echo 'curl https://sh.rustup.rs -sSf | sh -s -- -y;' | su vagrant
     git clone --recursive https://github.com/cloudflare/quiche
     git clone https://github.com/bschwind/mqtt-broker.git
   SHELL
  end