use quic_socket;

fn main() {
    let addr = "127.0.0.1:4444".parse().unwrap();
    let socket = QuickSocket::bind(addr);
    let listener = socket.connect()?;
}
