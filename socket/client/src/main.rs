use quic_socket::QuicSocket;
use tokio;

#[tokio::main]
async fn main() {
    let addr = "0.0.0.0:4443".parse().unwrap();
    let socket = QuicSocket::bind(addr).await.unwrap();
    let acc_addr = "0.0.0.0:4444".parse().unwrap();
    let mut out = [0; 1350];
    let mut listener = socket.accept(acc_addr).unwrap();
    let write = listener.send(&mut out).await.expect("initial send failed");
    println!("{:?}", &out[..write])
}
