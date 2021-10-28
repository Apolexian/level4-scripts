use quic_socket::QuicSocket;
use tokio;

#[tokio::main]
async fn main() {
    let addr = "0.0.0.0:4443".parse().unwrap();
    let socket = QuicSocket::bind(addr).await.unwrap();
    let conn_addr = "0.0.0.0:4444".parse().unwrap();
    let mut out = [0; 1350];
    let mut listener = socket.connect(conn_addr).unwrap();
    listener.send(&mut out).await;
    println!("{:?}", out)
}
