use quic_socket::{QuicServer, QuicSocket};
use tokio;

#[tokio::main]
async fn main() {
    // quic_socket::gen_certificates().unwrap();
    let addr = "127.0.0.1:4442".parse().unwrap();
    let mut server = QuicServer::new(Some(addr));
    let read = server.recv().await.unwrap();
    println!("{:?}", read);
}
