use quic_socket::QuicListener;
use tokio;

#[tokio::main]
async fn main() {
    let addr = "127.0.0.1:4442".parse().unwrap();
    let read = QuicListener::recv(addr, "../client/cert.der".to_string())
        .await
        .unwrap();
    println!("{:?}", read);
}
